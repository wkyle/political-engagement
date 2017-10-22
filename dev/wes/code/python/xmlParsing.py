#!/usr/bin/python3

import xml.etree.ElementTree as et
import os, re, time
from tools import *
from bs4 import BeautifulSoup
import urllib.request as request
from numpy import *
import matplotlib.pyplot as plt
from scipy import stats


rootDir = '/home/wes/Personal/law/toolkit/databaseXML/bills'
xmlBaseUrl = 'http://www.parl.gc.ca/LegisInfo/BillDetails.aspx?Language=E&Mode=1&billId='
pubErrorsLogPath = '/home/wes/Personal/law/toolkit/publication_error_log.txt'

regex = re.compile(r"(\b(?:(?!Act\b|The |An |Criminal Code[,.;:)(]{0,1} |This |Those |These |That |Every |No Act |Part |Section |Schedule |Clause |Subclause |Division |Review of |Summary of |Purpose[s]* of |Amendment[s]{0,1} to |Consequential |Enactment of |References |[A-Z]{1} |[IiVvXx]{1,3} )){1}(?:(?:[A-Z][a-z0-9-]*–*'*’*s*,* *){1}(?:(?!Act\b)[A-Z][a-z0-9-]*–*'*’*s*,* *|o[nf] |[0-9]{4} |to |in |(?<!Act\s)and |of |on |to |the |[A-Z]{1}-[0-9]{1,3} |\([A-Za-z0-9\s]+\) )*(?:Act\b)(?:(?:, | )[0-9]{4}){0,1})|Criminal Code|Customs Tariff|Marine Mammal Regulations)")



def make_my_db():

    newBillsRoot = et.Element('bills')
    trees = get_bill_xml(rootDir)
    roots = [tree.getroot() for tree in trees]
    c=0
    pubErrors = []
    for root in roots:
        try:
            introDate = root.find('BillIntroducedDate').text
            introDate = {'day' : introDate[8:10], 
                    'month' : introDate[5:7], 
                    'year' : introDate[:4]}
        except:
            introDate = {'day' : '', 
                    'month' : '', 
                    'year' : ''}

        try:
            session = root.find('ParliamentSession')
            session = session.attrib['parliamentNumber'] + '-' + session.attrib['sessionNumber']
        except:
            session = ''

        try:
            number = root.find('BillNumber')
            number = number.attrib['prefix'] + '-' + number.attrib['number']
        except:
            number = ''

        try:
            title = root.find('BillTitle')
            title = title[0].text
        except:
            title = ''


        try:
            shortTitle = root.find('ShortTitle')
            shortTitle = shortTitle[0].text
        except:
            shortTitle = ''

        try:
            billId = root.attrib['id']
        except:
            billId = ''

        try:
            sponsor = root.find('SponsorAffiliation/Person/FullName')
            sponsor = sponsor.text
        except:
            sponsor = ''

        try:
            billType = root.find('BillType')
            billType = billType[0].text
        except:
            billType = ''

        try:
            progress = root.find('Events/LastMajorStageEvent/Event/Status')
            progress = progress[0].text
        except:
            progress = ''

        try:
            latestPublication = root.findall('Publications/Publication/PublicationFiles/PublicationFile')
            latestPublication = latestPublication[-2].attrib['relativePath']
            latestPublication = get_full_text_url('http://www.parl.gc.ca' + latestPublication)
        except Exception as e:
            latestPublication = ''
            pubErrors.append('Latest publication error: ' + str(len(pubErrors) + 1) + 
                             '\nTitle: ' + title + 
                             '\nBill ID: ' + billId + 
                             '\nSession: ' + session + 
                             '\nBill Number: ' + number + 
                             '\nDate Introduced: ' + introDate['day'] + '/' + 
                             introDate['month'] + '/' + introDate['year'] + '\n\n')

        try:
            xmlPath = rootDir + '/' + billId + '/' + session + '-' + billId + '.xml'
        except:
            xmlPath = ''

        try:
            xmlUrl = xmlBaseUrl + billId + '&download=xml'
        except:
            xmlUrl = ''

        a = BillXml(newBillsRoot, billId, 
                    title, shortTitle, 
                    sponsor, introDate, 
                    session, number, billType, 
                    progress, latestPublication, xmlUrl, xmlPath).getBill()
        c+=1
        print(c)

    a = et.ElementTree(a)
    a.write('/home/wes/Personal/law/toolkit/bill_database.xml', short_empty_elements=True)

    with open(pubErrorsLogPath, 'w') as f:
        [f.write(i) for i in pubErrors]





