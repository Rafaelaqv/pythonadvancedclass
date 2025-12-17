import xarray as xr
import geopandas as gpd
import pandas as pd
import rioxarray
from shapely.geometry import mapping
from rioxarray.exceptions import NoDataInBounds
from tqdm import tqdm
from typing import Tuple, Optional

# ----------------------------------------------------------
# Helper: Adjust Longitude
# ----------------------------------------------------------
def standardize_longitude(da: xr.DataArray, lon_name: str) -> xr.DataArray:
    """
    Standardizes longitude coordinates from a 0-360 range to a -180 to 180 range.
    
    This is often necessary when aligning global climate models (0-360) with 
    standard shapefiles (EPSG:4326, which uses -180/180).

    Args:
        da (xr.DataArray): The input xarray DataArray containing climate data.
        lon_name (str): The name of the longitude dimension in the DataArray.

    Returns:
        xr.DataArray: The DataArray with adjusted longitude coordinates, 
        sorted by longitude to ensure monotonic increase.
    """
    # Check if the data uses 0-360 format (values > 180 exist)
    if da[lon_name].max() > 180:
        print("   -> 🌍 Auto-correcting Longitude from 0-360 to -180/180...")
        
        # Apply the conversion logic: (lon + 180) % 360 - 180
        new_lon = (da[lon_name] + 180) % 360 - 180
        da = da.assign_coords({lon_name: new_lon})
        
        # Sort by longitude is crucial; otherwise, slicing operations 
        # (e.g., .sel(lon=slice(...))) might fail or return incorrect data.
        da = da.sortby(lon_name)
        
    return da

# ----------------------------------------------------------
# Helper: Identify Spatial Dimensions
# ----------------------------------------------------------
def identify_spatial_dims(da: xr.DataArray) -> Tuple[str, str]:
    """
    Automatically detects the names of latitude and longitude dimensions in a DataArray.
    
    It checks against a list of common naming conventions (e.g., 'lat', 'latitude', 'y').

    Args:
        da (xr.DataArray): The input DataArray to inspect.

    Returns:
        Tuple[str, str]: A tuple containing (latitude_name, longitude_name).

    Raises:
        ValueError: If spatial dimensions cannot be identified from the common list.
    """
    lat_options = ['latitude', 'lat', 'LATITUDE', 'LAT', 'y', 'Y']
    lon_options = ['longitude', 'lon', 'long', 'LONGITUDE', 'LONG', 'x', 'X']
    
    lat_name = None
    lon_name = None
    
    # Iterate through options to find the matching latitude coordinate
    for name in lat_options:
        if name in da.coords:
            lat_name = name
            break
            
    # Iterate through options to find the matching longitude coordinate
    for name in lon_options:
        if name in da.coords:
            lon_name = name
            break
            
    if not lat_name or not lon_name:
        raise ValueError(
            f"Could not automatically identify spatial dimensions. "
            f"Coordinates found: {list(da.coords)}"
        )
        
    return lat_name, lon_name

# ----------------------------------------------------------
# Helper: Safe Slice
# ----------------------------------------------------------
def safe_slice(da: xr.DataArray, min_val: float, max_val: float, dim_name: str) -> xr.DataArray:
    """
    Slices a DataArray safely, handling both ascending and descending coordinate orders.

    Standard xarray slicing requires `slice(min, max)` for ascending data, 
    but `slice(max, min)` for descending data (like latitude from 90 to -90).

    Args:
        da (xr.DataArray): Input data.
        min_val (float): Minimum bound of the slice.
        max_val (float): Maximum bound of the slice.
        dim_name (str): Name of the dimension to slice.

    Returns:
        xr.DataArray: The subset of the data within the specified bounds.
    """
    if dim_name not in da.coords:
        return da
        
    # Check if dimension exists and has more than 1 point to determine order
    if da[dim_name].size > 1:
        # Check if the first value is greater than the last (Descending order)
        if da[dim_name][0] > da[dim_name][-1]:
            return da.sel({dim_name: slice(max_val, min_val)})
        else:
            # Ascending order
            return da.sel({dim_name: slice(min_val, max_val)})
    else:
        # If single point or unsorted/unknown, try standard slice or nearest method implicit in usage
        return da.sel({dim_name: slice(min_val, max_val)})

# ----------------------------------------------------------
# Spatial Filter Helper
# ----------------------------------------------------------
def filter_xarray_with_shape(xds: xr.DataArray, gdf: gpd.GeoDataFrame, lat_name: str, lon_name: str) -> xr.DataArray:
    """
    Clips an xarray DataArray using a vector geometry (GeoDataFrame).
    
    This function uses `rioxarray` to mask out data outside the polygon boundaries.

    Args:
        xds (xr.DataArray): The spatial data to be clipped.
        gdf (gpd.GeoDataFrame): The shapefile data containing the geometry.
        lat_name (str): Name of the latitude dimension.
        lon_name (str): Name of the longitude dimension.

    Returns:
        xr.DataArray: The clipped data containing only pixels inside the geometry.

    Raises:
        ValueError: If the xarray object is missing a CRS (Coordinate Reference System).
        NoDataInBounds: If the clip operation results in empty data (no overlap).
    """
    # Register spatial dimensions with rioxarray
    xds.rio.set_spatial_dims(x_dim=lon_name, y_dim=lat_name, inplace=True)

    # Ensure the DataArray has a CRS assigned
    if not xds.rio.crs:
        raise ValueError("The xarray dataset does not have spatial reference (CRS).")

    # Reproject GeoDataFrame to match the DataArray's CRS if they differ
    if gdf.crs != xds.rio.crs:
        gdf = gdf.to_crs(xds.rio.crs)

    geom = gdf.geometry

    try:
        # Perform the clip. 
        # all_touched=True ensures pixels intersecting the boundary are included.
        # This is crucial for small coastal regions or narrow shapes.
        xds_clipped = xds.rio.clip(
            geom.apply(mapping),
            xds.rio.crs,
            drop=True,
            all_touched=True 
        )
    except NoDataInBounds:
        # Re-raise to be handled by the main loop
        raise NoDataInBounds
        
    return xds_clipped

