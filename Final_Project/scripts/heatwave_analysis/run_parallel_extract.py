import pandas as pd
import geopandas as gpd
import xarray as xr
import numpy as np
import os
import shutil
from mpi4py import MPI

# Import the original extraction module WITHOUT any modifications.
# This script only orchestrates parallel execution around `extract.extract_data`.
import extract 

# ==========================================
# CONFIGURATION
# ==========================================
# Path to the climate data (NetCDF / xarray-readable file)
DATA_FILE = r'C:\Users\rafaq\OneDrive\Documentos\IU\Travis_project\data_Era5\dados_era5_rio_janeiro_1980_2024\tmax-rj.1940.2024.v.nc'

# Path to the original shapefile containing all municipalities/regions
SHAPEFILE_PATH = r'C:\Users\rafaq\OneDrive\Documentos\Tese_Brasil\municipios_RJ\RJ_Municipios_2024\RJ_Municipios_2024.shp'

# Column in the shapefile that uniquely identifies each region/municipality
REGION_COLUMN = "NM_MUN"

# Name of the final CSV file with the consolidated extraction results
OUTPUT_FILE   = "result_complet_extract.csv"

# Temporary folder where per-rank shapefiles will be written
TEMP_FOLDER   = "temp_mpi_shapes"

# ==========================================
# MPI SETUP
# ==========================================
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

def main():
    """
    Run the extraction pipeline in parallel using MPI.

    Overview
    --------
    This script parallelizes the spatial extraction of climate data
    for multiple regions defined in a shapefile. The workflow is:

    1. All ranks lazily open the climate dataset using xarray.
    2. Rank 0:
       - Reads the full shapefile containing all regions.
       - Splits the list of regions into `size` chunks (one per MPI rank).
       - Writes one temporary shapefile per rank, each containing
         only the subset of regions assigned to that rank.
    3. All ranks:
       - Read their corresponding temporary shapefile (if it exists).
       - Call `extract.extract_data(...)` on that subset of regions.
    4. Rank 0:
       - Gathers all partial DataFrames from the ranks.
       - Concatenates them into a single DataFrame.
       - Writes the final CSV to disk.
       - Removes the temporary shapefile folder.

    Notes
    -----
    - The original extraction logic is fully encapsulated in
      `extract.extract_data` and is not modified here.
    - This script only handles parallel orchestration (I/O, splitting,
      gathering) using `mpi4py`.
    """

    # 1. Load the climate data (lazy load with xarray).
    # All MPI processes open the same dataset. This is typically lightweight
    # because xarray defers reading the full data from disk until needed.
    ds = xr.open_dataset(DATA_FILE)
    
    # If your dataset contains multiple variables, you could select one here.
    # Example: da = ds['tmax']
    # In this script we assume `extract.extract_data` knows how to handle `ds`
    # (either as a Dataset or as a specific DataArray).
    da = ds  

    # ---------------------------------------------------------
    # STEP 1: RANK 0 PREPARES THE WORKLOAD (SPLIT SHAPEFILE)
    # ---------------------------------------------------------
    path_meu_shape = ""
    
    if rank == 0:
        print(f"--- [Master] Starting parallelization with {size} processes ---")
        
        # Create temporary folder (if it does not already exist)
        if not os.path.exists(TEMP_FOLDER):
            os.makedirs(TEMP_FOLDER)
            
        # Read the original shapefile with all regions
        full_gdf = gpd.read_file(SHAPEFILE_PATH)
        unique_regions = full_gdf[REGION_COLUMN].unique()
        
        print(f"--- Total number of regions to process: {len(unique_regions)}")
        
        # Split the list of regions into `size` chunks, one per MPI rank
        region_chunks = np.array_split(unique_regions, size)
        
        # Save a temporary shapefile for each rank, containing only its subset
        for i, regions_subset in enumerate(region_chunks):
            # Filter the GeoDataFrame to only the regions assigned to this chunk
            subset_gdf = full_gdf[full_gdf[REGION_COLUMN].isin(regions_subset)]
            
            # Path for the temporary shapefile for rank i
            temp_filename = os.path.join(TEMP_FOLDER, f"shape_rank_{i}.shp")
            
            # Write the subset to disk (only if not empty)
            if not subset_gdf.empty:
                subset_gdf.to_file(temp_filename)
            else:
                # If this chunk has no regions (e.g., more ranks than regions),
                # we skip creating a file. That rank will simply have no work.
                pass
                
        print("--- [Master] Temporary shapefiles created. Releasing workers...")

    # Barrier: all ranks wait here until Rank 0 finishes setting up the shapefiles.
    comm.Barrier()

    # ---------------------------------------------------------
    # STEP 2: EACH RANK PROCESSES ITS ASSIGNED SUBSET
    # ---------------------------------------------------------
    
    # Determine the path to the temporary shapefile for this rank
    my_temp_shape = os.path.join(TEMP_FOLDER, f"shape_rank_{rank}.shp")
    
    # Initialize an empty DataFrame to hold this rank's partial results
    df_result = pd.DataFrame()

    # Check whether this rank has a corresponding shapefile to process
    # (there may be more ranks than chunks if the number of regions is small)
    if os.path.exists(my_temp_shape):
        print(f"[Rank {rank:02d}] Starting extraction for file: {my_temp_shape}")
        
        # === CORE IDEA ===
        # We call the ORIGINAL extraction function here.
        # From the perspective of `extract.extract_data`, this is just a normal
        # shapefile with a subset of regions. It is "unaware" that the work
        # has been partitioned across ranks.
        try:
            df_result = extract.extract_data(
                da=da, 
                shapefile_path=my_temp_shape, 
                region_column=REGION_COLUMN
            )
        except Exception as e:
            print(f"[Rank {rank:02d}] Extraction error: {e}")
            
        print(f"[Rank {rank:02d}] Finished. Rows generated: {len(df_result)}")
    else:
        # This rank has no shapefile assigned and therefore no work to do.
        print(f"[Rank {rank:02d}] No work (temporary shapefile not found).")

    # ---------------------------------------------------------
    # STEP 3: GATHER AND CONSOLIDATE RESULTS
    # ---------------------------------------------------------
    # Rank 0 receives the partial DataFrames from all ranks.
    all_dfs = comm.gather(df_result, root=0)

    if rank == 0:
        print("--- Consolidating results from all ranks... ---")
        # Filter out empty DataFrames (in case some ranks had no work or errors)
        valid_dfs = [d for d in all_dfs if not d.empty]
        
        if valid_dfs:
            # Concatenate all partial results into a single DataFrame
            final_df = pd.concat(valid_dfs, ignore_index=True)
            final_df.to_csv(OUTPUT_FILE, index=False)
            print(f"✅ SUCCESS! Final file saved to: {OUTPUT_FILE}")
            print(f"   Total number of rows processed: {len(final_df)}")
        else:
            print("⚠️ Warning: No data was generated by any rank.")

        # Cleanup: remove the temporary shapefiles folder
        try:
            shutil.rmtree(TEMP_FOLDER)
            print("--- Temporary shapefiles removed ---")
        except:
            # If cleanup fails, we silently ignore it to avoid crashing at the end.
            pass

if __name__ == "__main__":
    main()
