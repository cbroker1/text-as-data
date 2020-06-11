#the below script pulls all reviews from a steam game 'Squad' and puts them
#into a .csv


import urllib.request
import urllib.parse
import json
import pandas as pd
from pandas import json_normalize


count = 0
url_base = 'https://store.steampowered.com/appreviews/393380?json=1&filter=updated&review_type=all&num_per_page=100&cursor='

#first pass
url = urllib.request.urlopen("https://store.steampowered.com/appreviews/393380?json=1&filter=updated&review_type=all&num_per_page=100&cursor=*")
data = json.loads(url.read().decode())
next_cursor = data['cursor']
next_cursor = next_cursor.replace('+', '%2B')
df1 = json_normalize(data['reviews'])
count += 100
print(next_cursor)
print(count)


#add results till stopcursor met, then send all results to csv
while True:
    url_temp = url_base + next_cursor
    url = urllib.request.urlopen(url_temp)
    data = json.loads(url.read().decode())
    next_cursor = data['cursor']
    next_cursor = next_cursor.replace('+', '%2B')
    df2 = json_normalize(data['reviews'])
    df1 = pd.concat([df1, df2])
    count += 100
    print(next_cursor)
    print(count)
    if next_cursor == 'AoJ4tey90tECcbOXSw==':
        # send to csv
        df1.to_csv('file_name.csv')
        break

#send df to csv
df1.to_csv('file_name.csv')
