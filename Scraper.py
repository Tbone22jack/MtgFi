import pandas as pd
import numpy
import requests
from bs4 import BeautifulSoup


cards = pd.read_csv("C:/Users/thoma/Desktop/Magic Project/data/cards.csv")

for index, row in cards.iterrows():
    url = 'https://www.mtggoldfish.com/price/' + row.loc['setName'].replace(" ","+") + '/' + row.loc['name'].replace(" ","+") + '#paper'

    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    cont = str(soup.prettify())


    x = cont.split("\n")
    found = False
    New = []
    for y in x:
        if found == True:
            if y.find("d += ") == -1:
                break
        if y.find("d += ") != -1:
            found = True
            New.append(y)
