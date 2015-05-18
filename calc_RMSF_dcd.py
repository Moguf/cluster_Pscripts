#!/bin/usr/env python
# coding: utf-8
# editor: ono
import argparse

import numpy as np
import scipy.spatial.distance as dist

import dcdfile



class CalcRMSF:
    def __init__(self):
        self.dcdfile=""
        self.npdata=[]


    def main(self):
        self._initArg()
        self.read(self.dcdfile,1000)
        self.calcRMSF()


    def read(self,inputfile,start=0):
        dcd=dcdfile.DcdFile()
        dcd.read(inputfile)
        self.npdata=np.array(dcd[start:])
        dcd.close()
        

    def doPy(self):
        npave=np.average(self.npdata,axis=0)
        print dist.cdist(npave,self.npdata[1])[0][0]
    
    def doC(self):
        pass
        


    def _initArg(self):
        parser = argparse.ArgumentParser(description='This scripts calculate RMSF from dcd-file.')
        parser.add_argument('inputfile',nargs='?',help="input-file[.dcd]")
        
        self.dcdfile=parser.parse_args().inputfile


    def test(self):
        self.read("./test/inp/test.dcd",9000)
        self.doPy()
        
        
if __name__=="__main__":
    test=CalcRMSF()
    test.test()
    #test.main()

