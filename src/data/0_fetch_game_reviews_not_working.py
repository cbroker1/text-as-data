#import packages
import os
import sys
import time
import json
import numpy as np
import pandas as pd
import urllib.parse
import urllib.request
from tqdm import tqdm
from datetime import datetime
from pandas import json_normalize

# generate game review df:

#steam 'chunks' their json files (the game reviews) in sets of 100
#ending with a signature, a 'cursor'. This cursor is then pasted
#onto the the same url, to 'grab' the next chunk and so on. 
#This sequence block with an 'end cursor' of 'AoJ4tey90tECcbOXSw=='

#set variables
url_base = 'https://store.steampowered.com/appreviews/393380?json=1&filter=updated&language=all&review_type=all&purchase_type=all&num_per_page=100&cursor='

#first pass
url = urllib.request.urlopen("https://store.steampowered.com/appreviews/393380?json=1&filter=updated&language=all&review_type=all&purchase_type=all&num_per_page=100&cursor=*")
data = json.loads(url.read().decode())
next_cursor = data['cursor']
next_cursor = next_cursor.replace('+', '%2B')
df1 = json_normalize(data['reviews'])
print(next_cursor)

#add results till stopcursor met, then send all results to csv
while True:
    time.sleep(0.5) # sleep for half-second
    url_temp = url_base + next_cursor
    url = urllib.request.urlopen(url_temp)
    data = json.loads(url.read().decode())
    next_cursor = data['cursor']
    next_cursor = next_cursor.replace('+', '%2B')
    df2 = json_normalize(data['reviews'])
    df1 = pd.concat([df1, df2])
    print(next_cursor)
    if next_cursor == 'AoJ44PCp0tECd4WXSw==' or next_cursor == '*': #stopcursor
        df_game_reviews = df1
        df1 = None
        df_game_reviews.to_csv(r'../data/raw/game_reviews_raw.csv', index=False)
        print('All finished! Check raw data directory for output.')
        break
        
#the hash output is each 'cursor' we loop through until the 'end cursor'.
#use this to monitor the download.