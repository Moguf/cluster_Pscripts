#!/bin/usr/env python
# coding: utf-8
# editor: ono
import argparse

import numpy

import dcdfile


class CalcRMSF:
    def __init__(self):
        self.dcdfile=""
        self.all_cordinates=[]

    def main(self):
        self._initArg()
        self.read(self.dcdfile)


    def test(self):
        self.read("./test/inp/test.dcd")
        

    def read(self,inputfile):
        self.dcd=dcdfile.DcdFile()
        self.dcd.read(inputfile)
        print self.dcd[1]


    def readAll(self):
        self.all_cordinates=[]

    def _initArg(self):
        parser = argparse.ArgumentParser(description='This scripts calculate RMSF from dcd-file.')
        parser.add_argument('inputfile',nargs='?',help="input-file[.dcd]")
        
        self.dcdfile=parser.parse_args().inputfile

        
if __name__=="__main__":
    test=CalcRMSF()
    test.test()
    #test.main()

