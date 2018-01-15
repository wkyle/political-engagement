#!/usr/bin/python3

#import packages
import json
import xml.etree.ElementTree as ET


jsonpath = "/home/wes/Personal/political-engagement/data/2017-11-07-OntarioScraping/Politicians.json"
xmlpath = "OntarioMPPSocial.xml"





tree = ET.parse(xmlpath)
handles = []
for mp in tree.getroot():
    lname = mp.findtext("Name").split()[-1]
    handle = mp.findtext("TwitterHandle").replace("@", "")
    handles.append([lname, handle])



with open(jsonpath, "r+") as f:
    data = json.load(f)
    for d in data:
        found = False
        for handle in handles:
            if handle[0] == d["LName"]:
                found = True
                d["Social"]["Twitter"] = handle[1]
                print(d["Social"]["Twitter"])
                break
        if not found:
            d["Social"]["Twitter"] = None
    f.seek(0)
    json.dump(data, f, indent=4)
    f.truncate()
