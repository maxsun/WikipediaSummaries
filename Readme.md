

# Wikipedia Text Corpus + Generator Code

This repo contains code for scanning Wikipedia and recording article summaries and links.

`scan.py` scrapes summaries and saves the following data (indexed by article title):

```
{
    'summary': str,
    'url': str,
    'links': [str],
    'doa': datetime
}
```

`wiki.json.gz` contains the currently collected data.
Most recently calculated stats:
- Contains 22204 summaries.
- Contains 1022974 links.
- 0.02170534148472982% of the known graph has been scanned.
- The most recently read article is "Mercury's moon".
- The articles with the most scanned links are: Neural Darwinism.
- The average age of each scan is 1 days 18:35:54.862751.

`python make_readme.py` will rebuild this Readme and update the stats.

`python make_textcorpus.py` will create `wiki.txt`; a file with all of the summaries combined.

    