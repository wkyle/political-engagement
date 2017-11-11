#!/usr/bin/python3

#import packages
import xml.etree.ElementTree as ET


data = []
with open("../../data/government/OntarioMPPTwitter.txt", "r") as f:
    f.readline()
    for line in f.readlines():
        l = line.split("\t")
        name = l[0].split(",")[1].strip() + " " + l[0].split(",")[0].strip()
        region = l[1]
        handle = l[2]
        data.append([name, region, handle])


tree = ET.ElementTree()
root = ET.Element("MPPs")
tree._setroot(root)
for i, d in enumerate(data):
    mpp = ET.SubElement(root, "MPP")
    mpp.attrib = {"id": str(i+1).zfill(3)}
    name = ET.SubElement(mpp, "Name")
    name.text = d[0].strip()
    region = ET.SubElement(mpp, "Region")
    region.text = d[1].strip()
    twitter = ET.SubElement(mpp, "TwitterHandle")
    twitter.text = d[2].strip()
    facebook = ET.SubElement(mpp, "FacebookPage")

tree.write("../../data/government/OntarioMPPSocial.xml", encoding="UTF-8")
