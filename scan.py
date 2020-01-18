
import wikipedia
import json
from datetime import datetime
import pandas as pd
import random
from make_readme import build_readme

from requests.exceptions import ConnectionError
from wikipedia.exceptions import PageError, DisambiguationError

def save(page_data):
    df = pd.DataFrame.from_dict(page_data, orient='index')
    df['doa'] = df['doa'].apply(lambda x: x.timestamp())
    df.to_json(
        path_or_buf='./wiki.json.gz',
        compression='gzip',
        )
    build_readme(page_data)
    print('Saved', len(page_data), 'pages.')

def load():
    try:
        df = pd.read_json('./wiki.json.gz', compression='gzip', orient='columns', convert_dates=False)
        df['doa'] = df['doa'].apply(lambda x: datetime.utcfromtimestamp(x))
        return df.to_dict(orient='index')
    except FileNotFoundError:
        print('Starting with new data.')
        return {}


page_data = load()

queue = ['Cognitive Science']
MAX_ADDITIONS = 1000
num_additions = 0

while num_additions < MAX_ADDITIONS:
    try:
        if len(queue) == 0:
            # add a random existing title if the queue has nothing.
            queue.append(random.choice(list(page_data.keys())))
        
        title = queue.pop(0)
        links = []
        try:
            page = wikipedia.page(title)
            page_data[title] = {
                'summary': page.summary,
                'links': page.links,
                'url': page.url,
                'doa': datetime.utcnow() #.strftime("%m/%d/%Y, %H:%M")
            }
            links = page.links
            print('Read:', page.title)
            num_additions += 1

            if num_additions % 10 == 0:
                print('Saving at checkpoint, after', num_additions, 'pages.')
                save(page_data)

        except ConnectionError as e:
            print('Lost connection while reading:', title)
        except PageError as e:
            print('Failed to find page for:', title)
        except DisambiguationError as e:
            links = e.options
            print('Failed to disambiguate:', title)

        for link in links:
            if link not in page_data and link not in queue:
                queue.append(link)

    except KeyboardInterrupt as e:
        print('\nStopping after', num_additions, 'read pages.')
        break

save(page_data)
