

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
- Contains 16985 summaries.
- Contains 858136 links.
- 0.019792899959913113% of the known graph has been scanned.
- The most recently read article is "Relative clause".
- The articles with the most scanned links are: Neural Darwinism.
- The average age of each scan is 1 days 08:39:14.100360.

`python make_readme.py` will rebuild this Readme and update the stats.

`python make_textcorpus.py` will create `wiki.txt`; a file with all of the summaries combined.

    