from mysql.connector import connect, Error
from getpass import getpass
import pandas as pd
import os
import pathlib
from sqlalchemy import create_engine, delete

def main():
    print("Cleaning Data")
    tables = ['sc_speed']
    db_connection = create_engine('mysql://User:Password@localhost:3306/traffic_data')
    connection = db_connection.connect()

    for table in tables:

        df = pd.read_sql("SHOW COLUMNS from "+table, con=db_connection)
        columns_names = df["Field"]
        print("removing all rows with null values")
        for column in columns_names:
            print("Removed: " + column)
            output = db_connection.execute("DELETE from "+table+" where "+column +" IS NULL")



if __name__ == "__main__":
    main()