def make_bill_sets():

    tree = get_my_db('/home/wes/Personal/law/toolkit/billDatabase.xml')
    bills = tree.getroot()
    num = len(bills)
    c = 1
    for bill in bills:
        pathToText = bill[8].text
        if pathToText:
            try:
                filename = '/home/wes/Personal/law/toolkit/databaseXML/bills/' + \
                          bill.attrib['id'] + '/' + bill.attrib['id'] + 'TEXT.txt'
                print(filename)
                text = return_bill_text('http://www.parl.gc.ca' + pathToText)
                with open(filename, "w") as f:
                    f.write(text)
            except Exception as e:
                print('failed ',bill.attrib['id'], e)
                continue
            '''
            ref = list(set(regex.findall(text)))
            ref = [' '.join(i.split()) for i in ref if i]
            ref = list(set(ref))
            '''
            print('\n\n=============Bill ' + str(c) + '/' + str(num) + '=============\n')
            '''
            [print(i) for i in ref]
            billRefs = et.Element('billsAmended')
            if ref:
                for item in ref:
                    newItem = et.SubElement(billRefs, 'referencedBill')
                    newItem.text = item
            bill.append(billRefs)
            '''
        c += 1
    #tree = et.ElementTree(bills)
    #tree.write('/home/wes/Personal/law/toolkit/amended_bill_database.xml', short_empty_elements=True)




def get_assented_bills():
    tree = get_my_db('/home/wes/Personal/law/toolkit/amended_bill_database.xml')
    bills = tree.getroot()
    ls = []
    for bill in bills:
        idNum = bill.attrib['id']
        if str(bill[7].text).lower() == 'royal assent':
            ls.append([idNum, bill[4].text, bill[5].text])
    return ls

def print_needed(needed):
    tree = get_my_db('/home/wes/Personal/law/toolkit/amended_bill_database.xml')
    bills = tree.getroot()
    for bill in bills:
        if bill.attrib['id'] in needed and 'Appropriation Act No.' not in str(bill[1].text):
            print(bill.attrib['id'], bill[4].text, bill[5].text)


def make_assented_database(lst, filePath):
    tree = get_my_db('/home/wes/Personal/law/toolkit/billDatabase.xml')
    bills = tree.getroot()
    newRoot = et.Element('bills')
    c = 0
    for bill in bills:
        if bill.attrib['id'] in lst and 'Appropriation Act No.' not in str(bill[1].text):
            textFilePath = '/home/wes/Personal/law/toolkit/databaseXML/bills/' + \
                           bill.attrib['id'] + '/' + bill.attrib['id'] + 'TEXT.txt'
            with open(textFilePath, 'r') as f:
                text = f.read().replace('\n', ' ')
            text = ' '.join(text.split())
            ref = list(set(re.findall(regex, text)))
            ref = [' '.join(i.split()) for i in ref if i]
            ref = list(set(ref))
            c+=1
            print('\n\n=============Bill ' + str(bill.attrib['id']) + ' | ' + str(c) + '=============\n')
            #[print(i) for i in ref]
            billRefs = et.Element('referencedBills')
            for item in ref:
                newItem = et.SubElement(billRefs, 'referencedBill')
                newItem.text = item
            bill.append(billRefs)
            newRoot.append(bill)            
            
    tree = et.ElementTree(newRoot)
    tree.write(filePath, short_empty_elements=True)


def get_refd_bills(filePath):
    tree = get_my_db(filePath)
    bills = tree.getroot()
    fullList = []
    entries = []
    for bill in bills:
        lst = [i.text for i in bill[11]]
        lst.sort()
        idn = bill.attrib['id']
        try:
            title = bill[1].text
        except:
            title = bill[0].text
        sess = bill[4].text
        num = bill[5].text
        stringItem = '\n\n\nBill: ' + str(num) + ' from session ' + str(sess) + '\n' + \
                     'Title: ' + str(title) + '\n' + \
                     'Bill ID: ' + str(idn) + '\n\n'
        for i in lst:
            stringItem += str(i) + '\n'

        fullList.extend(lst)
        entries.append(stringItem)
    fullList = list(set(fullList))
    with open('/home/wes/Personal/law/toolkit/refd_in_network.txt', 'w') as f:
        [f.write(i) for i in entries]
    return fullList


