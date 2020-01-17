
import wikipedia
import json
from datetime import datetime

from requests.exceptions import ConnectionError
from wikipedia.exceptions import PageError, DisambiguationError

data_path = './out/wiki.json'
text_path = './out/wiki.txt'

def save(data, path=data_path):
    print('Saving...')
    open(path, 'w').write(json.dumps(data))
    print('Saved', len(data), 'pages.')

page_data = {}
try:
    page_data = json.loads(open(data_path).read())
except FileNotFoundError as e:
    print('No existing data found; initializing blank corpus data.')


MAX_ADDITIONS = 3000
queue = ['Human Brain']
num_additions = 0
while len(queue) > 0 and num_additions < MAX_ADDITIONS:
    title = queue.pop(0)
    links = []
    if title not in page_data:
        # print('Reading:', title)
        try:
            page = wikipedia.page(title)
            links = page.links
            page_data[title] = {
                'summary': page.summary,
                'links': page.links,
                'url': page.url,
                'DOA': datetime.utcnow().strftime("%H:%M:%S")
            }
            print('Read:', page.title)

            num_additions += 1
            if num_additions % 5 == 0 or num_additions == MAX_ADDITIONS:
                save(page_data)

        except ConnectionError as e:
            print('Lost connection while reading:', title)
        except PageError as e:
            print('Failed to find page for:', title)
        except DisambiguationError as e:
            print('Failed to disambiguate:', title)
    else:
        links = page_data[title]['links']

    for link in links:
        if link not in page_data and link not in queue:
            queue.append(link) 

