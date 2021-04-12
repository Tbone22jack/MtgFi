import pandas as pd
import numpy as np
import time
import os
from tqdm import tqdm

dir_path = os.path.dirname(os.path.realpath(__file__))

print('This program extracts out the name and set code for each card and matches that code with a set name')
print('and exports a csv with the card name, set code, and set name for scraping later')

cards = pd.read_csv(os.path.join(dir_path,"MTGJSON","AllPrintingsCSVFiles","cards.csv"),
                    usecols = ["name","setCode", "supertypes"])
cards.columns = ["name","setCode", "type"]

sets = pd.read_csv(os.path.join(dir_path,"MTGJSON","AllPrintingsCSVFiles","sets.csv"),
                   usecols = ["name","code", "releaseDate"])
sets.columns = ["setCode","setName","releaseDate"]

# add cards together
combine = cards.merge(sets, on='setCode')
#combine = combine.drop(['setCode'], axis=1)

# make a list of unique names
new_combine = combine.sort_values(by=['releaseDate'], ascending=True)
final_combine = new_combine.drop_duplicates(subset=['name'])

print(combine.head(5))
final_combine.to_csv(os.path.join(dir_path,"filtered_cards.csv"))
