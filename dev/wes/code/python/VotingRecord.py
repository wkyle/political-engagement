#!/usr/bin/python3

#import packages
import numpy as np
import matplotlib.pyplot as plt
import xml.etree.ElementTree as ET
import requests




session_tag = "SessionNumber"
parliament_tag = "ParliamentNumber"
vote_tag = "DecisionDivisionNumber"

votes_xml = "/home/wes/Downloads/Export.xml"

data = []
master_list = []

tree = ET.parse(votes_xml)
root = tree.getroot()
for vote in root:
    data.append({"parliament": vote.findtext(parliament_tag),
                 "session": vote.findtext(session_tag),
                 "number": vote.findtext(vote_tag)})
    

for vote in data:
    url = "https://www.ourcommons.ca/Parliamentarians/en/HouseVotes/ExportDetailsVotes?output=XML&parliament=" + vote["parliament"] + "&session=" + vote["session"] + "&vote=" + vote["number"]
    response = requests.get(url)
    content = response.content
    root = ET.fromstring(content)
    for voter in root:
        name = voter.findtext("Name")
        print(name)
        master_list.append(name)


master_list = list(set(master_list))
[print(i) for i in master_list]
print(len(master_list))
