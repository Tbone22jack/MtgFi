import pandas as pd
import numpy
import requests
from bs4 import BeautifulSoup
import re
import os
from random import randint
from time import sleep
from tqdm import tqdm
import datetime




def file_generator(filename):
    '''
    Returns file contents quickly
    ''' 
    with open(filename, 'r') as file_handler:
        for line in file_handler:
                yield line



dir_path = os.path.dirname(os.path.realpath(__file__))
cards = pd.read_csv(os.path.join(dir_path, "cards.csv"))


# open robots.txt

strUrl = 'https://www.mtggoldfish.com/robots.txt'
requests.get(strUrl)

# make a progress bar
progress = tqdm(desc=f"Counting Cards", total=21744)


for index, row in tqdm(cards.iterrows()):
    #check if info is already downloaded
    card_name = row.loc['setName'].replace(" ","+") + '/' + row.loc['name'].replace(' // ','+').replace(', ', '+').replace(" ","+").replace("'",'')
    card_info_filepath = os.path.join(dir_path, "Card_Text", card_name.replace('/','_') + '.txt')
    price_info_filepath = os.path.join(dir_path, "Price_Info", card_name.replace('/','_') + '.txt')
    if os.path.exists(card_info_filepath) and os.path.exists(price_info_filepath):
        progress.update(1)
        continue


    print(card_name)


    # wait for a random amount of time
    sleep_time  = randint(10,20)
    sleep(sleep_time)

    
    # get html from website
    strUrl = 'https://www.mtggoldfish.com/price/' + card_name + '#paper'
    webpage = requests.get(strUrl)
    if webpage.status_code == 404:
        with open(os.path.join(dir_path, 'failed.txt'),'a') as file_handler:
            now = datetime.datetime.now()
            file_handler.write(now.strftime('%m/%d/%Y, %H:%M:%S') + '  |  ' + card_name + '\n')
            progress.update(1)
            continue
    html = webpage.content

    # get dates
    regularExpression = re.compile(r'\s\sd\s\+=\s\"\\n([^"]+)\"')
    lstDates = regularExpression.findall(str(html, 'UTF-8'))
    strDates = '\n'.join(lstDates)

    # get text about card
    parsed_html = BeautifulSoup(html, 'html.parser')
    strOracle = str(parsed_html.body.find('div', attrs={'id':'oracle-text'}))
    # clean text
    strOracle = re.sub('<br\/\s*?>', ' ', strOracle)
    strOracle = re.sub(r'<(.|\n)*?>', "", strOracle).replace('\n', ' ')
    strOracle = re.sub(r' +', ' ', strOracle).strip()

    # write info in appropriate place
    with open(card_info_filepath, 'w') as file_handler:
        file_handler.write(strOracle)

    with open(price_info_filepath, 'w') as file_handler:
        file_handler.write(strDates)
    
    progress.update(1)

    

