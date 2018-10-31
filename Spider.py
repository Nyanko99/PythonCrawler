from html.parser import HTMLParser

import FileManager
import threading
import urllib.request
import urllib.error
import contextlib

import sys



class Spider(threading.Thread, HTMLParser):


    #PX ID [0] , PX [1] , Pub ID[2] , Pub name[3], Domain [4], SMI ID [5] , Req [6] , IMP [7] , VTR[8] , Rev[9]
    entry = []
    result = []
    SellerStatusPX = ""
    SellerStatusEPB = ""

    pageContent = []


    def __init__(self, name):
        threading.Thread.__init__(self)
        self.name = name

    def run(self):
        while not FileManager.q.empty():
            self.result = []
            #self.print_Name()
            self.getEntry()
            self.SellerStatusPX = ""
            self.SellerStatusEPB = ""
            print(FileManager.q.qsize())

            self.initEntry()
            #website = self.entry[4]
            website = self.testProtocol(self.entry[4])
            if(self.testWebsite(website)):
                self.searchWebsite(self.convertSite(website))
            else:
                self.addErrorLines("NO URL")

            self.addKPI()
            self.writeToFile(self.result)
            FileManager.q.task_done()


    def print_Name(self):
        print(self.name + " is working on..")

    def getEntry(self):
        entryLine = FileManager.q.get()
        self.entry = entryLine.split(";")

    def initEntry(self):
        self.result.append(self.entry[1])
        self.result.append(self.entry[3])
        self.result.append(self.entry[4])
        self.result.append(self.entry[2])
        self.result.append(self.entry[5])
        #print(self.entry[4] + "\n")

    def convertSite(self,site):
        if(site.endswith('/')):
            site = site[:-1]
        site = site + "/ads.txt"

        return site

    def testProtocol(self, site):
        try:
            httpUrl = "http://" + site.split("//")[1]
            httpsUrl = "https://" + site.split("//")[1]
            if(self.testWebsite(httpUrl)):
                return httpUrl
            elif self.testWebsite(httpsUrl):
                return httpsUrl
            else:
                return site
        except:
            return site

    def testWebsite(self, site):
        try:

            req_headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
            req = urllib.request.Request(site,headers=req_headers)
            f = urllib.request.urlopen(req)
            with contextlib.closing(urllib.request.urlopen(req)) as f:
                return True
        except :

            #print(site)
            #print(sys.exc_info()[0])
            return False


    def searchWebsite(self, site):
        try:

            req_headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
            req = urllib.request.Request(site,headers=req_headers)
            f = urllib.request.urlopen(req)
            adstxt = f.readlines()

            for line in adstxt:
                self.pageContent.append(line.decode(encoding='UTF-8',errors='ignore'))

            PXID = self.findEntry(self.entry[2],0, self.pageContent)
            EPBID = self.findEntry(self.entry[5],1, self.pageContent)

            self.processIDResult(PXID,self.SellerStatusPX)
            self.processIDResult(EPBID, self.SellerStatusEPB)
        except urllib.error.HTTPError as err:
            self.addErrorLines("NO ADS.TXT")
            #print(site)
            #print(sys.exc_info()[0])
        except urllib.error.URLError as err:
            self.addErrorLines("NO ADS.TXT")
            # print(site)
            # print(sys.exc_info()[0])
        except :
            self.addErrorLines("Codec Error")
            print(site)
            print(sys.exc_info()[0])


    def addErrorLines(self,msg):
        self.result.append(msg)
        self.result.append("")
        self.result.append("")
        self.result.append("")

    def addKPI(self):
        if len(self.entry) > 6:
            for x in range(6,len(self.entry)):
                self.result.append(self.entry[x])


    def findEntry(self, ID,SellerStatus, content):
        IDFound = False
        for line in content:
            if"freewheel" in line :
                IDFound = IDFound or ID in line
                if IDFound:
                    if SellerStatus == 0:
                        self.SellerStatusPX = self.checkSellerStatus(line)
                    else:
                        self.SellerStatusEPB = self.checkSellerStatus(line)
        return IDFound

    def checkSellerStatus(self, line):
        if "RESELLER" in line:
            return "RESELLER"
        elif "DIRECT" in line:
            return "DIRECT"
        else:
            return ""

    def processIDResult(self, status, sellerStatus):
        if(status):
            self.result.append("Exists")
        else:
            self.result.append("Missing")
        self.result.append(sellerStatus)

    def writeToFile(self, entry):
        csvResult = self.convertToCSV(entry)
        #print(csvResult)
        FileManager.WriteToResultFile(FileManager,csvResult,"a")


    def convertToCSV(self,entry):
        csvEntry =""
        for line in entry:
            csvEntry += line + ";"
        csvEntry= csvEntry[:-1]
        return csvEntry