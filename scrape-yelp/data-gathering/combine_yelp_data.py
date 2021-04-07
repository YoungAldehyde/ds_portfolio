import argparse
import sys
import glob
import os
import pandas as pd
from datetime import datetime

class CombineYelpCsv:
    def __init__(self, path):
        self.path = path

    def concat_df(self):
        all_files = glob.glob(self.path + "/*.csv")
        yelp_data_city_csv_list = os.listdir(self.path)

        city_names = []
        for i in range(len(yelp_data_city_csv_list)):
            city_name = yelp_data_city_csv_list[i].split('_')[0]
            city_names.append(city_name)

        li = []

        for filename, city_name in zip(all_files, city_names):
            df = pd.read_csv(filename, index_col=None, header=0)
            df['city'] = city_name
            li.append(df)

        frame = pd.concat(li, axis=0, ignore_index=True)

        frame_cleaned = frame.dropna(subset=['zip_code','longitude','latitude'])

        today = datetime.today().strftime('%Y-%m-%d')
        frame_cleaned.to_csv(f'yelp_data_us_top20_cities_updated_{today}.csv',index=False)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="sample command: python combine_yelp_data.py ./yelp_data_by_city/")
    parser.add_argument("filepath", help="path of the input csv file for each city",
                        default = './yelp_data_by_city/',
                        type = str)

    args = parser.parse_args()

    CombineYelpCsv(args.filepath).concat_df()

else:
    sys.exit("Incorrect command")