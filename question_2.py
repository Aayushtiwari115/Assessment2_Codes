# question_2_Solution
# ---------------------------------------------------------------------
# Seasonal Temperature Analysis from Monthly Station CSVs
# ---------------------------------------------------------------------
# This script ingests monthly temperature observations from multiple
# station CSV files stored under a 'temperatures/' directory, reshapes
# them into a long-form analytical table, and computes:
#   (i)   seasonal mean temperatures (Summer, Autumn, Winter, Spring),
#   (ii)  the station(s) with the largest observed temperature range, and
#   (iii) station-level temperature stability/variability via standard deviation.
#
# Methodological notes:
# - Each CSV is assumed to contain one row per station and 12 columns for months
#   (January ... December) plus 'STATION_NAME'.
# - Data are melted to long format to facilitate seasonal subsetting and
#   aggregation operations.
# - Seasons are defined using a conventional austral mapping:
#     Summer: Dec–Feb; Autumn: Mar–May; Winter: Jun–Aug; Spring: Sep–Nov.
# - Results are persisted to three text files for auditability and downstream use.
#
# Reproducibility & Transparency:
# - The pipeline is expressed as pure functions with single responsibilities.
# - No in-place mutation of inputs; outputs are explicitly returned and saved.
# - Computation is limited to descriptive statistics (mean, range, std. dev.).
#
# Dependencies: pandas, glob, os
# ---------------------------------------------------------------------

from __future__ import annotations

import glob
import os
from typing import Dict, List, Tuple

import pandas as pd

# ------------------------- Constants ---------------------------------

DATA_FOLDER: str = "temperatures"

SEASON_MONTHS: Dict[str, List[str]] = {
    "Summer": ["December", "January", "February"],
    "Autumn": ["March", "April", "May"],
    "Winter": ["June", "July", "August"],
    "Spring": ["September", "October", "November"],
}

MONTH_COLUMNS: List[str] = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December",
]


# ------------------------- Data I/O & Reshaping -----------------------

def load_data(folder: str) -> pd.DataFrame:
    """
    Load and vertically concatenate monthly temperature data from all CSV files in `folder`.

    Files are expected to include a 'STATION_NAME' column and one column per month.
    The function reshapes each file from wide to long format with columns:
    ['STATION_NAME', 'Month', 'Temperature'].

    Args:
        folder: Path to the directory containing temperature CSV files.

    Returns:
        A pandas DataFrame in long format with non-null 'Temperature' observations.
    """
    all_files: List[str] = glob.glob(os.path.join(folder, "*.csv"))
    df_list: List[pd.DataFrame] = []

    for file in all_files:
        df = pd.read_csv(file)
        df_long = df.melt(
            id_vars=["STATION_NAME"],
            value_vars=MONTH_COLUMNS,
            var_name="Month",
            value_name="Temperature",
        )
        df_list.append(df_long)

    combined_df = pd.concat(df_list, ignore_index=True)
    combined_df = combined_df.dropna(subset=["Temperature"])
    return combined_df


# ------------------------- Analytics ----------------------------------

def calculate_seasonal_avg(df: pd.DataFrame) -> Dict[str, float]:
    """
    Compute mean temperature for each predefined season.

    Args:
        df: Long-form DataFrame with columns ['STATION_NAME', 'Month', 'Temperature'].

    Returns:
        Mapping season -> mean temperature rounded to 1 decimal place.
    """
    results: Dict[str, float] = {}
    for season, months in SEASON_MONTHS.items():
        avg_temp = df[df["Month"].isin(months)]["Temperature"].mean()
        results[season] = round(avg_temp, 1)
    return results


