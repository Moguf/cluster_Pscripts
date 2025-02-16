#!/usr/bin/env python2.7
import re

import numpy as np

from my_error import MyError

class ReadTs:
    def __init__(self):
        self.data={}
        self.filename=""

    def main(self,filename):
        self.read(filename)
        print self.data

    def read(self,filename):
        self.filename=filename
        rfile=open(filename,"r")
        ts_variety=[]
        
        for iline in rfile.readlines():
            if re.search("^#(all|unit|[0-9].)",iline):
                #read #unit #all #1 #2 ... #10 ...
                ilist=iline.strip().split()
                key=ilist[0][1:]
                #key = all unit 1 2 3 ...

                if ilist[1]=="0":
                    #initialize dictonary data
                    if '**********' in ilist:
                        raise MyError("CAUTION!!!!:","Enerey is INFINIY!!!Please chcek your Initial structure!!!")

                    self.data[key]=[[float(i) for i in ilist[1:]]]
                    continue
                    
                if key=="unit":
                    self.data[key]=ilist[1:]
                    continue
                    
                #read data
                self.data[key].append([float(i) for i in ilist[1:]])
        self._transposeData()

    def _transposeData(self):
        for key in self.data:
            if key=="unit":
                continue
            self.data[key]=np.array(self.data[key])
        self.data['all']=self.data['all'].T


if __name__=="__main__":
    test=ReadTs()
    test.main("./test/inp/test.ts")



    
