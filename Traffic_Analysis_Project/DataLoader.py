from mysql.connector import connect, Error
from getpass import getpass
import pandas as pd
import os
import pathlib
from sqlalchemy import create_engine


def main():
    dataDict = [
        {
            "path":"D:/TrafficData/TrafficDataCollection/SC_Speed",
            "table":"SC_SPEED"
        },
        {
            "path":"D:/TrafficData/TrafficDataCollection/CC_Volume",
            "table":"CC_VOLUME"
        },
        {
            "path":"D:/TrafficData/TrafficDataCollection/CC_Class",
            "table":"CC_CLASS"
        }
    ]

    classTableQuery = """
    CREATE TABLE CC_CLASS(
    id INT AUTO_INCREMENT PRIMARY KEY,
    RC_STATION VARCHAR(20),
    REGION INT,
    REGION_CODE INT,
    COUNTY_CODE INT,
    STATION INT,
    RCSTA INT,
    FUNCTIONAL_CLASS INT,
    FACTOR_GROUP INT,
    YEAR INT,
    MONTH INT,
    DAY INT,
    DAY_OF_WEEK VARCHAR(25),
    FEDERAL_DIRECTION INT,
    LANE_CODE INT,
    LANES_IN_DIRECTION INT,
    DATA_INTERVAL INT,
    CLASS_F1 INT,
    CLASS_F2 INT,
    CLASS_F3 INT,
    CLASS_F4 INT,
    CLASS_F5 INT,
    CLASS_F6 INT,
    CLASS_F7 INT,
    CLASS_F8 INT,
    CLASS_F9 INT,
    CLASS_F10 INT,
    CLASS_F11 INT,
    CLASS_F12 INT,
    CLASS_F13 INT,
    TOTAL INT
    )
    """

    volumeQuery="""
    CREATE TABLE CC_VOLUME(
    id INT AUTO_INCREMENT PRIMARY KEY,
    RC_STATION VARCHAR(20),
    REGION INT,
    REGION_CODE INT,
    COUNTY_CODE INT,
    STATION INT,
    RCSTA INT,
    FUNCTIONAL_CLASS INT,
    FACTOR_GROUP INT,
    YEAR INT,
    MONTH INT,
    DAY INT,
    DAY_OF_WEEK VARCHAR(25),
    FEDERAL_DIRECTION INT,
    LANES_IN_DIRECTION INT,
    INTERVAL_01 INT,
    INTERVAL_02 INT,
    INTERVAL_03 INT,
    INTERVAL_04 INT,
    INTERVAL_05 INT,
    INTERVAL_06 INT,
    INTERVAL_07 INT,
    INTERVAL_08 INT,
    INTERVAL_09 INT,
    INTERVAL_10 INT,
    INTERVAL_11 INT,
    INTERVAL_12 INT,
    INTERVAL_13 INT,
    INTERVAL_14 INT,
    INTERVAL_15 INT,
    INTERVAL_16 INT,
    INTERVAL_17 INT,
    INTERVAL_18 INT,
    INTERVAL_19 INT,
    INTERVAL_20 INT,
    INTERVAL_21 INT,
    INTERVAL_22 INT,
    INTERVAL_23 INT,
    INTERVAL_24 INT
    )
    """
    speedQuery = """
        CREATE TABLE SC_SPEED(
        id INT AUTO_INCREMENT PRIMARY KEY,
        RC_STATION VARCHAR(20),
        COUNT_ID VARCHAR(25),
        REGION INT,
        REGION_CODE INT,
        COUNTY_CODE INT,
        STATION INT,
        RCSTA INT,
        FUNCTIONAL_CLASS INT,
        FACTOR_GROUP INT,
        SPECIFIC_RECORDER_PLACEMENT VARCHAR(100),
        CHANNEL_NOTES VARCHAR(100),
        DATA_TYPE VARCHAR(100),
        SPEED_LIMIT INT,
        YEAR INT,
        MONTH INT,
        DAY INT,
        DAY_OF_WEEK VARCHAR(25),
        FEDERAL_DIRECTION INT,
        LANE_CODE INT,
        LANES_IN_DIRECTION INT,
        COLLECTION_INTERVAL INT,
        DATA_INTERVAL DECIMAL(4,2),
        BIN_1 INT,
        BIN_2 INT,
        BIN_3 INT,
        BIN_4 INT,
        BIN_5 INT,
        BIN_6 INT,
        BIN_7 INT,
        BIN_8 INT,
        BIN_9 INT,
        BIN_10 INT,
        BIN_11 INT,
        BIN_12 INT,
        BIN_13 INT,
        BIN_14 INT,
        BIN_15 INT,
        TOTAL INT,
        BATCH_ID INT
        )
        """
    try:
        with connect(
            host="localhost",
            user="User",
            password="Password",
            autocommit=True
        ) as connection:
            with connection.cursor() as cursor:
                print("creating database")
                #cursor.execute("CREATE DATABASE traffic_data")
                cursor.execute("USE traffic_data")
                #print("creating class table")
                #cursor.execute(classTableQuery)
                #print("creating volume table")
                #cursor.execute(volumeQuery)
                print("creating speed table")
                #cursor.execute(speedQuery)
        # Replace user and password with values. TODO: create input so these values will not be hard coded
        engine = create_engine('mysql://User:Password@localhost/traffic_data',encoding='utf-8')
        for item in dataDict:
            dataDir = pathlib.Path(item["path"])
            for file in dataDir.iterdir():
                print("Loading "+ str(file))
                dataFrame = pd.read_csv(file, skipinitialspace=True, encoding='utf-8')
                cols = dataFrame.select_dtypes(['object']).columns
                dataFrame[cols] = dataFrame[cols].apply(lambda x: x.str.strip())
                dataFrame.columns = dataFrame.columns.str.replace(' ', '')
                dropped= dataFrame.drop(columns=["LATITUDE","LONGITUDE","UNCLASSIFIED","FLAG_FIELD"])
                dropped.to_sql(item["table"], con=engine, if_exists='append', index=False)

    except Error as e:
        print(e)

if __name__ == "__main__":
    main()