def check_ass_bill_stats(kwarg):
    tree = get_my_db('/home/wes/Personal/law/toolkit/assentedDatabase.xml')
    bills = tree.getroot()
    if kwarg == 'date':
        for bill in bills:
            errmsg = kwarg + ' not found... \nCheck http://www.parl.gc.ca/LegisInfo/BillDetails.aspx?Language=E&Mode=1&billId=' + bill.attrib['id'] + '\n'
            try:
                a = bill[3].attrib
                if not a:
                    print(errmsg)
            except:
                print(errmsg)
    elif kwarg == 'sponsor':
        for bill in bills:
            errmsg = kwarg + ' not found... \nCheck http://www.parl.gc.ca/LegisInfo/BillDetails.aspx?Language=E&Mode=1&billId=' + bill.attrib['id'] + '\n'
            try:
                a = bill[2].text
                if not a:
                    print(errmsg)
            except:
                print(errmsg)
    elif kwarg == 'title':
        for bill in bills:
            errmsg = kwarg + ' not found... \nCheck http://www.parl.gc.ca/LegisInfo/BillDetails.aspx?Language=E&Mode=1&billId=' + bill.attrib['id'] + '\n'
            try:
                a = bill[0].text
                if not a:
                    print(errmsg)
            except:
                print(errmsg)
    elif kwarg == 'short title':
        for bill in bills:
            errmsg = kwarg + ' not found... \nCheck http://www.parl.gc.ca/LegisInfo/BillDetails.aspx?Language=E&Mode=1&billId=' + bill.attrib['id'] + '\n'
            try:
                a = bill[1].text
                if not a:
                    print(errmsg)
            except:
                print(errmsg)
    elif kwarg == 'session':
        for bill in bills:
            errmsg = kwarg + ' not found... \nCheck http://www.parl.gc.ca/LegisInfo/BillDetails.aspx?Language=E&Mode=1&billId=' + bill.attrib['id'] + '\n'
            try:
                a = bill[4].text
                if not a:
                    print(errmsg)
            except:
                print(errmsg)
    elif kwarg == 'number':
        for bill in bills:
            errmsg = kwarg + ' not found... \nCheck http://www.parl.gc.ca/LegisInfo/BillDetails.aspx?Language=E&Mode=1&billId=' + bill.attrib['id'] + '\n'
            try:
                a = bill[5].text
                if not a:
                    print(errmsg)
            except:
                print(errmsg)
    elif kwarg == 'type':
        for bill in bills:
            errmsg = kwarg + ' not found... \nCheck http://www.parl.gc.ca/LegisInfo/BillDetails.aspx?Language=E&Mode=1&billId=' + bill.attrib['id'] + '\n'
            try:
                a = bill[6].text
                if not a:
                    print(errmsg)
            except:
                print(errmsg)
    elif kwarg == 'progress':
        for bill in bills:
            errmsg = kwarg + ' not found... \nCheck http://www.parl.gc.ca/LegisInfo/BillDetails.aspx?Language=E&Mode=1&billId=' + bill.attrib['id'] + '\n'
            try:
                a = bill[7].text
                if not a:
                    print(errmsg)
            except:
                print(errmsg)
    elif kwarg == 'refd bills':
        for bill in bills:
            errmsg = kwarg + ' not found... \nCheck http://www.parl.gc.ca/LegisInfo/BillDetails.aspx?Language=E&Mode=1&billId=' + bill.attrib['id'] + '\n'
            try:
                a = bill[11]
            except:
                print(errmsg)
    else:
        pass
    print('\n\n')

#figure out which assented bills still have no text
'''
assented = get_assented_bills()
noText = detect_no_text('/home/wes/Personal/law/toolkit/databaseXML/bills/')
assentID = [i[0] for i in assented]
needed = [i for i in noText if i in assentID]
print_needed(needed)
'''


#print how many nodes I've got
'''
print(len(assented))
'''


#make xml of only the 451 assented bills
'''
assented = get_assented_bills()
assented = [i[0] for i in assented]
make_assented_database(assented, '/home/wes/Personal/law/toolkit/assentedDatabase.xml')
'''


