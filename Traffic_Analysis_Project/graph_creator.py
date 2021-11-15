from mysql.connector import connect, Error
from getpass import getpass
import pandas as pd
import os
import pathlib
from sqlalchemy import create_engine, delete
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
import time
import json

def speed_limit_graph(speed_data):
    print("speed_limit")
    limit_labels = [5,10,15,20,25,30,35,40,45,50,55,60,65]

    fast_data = []
    slow_data = []
    for speed_limit in limit_labels:
        fast_data.append(speed_data[speed_limit]["fast"])
        slow_data.append(speed_data[speed_limit]["slow"])

    ind = np.arange(13)

    plt.figure(figsize=(10, 5))
    width = .25
    ax = plt.gca()
    ax.yaxis.set_major_formatter(ticker.EngFormatter())

    plt.bar(ind, fast_data, width, label='Speeders')
    plt.bar(ind + width, slow_data, width, label="Non-Speeders")

    plt.xlabel("Speed Limits")
    plt.ylabel("Total Number of Vehicles")
    plt.title("Speed Limit speeding comparison 2015-2020")
    plt.legend(loc='best')
    plt.xticks(ind + width / 12, limit_labels)
    title = "SpeedLimitComparison"
    plt.savefig("D:/TrafficData/Traffic_Analysis_Project/Graphs/" + title)
    plt.close()

def long_month_graph(fast_data,slow_data,title,labels,filename,divisor):
    ind = np.arange(12)
    fast_avg = np.true_divide(np.asarray(fast_data),divisor)
    slow_avg = np.true_divide(np.asarray(slow_data), divisor)
    plt.figure(figsize=(10, 5))
    width = .25
    ax = plt.gca()
    ax.yaxis.set_major_formatter(ticker.EngFormatter())
    plt.bar(ind, fast_avg, width, label='Speeders')
    plt.bar(ind + width, slow_avg, width, label="Non-Speeders")

    plt.xlabel("Months")
    plt.ylabel("Total Number of Vehicles")
    plt.title(title)

    plt.xticks(ind + width / 11, labels)
    plt.legend(loc='best')
    plt.savefig("D:/TrafficData/Traffic_Analysis_Project/Graphs/" + filename)
    plt.close()

def daily_speed_graph(daily_data,day_list):
    print("daily")
    day_labels = ["Mon","Tue","Wed","Thur",'Fri',"Sat","Sun"]

    fast_data =[]
    slow_data = []
    for day_key in day_list:
        fast_data.append(daily_data[day_key]["fast"])
        slow_data.append(daily_data[day_key]["slow"])

    ind = np.arange(7)

    plt.figure(figsize=(10, 5))
    width = .25
    ax = plt.gca()
    ax.yaxis.set_major_formatter(ticker.EngFormatter())

    plt.bar(ind, fast_data, width, label='Speeders')
    plt.bar(ind + width, slow_data, width, label="Non-Speeders")

    plt.xlabel("Days")
    plt.ylabel("Total Number of Vehicles")
    plt.title("Speeders vs Non-Speeders over days of the week, 2015-2020")
    plt.legend(loc='best')
    plt.xticks(ind + width / 6, day_labels)
    title = "DailyComparison"
    plt.savefig("D:/TrafficData/Traffic_Analysis_Project/Graphs/" + title)

    plt.close()



def yearly_speed_graph(year_data):
    print("year")
    region_label = ["1","2","3","4","5","6","7","8","9","10","11"]
    for year in range(2015,2021):
        speeders=[]
        nonspeeders=[]
        for region in range(1,12):
            speeders.append(year_data[year][region]["speed"])
            nonspeeders.append(year_data[year][region]["slow"])

        ind = np.arange(11)

        plt.figure(figsize=(10, 5))
        width = .25
        ax = plt.gca()
        ax.yaxis.set_major_formatter(ticker.EngFormatter())

        plt.bar(ind, speeders, width, label='Speeders')
        plt.bar(ind + width, nonspeeders, width, label="Non-Speeders")

        plt.xlabel("Regions")
        plt.ylabel("Total Number of Vehicles")
        plt.title("Yearly Comparison of Speeding Cars: " + str(year))
        plt.legend(loc='best')
        plt.xticks(ind + width / 10, region_label)
        title = "Speeding_Year_"+str(year)+".png"
        plt.savefig("D:/TrafficData/Traffic_Analysis_Project/Graphs/" + title)

        plt.close()


