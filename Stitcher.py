# Combines price info with miscellaneous info from mtgjson


from os import listdir, remove
import os
import pandas as pd
import numpy as np
from tqdm import tqdm  # all this does is add a progress bar
from Scraper import local_url_maker, dir_path, count_number_of_lines, file_generator


# get file names
price_dir = os.path.join(dir_path, "Price_Info")
csv_output = os.path.join(dir_path, "final.csv")

csv_path = os.path.join(dir_path, "filtered_cards.csv")
cards = pd.read_csv(csv_path)
i = 0

# progress bar
number_of_cards = count_number_of_lines(csv_path)
progress = tqdm(desc=f"Checking files", total=number_of_cards)

for index, row in tqdm(cards.iterrows()):
    price_info_filepath = local_url_maker(row.loc['setName'], row.loc['name'])
    if os.path.exists(price_info_filepath):
        i += 1
    progress.update(1)

number_of_files = i
print("Number of files that can be parsed: ", i)


list_of_files = []
list_of_card_names = []
list_of_card_set_names = []

for index, row in cards.iterrows():
    price_info_filepath = local_url_maker(row.loc['setName'], row.loc['name'])
    if os.path.exists(price_info_filepath):
        i += 1
        list_of_files.append(price_info_filepath)
        list_of_card_names.append(row.loc['name'])
        list_of_card_set_names.append(row.loc['setName'])
    progress.update(1)


array_dates    = []
array_openings = []

print('Preparing Data')
for file_name in list_of_files[:10]:
    index_row = 0
    array_dates_for_card  = []
    array_openings_for_card = []
    # open file
    file_object = open(file_name,"r")

    
    index = 0
    # look for duplicates
    seen = set()
    for row in file_object:
        index += 1
        if index == 1: # skip first line
            continue
        data_list = row.split(",")
        # append data to lists
        if data_list[0] in seen:
            break
        seen.add(data_list[0])
        array_dates_for_card.append(data_list[0])
        array_openings_for_card.append(data_list[1])

    # append lists to meta-lists
    array_dates.append(array_dates_for_card)
    array_openings.append(array_openings_for_card)


print("Preparing date array")
Dates = []
index  = 0
for dates in array_dates:
    Dates += dates

Dates = set(Dates)  # keep only unique values
Dates = list(Dates) # make a list again
Dates.sort()        # sort

M = pd.DataFrame(Dates, index = Dates, columns = ['dates']) # final matrix

# Add each card timeseries to M
print('Creating mini panda dataframes')
list_of_dataframes = [M]
for index_card in range(len(array_dates)):
    # make timeseries matrix
    column_name = list_of_card_names[index_card]
    card_dates = array_dates[index_card]
    prices = array_openings[index_card]
    dataframe = pd.DataFrame({column_name:prices}, index = card_dates)
    list_of_dataframes.append(dataframe)

print('Concatenating all the matrices; may take a while')
M = pd.concat(list_of_dataframes, axis=1, sort=False)

# memory management
del array_dates, Dates, list_of_dataframes
print(M.head(10))

M.to_csv(csv_output)