#compile list of (unique) referenced bills
'''
lst = get_refd_bills('/home/wes/Personal/law/toolkit/assentedDatabase.xml')
'''
#save list to text  file
'''
with open('/home/wes/Personal/law/toolkit/refd_in_network.txt', 'w') as f:
    f.write('#this is a list of bill names referenced in the network of assented bills\n#\n')
    [f.write(i + '\n') for i in lst]
'''


#check my assented database to make sure every bill has data
'''
check_ass_bill_stats('title')
'''
#a bunch of bills have no short title. Oh well. Not much I can do.


#lets look again at the results of my text parsing to see
#if I can clean up my regex
'''
tree = get_my_db('/home/wes/Personal/law/toolkit/assentedDatabase.xml')
bills = tree.getroot()
l = []
num = list(range(0,100))
freq = [0]*len(num)
for bill in bills:
    billid = bill.attrib['id']
    title = bill[0].text
    short_title = bill[1].text
    texturl = bill[8].text
    textpath = bill[12].text
    with open(textpath, 'r') as f:
        text = f.read()
    refs = list(set(regex.findall(text)))
    refs = [' '.join(i.split()) for i in refs if i]
    refs = list(set(refs))
    if short_title in refs:
        refs.remove(short_title)
    for i,item in enumerate(num):
        if len(refs) == item:
            freq[i] += 1
    #print(billid, title, '\n')
    #print('http://www.parl.gc.ca' + texturl +'\n\n')
    #[print(i) for i in refs]
    #print('\n\n\n')
    l.extend(refs)
#seen = set([x for x in l if l.count(x) > 1])
#n = [l.count(i) for i in seen]
#seen = list(seen)
#n, seen = zip(*sorted(zip(n, seen)))
#[print(i, j) for i,j in zip(seen,n)]

x = [i for i in num[1:24]]
y = [i/sum(freq) for i in freq[1:24]]

p = stats.linregress(x,y)
print('CRITICAL EXPONENT: ',p[0])
[print(i,j) for i,j in zip(num,freq)]
plt.scatter(x,y)
plt.savefig('/home/wes/Personal/law/toolkit/degree_dist.png', dpi=300)
'''


#I want to add some entries to my assented database for textPath
'''
tree = get_my_db('/home/wes/Personal/law/toolkit/billDatabase.xml')
bills = tree.getroot()
for bill in bills:
    textPath = '/home/wes/Personal/law/toolkit/databaseXML/bills/' + \
               str(bill.attrib['id']) + '/' + str(bill.attrib['id']) + 'TEXT.txt'
    newItem = et.SubElement(bill, 'textPath')
    newItem.text = textPath
tree.write('/home/wes/Personal/law/toolkit/billDatabase.xml', short_empty_elements=True)
'''


#Let's look at how long each text file is.
'''
mk_unique_words_plot()
'''


#I can look through all the texts and search for keywords
'''
tree = get_my_db('/home/wes/Personal/law/toolkit/assentedDatabase.xml')
bills = tree.getroot()
w = ['minimum wage', 'wage', 'low income', 'full-time', 'full time', 'part-time', 'part time']
for bill in bills:
    path = bill[12].text
    with open(path, 'r') as f:
        s = f.read()
    s = s.split()
    l = [i for i in s if i in w]
    if len(l) > 0:
        print(bill.attrib['id'], bill[0].text,'\n')
        print('http://www.parl.gc.ca' + bill[8].text + '\n')
        [print(i) for i in l]
        print('\n\n\n')
'''



tree = get_my_db('/home/wes/Personal/law/toolkit/billDatabase.xml')
bills = tree.getroot()

tree1 = get_my_db('/home/wes/Personal/law/toolkit/assentedDatabase.xml')
bills1 = tree1.getroot()

year = [i for i in range(2001,2016)]
num = [0]*len(year)
num_ass = [0]*len(year)

for bill in bills:
    y = int(bill[3].attrib['year'])
    for i, item in enumerate(year):
        if y == item:
            num[i] += 1

for bill in bills1:
    y = int(bill[3].attrib['year'])
    for i, item in enumerate(year):
        if y == item:
            num_ass[i] += 1



#plt.plot(year,num)
plt.plot(year,num_ass)
plt.show()
