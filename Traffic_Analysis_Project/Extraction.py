# @Author: Brian Finnerty
# @CreationDate: 10/25/2021
# Details: This program will do the following: extract all zip files from the extraction directory, place files
# into data_dirs, sorted by year, move zips to the already_extracted dir and append to the running tally file.
import argparse
import zipfile
import os

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("--tally_file", default="D:/TrafficData/GeneralData/Unzip_Tracker.txt")
    parser.add_argument("--target_dir", default="D:/TrafficData/TrafficDataCollection")
    parser.add_argument("--extraction_dir",default="D:/TrafficData/Traffic_Extraction")
    return parser.parse_args()

def gather_names(tally_file,extraction_dir):
    file_list = os.listdir(extraction_dir)
    with open(tally_file,"r") as read_f:
        for file_name in file_list:
            file_path = os.path.join(extraction_dir,file_name)
            if file_path in read_f.read():
                file_list.remove(file_name)
                os.remove(file_path)
    return file_list

def unzip(ziplist,extract_dir,tally_file,target_dir):
    for file_name in ziplist:
        extraction_path = os.path.join(extract_dir,file_name)
        final_dir = ""
        if "CC_Volume" in file_name:
            final_dir = "CC_Volume"
        elif "CC_Class" in file_name:
            final_dir = "CC_Class"
        elif "sc_speed" in file_name:
            final_dir = "SC_Speed"
        else:
            final_dir = "extras"

        with zipfile.ZipFile(extraction_path, "r") as zip:
            zip.extractall(path=os.path.join(target_dir,final_dir))
        with open(tally_file, "a") as f:
            f.write(extraction_path+"\n")
        os.remove(extraction_path)

def main():
    args = parse_arguments()
    if not os.path.exists(args.tally_file):
        with open(args.tally_file, "w"):
            pass
    file_list = gather_names(args.tally_file,args.extraction_dir)
    unzip(file_list, args.extraction_dir, args.tally_file,args.target_dir)



if __name__=="__main__":
    main()