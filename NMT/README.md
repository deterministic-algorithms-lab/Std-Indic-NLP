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
python3 datasets/pib_v0.2 --data_path
```
