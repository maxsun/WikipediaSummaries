
import json
import pandas as pd
from datetime import datetime, timedelta

df = pd.read_json('./wiki.json.gz', compression='gzip', orient='columns', convert_dates=False)
df['doa'] = df['doa'].apply(lambda x: datetime.utcfromtimestamp(x))
page_data = df.to_dict(orient='index')

text = ''
for title in page_data.keys():
    text += page_data[title]['summary'] + '\n\n'

open('wiki.txt', 'w').write(text)
