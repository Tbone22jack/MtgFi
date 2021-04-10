# Combines price info with miscellaneous info from mtgjson


from os import listdir, remove
from tqdm import tqdm  # all this does is add a progress bar
from Scraper import local_url_maker, dir_path



# get file names
price_dir = os.path.join(dir_path, "Price_Info")
csv_output = os.path.join(dir_path, "final.csv")

list_of_files = listdir(price_dir)
# only accept .txt files
list_of_files = [item for item in list_of_files if item[-4:] == '.txt']


array_dates    = []
array_openings = []
array_closings = []
array_deltas   = []

print('Preparing Data')
for file_name in tqdm(list_of_files):
    index_row= 0
    array_dates_for_a_Stock  = []
    array_openings_for_stock = []
    array_closings_for_stock = []
    array_deltas_for_stock   = []
    # open file
    file_object = open(price_dir+file_name,"r")

    index = 0
    for row in file_object:
        index += 1
        if index == 1: # skip first line
            continue
        row = row.split(",")
        # append data to lists
        array_dates_for_a_Stock.append(row[0])
        opening = row[1]
        array_openings_for_stock.append(opening)
        closing = row[4]
        array_closings_for_stock.append(closing)
        array_deltas_for_stock.append(float(closing)  -  float(opening))

    # close file
    file_object.close()

    # append lists to meta-lists
    array_dates.append(array_dates_for_a_Stock)
    array_closings.append(array_closings_for_stock)
    array_openings.append(array_openings_for_stock)
    array_deltas.append(array_deltas_for_stock)