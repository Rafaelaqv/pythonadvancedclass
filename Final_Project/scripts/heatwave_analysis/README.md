## Climate Data Extraction & Heatwave Analysis Library

This library was developed to perform **geospatial climate data extraction and extreme event analysis**, with a particular focus on heatwaves. The core detection algorithm follows the methodology proposed by **Geirinhas et al. (2021)**, identifying heatwave events based on daily relative temperature thresholds. A heatwave is defined as a sequence of consecutive days in which maximum temperature ($T_{max}$) exceeds a percentile-based threshold derived from the local climatology. These thresholds are computed using a **15-day centered moving window**.

Designed for flexibility and extensibility, the toolkit enables users to quantify temporal and spatial changes in heatwave frequency and intensity across multiple configurations: 

* **Percentiles:** 80th, 90th, and 95th.
* **Durations:** Short (3–4 days), Medium (5–7 days), and Long (>7 days).

To efficiently process large historical datasets (e.g., ERA5 or CHIRPS), the library incorporates **parallel computing via mpi4py**, allowing extraction and heatwave analysis to be distributed across multiple processors.

As a practical demonstration, this repository includes **a case study examining heatwave frequency across the State of Rio de Janeiro (Brazil) from 1940–2024**. The goal is to investigate how heatwaves vary spatially and how their frequency and intensity have evolved over time in a geographically diverse region. Specifically, the analysis seeks to address the following questions:

1. How do heatwaves vary spatially across the state of Rio de Janeiro?
2. How has the frequency of heatwaves changed between 1940-1960 and 2004-2024 across the state’s municipalities?
3. What are the differences in the temporal trends of heatwaves among the city of Rio de Janeiro (the capital), Petrópolis (a high-altitude municipality), and the state as a whole?

## Library Structure

The library is organized into two main modules:

1. **Extraction Module** - Extracts climate data from NetCDF files for regions defined in shapefiles.
2. **Detection and Analysis Module** - Detects and characterizes heatwave events using percentile and durations thresholds.

---

## File Descriptions

### **Core Modules**

#### `extract.py`

**Purpose:** Main library for spatial extraction of climate data.

**Key Features:**

- Extraction of NetCDF/xarray data for regions defined by polygons (shapefiles);

- Automatic coordinate system conversion (0-360° → -180/180°);

- Automatic identification of spatial dimensions (lat/lon);

- Precise geometric clipping using `rioxarray`;

- Smart Fallback: Uses region centroid when the polygon is smaller than the grid pixel resolution;

- Calculation of spatial averages per region. 

**Main Functions:**

- `extract_data()`: Main function that processes all regions in the shapefile;

- `standardize_longitude()`: Standardizes longitude coordinates; 

- `identify_spatial_dims()`: Automatically detects spatial dimension names;

- `filter_xarray_with_shape()`: Performs the actual spatial masking and clipping.

**Typical Usage:**

```python
import xarray as xr
from extract import extract_data

# Load climate data
ds = xr.open_dataset('climate.nc')

# Extract data for regions
df = extract_data(
    da=ds['t2m'],
    shapefile_path='municipalities.shp',
    region_column='NM_MUN',
    buffer=0.25
)
```

---

#### `core_heatwave.py`

**Purpose:** Implements the heatwave detection algorithm based on Geirinhas et al. (2021).

**Key Features:**

- **Climatological Baseline:** Calculates percentile thresholds (e.g., 90th) for each **Day of Year (DOY)** using a 15-day centered moving window;

- **Event Detection:** Identifies consecutive days where $T_{max}$ exceeds the specific threshold (e.g., 90th percentile);

- **Metric Calculation:** Characterizes events by intensity, duration, and frequency; 

- **Seasonality Handling:** Automatically assigns seasons (DJF, MAM, etc.) to events.

**Main Class: `HeatwaveDetector`**

**Methods:**

- `__init__()`: Initializes the detector and prepares the time series;

- `get_doy_threshold()`: Calculates thresholds for each day of year;

- `analyze()`: Executes complete analysis and returns events + metrics;

- `_get_season()`: Helper function to classify meteorological seasons.

**Typical Usage:**

```python
from core_heatwave import HeatwaveDetector

# Initialize detector
detector = HeatwaveDetector(
    df=temperature_data,
    variable='t2m',
    date_col='time',
    reference_period=(1980, 2010)
)

# Analyze heatwaves
events_df, metrics_df = detector.analyze(
    percentiles=[80, 90, 95],
    min_duration=3
)
```

---

### **Parallelization Scripts (MPI)**

#### `run_parallel_extract.py`

**Purpose:** Orchestrates parallel climate data extraction using MPI.

**Parallelization Strategy:**

1. **Master (Rank 0):** Splits the shapefile into N parts (one per process);
2. **Workers (All ranks):** Each process handles its subset of regions independently;
3. **Gather:** Rank 0 consolidates all results into a single CSV.

**Workflow:**

