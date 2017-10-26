#!/usr/bin/python3

import requests
import urllib.request as rq
import xml.etree.ElementTree as ET


mp_xml_url = "http://www.ourcommons.ca/Parliamentarians/en/members/export?output=XML"


def interpret_status_code(httpCode):
    return requests.status_codes._codes[httpCode][0]


def get_status_code(url):
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


def retreive_xml(url):
    xml_string = requests.get(url).content
    xml_root = ET.fromstring(xml_string)
    return xml_root


code = get_status_code(mp_xml_url)
if str(code)[0] == "2":
    xml = retreive_xml(mp_xml_url)
    print(len(xml))
