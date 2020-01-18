
import json
import pandas as pd
from datetime import datetime, timedelta

def build_readme(page_data, path='Readme.md'):

    all_links = set([l for title, p in page_data.items() for l in p['links']])

    def find_page_scan_ratio(title):
        p = page_data[title]
        num_found = 0
        for link in p['links']:
            if link in page_data:
                num_found += 1
        return num_found / len(p['links'])

    num_scanned_pages = len(page_data)
    num_links = len(all_links)

    titles_by_scan_ratio = sorted(
        page_data.keys(),
        key=find_page_scan_ratio,
        reverse=True)

    titles_by_doa = sorted(
        page_data.keys(),
        key=lambda x: page_data[x]['doa'],
        reverse=True)

    now = datetime.utcnow()
    page_ages = [now - p['doa'] for _, p in page_data.items()]
    average_timedelta = sum(page_ages, timedelta(0)) / len(page_ages)

    readme = """

# Wikipedia Text Corpus + Generator Code

This repo contains code for scanning Wikipedia and recording article summaries and links.

`scan.py` scrapes summaries and saves the following data (indexed by article title):

```
{{
    'summary': str,
    'url': str,
    'links': [str],
    'doa': datetime
}}
```

`wiki.json.gz` contains the currently collected data.
Most recently calculated stats:
- Contains {0} summaries.
- Contains {1} links.
- {2}%% of the known graph has been scanned.
- The most recently read article is "{3}".
- The articles with the most scanned links are: {4}.
- The average age of each scan is {5}.

`python make_readme.py` will rebuild this Readme and update the stats.

`python make_textcorpus.py` will create `wiki.txt`; a file with all of the summaries combined.

    """.format(
        num_scanned_pages,
        num_links,
        num_scanned_pages / num_links,
        titles_by_doa[0],
        titles_by_scan_ratio[0],
        average_timedelta
        )

    open(path, 'w').write(readme)


if __name__ == '__main__':
    df = pd.read_json('./wiki.json.gz', compression='gzip', orient='columns', convert_dates=False)
    df['doa'] = df['doa'].apply(lambda x: datetime.utcfromtimestamp(x))
    build_readme(df.to_dict(orient='index'))