```
Rank 0: Reads complete shapefile → Splits into chunks → Creates temporary shapefiles
   ↓
All: Process their assigned regions using extract.extract_data()
   ↓
Rank 0: Receives results → Concatenates → Saves final CSV → Removes temporary files
```

**How to Execute:**

```bash
# Example: Using 4 parallel processes
mpiexec -n 4 python run_parallel_extract.py
```

**Note on -n flag: Adjust this value to change the number of parallel processes.**

- -n 4 → uses 4 MPI processes (ranks 0–3).

- You can try other values (e.g., 2, 8) depending on your machine's CPU cores.

**Prerequisites & Setup: This script assumes that:**

- Environment: mpi4py is installed and mpiexec (or mpirun) is available in your system path;

- Dependencies: xarray, geopandas, pandas, numpy are installed;

- File Structure: The module extract.py must be in the same directory (or on the Python path); 

- Configuration: You must edit the paths inside run_parallel_extract.py before running:  DATA_FILE and SHAPEFILE_PATH

**Expected Output:**

- `result_complet_extract.csv`: Consolidated table with extracted time series for all regions.

---

#### `heatwave_mpi.py`

**Purpose:** Parallel heatwave analysis for multiple regions.

**Strategy:**

1. All processes load the CSV generated by the extraction step;

2. The list of unique regions is divided equally among processes;

3. Each process applies the `HeatwaveDetector` class to its assigned regions;

4. Rank 0 consolidates all event tables and metrics.

**Workflow:**

```
All: Load input CSV → Receive subset of regions
   ↓
Each rank: Applies HeatwaveDetector to its regions
   ↓
Rank 0: Receives events + metrics → Concatenates → Saves global CSVs
```

**How to Execute:**

```bash
# Example: Using 2 parallel processes
mpiexec -n 2 python heatwave_mpi.py
```

**Note on -n flag: Since heatwave detection is computationally intensive, using more cores (e.g., -n 4 or -n 8) significantly reduces runtime on large datasets.**

---

### **Test and Demonstration Notebooks**

## Test and Demonstration Notebooks

| Notebook | Purpose |
|----------|---------|
| `1_extract_test.ipynb` | Validates the extraction workflow. Includes data inspection, sanity checks, and visualization of the spatial mask. |
| `2_heatwave_test.ipynb` | Demonstrates the `HeatwaveDetector` class. Compares detection on a regional scale (State) vs. local scale (Municipality). |
| `3_total_table.ipynb` | Consolidates results. Merges state and municipal outputs into unified master tables (`MASTER_metrics` and `MASTER_events`). |
| `4_products_analysis.ipynb` | In-depth analysis. Generates maps, trend plots, and spatial comparisons (e.g., Rio vs Petrópolis). |

---

## **Repository Structure**

## Repository Structure

```plaintext
├── extract.py                # Spatial extraction for climate datasets
├── run_parallel_extract.py   # MPI orchestration for extraction
├── core_heatwave.py          # Heatwave detection logic (percentiles, events, metrics)
├── heatwave_mpi.py           # MPI orchestration for heatwave analysis
│
├── 1_extract_test.ipynb      # Notebook to validate the extraction workflow
├── 2_heatwave_test.ipynb     # Notebook to validate the heatwave calculation
├── 3_total_table.ipynb       # Combines extraction + heatwave output for analysis
├── 4_products_analysis.ipynb # Statistical and spatial analysis of final results
```

## Complete Workflow

### 🟦 1️⃣ Data Extraction
- **Scripts:** `extract.py`, `run_parallel_extract.py`
- **Notebook:** `1_extract_test.ipynb`
- **Output:** `result_complet_extract.csv`, `processed_data/results_rj_municipalities.csv`, `processed_data/results_rj_state.csv` and `processed_data/validation_plot.png`

---

### 🟩 2️⃣ Heatwave Analysis
- **Scripts:** `core_heatwave.py`, `heatwave_mpi.py`
- **Notebook:** `2_heatwave_test.ipynb`
- **Outputs:** `outputs/GLOBAL_EVENTS.csv`, `outputs/GLOBAL_METRICS.csv`

---

### 🟨 3️⃣ Results Analysis
- **Notebooks:** `3_total_table.ipynb`, `4_products_analysis.ipynb`
- **Final Outputs:**
  * `outputs/MASTER_events_all_regions.csv`
  * `outputs/MASTER_metrics_all_regions.csv`
  * `heatwave_timeseries_panel.png`
  * `heatwave_maps_percentile_80.png`
  * `heatwave_maps_percentile_90.png`
  * `heatwave_maps_percentile_95.png`
  * `outputs\heatwave_maps_diff_allpercentile.png`

---

## Installation & Requirements

To replicate this environment, ensure you have **Python 3.8+** installed.

### Quick Setup

You can install all necessary dependencies automatically using `pip`:

```bash
pip install -r requirements.txt
```

**System Dependencies (MPI)**

For the parallel scripts (run_parallel_extract.py and heatwave_mpi.py) to work, you must have an MPI implementation installed on your system:

- Linux: `sudo apt-get install mpich`

- Windows: Install Microsoft MPI.

