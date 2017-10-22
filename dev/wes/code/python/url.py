#!/usr/bin/python3
from PySide import QtCore, QtGui
import re, time, os
import urllib.request as request
from bs4 import BeautifulSoup
import xml.etree.ElementTree as et
import tools

xmlDirectory = '/home/wes/Personal/law/toolkit/databaseXML/'
baseUrl = 'http://www.parl.gc.ca/LegisInfo/'
sessionUrl = 'Home.aspx?Language=E&Mode=1&ParliamentSession='
billDetailsUrl = 'BillDetails.aspx?Language=E&Mode=1&billId='



class XmlDownloadWorker(QtCore.QThread):

    updateProgress = QtCore.Signal(int)

    def __init__(self, sessionXmlUrl, pathToFile):
        QtCore.QThread.__init__(self)
        self.sessionXmlUrl = sessionXmlUrl
        self.pathToFile = pathToFile
        
    def run(self):
        request.urlretrieve(self.sessionXmlUrl, \
                            self.pathToFile, \
                            reporthook=self.hook)

    def hook(self, sofar, blocksize, totalsize):
    
        if sofar*blocksize >= totalsize:
            print(100)
            self.updateProgress.emit(100)
        else:
            self.updateProgress.emit(100*sofar*blocksize/totalsize)
            print(int(100*sofar*blocksize/totalsize))


class LegisBillCompiler():
    
    def __init__(self, baseUrl, sessionUrl, xmlDirectory):

        self.xmlDirectory = xmlDirectory
        self.baseUrl = baseUrl
        self.sessionUrl = sessionUrl
        self.userAgent = {'User-Agent': \
                          'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) Chrome/35.0.1916.47 Safari/537.36'}
        self.regexChkPage = re.compile(r'Sorry, your query yielded no results.')


    def get_listings_xml(self, max_session):

        for i in range(35,max_session+1):
            for j in range(1,5):
                session = str(i) + '-' + str(j)

                url = self.baseUrl + \
                      self.sessionUrl + \
                      session
                req = request.Request(url, data = None, headers = self.userAgent)
                page = request.urlopen(req)
                print('Checking session ' + session)
                html = page.read().decode('utf-8')

                if self.regexChkPage.search(html):
                    break

                downloadUrl = url + '&download=xml'
                print('Downloading: ', xmlDirectory + session + 'XML.xml')
                request.urlretrieve(downloadUrl, \
                                    self.xmlDirectory + session + 'XML.xml', \
                                    reporthook=self.hook)


    def hook(self, sofar,blocksize,totalsize):
    
        if sofar*blocksize >= totalsize:
            print('Percent: 100')
        else:
            print('Percent: {:.0f}'.format(100*sofar*blocksize/totalsize))


class LegisBill():
    
    def __init__(self, name, billId, session):
        self.title = name
        self.billId = billId
        self.session = session
        self.relativeUrl = None
        self.docId = None
        self.text = None
        self.xmlDetails = None
        self.sponsor = None
        self.primeMinister = None

    def get_title(self):
        return self.title

    def get_billId(self):
        return self.billId

    def get_session(self):
        return self.session

    def get_details(self):
        self.detailsUrl = baseUrl + billDetailsUrl + self.billId
        self.download_xml()

    def download_xml(self):
        downloadUrl = self.detailsUrl + '&download=xml'
        print('Getting bill details XML file for bill ID ', self.billId)
        newDir = xmlDirectory + 'bills/' + self.billId
        print(newDir)
        try:
            os.mkdir(newDir)
        except:
            pass
        request.urlretrieve(downloadUrl, \
                                    newDir + '/' + self.session + '-' + self.billId + '.xml')#, \
                                    #reporthook=self.hook)


    def import_xml_from_file(self):
        pass




class XmlFileLoader():
    
    def __init__(self, rootDir):
        self.rootDir = rootDir
        self.isDir = self._check_exist()

    def _check_exist(self):
        os.path.isdir(self.rootDir)

    def get_bill_xml(self):
        files = []
        fileTrees = []
        for (dirpath, dirnames, filenames) in os.walk(self.rootDir):
            if filenames:
                files.append(os.path.join(dirpath, filenames[0]))
        for aFile in files:
            fileTrees.append(et.parse(aFile))
        return fileTrees




#comp = LegisBillCompiler(baseUrl, sessionUrl, xmlDirectory)
#comp.get_listings_xml(43)

'''
bills = populate_bills(xmlDirectory)
for bill in bills[1840:]:
    bill.get_details()
'''


b = XmlFileLoader('/home/wes/Personal/law/toolkit/databaseXML/bills')
l = b.get_bill_xml()
[print(i.getroot()[1].attrib) for i in l]

