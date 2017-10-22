# political-engagement
Tools for Canadian political participation and engagement project.



## File Structure

To print file structure in console:

```
tree -P '*.py|*.txt|*.js|*.xml' --filelimit 14
```



```
.
├── data
│   ├── legislation
│   │   ├── databaseXML
│   │   └── linked_bill_database.xml
│   └── mapping
│       ├── AB
│       ├── BC
│       ├── CAN
│       │   └── shapefile
│       ├── MB
│       ├── NB
│       ├── NL
│       ├── NS
│       ├── NT
│       ├── NU
│       ├── ON
│       ├── PE
│       ├── QC
│       ├── SK
│       └── YT
├── dev
│   ├── elliot
│   │   ├── code
│   │   │   ├── js
│   │   │   └── python
│   │   └── readme.txt
│   └── wes
│       ├── assets
│       │   └── regex.txt
│       ├── code
│       │   ├── js
│       │   └── python
│       │       ├── codeFED.py
│       │       ├── colormaps.py
│       │       ├── tools.py
│       │       ├── url.py
│       │       └── xmlParsing.py
│       └── data
│           ├── legislation
│           │   ├── databaseXML
│           │   └── linked_bill_database.xml
│           └── mapping
│               ├── AB
│               │   └── PED_AB_raw.shp.xml
│               ├── BC
│               ├── CAN
│               │   └── shapefile
│               ├── MB
│               ├── NB
│               ├── NL
│               ├── NS
│               ├── NT
│               ├── NU
│               ├── ON
│               ├── PE
│               ├── QC
│               ├── SK
│               └── YT
└── production
    └── readme.txt 

```