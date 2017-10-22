#!/usr/bin/python3

import urllib.request as request
import os, re, html2text
import xml.etree.ElementTree as et
from bs4 import BeautifulSoup
from bs4.element import Comment, NavigableString
import matplotlib.pyplot as plt
from numpy import *
from scipy.signal import savgol_filter

def uniquefy_list(l1, l2):
    if isinstance(l1, list) and isinstance(l2, list):
        return list(set(l2).difference(l1))
    else:
        return None


def mk_one_line(s):
    return s.replace('\n', '')


def clean_html_url(url):

    """
    Replaces html standard for special characters with regular
    text .
    input: string or list of strings
    returns: string or list of strings, whichever was given
    """

    if type(url) is str:
        url = url.replace("&amp;", "&")
        url = url.replace("%3d", "=")
        url = url.replace("%2f", "/")
        url = url.replace("%3f", "?")
        url = url.replace("%26", "&")        
        return url
    elif type(url) is list:
        for item in url:
            if not type(item) == str:
                return None
            url[url.index(item)] = item.replace("&amp;", "&")
            url[url.index(item)] = item.replace("%3d", "=")
            url[url.index(item)] = item.replace("%2f", "/")
            url[url.index(item)] = item.replace("%3f", "?")
            url[url.index(item)] = item.replace("%26", "&")
        return url
    else:
        return None



def has_connection(reference):
    try:
        request.urlopen(reference, timeout=1)
        return True
    except request.URLError:
        return False



def write_to_file(path, string):
    
    with open(path, 'w') as f:
        f.write(string)



def remove_tags(text):
    TAG_RE = re.compile(r'<[^>]+>')
    if isinstance(text,str):
        return TAG_RE.sub('', text)
    else:
        return None



def get_bill_xml(rootDir):
    files = []
    fileTrees = []
    for (dirpath, dirnames, filenames) in os.walk(rootDir):
        if filenames and filenames[0].endswith('xml'):
            files.append(os.path.join(dirpath, filenames[0]))
    for aFile in files:
        fileTrees.append(et.parse(aFile))
    return fileTrees


def detect_no_text(rootDir):
    dirs = []
    for (dirpath, dirnames, filenames) in os.walk(rootDir):
        if len(filenames) < 2:
            billId = dirpath.split("/")[-1]
            dirs.append(billId)
    return dirs


# Identify the start comment
def isBeginText(text):
    return (isinstance(text, Comment) and
            text.strip().startswith("Publication Content."))



# Identify the end comment
def isEndText(text):
    return (isinstance(text, Comment) and
            text.strip().startswith("Publication Sidebar."))



def return_bill_text(url):
    s = ''
    userAgent = {'User-Agent': \
                 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) \
                 Chrome/35.0.1916.47 Safari/537.36'}
    req = request.Request(url, data = None, headers = userAgent)
    page = request.urlopen(req).read().decode('utf-8')
    
    soup = BeautifulSoup(page)
    start = " Publication Content. "
    end = " Publication Sidebar. "

    comments = soup.findAll(text=lambda text:isinstance(text, Comment))
    [cmt.extract() for cmt in comments if cmt.string != start and cmt.string != end]

    # Step 1: find the beginning and ending markers
    node_start = [ cmt for cmt in comments if cmt.string == start ][0]
    node_end = [ cmt for cmt in comments if cmt.string == end ][0]

    # Step 2, subtract the 2nd list of strings from the first
    all_text = node_start.find_all_next(text=True)
    all_after_text = node_end.find_all_next(text=True)

    subset = all_text[:-(len(all_after_text) + 1)]
    for i in subset:
        s+=i

    #s = html2text.html2text(page).replace("_", "")
    return s



def get_full_text_url(url):
    userAgent = {'User-Agent': \
                 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) \
                 Chrome/35.0.1916.47 Safari/537.36'}
    req = request.Request(url, data = None, headers = userAgent)
    page = request.urlopen(req).read().decode('utf-8')
    soup = BeautifulSoup(page)
    regex = re.compile('(?<=[rR][eE][fF][eE][rR][eE][rR][uU][rR][lL]=)(.+)')
    href = ''
    for tag in soup.find_all('a'):
        if 'Click here for the entire document' == str(tag.string):
            if str(tag.string).endswith('.PDF') or str(tag.string).endswith('.pdf'):
                href = ''
                break
            else:
                href = str(tag.attrs['href'])
                break
        elif 'class' in tag.attrs:
            
            if 'lnkID0AGC0HC' in tag.attrs['id']:
                if str(tag.attrs['href']).endswith('.PDF') or str(tag.attrs['href']).endswith('.pdf'):
                    href = ''
                    break
                else:
                    href = str(tag.attrs['href'])
                    break
    try:
        match = regex.findall(href)[0]
    except:
        match = ''
    if match:
        match = clean_html_url(match)
        return match
    else:
        return url

