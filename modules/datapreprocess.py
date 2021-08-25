from definitions import *
import pandas as pd
from datetime import datetime
from pandas.tseries.offsets import MonthEnd


def preprocess_month(month):
    data = get_traffic_data(month)

    processed_data = (
        data.pipe(time_columns_to_datetime)
            .pipe(remove_excess_columns)
            .pipe(calculate_number_of_moving_bikes_per_station)
            .pipe(fill_all_time_slots_for_stations, month)
            .pipe(add_station_data)
            .pipe(save_processed_traffic_data, month)
        )
    

def time_columns_to_datetime(df):
    # Make time a datetime object to ease handling. Also floor to starting hour
    df[COLUMN_DEPARTURE_DATETIME] = pd.to_datetime(df[COLUMN_DEPARTURE_TIME_OLD], 
        errors = "ignore").dt.floor(freq = "H")
    df[COLUMN_RETURN_DATETIME] = pd.to_datetime(df[COLUMN_RETURN_TIME_OLD], 
        errors = "ignore").dt.floor(freq = "H")
    return df

def save_processed_traffic_data(df, month):
    filename = get_processed_traffic_data_filename_without_extension(month)

    # Right now we also save the csv for testing purposes
    df.to_parquet(filename + PARQUET_SUFFIX)
    df.to_csv(filename + CSV_SUFFIX)

def get_processed_traffic_data_filename_without_extension(month):
    project_directory = get_root_directory()

    # We omit the file extension so we can save both .csv and .parquet
    path = PROCESSED_DATA_FOLDER
    filename = YEAR_PREFIX + '{:02.0f}'.format(month)
    return project_directory + path + filename 

def get_traffic_data(month):
    filename = get_raw_traffic_data_filename(month)
    return pd.read_csv(filename, sep = ",")

def get_raw_traffic_data_filename(month):
    project_directory = get_root_directory()

    path = RAW_DATA_FOLDER
    extension = CSV_SUFFIX
    filename = YEAR_PREFIX + '{:02.0f}'.format(month)
    return project_directory + path + filename + extension

def remove_excess_columns(df):
    return df.drop(columns=
        [COLUMN_COVERED_DISTANCE_OLD, COLUMN_DURATION_OLD, 
            COLUMN_DEPARTURE_TIME_OLD, COLUMN_RETURN_TIME_OLD])

def calculate_number_of_moving_bikes_per_station(df):
    # Get the outgoing bikes per station at timeframe
    outgoing = df.groupby(COLUMN_DEPARTURE_STATION_ID_OLD)[COLUMN_DEPARTURE_DATETIME].value_counts()
    outgoing = outgoing.sort_index()

    # Rename columns to help with merging
    outgoing = outgoing.rename_axis(index = {COLUMN_DEPARTURE_DATETIME : COLUMN_EVENT_DATETIME, 
        COLUMN_DEPARTURE_STATION_ID_OLD : COLUMN_STATION_ID})
    outgoing = outgoing.rename(COLUMN_NUMBER_OF_DEPARTING)

    # Get the arriving bikes per station at timeframe
    arriving = df.groupby(COLUMN_RETURN_STATION_ID_OLD)[COLUMN_RETURN_DATETIME].value_counts()
    arriving = arriving.sort_index()

    # Rename columns to help with merging
    arriving = arriving.rename_axis(index = {COLUMN_RETURN_DATETIME : COLUMN_EVENT_DATETIME, 
        COLUMN_RETURN_STATION_ID_OLD : COLUMN_STATION_ID})
    arriving = arriving.rename(COLUMN_NUMBER_OF_ARRIVING)

    outgoing_arriving_merge = pd.merge(outgoing, arriving, on = [COLUMN_STATION_ID, COLUMN_EVENT_DATETIME], how = "outer")
    outgoing_arriving_merge = outgoing_arriving_merge.fillna(0)
    
    return outgoing_arriving_merge

def fill_all_time_slots_for_stations(df, month):
    # Gets all unique stations
    stations = set(df.index.get_level_values(0))

    # Get first and last date of the month
    first_day_of_month = YEAR_2019 + '{:02.0f}'.format(month) + FIRST_DAY_MIDNIGHT

    # MonthEnd(0) moves a date to the last day of the month. That is why we start with the first day of the month.
    last_day_of_month = pd.Timestamp(YEAR_2019 + '{:02.0f}'.format(month) + FIRST_DAY_LAST_HOUR) + MonthEnd(0)

    # Get hourly indexes for all days of the month
    all_dates = pd.date_range(first_day_of_month, last_day_of_month, freq = "H")
    idx = pd.MultiIndex.from_product([stations, all_dates], 
        names = [COLUMN_STATION_ID, COLUMN_EVENT_DATETIME])

    # Make a dataframe with all hourly data for every station
    mega_frame_with_station_date_cartesian_product = pd.DataFrame(index = idx)

    # Merge the hourly arriving/departuring numbers and fill the hours where there is no traffic
    merged = pd.merge(mega_frame_with_station_date_cartesian_product, df, 
        on = [COLUMN_STATION_ID, COLUMN_EVENT_DATETIME], how = "left")
    merged_and_filled = merged.fillna(0)
    merged_and_filled = merged_and_filled.reset_index()

    return merged_and_filled

def add_station_data(df):
    station_data = get_station_data()
    return pd.merge(df, station_data, left_on = COLUMN_STATION_ID, 
        right_on = COLUMN_STATION_ID_OLD, how = "inner")

def get_station_data():
    project_directory = get_root_directory()

    stations = pd.read_csv(project_directory + RAW_DATA_FOLDER + STATION_DATA_FILENAME + CSV_SUFFIX)
    stations = stations.drop([COLUMN_STATION_FID_OLD, COLUMN_STATION_NAME_FINNISH_OLD, COLUMN_STATION_NAME_SWEDISH_OLD, 
        COLUMN_STATION_ADRESS_OLD, COLUMN_STATION_CITY_FINNISH_OLD, COLUMN_STATION_CITY_SWEDISH_OLD, 
        COLUMN_STATION_OPERAATTOR_OLD], axis = 1)
    return stations


