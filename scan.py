
import wikipedia
import json
from datetime import datetime
import pandas as pd
import random
from make_readme import build_readme

from requests.exceptions import ConnectionError
from wikipedia.exceptions import PageError, DisambiguationError

def save(page_data):
    start_time = datetime.now()
    print('Saving - do not exist. This can take a few minutes.')
    df = pd.DataFrame.from_dict(page_data, orient='index')
    df['doa'] = df['doa'].apply(lambda x: x.timestamp())
    df.to_json(
        path_or_buf='./wiki.json.xz',
        compression='xz',
        )
    build_readme(page_data)
    duration = datetime.now() - start_time
    print('Saved', len(page_data), 'pages in', duration)

def load():
    try:
        df = pd.read_json('./wiki.json.xz', compression='xz', orient='columns', convert_dates=False)
        df['doa'] = df['doa'].apply(lambda x: datetime.utcfromtimestamp(x))
        return df.to_dict(orient='index')
    except FileNotFoundError:
        print('Starting with new data.')
        return {}


page_data = load()

all_titles = set()
all_links = set()
for k in page_data.keys():
    all_titles.update(page_data[k]['titles'])
    all_links.update(page_data[k]['links'])

print(len(all_titles))
print(len(all_links))


queue = ['United Nations']
MAX_ADDITIONS = 10000
num_additions = 0

while num_additions < MAX_ADDITIONS:
    try:
        if len(queue) == 0:
            # add a random existing title if the queue has nothing.
            queue.append(random.choice(list(page_data.keys())))
        
        title = queue.pop(0).replace('https://en.wikipedia.org/wiki/', '')
        links = []
        try:
            page = wikipedia.page(title)
            if page.url in page_data and title not in page_data[page.url]['titles']:
                print('Adding {0} to {1}'.format(title, page_data[page.url]['titles']))
                page_data[page.url]['titles'].append(title)
                page_data[page.url]['doa'] = datetime.utcnow()
                page_data[page.url]['summary'] = page.summary
            else:
                print('Read {0} to {1}'.format(title, page.title))
                page_data[page.url] = {
                    'name': page.title
                    'titles': [title],
                    'links': page.links,
                    'doa': datetime.utcnow(),
                    'summary': page.summary
                }
            all_titles.add(title)

            # page_data[title] = {
            #     'summary': page.summary,
            #     'links': page.links,
            #     'url': page.url,
            #     'doa': datetime.utcnow() #.strftime("%m/%d/%Y, %H:%M")
            # }
            links = page.links
            num_additions += 1

            if num_additions % 500 == 0:
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
            if link not in all_titles and link not in queue:
                queue.append(link.replace('https://en.wikipedia.org/wiki/', ''))

    except KeyboardInterrupt as e:
        print('\nStopping after', num_additions, 'read pages.')
        break

save(page_data)
