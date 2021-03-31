import pandas as pd
import numpy
import time

#This program extracts out the name and set code for each card and matches that code with a set name
#and exports a csv with the card name, set code, and set name for scraping later
cards_col = ["name","code","uuid"]
sets_col = ["code","setName"]
cards = pd.read_csv("C:/Users/thoma/Downloads/AllPrintingsCSVFiles/cards.csv", usecols = ["setCode","name","uuid"])
cards.columns = cards_col
print(cards)
sets = pd.read_csv("C:/Users/thoma/Downloads/AllPrintingsCSVFiles/sets.csv", usecols = ["code","name"])
sets.columns = sets_col
combine = pd.merge(cards, sets,on ="code")

#This portion is optional as this just reduces the load
combine = combine.drop_duplicates(subset = ['name'])

print(combine)
combine.to_csv("C:/Users/thoma/Desktop/Magic Project/data/cards0.csv")
