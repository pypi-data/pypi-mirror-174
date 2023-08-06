#This function takes a data frame, column name from within that data frame, and a specific value that the column may contain. The function is meant to go through the column in the data frame and return a sum that reflects
#the total number of visits to an individual brewery

import pandas as pd
import numpy as np

def load_data():
    df = pd.read_csv(data_text)

    return df

def count_ripper(data_frame, column_name, brewery_name):

    individual_brewery = data_frame.loc[(data_frame[column_name] == brewery_name)]

    individual_brewery_na_dropped = individual_brewery.raw_visit_counts.dropna()

    individual_brewery_visits = list(individual_brewery_na_dropped)

    return sum(individual_brewery_visits)


def date_volume_check(data_frame, column_name, brewery_name, date_column_name):
    date_volume_df = data_frame.loc[data_frame[column_name] == brewery_name]

    date_volume_df = date_volume_df[[date_column_name]]

    date_volume_df.reset_index(inplace=True, drop=True)

    date_volume_df.columns = ['Date']

    date_volume_df['Date'] = pd.to_datetime(date_volume_df['Date'])

    date_volume_list = date_volume_df['Date'].unique()

    date_volume_list = list(date_volume_df['Date'])

    counter = 0

    for date in date_volume_list:
        counter += 1

    return counter

def brewery_with_dates(df, column_name_1, column_name_2, column_name_3, brewery_name):
  single_brewery_from_frame = df.loc[df[column_name_3] == brewery_name]

  single_brewery_from_frame_reduced = single_brewery_from_frame[[column_name_1, column_name_2, column_name_3]]

  single_brewery_from_frame_reduced.reset_index(inplace=True, drop = True)

  single_brewery_from_frame_reduced.columns = ['Date', 'Attendance', 'Brewery']

  single_brewery_from_frame_reduced['Date'] = pd.to_datetime(single_brewery_from_frame_reduced['Date'])

  return single_brewery_from_frame_reduced

def quick_consolidate(df):
    breweries_only = df.dropna(subset=['location_name'])

    breweries_only = breweries_only[(breweries_only.location_name != 'Artisanal Brewing Ventures') & (breweries_only.location_name != 'Optimist Hall') &
                                (breweries_only.location_name != 'Red Clay Cider Works') & (breweries_only.location_name != 'Adams Beverages of North Carolina') &
                                (breweries_only.location_name != 'Kind Beer Distributing')& (breweries_only.location_name != 'GoodRoad CiderWorks') &
                                (breweries_only.location_name != 'Deutsche Beverage Technology') & (breweries_only.location_name != 'Seven Jars Products') &
                                (breweries_only.location_name != "OMB Captain Jack's Tavern") & (breweries_only.location_name != 'The Chamber By Wooden Robot') &
                                (breweries_only.location_name != 'The Chamber Wooden Robot')]
    return breweries_only
