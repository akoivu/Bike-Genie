import pandas as pd
from datetime import datetime

def preprocess_month(month):
    data = get_traffic_data(month)

    processed_data = (
        data.pipe(time_columns_to_datetime)
            .pipe(remove_excess_columns)
            .pipe(calculate_number_of_moving_bikes_per_station)
            .pipe(fill_all_time_slots_for_stations, )
        )
    # Save the processed data for use
    filename = get_filename(month)
    processed_data.to_parquet("/data/processed/" + filename + "-processed.parquet")

def time_columns_to_datetime(df):
    # Make time a datetime object to ease handling. Also floor to starting hour
    df["Dep date"] = pd.to_datetime(df["Departure"], errors = "ignore").dt.floor(freq = "H")
    df["Return date"] = pd.to_datetime(df["Return"], errors = "ignore").dt.floor(freq = "H")
    return df

def get_traffic_data(month):
    filename = get_filename(month)
    return pd.read_csv(filename, sep = ",")

def get_filename(month):
    path = "/data/raw/"
    extension = ".csv"
    filename = "2019-" + '{:02.0f}'.format(month)
    return path + filename + extension

def remove_excess_columns(df):
    return df.drop(columns=["Covered distance (m)", "Duration (sec.)", "Departure", "Return"])

def calculate_number_of_moving_bikes_per_station(df):
    # Get the outgoing bikes per station at timeframe
    outgoing = df.groupby("Departure station id")["Dep date"].value_counts()
    outgoing = outgoing.sort_index()
    outgoing = outgoing.rename_axis(index = {"Dep date" : "Date", "Departure station id" : "ID"})
    outgoing = outgoing.rename("Outgoing")

    # Get the arriving bikes per station at timeframe
    arriving = df.groupby("Return station id")["Return date"].value_counts()
    arriving = arriving.sort_index()
    arriving = arriving.rename_axis(index = {"Return date" : "Date", "Return station id" : "ID"})
    arriving = arriving.rename("Arriving")

    outgoing_arriving_merge = pd.merge(outgoing, arriving, on = ["ID", "Date"], how = "outer")
    outgoing_arriving_merge = outgoing_arriving_merge.fillna(0)
    
    return outgoing_arriving_merge

def fill_all_time_slots_for_stations(df, month):
    # Gets all unique stations
    stations = set(df.index.get_level_values(0))

    # Get first and last date of the month
    first_day_of_month = "2019-" + '{:02.0f}'.format(month) + "-01 00:00:00"
    last_day_of_month = pd.Timestamp("2019-" + '{:02.0f}'.format(month) + "-01 23:00:00") + MonthEnd(0)

    # Get hourly indexes for all days of the month
    all_dates = pd.date_range(first_day_of_month, last_day_of_month, freq = "H")
    idx = pd.MultiIndex.from_product([stations, all_dates], names = ["ID", "Date"])

    # Make a dataframe with all hourly data for every station
    mega_frame_with_station_date_cartesian_product = pd.DataFrame(index = idx)

    # Merge the hourly arriving/departuring numbers and fill the hours where there is no traffic
    merged = pd.merge(mega_frame_with_station_date_cartesian_product, df, on = ["ID", "Date"], how = "left")
    merged_and_filled = merged.fillna(0)
    merged_and_filled = merged_and_filled.reset_index()

    return merged_and_filled

def add_station_data():
    station_data = get_station_data()
    return pd.merge(processed, station_data, on = "ID", how = "inner")

def get_station_data():
  stations = pd.read_csv("/data/raw/Helsingin_ja_Espoon_kaupunkipyöräasemat.csv")
  stations = stations.drop(["FID", "Nimi", "Namn", "Adress", "Kaupunki", "Stad", "Operaattor"], axis = 1)
  return stations
