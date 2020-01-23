

# Wikipedia Text Corpus + Generator Code

This repo contains code for scanning Wikipedia and recording article summaries and links.

`scan.py` scrapes summaries and saves the following data (indexed by article url):

```
{
    'title': str,
    'summary': str,
    'links': [str],
    'doa': datetime
}
```

`wiki.json.gz` contains the currently collected data.
Most recently calculated stats:
- Contains 28,441 summaries.
- Contains 1,221,463 links.
- 2.33% of the known graph has been scanned.
- The most recently read article is "https://en.wikipedia.org/wiki/Johanan_ben_Baroka".
- The article with the most scanned links is "https://en.wikipedia.org/wiki/Liminal_deity".
- On average, the scans were updated 3 days ago.

`python make_readme.py` will rebuild this Readme and update the stats.

`python make_textcorpus.py` will create `wiki.txt`; a file with all of the summaries combined.

    