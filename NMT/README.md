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

## Points to Note :

0.) ```lg1, lg2,.. lgi``` denote [ISO 639-1](https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes) codes of corresponding languages.

1.) If ```lg1-lg2.lg1``` exists in ```para/``` , then so must ```lg1-lg2.lg2``` must also be there.

2.) If ```lg1-lg2.lgi``` exists in ```para/```, then ```lg1``` must be alphabetically smaller than ```lg2``` .
