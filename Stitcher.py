'''

Combines price info or miscellaneous info from mtgjson and pickles them


'''


from os import listdir, remove
import os
import pandas as pd
import numpy as np
from tqdm import tqdm  # all this does is add a progress bar
from Scraper import local_url_maker, dir_path, count_number_of_lines, file_generator
import pickle
from csv import reader


def stitch_dates():
    csv_path = os.path.join(dir_path, "filtered_cards.csv")
    cards = pd.read_csv(csv_path)


    list_of_files = []
    list_of_card_names = []
    list_of_card_set_names = []

    i = 0
    for index, row in tqdm(cards.iterrows(), total=cards.shape[0]):
        price_info_filepath = local_url_maker(row.loc['setName'], row.loc['name'])
        if os.path.exists(price_info_filepath):
            list_of_files.append(price_info_filepath)
            list_of_card_names.append(row.loc['name'])
            list_of_card_set_names.append(row.loc['setName'])
            i += 1

    number_of_files = i
    print("Number of files that can be parsed: ", i)

    array_dates    = []
    array_prices = []

    print("Preparing date array")
    for file_name in tqdm(list_of_files):
        index_row = 0
        array_dates_for_card  = []
        prices_for_card = []
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
            prices_for_card.append(data_list[1])

        # append lists to meta-lists
        array_dates.append(array_dates_for_card)
        array_prices.append(prices_for_card)


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
    for index_card in tqdm(range(len(array_dates))):
        # make timeseries matrix
        column_name = list_of_card_names[index_card]
        card_dates = array_dates[index_card]
        prices = array_prices[index_card]
        dataframe = pd.DataFrame({column_name:prices}, index = card_dates)
        list_of_dataframes.append(dataframe)

    print('Concatenating all the matrices; may take a while')
    M = pd.concat(list_of_dataframes, axis=1, sort=False)
    M = M.ffill() # forward fill

    # memory management
    del array_dates, Dates, list_of_dataframes, array_prices
    print(M.tail(10))

    print('Saving the dates Dataframe to a pickle')
    with open(os.path.join(dir_path, 'pickledDates'), 'wb') as file_handler:
        pickle.dump(M,file_handler)



def get_card_info(text_you_want, uid1='',uid1_text='',uid2='',uid2_text=''):
    '''
possible unique id's:

index,id,artist,asciiName,availability,borderColor,cardKingdomFoilId,
cardKingdomId,colorIdentity,colorIndicator,colors,convertedManaCost,
duelDeck,edhrecRank,faceConvertedManaCost,faceName,flavorName,flavorText,frameEffects,
frameVersion,hand,hasAlternativeDeckLimit,hasContentWarning,hasFoil,hasNonFoil,
isAlternative,isFullArt,isOnlineOnly,isOversized,isPromo,isReprint,isReserved,
isStarter,isStorySpotlight,isTextless,isTimeshifted,keywords,layout,leadershipSkills,
life,loyalty,manaCost,mcmId,mcmMetaId,mtgArenaId,mtgjsonV4Id,mtgoFoilId,mtgoId,
multiverseId,name,number,originalReleaseDate,originalText,originalType,otherFaceIds,
power,printings,promoTypes,purchaseUrls,rarity,scryfallId,scryfallIllustrationId,
scryfallOracleId,setCode,side,subtypes,supertypes,tcgplayerProductId,text,toughness,
type,types,uuid,variations,watermark
    '''
    _g = file_generator(os.path.join(dir_path, 'MTGJSON', 'AllPrintingsCSVFiles', 'cards.csv'))
    ids = list(reader([next(_g)]))[0]
    if (text_you_want in ids) and (uid1 in ids):
        if uid2 != '':
            if uid2 in ids:
                pass
            else:
                print('uid2 not found')
                return -1
        else:
            pass
    else:
        print('text_you_want and/or uid1 not found')
        return -1
    
    index_text_you_want = ids.index(text_you_want)
    i1 = ids.index(uid1)

    # if two unique identifiers are provided
    if (uid1 != '') and (uid2 != ''):
        i2 = ids.index(uid2)
        while True:
            try:
                line = list(reader([next(_g)]))[0]
                if (line[i1] == uid1_text) and (line[i2] == uid2_text):
                    return line[index_text_you_want]
            except IndexError:
                pass
            except:
                return -1
    # if one unique identifier is provided
    elif (uid1 != '') and (uid2 == ''):
        while True:
            try:
                line = list(reader([next(_g)]))[0]
                if line[i1] == uid1_text:
                    return line[index_text_you_want]
            except IndexError:
                pass
            except:
                return -1
    # on the weird chance that an identifier is labeled blank
    # this can only happen if a column header in the csv is blank
    else:
        return -1


def stitch_card_info():
    pass



if __name__ == '__main__':
    stitch_dates()
    # stitch_card_info()
    """
    print(get_card_info('flavorText', 'name', "Ancestor's Chosen"))

    csv_path = os.path.join(dir_path, "filtered_cards.csv")
    cards = pd.read_csv(csv_path)
    card_info = pd.read_csv(os.path.join(dir_path, 'MTGJSON', 'AllPrintingsCSVFiles', 'cards.csv'))

    list_of_files = []
    list_of_card_names = []
    list_of_card_setCodes = []

    i = 0
    for index, row in tqdm(cards.iterrows(), total=cards.shape[0]):
        price_info_filepath = local_url_maker(row.loc['setName'], row.loc['name'])
        if os.path.exists(price_info_filepath):
            list_of_files.append(price_info_filepath)
            list_of_card_names.append(row.loc['name'])
            list_of_card_setCodes.append(row.loc['setCode'])
            i += 1

    number_of_files = i
    print("Number of files that can be parsed: ", i)

    array_words = []

    i = -1
    print("Preparing word array")
    for file_name in tqdm(list_of_files):
        i+=1
        i1 = card_info['name'] == list_of_card_names[i]
        match = card_info.loc[i1]
        # i2 = match['setCode'] == list_of_card_setCodes[i]
        for j in range(match.shape[0]):
            text = match.iloc[j]['originalText']
            if type(text) == type(str()):
                array_words.append(text)
                break
        if (j == match.shape[0]-1) and (type(text) == type(float)):
            print('there is a card without text: ', list_of_card_names[i])
            array_word.append('')
        '''
        try:
            array_words.append(match.loc[i2]['originalText'].max()) # max makes it a string, strangely enough
        except:
            # occurs when there are two matches
            array_words.append(match.loc[i2].iloc[0]['originalText'])
        '''
        # array_words.append(get_card_info('originalText', 'name', list_of_card_names[i], 'originalReleaseDate', list_of_card_setCodes[i]))
    
    with open('list_of_words.txt','w') as file_handler:
        file_handler.write(' '.join(array_words))
    """