def find_largest_temp_range(df: pd.DataFrame) -> List[Tuple[str, float, float, float]]:
    """
    Identify station(s) exhibiting the largest absolute temperature range (max - min).

    Args:
        df: Long-form DataFrame with columns ['STATION_NAME', 'Month', 'Temperature'].

    Returns:
        A list of tuples (station, range, t_max, t_min) for the station(s) with maximal range.
    """
    ranges: List[Tuple[str, float, float, float]] = []
    max_range: float = 0.0

    for station, temps in df.groupby("STATION_NAME")["Temperature"]:
        t_max = float(temps.max())
        t_min = float(temps.min())
        r = t_max - t_min
        if r > max_range:
            max_range = r
            ranges = [(station, r, t_max, t_min)]
        elif r == max_range:
            ranges.append((station, r, t_max, t_min))
    return ranges


def find_temperature_stability(
    df: pd.DataFrame,
) -> Tuple[List[Tuple[str, float]], List[Tuple[str, float]]]:
    """
    Determine most stable and most variable stations by standard deviation.

    Args:
        df: Long-form DataFrame with columns ['STATION_NAME', 'Month', 'Temperature'].

    Returns:
        A 2-tuple:
          - most_stable:  list of (station, std_dev) having the minimum std. deviation
          - most_variable: list of (station, std_dev) having the maximum std. deviation
    """
    std_list: List[Tuple[str, float]] = [
        (station, float(temps.std()))
        for station, temps in df.groupby("STATION_NAME")["Temperature"]
    ]
    min_std = min(std_list, key=lambda x: x[1])[1]
    max_std = max(std_list, key=lambda x: x[1])[1]
    most_stable = [(s, sd) for s, sd in std_list if sd == min_std]
    most_variable = [(s, sd) for s, sd in std_list if sd == max_std]
    return most_stable, most_variable


# ------------------------- Persistence --------------------------------

def save_seasonal_avg(results: Dict[str, float]) -> None:
    """
    Persist seasonal mean temperatures to 'average_temp.txt'.

    Args:
        results: Mapping of season -> mean temperature.
    """
    with open("average_temp.txt", "w") as f:
        for season, temp in results.items():
            f.write(f"{season}: {temp}°C\n")


def save_largest_temp_range(results: List[Tuple[str, float, float, float]]) -> None:
    """
    Persist stations with largest temperature range to 'largest_temp_range_station.txt'.

    Args:
        results: List of tuples (station, range, t_max, t_min).
    """
    with open("largest_temp_range_station.txt", "w") as f:
        for station, r, t_max, t_min in results:
            f.write(
                f"Station {station}: Range {r:.1f}°C "
                f"(Max: {t_max:.1f}°C, Min: {t_min:.1f}°C)\n"
            )


def save_temperature_stability(
    most_stable: List[Tuple[str, float]],
    most_variable: List[Tuple[str, float]],
) -> None:
    """
    Persist stability/variability results to 'temperature_stability_stations.txt'.

    Args:
        most_stable:   List of (station, std_dev) with minimum dispersion.
        most_variable: List of (station, std_dev) with maximum dispersion.
    """
    with open("temperature_stability_stations.txt", "w") as f:
        for station, sd in most_stable:
            f.write(f"Most Stable: Station {station}: StdDev {sd:.1f}°C\n")
        for station, sd in most_variable:
            f.write(f"Most Variable: Station {station}: StdDev {sd:.1f}°C\n")


# ------------------------- Orchestration ------------------------------

def main() -> None:
    """
    End-to-end execution:
      1) load & reshape data,
      2) compute seasonal averages, largest ranges, and stability,
      3) persist results to plain-text files,
      4) provide a simple console acknowledgement.
    """
    df = load_data(DATA_FOLDER)
    seasonal_avg = calculate_seasonal_avg(df)
    largest_range = find_largest_temp_range(df)
    most_stable, most_variable = find_temperature_stability(df)

    save_seasonal_avg(seasonal_avg)
    save_largest_temp_range(largest_range)
    save_temperature_stability(most_stable, most_variable)
    print("Analysis complete. Results saved to text files.")


if __name__ == "__main__":
    main()
