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
│   │   ├── databaseXML [17 entries exceeds filelimit, not opening dir]
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
│       │   │   └── politician_modules
│       │   │       ├── council_modules.js
│       │   │       ├── mla_modules.js
│       │   │       └── mp_modules.js
│       │   └── python
│       │       ├── codeFED.py                                                                                                                                                                                                                     
│       │       ├── colormaps.py                                                                                                                                                                                                                   
│       │       ├── tools.py                                                                                                                                                                                                                       
│       │       ├── url.py                                                                                                                                                                                                                         
│       │       └── xmlParsing.py                                                                                                                                                                                                                  
│       └── data                                                                                                                                                                                                                                   
│           ├── government                                                                                                                                                                                                                         
│           │   └── DBUpdate.py                                                                                                                                                                                                                    
│           ├── legislation                                                                                                                                                                                                                        
│           │   ├── databaseXML [17 entries exceeds filelimit, not opening dir]                                                                                                                                                                    
│           │   └── linked_bill_database.xml                                                                                                                                                                                                       
│           └── mapping                                                                                                                                                                                                                            
│               ├── AB                                                                                                                                                                                                                             
│               │   └── PED_AB_raw.shp.xml                                                                                                                                                                                                         
│               ├── BC                                                                                                                                                                                                                             
│               ├── CAN                                                                                                                                                                                                                            
│               │   └── shapefile                                                                                                                                                                                                                  
│               ├── MB                                                                                                                                                                                                                             
│               │   └── PED_MB_raw.shp.xml                                                                                                                                                                                                         
│               ├── NB                                                                                                                                                                                                                             
│               ├── NL                                                                                                                                                                                                                             
│               ├── NS                                                                                                                                                                                                                             
│               ├── NT
│               ├── NU
│               ├── ON
│               ├── PE
│               ├── QC
│               ├── SK
│               │   └── PED_SK_raw.shp.xml
│               └── YT
└── production
    └── readme.txt


```