def make_monthly_graph(slow_data,fast_data, labels,region,year):
    ind = np.arange(12)

    plt.figure(figsize=(10, 5))
    width = .25
    ax = plt.gca()
    ax.yaxis.set_major_formatter(ticker.EngFormatter())

    plt.bar(ind, fast_data, width, label='Speeders')
    plt.bar(ind + width, slow_data, width, label="Non-Speeders")

    plt.xlabel("Months")
    plt.ylabel("Total Number of Vehicles")
    plt.title("Monthly Comparison of Speeders Year: " + str(year) + " Region: " + str(region))
    plt.legend(loc='best')
    plt.xticks(ind + width / 11, labels)
    title = str(year) + "_" + str(region) + "_MthYear.png"
    plt.savefig("D:/TrafficData/Traffic_Analysis_Project/Graphs/" + title)

    plt.close()

def speed_mth_year_graph(SvN_data):
    # Data on x axis
    months_labels = ['Jan','Feb','Mar','Apr','May',"Jun","Jul","Aug","Sept","Oct","Nov","Dec"]
    total_speeding = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    total_slow = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    final_speeding = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    final_slow = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    for year in  range(2015,2021):
        for region in range(1,12):
            monthly_data_speeding = []
            monthly_data_slow = []
            for month in range(1,13):
                key=str(year)+"_"+str(month)
                monthly_data_speeding.append(SvN_data[key][region]["speed"])
                monthly_data_slow.append(SvN_data[key][region]["slow"])
                total_speeding[month-1] += SvN_data[key][region]["speed"]
                total_slow[month - 1] += SvN_data[key][region]["slow"]

                if year == 2020:
                    final_speeding[month-1]+=SvN_data[key][region]["speed"]
                    final_slow[month - 1] += SvN_data[key][region]["slow" ]

            make_monthly_graph(monthly_data_slow,monthly_data_speeding, months_labels,region,year)
            print("Region: "+str(region)+" and Year: "+str(year) + " graph generated")

            if year == 2019 and region == 11:
                print("Producing average month for 2015-2019")
                long_month_graph(total_speeding,total_slow,"2015-2019 Avg Monthly Comparison",
                                 months_labels,"2015_2019_month_avg.png",5)
            if year == 2020 and region == 11:
                print("Producing average Month for 2015-2020")
                long_month_graph(total_speeding,total_slow,"2015-2020 Avg Monthly Comparison",
                                 months_labels,"2015_2020_month_avg.png",6)
                print("Making 2020 monthly graph")
                long_month_graph(final_speeding, final_slow, "2020 Monthly Speeding Data", months_labels,
                                 "2020_monthly_speeding.png",1)





def speed_comparision(speeding,not_speeding,df,speed_chart,bins):
    region_dict ={}
    for region_nbr in range(1,12):
        region_df = df.loc[df["REGION"]==region_nbr]
        for speed_limit in range(5,70,5):
            limited_df = region_df.loc[region_df["SPEED_LIMIT"]==speed_limit]
            for bin in bins:
                if bin in speed_chart[speed_limit]:
                    not_speeding += limited_df[bin].sum()
                else:
                    speeding += limited_df[bin].sum()
        region_dict[region_nbr]={
            'speed':int(speeding),
            "slow":int(not_speeding),
            "region":int(region_nbr)
        }
    return region_dict



