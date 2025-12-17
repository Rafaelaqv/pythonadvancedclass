import numpy as np
import pandas as pd
import warnings
from typing import List, Tuple, Dict, Optional, Union

# Ignore numpy empty slice warnings (common when calculating percentiles on empty windows)
warnings.filterwarnings("ignore", category=RuntimeWarning)

class HeatwaveDetector:
    """
    Implements a Heatwave Detection Algorithm based on daily relative thresholds.
    
    Methodology (Adapted from Geirinhas et al. 2021):
    1.  **Climatological Baseline:** Calculates a percentile threshold (e.g., 90th) 
        for each calendar day (Day of Year - DOY).
    2.  **Moving Window:** Uses a circular window (e.g., 15 days) to ensure 
        sample size sufficiency and smooth seasonality.
    3.  **Event Detection:** Identifies consecutive days where Temperature > Threshold.
    4.  **Characterization:** Computes intensity, duration, and frequency metrics.

    Attributes:
        df (pd.DataFrame): The pre-processed dataframe with datetime index.
        var (str): The column name of the variable being analyzed (e.g., 't2m').
        baseline_df (pd.DataFrame): The subset of data used to calculate thresholds.
    """

    def __init__(
        self, 
        df: pd.DataFrame, 
        variable: str = 't2m', 
        date_col: str = 'time', 
        reference_period: Optional[Tuple[int, int]] = None
    ):
        """
        Initializes the detector and prepares the time series.

        Args:
            df (pd.DataFrame): Input DataFrame containing climate data.
            variable (str): Column name of the temperature variable.
            date_col (str): Column name representing the date/time.
            reference_period (tuple, optional): A tuple (start_year, end_year) 
                                                defining the baseline for threshold calculation.
                                                If None, uses the entire dataset.

        Raises:
            ValueError: If the specified columns do not exist in the DataFrame.
        """
        self.df = df.copy()
        self.var = variable
        
        # 1. Column Validation
        if self.var not in self.df.columns:
            raise ValueError(
                f"Column '{self.var}' not found in DataFrame. "
                f"Available columns: {list(self.df.columns)}"
            )

        if date_col not in self.df.columns:
            raise ValueError(
                f"Date column '{date_col}' not found in DataFrame. "
                f"Available columns: {list(self.df.columns)}"
            )
            
        # 2. Date Configuration
        # Convert to datetime objects and set as the dataframe index
        self.df[date_col] = pd.to_datetime(self.df[date_col])
        self.df = self.df.set_index(date_col).sort_index()
        
        # 3. Fill Missing Days (CRITICAL STEP)
        # We must ensure a perfect daily frequency. If a day is missing in the raw data,
        # it might break a heatwave streak effectively splitting one event into two.
        # .asfreq() inserts NaNs for missing dates, preserving the timeline structure.
        self.df = self.df.resample('D').asfreq()
        
        # Create auxiliary calendar columns for grouping
        self.df['doy'] = self.df.index.dayofyear
        self.df['year'] = self.df.index.year
        self.df['month'] = self.df.index.month
        
        # Define Reference Period (Baseline)
        if reference_period:
            self.baseline_df = self.df[
                (self.df['year'] >= reference_period[0]) & 
                (self.df['year'] <= reference_period[1])
            ].copy()
        else:
            self.baseline_df = self.df.copy()

    def get_doy_threshold(self, percentile: float, window_size: int = 15) -> Dict[int, float]:
        """
        Calculates the percentile threshold for each Day of Year (DOY) using a 
        circular moving window.

        Circular Window logic:
        For Jan 1st, the window includes days from late December and early January.
        This ensures smooth transitions across the year boundary.

        Args:
            percentile (float): The percentile to compute (e.g., 90 for 90th percentile).
            window_size (int): The total size of the window in days (centered). 
                               Default is 15 (+/- 7 days).

        Returns:
            Dict[int, float]: A dictionary mapping {Day_of_Year: Threshold_Value}.
        """    
        # Safety Check: Empty baseline -> explicit error
        if self.baseline_df.empty:
            raise ValueError(
                "Baseline dataframe is empty. "
                "Check 'reference_period' or input data range."
            )

        radius = window_size // 2
        doy_threshold_map = {}

        # Extract numpy arrays for performance (much faster than iterating pandas rows)
        base_doy = self.baseline_df['doy'].values
        base_val = self.baseline_df[self.var].values

        # Filter NaNs to avoid calculation errors or skewed percentiles
        valid_mask = ~np.isnan(base_val)
        base_doy = base_doy[valid_mask]
        base_val = base_val[valid_mask]

        # Define cycle (365 or 366) based on data present in the baseline
        days_in_year = int(self.baseline_df['doy'].max())

        # Iterate dynamically through every day of the year
        for day in range(1, days_in_year + 1):
            
            # Circular distance calculation:
            # Calculates the shortest distance between days considering the 365-day wrap.
            # Example: Distance between Day 365 and Day 2 is 2 days.
            dist = np.minimum(
                np.abs(base_doy - day), 
                days_in_year - np.abs(base_doy - day)
            )
            
            # Select data within the window radius
            window_data = base_val[dist <= radius]
            
            # Statistical robustness check:
            # Require a minimum number of data points (e.g., 10) to calculate a valid percentile.
            if len(window_data) >= 10: 
                doy_threshold_map[day] = np.percentile(window_data, percentile)
            else:
                doy_threshold_map[day] = np.nan
                
        return doy_threshold_map

    def analyze(
        self, 
        percentiles: List[float] = [80, 90, 95], 
        min_duration: int = 3
    ) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """
        Executes the full heatwave analysis workflow.

        Steps:
        1. Calculates thresholds for specified percentiles.
        2. Identifies 'Hot Days' (Temp > Threshold).
        3. Groups consecutive hot days into 'Events'.
        4. Filters events shorter than `min_duration`.
        5. Computes metrics (intensity, duration, frequency).

        Args:
            percentiles (List[float]): List of percentiles to analyze.
            min_duration (int): Minimum number of consecutive days to classify as a heatwave.

        Returns:
            Tuple[pd.DataFrame, pd.DataFrame]:
                - events_df: Detailed list of every individual heatwave event.
                - metrics_df: Aggregated statistics summary.
        """
        all_events = []

        for p in percentiles:
            # 1. Calculate Seasonal Threshold (Climatology)
            doy_map = self.get_doy_threshold(percentile=p, window_size=15)
            thresh_col = f'thresh_{p}'
            
            # 2. Map threshold to the full time series based on DOY
            self.df[thresh_col] = self.df['doy'].map(doy_map)
            
            # 3. Detect Hot Days (Boolean Series)
            hot_days = self.df[self.var] > self.df[thresh_col]
            
            # 4. Group Consecutive Days (The "Streaks" Logic)
            # Logic explanation:
            # hot_days.shift() shifts the boolean series by one day.
            # (hot_days != hot_days.shift()) identifies where the status changes (False->True or True->False).
            # .cumsum() increments a counter every time the status changes, creating a unique ID for each group.
            groups = (hot_days != hot_days.shift()).cumsum()
            
            # Filter only groups that are actually True (hot days), discarding the "cool" periods
            event_groups = self.df[hot_days].groupby(groups)
            
            for _, group in event_groups:
                duration = len(group)
                
                # Check minimum duration criteria
                if duration >= min_duration:
                    
                    # Categorize duration for summary stats
                    if 3 <= duration <= 4:
                        cat = '3-4 days'
                    elif 5 <= duration <= 7:
                        cat = '5-7 days'
                    else:
                        cat = '>7 days'
                    
                    # Calculate Event Metrics
                    mean_temp = group[self.var].mean()
                    max_temp = group[self.var].max()
                    
                    # Intensity (Anomaly relative to local threshold)
                    anomalies = group[self.var] - group[thresh_col]
                    intensity_mean = anomalies.mean()
                    intensity_max = anomalies.max()

                    all_events.append({
                        'percentile': p,
                        'duration_category': cat,
                        'start_date': group.index[0],
                        'end_date': group.index[-1],
                        'duration_days': duration,
                        'mean_temperature': mean_temp,
                        'max_temperature': max_temp,
                        'intensity_mean': intensity_mean,
                        'intensity_max': intensity_max,
                        'year': group.index[0].year,
                        'season': self._get_season(group.index[0].month)
                    })

        events_df = pd.DataFrame(all_events)
        
        # Handle case where no events are found
        if events_df.empty:
            print(f"⚠️ No heatwave events detected (min_duration={min_duration}).")
            return pd.DataFrame(), pd.DataFrame()

        # 5. Calculate Aggregated Metrics
        # Groups data by percentile and category to produce the final summary table
        metrics_df = events_df.groupby(['percentile', 'duration_category']).agg(
            total_events=('duration_days', 'count'), 
            avg_duration=('duration_days', 'mean'),
            avg_intensity=('intensity_mean', 'mean'),
            max_intensity=('intensity_max', 'max')
        ).reset_index()
        
        # Calculate Annual Frequency (Total Events / Number of Years)
        n_years = self.df['year'].nunique()
        metrics_df['annual_frequency'] = metrics_df['total_events'] / n_years

        return events_df, metrics_df

    def _get_season(self, month: int) -> str:
        """
        Helper method to determine meteorological season from month number.
        """
        if month in [12, 1, 2]: return 'DJF'
        if month in [3, 4, 5]: return 'MAM'
        if month in [6, 7, 8]: return 'JJA'
        return 'SON'