# ----------------------------------------------------------
# Main Extraction Function
# ----------------------------------------------------------
def extract_data(
    da: xr.DataArray, 
    shapefile_path: str, 
    region_column: str, 
    buffer: float = 0.25
) -> pd.DataFrame:
    """
    Iterates through regions in a shapefile, extracts climate data, calculates spatial averages,
    and consolidates the results into a single DataFrame.

    This is the core function of the library. It handles CRS matching, dynamic slicing
    (for performance), and precise geometric clipping.

    Args:
        da (xr.DataArray): The climate data (must contain spatial coords and optionally time).
        shapefile_path (str): File path to the .shp or .gpkg file defining regions.
        region_column (str): Column name in the shapefile to identify unique regions (e.g., 'city_name').
        buffer (float, optional): Buffer in degrees to add around the bounding box 
                                  before clipping. Defaults to 0.25.

    Returns:
        pd.DataFrame: A long-format DataFrame containing the spatially averaged data 
                      for all processed regions. Returns empty DF if no data found.
    """
    print(f"=== Extracting data for each region based on column: '{region_column}' ===")
    
    # 1. Identify spatial dimension names automatically
    lat_name, lon_name = identify_spatial_dims(da)
    
    # 2. Standardize longitude to -180/180 if necessary
    da = standardize_longitude(da, lon_name)
    
    # 3. Load Shapefile and enforce WGS84 (EPSG:4326) standard
    gdf = gpd.read_file(shapefile_path)
    gdf = gdf.to_crs("EPSG:4326")

    # 4. Ensure DataArray also has WGS84 CRS
    if not da.rio.crs:
        da.rio.write_crs("EPSG:4326", inplace=True)
        
    results = []
    
    # Iterate over each unique region in the shapefile
    unique_regions = gdf[region_column].unique()
    for region in tqdm(unique_regions, desc="Processing regions"):
        
        # Filter the GeoDataFrame for the current region
        region_gdf = gdf[gdf[region_column] == region]
        
        # Get the bounding box (minx, miny, maxx, maxy)
        minx, miny, maxx, maxy = region_gdf.total_bounds
        
        # Performance Step: Roughly slice the DataArray to the bounding box + buffer.
        # This prevents loading/processing the entire global map for a small region.
        da_subset = safe_slice(da, miny - buffer, maxy + buffer, lat_name)
        da_subset = safe_slice(da_subset, minx - buffer, maxx + buffer, lon_name)
        
        # Re-write CRS to subset (sometimes lost during slicing)
        da_subset.rio.write_crs("EPSG:4326", inplace=True)
        
        try:
            # Precision Step: Clip using the exact polygon geometry
            da_sub = filter_xarray_with_shape(da_subset, region_gdf, lat_name, lon_name)
            
            # Calculate Spatial Mean (reduce lat/lon to a single value per time step)
            # Result converts to DataFrame (columns: time, value, etc.)
            df_sub = (
                da_sub
                .mean(dim=[lat_name, lon_name])
                .to_dataframe()
                .reset_index() 
            )
            
        except (NoDataInBounds, ValueError):
            # Fallback Strategy:
            # If the region is too small (smaller than grid cell) or irregular,
            # 'rio.clip' might fail. We use the region's centroid to pick the nearest pixel.
            # print(f"Fallback to centroid for {region}") # Optional verbose log
            centroid = region_gdf.centroid.iloc[0]
            try:
                da_sub = da.sel(
                    {lat_name: centroid.y, lon_name: centroid.x},
                    method="nearest"
                )
                df_sub = da_sub.to_dataframe().reset_index()
            except Exception:
                # If even centroid fails, skip this region
                continue
        
        # --- Post-Processing the DataFrame ---
        
        # Clean up: Remove technical 'spatial_ref' column if generated by rioxarray
        if "spatial_ref" in df_sub.columns:
            df_sub = df_sub.drop(columns=["spatial_ref"])
            
        # Feature Engineering: Extract calendar components if 'time' exists
        if "time" in df_sub.columns:
            df_sub["year"] = pd.to_datetime(df_sub["time"]).dt.year
            df_sub["month"] = pd.to_datetime(df_sub["time"]).dt.month
            df_sub["day"] = pd.to_datetime(df_sub["time"]).dt.day
        
        # Tag the data with the region name
        df_sub["region"] = region

        # Append to master list
        results.append(df_sub)
            
    # Concatenate all region dataframes into one
    if results:
        df_out = pd.concat(results, ignore_index=True)
        print(f"✅ Extraction complete for {len(results)} subregions")
        return df_out
    else:
        print("⚠️ No subregions processed")
        return pd.DataFrame()


