import pandas as pd
import numpy as np
import time
import os
from tqdm import tqdm

dir_path = os.path.dirname(os.path.realpath(__file__))

print('This program extracts out the name and set code for each card and matches that code with a set name')
print('and exports a csv with the card name, set code, and set name for scraping later')

cards = pd.read_csv(os.path.join(dir_path,"MTGJSON","AllPrintingsCSVFiles","cards.csv"),
                    usecols = ["name","setCode", "originalType"])
cards.columns = ["name","type", "setCode"]

sets = pd.read_csv(os.path.join(dir_path,"MTGJSON","AllPrintingsCSVFiles","sets.csv"),
                   usecols = ["name","code", "releaseDate"])
sets.columns = ["setCode","setName","releaseDate"]

# add cards together
combine = cards.merge(sets, on='setCode')
#combine = combine.drop(['setCode'], axis=1)

# drop lands
boolean_land = combine["type"] == "Land"
combine = combine.loc[~boolean_land]

# drop duplicates
card_names = combine['name'].drop_duplicates().tolist()

# Drop duplicates of cards with the same name but keep the earliest release date
# In order to do this, I put the data in lists, then converted the list into a dataframe
# Apparently, this is a tiny bit faster than keeping everything in pandas
releaseDates = []
setNames = []
setCodes = []

for index in tqdm(range(len(card_names))):
    boolean_name_match = combine['name'] == card_names[index]
    # if name is unique, just add it to lists
    if boolean_name_match.sum() == 1:
        releaseDates.append(combine['releaseDate'].loc[boolean_name_match])
        setNames.append(combine['setName'].loc[boolean_name_match])
        setCodes.append(combine['setCode'].loc[boolean_name_match])
        continue
    
    # otherwise, iterate through dates and pick the smallest one
    name_match = combine.loc[boolean_name_match]
    lowest_date = name_match['releaseDate'].iloc[0]
    index_lowest_date = 0
    for j in range(1,len(name_match)):
        temp_date = name_match['releaseDate'].iloc[j]
        if temp_date < lowest_date:
            lowest_date = name_match['releaseDate'].iloc[j]
            index_lowest_date = j
    
    releaseDates.append(lowest_date)
    setNames.append(name_match['setName'].iloc[j])
    setCodes.append(name_match['setCode'].iloc[j])

filtered_cards = pd.DataFrame({'name':card_names,
                               'setName':setNames,
                               'releaseDates':releaseDates,
                               'setCodes':setCodes})

print(filtered_cards.head(5))
filtered_cards.to_csv(os.path.join(dir_path,"filtered_cards.csv"))
