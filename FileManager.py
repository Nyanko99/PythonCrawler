import os
from tkinter.filedialog import askopenfile
from queue import Queue

path = ""
q = Queue()

def ChooseFile(self):
    self.file = askopenfile()
    self.path = self.file.name
    self.path = self.path[:-4]


def ReadFile(self):

    content = self.file.readlines()
    for line in content:
        q.put(line)

def CreateResultFile(self):
    if( os.path.isfile(self.path+"result.csv")):
        os.remove(self.path+"result.csv")

    f = open(self.path+"result.csv","x")


def WriteToResultFile(self, entry, mode):
    #f = open(self.path + "result.csv", mode)
    #f.write(entry + '\n' )
    #print(entry, file = f)

    with open(self.path + "result.csv", mode) as f:
        f.write(entry)
