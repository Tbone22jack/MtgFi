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

#new-iteration started at 1:55am
#started again around 2:37
#TODO: make a list of cards that give it a 404


def file_generator(filename):
    '''
    Returns file contents quickly
    ''' 
    with open(filename, 'r') as file_handler:
        for line in file_handler:
                yield line


dir_path = os.path.dirname(os.path.realpath(__file__))


def url_maker(set_name, card_name):
    set_name = set_name.replace(' / ','+').replace(' // ','+').replace(" ","+").replace("'",'').replace(':','').replace('.','').replace('-','+')
    card_name = card_name.replace(' / ','+').replace(' // ','+').replace(', ', '+').replace(" ","+").replace("'",'').replace('-','+')
    return set_name + '/' + card_name

def local_url_maker(set_name, card_name):
    card_url = url_maker(set_name, card_name)
    return os.path.join(dir_path, "Price_Info", card_url.replace('/','_') + '.txt')

def count_number_of_lines(filename):
    file_gen = file_generator(filename)
    i = 0
    while True:
        try:
            next(file_gen)
            i += 1
        except Exception as e:
            print(e)
            break
    print(filename)
    return i


if __name__ == '__main__':
    csv_path = os.path.join(dir_path, "filtered_cards.csv")
    cards = pd.read_csv(csv_path)

    # open robots.txt

    strUrl = 'https://www.mtggoldfish.com/robots.txt'
    requests.get(strUrl)
    
    # make a progress bar
    number_of_cards = count_number_of_lines(csv_path)
    progress = tqdm(desc=f"Counting Cards", total=number_of_cards)

    for index, row in tqdm(cards.iterrows()):

        card_url = url_maker(row.loc['setName'], row.loc['name'])
        #card_info_filepath = os.path.join(dir_path, "Card_Text", card_url.replace('/','_') + '.txt')
        price_info_filepath = local_url_maker(row.loc['setName'], row.loc['name'])
        if os.path.exists(price_info_filepath):
            progress.update(1)
            continue

        if index <= 8325:
            progress.update(1)
            continue

        print(card_url)


        # wait for a random amount of time
        sleep_time  = randint(3,5)
        sleep(sleep_time)

        
        # get html from website
        strUrl = 'https://www.mtggoldfish.com/price/' + card_url + '#paper'
        webpage = requests.get(strUrl)
        if webpage.status_code == 404:
            with open(os.path.join(dir_path, 'failed.txt'),'a') as file_handler:
                now = datetime.datetime.now()
                file_handler.write(now.strftime('%m/%d/%Y, %H:%M:%S') + '  |  ' + card_url + '\n')
                progress.update(1)
                continue
        html = webpage.content

        # get dates
        regularExpression = re.compile(r'\s\sd\s\+=\s\"\\n([^"]+)\"')
        lstDates = regularExpression.findall(str(html, 'UTF-8'))
        strDates = '\n'.join(lstDates)

        # get text about card
        # parsed_html = BeautifulSoup(html, 'html.parser')
        # strOracle = str(parsed_html.body.find('div', attrs={'id':'oracle-text'}))
        # # clean text
        # strOracle = re.sub('<br\/\s*?>', ' ', strOracle)
        # strOracle = re.sub(r'<(.|\n)*?>', "", strOracle).replace('\n', ' ')
        # strOracle = re.sub(r' +', ' ', strOracle).strip()

        # write info in appropriate place
        with open(price_info_filepath, 'w') as file_handler:
            file_handler.write(strDates)
        
        progress.update(1)




