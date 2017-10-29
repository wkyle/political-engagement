#!/usr/bin/python3

import requests
import urllib.request as rq
import xml.etree.ElementTree as ET


mp_xml_url = "http://www.ourcommons.ca/Parliamentarians/en/members/export?output=XML"
output_file = "../../data/government/mp_list.xml"

def interpretStatusCode(httpCode):
    return requests.status_codes._codes[httpCode][0]


def getStatusCode(url):
    """ This function retreives the status code of a website by requesting
        HEAD data from the host. This means that it only requests the headers.
        If the host cannot be reached or something else goes wrong, it returns
        None instead.
    """
    try:
        req = rq.Request(url, headers={"User-Agent": "Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11"}, method="HEAD")
        conn = rq.urlopen(req)
        return conn.getcode()
    except Exception as e:
        if e.code == 405:
            try:
                conn = rq.urlopen(url)
                return conn.getcode()
            except Exception as e:
                return None


def retreiveXML(url):
    code = getStatusCode(url)
    if str(code)[0] == "2":
        xml_string = requests.get(url).content
        xml_root = ET.fromstring(xml_string)
        return xml_root
    else:
        return None




root = retreiveXML(mp_xml_url)
tree = ET.ElementTree(root)
for mp in root:
    name = mp.find("PersonOfficialFirstName").text
    surname = mp.find("PersonOfficialLastName").text
    name = "-".join([name,surname])
    vote_record_url = "http://www.ourcommons.ca/Parliamentarians/en/members/" + name + "/ExportVotes?output=XML"
    member_voting_record = ET.SubElement(mp, "MemberVotingRecord")
    voting_record = ET.SubElement(member_voting_record,"VotingRecordXML")
    voting_events = ET.SubElement(member_voting_record, "VotingEvents")
    voting_record.text = vote_record_url
    vote_record_root = retreiveXML(vote_record_url)
    for vote in vote_record_root:
        try:
            vote.remove(vote.find("PersonOfficialFirstName"))
            vote.remove(vote.find("PersonaOfficialLastName"))
            vote.remove(vote.find("PersonShortHonorific"))
            vote.remove(vote.find("ConstituencyName"))
            vote.remove(vote.find("ConstituencyProvinceTerritoryName"))
        except:
            pass
        voting_events.append(vote)
        
            
tree.write(output_file, encoding="UTF-8")