class BillXml():
    
    '''
    docstring is a docstring
    '''
    
    def __init__(self, root, billId, 
                 title = '', shortTitle = '', 
                 sponsor = '', introDate = {'day' : '', 'month' : '', 'year' : ''}, 
                 session = '', number = '', 
                 billType = '', progress = '', 
                 textUrl = '', xmlUrl = '', 
                 xmlPath = None):
        
        self.root = root
        self.billId = et.SubElement(self.root, 'bill', {'id' : billId})
        self.title = et.SubElement(self.billId, 'title')
        self.title.text = title
        self.shortTitle = et.SubElement(self.billId, 'shortTitle')
        self.shortTitle.text = shortTitle
        self.sponsor = et.SubElement(self.billId, 'sponsor')
        self.sponsor.text = sponsor
        self.introDate = et.SubElement(self.billId, 'introDate', introDate)
        self.session = et.SubElement(self.billId, 'session')
        self.session.text = session
        self.number = et.SubElement(self.billId, 'number')
        self.number.text = number
        self.billType = et.SubElement(self.billId, 'billType')
        self.billType.text = billType
        self.progress = et.SubElement(self.billId, 'progress')
        self.progress.text = progress
        self.textUrl = et.SubElement(self.billId, 'textUrl')
        self.textUrl.text = textUrl
        self.xmlUrl = et.SubElement(self.billId, 'xmlUrl')
        self.xmlUrl.text = xmlUrl
        self.xmlPath = et.SubElement(self.billId, 'xmlPath')
        self.xmlPath.text = xmlPath

    def getBill(self):
        return self.root


def get_my_db(pathToFile):
    root = et.parse(pathToFile)
    return root


def mk_unique_words_plot():
    with open('/home/wes/Personal/reference/english-dict/dictionary.txt') as f:
        dic = f.read().splitlines()
    tree = get_my_db('/home/wes/Personal/law/toolkit/assentedDatabase.xml')
    bills = tree.getroot()
    date = []
    length = []
    c = 0
    for bill in bills:
        path = bill.find('textPath').text
        docID = bill.attrib['id']
        t = float(bill.find('introDate').attrib['year']) + \
            float(bill.find('introDate').attrib['month'])/12. + \
            float(bill.find('introDate').attrib['day'])/365.25
        date.append(t)
        with open(path, 'r') as f:
            words = f.read().split()
            print('checking dictionary: ', c)
            #s = list(set(words) & set(dic))
            s = [i for i in words if i in dic]
            c += 1
            l = len(s)
            length.append(l)

    length = log10(length)
    xy = [i for i in sorted(zip(date,length))]
    date = [i[0] for i in xy]
    length = [i[1] for i in xy]

    smooth = savgol_filter(length, 125, 3)

    plt.scatter(date,length, label='bills')
    plt.plot(date, smooth, c='r', label='smooth trend')
    plt.ylabel('# written English words ($log_{10}(N)$)')
    plt.xlabel('year')
    plt.title('Lengths of Canadian Bills to Receive Royal Assent')
    #plt.ylim()
    plt.legend(loc='lower right')
    plt.savefig('bill_length_vs_pub_year.pdf', dpi=400)


def filter_db(root, kw='ceremonial bills'):
    if kw == 'ceremonial bills':
        regex1 = re.compile("(granting to her majesty certain sums of money)")
        for bill in root:
            if re.search(regex1, bill[0].text.lower()):
                root.remove(bill)
                continue
            if bill[5].text == 'C-1':
                root.remove(bill)
                continue
        return root
    elif kw == 'early sessions':
        blacklist = ['35', '36']
        for bill in root:
            if bill[4].text[0:2] in blacklist:
                root.remove(bill)
        return root