def main():
    years= [2015,2016,2017,2018,2019,2020]
    bin= ["BIN_1","BIN_2","BIN_3","BIN_4","BIN_5","BIN_6","BIN_7","BIN_8","BIN_9","BIN_10","BIN_11","BIN_12","BIN_13",
           "BIN_14","BIN_15"]
    speed_conversion={
        5:"BIN_1",10:"BIN_1 BIN_2",15:"BIN_1 BIN_2",20:"BIN_1 BIN_2",25:"BIN_1 BIN_2 BIN_3", 30:"BIN_1 BIN_2 BIN_3 BIN_4",35:"BIN_1 BIN_2 BIN_3 BIN_4 BIN_5",
        40: "BIN_1 BIN_2 BIN_3 BIN_4 BIN_5 BIN_6", 45:"BIN_1 BIN_2 BIN_3 BIN_4 BIN_5 BIN_6 BIN_7",50:"BIN_1 BIN_2 BIN_3 BIN_4 BIN_5 "
                                                "BIN_6 BIN_7 BIN_8",55:"BIN_1 BIN_2 BIN_3 BIN_4 BIN_5 BIN_6 BIN_7 BIN_8 BIN_9",
        60: "BIN_1 BIN_2 BIN_3 BIN_4 BIN_5 BIN_6 BIN_7 BIN_8 BIN_9 BIN_10",65:"BIN_1 BIN_2 BIN_3 BIN_4 BIN_5 BIN_6 BIN_7 BIN_8 BIN_9 BIN_10 BIN_11"
    }
    days = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]

    db_connection = create_engine('mysql://User:Password@localhost:3306/traffic_data')
    connection = db_connection.connect()

    # This will be the section for generating graphs for sc_speed
    yearly_speed = {}
    month_speed = {}
    daily_speed = {"Monday":{"fast":0,"slow":0},"Tuesday":{"fast":0,"slow":0},"Wednesday":{"fast":0,"slow":0},
                   "Thursday":{"fast":0,"slow":0},"Friday":{"fast":0,"slow":0},"Saturday":{"fast":0,"slow":0},
                   "Sunday":{"fast":0,"slow":0}}
    speed_data = {5: {"fast": 0, "slow": 0}, 10: {"fast": 0, "slow": 0}, 15: {"fast": 0, "slow": 0},
                   20: {"fast": 0, "slow": 0}, 25: {"fast": 0, "slow": 0}, 30: {"fast": 0, "slow": 0},
                   35: {"fast": 0, "slow": 0},40: {"fast": 0, "slow": 0}, 45: {"fast": 0, "slow": 0},
                   50: {"fast": 0, "slow": 0}, 55: {"fast": 0, "slow": 0}, 60: {"fast": 0, "slow": 0},
                   65: {"fast": 0, "slow": 0}}
    start = time.time()
    # is reading all the data at once slower or faster

    for year in years:
        print("Loading year: "+str(year))
        df = pd.read_sql("SELECT * from sc_speed where YEAR="+str(year), con=db_connection)
        year_entry = speed_comparision(0,0,df,speed_conversion,bin)
        # gather speeding records for each year
        yearly_speed[year] = year_entry
        # Gather speeding records for each month in a year
        for month in range(1,13):
            print("parsing month: "+str(month))
            month_df = df.loc[df["MONTH"]==month]
            month_entry = speed_comparision(0,0,month_df,speed_conversion,bin)
            key = str(year)+"_"+str(month)
            month_speed[key] = month_entry

        # Gather speeding records for each day
        for day in days:
            print("Parsing Day: " + day)
            daily_df = df.loc[df["DAY_OF_WEEK"] == day]
            daily_entry = speed_comparision(0,0,daily_df,speed_conversion,bin)
            for region in range(1,12):
                daily_speed[day]["fast"]+= int(daily_entry[region]["speed"])
                daily_speed[day]["slow"]+= int(daily_entry[region]["slow"])

        # Gather data for each speed limit
        for key in speed_data:
            print("Parsing Speed limit: " + str(key))
            limit_df = df.loc[df["SPEED_LIMIT"] == key]
            limit_entry = speed_comparision(0,0,limit_df,speed_conversion,bin)
            for region in range(1,12):
                speed_data[key]["fast"] += int(limit_entry[region]["speed"])
                speed_data[key]["slow"] += int(limit_entry[region]["slow"])


    # This is a set of dictionaries that has speeding and not speeding for each month. [Speeding, not_speeding]
    end = time.time()
    print(end - start)

    #speed_mth_year_graph(month_speed)
    #yearly_speed_graph(yearly_speed)
    #daily_speed_graph(daily_speed,days)
    #speed_limit_graph(speed_data)

    with open("records_file.txt","a") as f:
        f.write("Speed Limit Data\n")
        f.write(json.dumps(speed_data,indent=2))
        f.write("Monthly Speed Data\n")
        f.write(json.dumps(month_speed,indent=2))
        f.write("Yearly Speed Data\n")
        f.write(json.dumps(yearly_speed,indent=2))
        f.write("Daily Speed Data\n")
        f.write(json.dumps(daily_speed,indent=2))


if __name__ == "__main__":
    main()