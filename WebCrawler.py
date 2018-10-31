
import FileManager
from Spider import Spider




class Crawler :


    def __init__(self):
        self.crawlieCount = 100

    def initializeResultFile(self):
        #entry = "PX;Publisher;Domain;PX ID;EPB ID;Pub ID Status;PXSeller;EPB ID Status;EPBSeller;Requests;Revenue"
        FileManager.CreateResultFile(FileManager)
        #FileManager.WriteToResultFile(FileManager,entry, "w")

    def StartSpider(self,name):
        spider = Spider(name)
        spider.start()


if __name__ == '__main__':

    CrawlerHead = Crawler()

    print("Choosing file..")
    FileManager.ChooseFile(FileManager)
    print("Reading file..")
    FileManager.ReadFile(FileManager)

    if(FileManager.path != ""):

        CrawlerHead.initializeResultFile()

        print(FileManager.q.qsize())
        print("")
        for x in range(CrawlerHead.crawlieCount):
            CrawlerHead.StartSpider("Spider" + str(x))
        FileManager.q.join()





