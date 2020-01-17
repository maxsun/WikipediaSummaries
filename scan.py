from typing import Dict, List
import wikipedia
import json
from datetime import datetime
import pandas as pd
import random

from requests.exceptions import ConnectionError
from wikipedia.exceptions import PageError, DisambiguationError

def save(page_data: Dict[str, Dict]) -> None:
    pd.DataFrame.from_dict(page_data).to_json(
        path_or_buf='./wiki.json.gz',
        compression='gzip')
    print('Saved', len(page_data), ' pages.')

def load() -> Dict:
    try:
        return pd.read_json('./wiki.json.gz', compression='gzip').to_dict()
    except FileNotFoundError:
        print('Starting with new data.')
        return {}


page_data: Dict[str, Dict] = load()
queue: List[str] = ['Cognitive Science']
MAX_ADDITIONS: int = 1000
num_additions: int = 0

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
                'doa': datetime.utcnow().strftime("%m/%d/%Y, %H:%M")
            }
            links = page.links
            print('Read:', page.title)
            num_additions += 1

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
