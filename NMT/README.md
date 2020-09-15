# Standard Format

```
data/
    mono/
        lg1.mono
        lg2.mono
        lg3.mono
        ...
    para/
        lg1-lg2.lg1
        lg1-lg2.lg2
        ...
```

# Points to Note :

0.) ```lg1, lg2,.. lgi``` denote [ISO 639-1](https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes) codes of corresponding languages.

1.) If ```lg1-lg2.lg1``` exists in ```para/``` , then so must one(and only one) ```lg1-lg2.lg2``` file be there in it.

2.) If ```lg1-lg2.lgi``` exists in ```para/```, then ```lg1``` must be alphabetically smaller than ```lg2``` .

# Datasets

## Press Information Bureau

The dataset is hosted at : http://preon.iiit.ac.in/~jerin/resources/datasets/

Link to paper : https://www.aclweb.org/anthology/2020.lrec-1.462.pdf

Repo to play Around : https://github.com/jerinphilip/ilmulti

**Example Command** : 
```
python3 Std-Indic-NLP/NMT/datasets/pib_v0.2.py --data_path data_dir/ --delete_old --exists
```

## PM-India Dataset

Data Hosted at : http://data.statmt.org/pmindia/

Link to Paper : https://arxiv.org/abs/2001.09907

Crawler for making dataset : https://github.com/bhaddow/pmindia-crawler

## UFAL en-ta Dataset

Description Website : http://ufal.mff.cuni.cz/~ramasamy/parallel/html/

Download Link : http://ufal.mff.cuni.cz/~ramasamy/parallel/data/v2/en-ta-parallel-v2.tar.gz

## NLPC en-ta Dataset

Description Repo : https://github.com/nlpcuom/English-Tamil-Parallel-Corpus

## Tsardia en-gu Dataset

Description Repo : https://github.com/shahparth123/eng_guj_parallel_corpus

## ALT Parallel Corpus for bn-en & en-hi

Asian Language Treebank : http://www2.nict.go.jp/astrec-att/member/mutiyama/ALT/

Description Website : http://www2.nict.go.jp/astrec-att/member/mutiyama/ALT/ALT-Parallel-Corpus-20191206/README.txt

Download Link : http://www2.nict.go.jp/astrec-att/member/mutiyama/ALT/ALT-Parallel-Corpus-20191206.zip