- MacOS: `brew install open-mpi`

### Required Python Libraries

| Category          | Libraries                                      |
|-------------------|------------------------------------------------|
| **Core Processing** | `xarray`, `numpy`, `pandas`, `mpi4py`        |
| **Geospatial**      | `geopandas`, `rioxarray`, `shapely`          |
| **Visualization**   | `matplotlib`, `seaborn`                      |
| **Utilities**       | `tqdm` *(Progress bars)*                     |

> *Note: Standard Python libraries used include `os`, `sys`, `shutil`, `itertools`, and `typing`.*

---

## Configuration

### Adjustments in Parallelization Scripts

**In `run_parallel_extract.py`:**
```python
DATA_FILE = "path/to/your/file.nc"
SHAPEFILE_PATH = "path/to/your/shapefile.shp"
REGION_COLUMN = "column_name"
OUTPUT_FILE = "extraction_result.csv"
```

**In `heatwave_mpi.py`:**
```python
INPUT_FILE = "extraction_result.csv"  # Output from extraction
VAR_NAME = "t2m"                      # Variable name
PERCENTILES = [80, 90, 95]           # Thresholds to analyze
REF_PERIOD = (1980, 2010)            # Reference period
```

---

## 📊 Output Structure

### Extraction CSV (`result_complet_extract.csv`)
| Column | Description |
|--------|-----------|
| `region` | Region/municipality name |
| `time` | Observation date/time |
| `t2m` (or other variable) | Climate variable value |
| `year`, `month`, `day` | Date components |

### Events CSV (`GLOBAL_EVENTS.csv`)
| Column | Description |
|--------|-----------|
| `region` | Region name |
| `percentile` | Percentile used (80, 90, 95) |
| `start_date` | Event start date |
| `end_date` | Event end date |
| `duration_days` | Duration in days |
| `mean_temperature` | Average event temperature |
| `max_temperature` | Maximum event temperature |
| `intensity_mean` | Mean anomaly (°C above threshold) |
| `intensity_max` | Maximum anomaly |
| `year` | Event year |
| `season` | Meteorological season (DJF, MAM, JJA, SON) |

### Metrics CSV (`GLOBAL_METRICS.csv`)
| Column | Description |
|--------|-----------|
| `region` | Region name |
| `percentile` | Percentile used |
| `duration_category` | Duration category (3-4 days, 5-7 days, >7 days) |
| `total_events` | Total number of events |
| `avg_duration` | Average event duration |
| `avg_intensity` | Average intensity |
| `max_intensity` | Maximum observed intensity |
| `annual_frequency` | Annual frequency of events |

---

## Key Use Cases

### Technical Capabilities

1. **Custom Spatial Extraction:** Efficiently mask and retrieve raw climate variables (e.g., Temperature) for any irregular geometry defined in a Shapefile (municipalities, watersheds, or custom regions).
    
2. **Sensitivity Analysis:** Test how different definitions affect heatwave detection statistics by easily swapping parameters (e.g., comparing 90th vs. 95th percentiles; 3-day vs. 5-day duration thresholds).

3. **High-Performance Computing (HPC):** Process decades of high-resolution daily data across hundreds of regions simultaneously using MPI, enabling large-scale studies without memory bottlenecks.

### 🔬 Scientific Applications

4. **Long-Term Trend Analysis:** Quantify climate change signals by evaluating shifts in the frequency, duration, and intensity of extreme events over historical periods (e.g., 1940–2024).

5. **Spatial Vulnerability Mapping:** IIdentify geographic hotspots and regions that are most susceptible to heatwave events

6. **Event Characterization:** Go beyond simple counting: analyze the seasonality (when they happen) and physical magnitude (how hot they get) of individual heatwave events.

---

## Technical Notes

### Performance & Scalability

- **Parallel Speedup:** The extraction module achieves **near-linear speedup** with the number of MPI processes added, limited primarily by disk read speeds.

- **Efficiency:** The MPI implementation is highly efficient for datasets containing >50 regions/municipalities.

- **I/O Bound:** The primary bottleneck is the NetCDF reading operation. *Tip: For extremely large global datasets (>1TB), integrating Dask within the `extract.py` module is recommended.*

### Known Limitations

1. **Spatial Resolution vs. Geometry:** * If a region polygon is smaller than the grid pixel resolution (common in small municipalities), the algorithm automatically falls back to a **"Centroid Nearest Neighbor"** approach to ensure data is retrieved.

2. **Data Continuity:** * Missing values (NaNs) in the source data are handled to prevent the heatwave detection loop from breaking, but extensive gaps may affect statistical confidence.

3. **Statistical Robustness:** * The moving window algorithm requires a minimum of **10 valid observations** (within the 15-day window) across the historical period to calculate a valid percentile threshold.

---

## Credits

**Author:** Rafaela Quintella Veiga  
**Course:** EAS-G690 (Prof. Travis O'Brien)  
**Purpose:** Developed for ERA5 climate data analysis and heatwave studies 

*Contact: [raquin@iu.edu]*

