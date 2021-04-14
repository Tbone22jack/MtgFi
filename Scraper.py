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
from help import getfile

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
    return getfile("Price_Info", card_url.replace('/','_') + '.txt')

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
    if os.path.exists(getfile('failed.csv')):
        failed_urls = pd.read_csv(getfile('failed.csv'), header = None, index_col = 0, squeeze = True)
        failed_urls = set(failed_urls)
    else:
        failed_urls = set()

    csv_path = getfile("filtered_cards.csv")
    cards = pd.read_csv(csv_path)

    # open robots.txt

    strUrl = 'https://www.mtggoldfish.com/robots.txt'
    requests.get(strUrl)
    
    # make a progress bar
    number_of_cards = count_number_of_lines(csv_path)
    progress = tqdm(desc=f"Counting Cards", total=number_of_cards)

    try:
        for index, row in tqdm(cards.iterrows()):

            card_url = url_maker(row.loc['setName'], row.loc['name'])
            price_info_filepath = local_url_maker(row.loc['setName'], row.loc['name'])
            
            # check if a previous attempt at this has already failed
            if card_url in failed_urls:
                progress.update(1)
                continue

            # check if already scraped
            if os.path.exists(price_info_filepath):
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
                failed_urls.add(card_url)
                if len(failed_urls) % 5 == 0:
                    pd.Series(list(failed_urls)).to_csv('failed.csv')
                with open(getfile('failed.txt'),'a') as file_handler:
                    now = datetime.datetime.now()
                    file_handler.write(now.strftime('%m/%d/%Y, %H:%M:%S') + '  |  ' + card_url + '\n')
                    progress.update(1)
                    continue
            html = webpage.content

            # get dates
            regularExpression = re.compile(r'\s\sd\s\+=\s\"\\n([^"]+)\"')
            lstDates = regularExpression.findall(str(html, 'UTF-8'))
            strDates = '\n'.join(lstDates)

            # write info in appropriate place
            with open(price_info_filepath, 'w') as file_handler:
                file_handler.write(strDates)
            
            progress.update(1)

    except Exception as e:
        print(e)
        print('Failed at card: ', row.loc['name'])
        pd.Series(list(failed_urls)).to_csv('failed.csv')
    
    print('Downloading cards was successful')
    pd.Series(list(failed_urls)).to_csv('failed.csv')

