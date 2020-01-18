

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
- Contains 5 summaries.
- Contains 1673 links.
- 0.002988643156007173%% of the known graph has been scanned.
- The most recently read article is "Alan Turing".
- The articles with the most scanned links are: Cognitive Science.
- The average age of each scan is 0 days 00:00:06.534819.

`python make_readme.py` will rebuild this Readme and update the stats.

`python make_textcorpus.py` will create `wiki.txt`; a file with all of the summaries combined.

    