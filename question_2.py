#question_2_Solution
import pandas as pd
import glob
import os

DATA_FOLDER = "temperatures"

SEASON_MONTHS = {
    "Summer": ["December", "January", "February"],
    "Autumn": ["March", "April", "May"],
    "Winter": ["June", "July", "August"],
    "Spring": ["September", "October", "November"]
}

def load_data(folder):
    all_files = glob.glob(os.path.join(folder, "*.csv"))
    df_list = []

    for file in all_files:
        df = pd.read_csv(file)
        df_long = df.melt(
            id_vars=["STATION_NAME"],
            value_vars=["January","February","March","April","May","June",
                        "July","August","September","October","November","December"],
            var_name="Month",
            value_name="Temperature"
        )
        df_list.append(df_long)

    combined_df = pd.concat(df_list, ignore_index=True)
    combined_df = combined_df.dropna(subset=["Temperature"])
    return combined_df

def calculate_seasonal_avg(df):
    results = {}
    for season, months in SEASON_MONTHS.items():
        avg_temp = df[df["Month"].isin(months)]["Temperature"].mean()
        results[season] = round(avg_temp, 1)
    return results

def find_largest_temp_range(df):
    ranges = []
    max_range = 0
    for station, temps in df.groupby("STATION_NAME")["Temperature"]:
        t_max = temps.max()
        t_min = temps.min()
        r = t_max - t_min
        if r > max_range:
            max_range = r
            ranges = [(station, r, t_max, t_min)]
        elif r == max_range:
            ranges.append((station, r, t_max, t_min))
    return ranges

def find_temperature_stability(df):
    std_list = [(station, temps.std()) for station, temps in df.groupby("STATION_NAME")["Temperature"]]
    min_std = min(std_list, key=lambda x: x[1])[1]
    max_std = max(std_list, key=lambda x: x[1])[1]
    most_stable = [(s, sd) for s, sd in std_list if sd == min_std]
    most_variable = [(s, sd) for s, sd in std_list if sd == max_std]
    return most_stable, most_variable

def save_seasonal_avg(results):
    with open("average_temp.txt", "w") as f:
        for season, temp in results.items():
            f.write(f"{season}: {temp}°C\n")

def save_largest_temp_range(results):
    with open("largest_temp_range_station.txt", "w") as f:
        for station, r, t_max, t_min in results:
            f.write(f"Station {station}: Range {r:.1f}°C (Max: {t_max:.1f}°C, Min: {t_min:.1f}°C)\n")

def save_temperature_stability(most_stable, most_variable):
    with open("temperature_stability_stations.txt", "w") as f:
        for station, sd in most_stable:
            f.write(f"Most Stable: Station {station}: StdDev {sd:.1f}°C\n")
        for station, sd in most_variable:
            f.write(f"Most Variable: Station {station}: StdDev {sd:.1f}°C\n")

def main():
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
