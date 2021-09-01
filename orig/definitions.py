# All general definitions

from pathlib import Path

# Path constants

RAW_DATA_FOLDER = "/data/raw/"
PROCESSED_DATA_FOLDER = "/data/processed/"
STATION_DATA_FILENAME = "Helsingin_ja_Espoon_kaupunkipyöräasemat"


# File prefixes and suffixes

PROCESSED_DATA_SUFFIX = "-processed"
YEAR_PREFIX = "2019-"

# File type

JSON_SUFFIX = ".json"
CSV_SUFFIX = ".csv"
PARQUET_SUFFIX = ".parquet"

# Original Dataset column names

COLUMN_DEPARTURE_TIME_OLD = "Departure"
COLUMN_RETURN_TIME_OLD = "Return"
COLUMN_COVERED_DISTANCE_OLD = "Covered distance (m)"
COLUMN_DURATION_OLD = "Duration (sec.)"
COLUMN_DEPARTURE_STATION_ID_OLD = "Departure station id" 
COLUMN_RETURN_STATION_ID_OLD = "Return station id"

COLUMN_STATION_ID_OLD = "ID"
COLUMN_STATION_FID_OLD = "FID"
COLUMN_STATION_NAME_FINNISH_OLD = "Nimi"
COLUMN_STATION_NAME_SWEDISH_OLD = "Namn"
COLUMN_STATION_NAME_ENGLISH_OLD = "Name"
COLUMN_STATION_ADDRESS_FINNISH_OLD = "Osoite"
COLUMN_STATION_ADDRESS_SWEDISH_OLD = "Adress"
COLUMN_STATION_CITY_FINNISH_OLD = "Kaupunki"
COLUMN_STATION_CITY_SWEDISH_OLD = "Stad"
COLUMN_STATION_OPERAATTOR_OLD = "Operaattor"
COLUMN_STATION_CAPACITY = "Kapasiteet"
COLUMN_STATION_X = 'x'
COLUMN_STATION_Y = 'y'

# New Dataset column names

COLUMN_DEPARTURE_DATETIME = "Dep date"
COLUMN_RETURN_DATETIME = "Return date"
COLUMN_EVENT_DATETIME = "Date"
COLUMN_STATION_ID = "Station ID"
COLUMN_NUMBER_OF_ARRIVING = "Arriving"
COLUMN_NUMBER_OF_DEPARTING = "Outgoing"

# Django-friendly column names

COLUMN_PRIMARY_KEY_DJANGO = 'pk'
COLUMN_MODEL_DJANGO = 'model'
COLUMN_FIELDS_DJANGO = 'fields'

COLUMN_NAME_DJANGO = 'name'
COLUMN_CITY_DJANGO = 'city'
COLUMN_ADDRESS_DJANGO = 'address'
COLUMN_CAPACITY_DJANGO = 'capacity'
COLUMN_POINT_DJANGO = 'point'

# Model names

MODEL_STATION = 'web.station'

# Useful time strings

YEAR_2019 = "2019-"
FIRST_DAY_MIDNIGHT = "-01 00:00:00"
FIRST_DAY_LAST_HOUR = "-01 23:00:00"

# Functions

def get_root_directory() -> Path:
    return str(Path(__file__).parent.parent)