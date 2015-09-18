#!/usr/bin/env python

import sys
import copy

from read_ninfo import ReadNinfo

class MakeNinfo(ReadNinfo):
    def __init__(self):
        ReadNinfo.__init__(self)

    def setPara(self,epsilon=0.1):
        for i,ilist in enumerate(self.data_contact):
            if ilist[1]!=ilist[2]:
                self.data["contact"][i][10]=float(ilist[10])*epsilon

                
    def setDefualt(self):
        self.data_contact=copy.deepcopy(self.data["contact"])

if __name__=="__main__":
    tclass=MakeNinfo()
    tclass.read(sys.argv[1])
    tclass.setDefualt()
    for i in range(1,101):
        tclass.setPara(0.01*i)
        filename="emc%03d.ninfo" % i 
        tclass.write(filename)
