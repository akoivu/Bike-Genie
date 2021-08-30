from definitions import *
import pandas as pd
import json

def get_station_data():
    project_directory = get_root_directory()

    stations = pd.read_csv(project_directory + RAW_DATA_FOLDER + STATION_DATA_FILENAME + CSV_SUFFIX)
    
    return stations

def preprocess_station_data_into_suitable_json():
    """To populate database of a Django project the JSON needs to be in a specific format. See Django documentation"""
    station_data = get_station_data()

    # Django requires a field with the model name for populating
    station_data[COLUMN_MODEL_DJANGO] = MODEL_STATION

    # Django wants the fields as their own column
    station_data[COLUMN_FIELDS_DJANGO] = station_data.apply(lambda row : {COLUMN_STATION_NAME_FINNISH_OLD : row[COLUMN_STATION_NAME_FINNISH_OLD],
                                                                          COLUMN_STATION_X : row[COLUMN_STATION_X],
                                                                          COLUMN_STATION_Y : row[COLUMN_STATION_Y],
                                                                          COLUMN_STATION_ADDRESS_FINNISH_OLD : row[COLUMN_STATION_ADDRESS_FINNISH_OLD],
                                                                          COLUMN_STATION_CITY_FINNISH_OLD : row[COLUMN_STATION_CITY_FINNISH_OLD],
                                                                          COLUMN_STATION_CAPACITY :  row[COLUMN_STATION_CAPACITY]}, axis = 1)

    # We use station id as the primary key
    station_data.rename(columns = {COLUMN_STATION_ID_OLD : COLUMN_PRIMARY_KEY_DJANGO}, inplace = True)
    
    # We drop unneeded columns
    dropped = drop_columns_of_unused_station_data(station_data)

    filename = get_processed_station_data_filename()
    result = dropped.to_json(orient = 'records')

    parsed = json.loads(result)
    print(json.dumps(parsed, indent=4))

def drop_columns_of_unused_station_data(df):
    """Drops the columns that we do not need for the station data. NOTE that this shouldn't be used for the traffic data"""
    return df.drop([COLUMN_STATION_FID_OLD, COLUMN_STATION_NAME_FINNISH_OLD, COLUMN_STATION_NAME_SWEDISH_OLD, COLUMN_STATION_NAME_ENGLISH_OLD, COLUMN_STATION_CITY_FINNISH_OLD, COLUMN_STATION_CITY_SWEDISH_OLD, 
        COLUMN_STATION_OPERAATTOR_OLD, COLUMN_STATION_ADDRESS_FINNISH_OLD, COLUMN_STATION_ADDRESS_SWEDISH_OLD,COLUMN_STATION_X, COLUMN_STATION_Y, COLUMN_STATION_CAPACITY], axis = 1)

def get_processed_station_data_filename():
    project_directory = get_root_directory()

    path = PROCESSED_DATA_FOLDER
    filename = STATION_DATA_FILENAME
    return project_directory + path + filename + JSON_SUFFIX

