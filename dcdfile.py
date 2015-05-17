#! /usr/bin/env python
# -*- coding: utf-8 -*-
#editor: ono

import argparse
import struct
import numpy as np


class DcdHeader:
    def __init__(self):
        self.nset = None
        self.istart = None
        self.nstep_save = None
        self.nstep = None
        self.nunit_real = None
        self.delta = None
        self.title = None
        self.tempk = None
        self.lunit2mp = None
        self.nmp_real = None


class DcdFile:
    def __init__(self):
        self.dcdfile=False
        self.dcdheader=DcdHeader()

    def main(self):
        self._initArg()
        self.read(self.dcdfile)

    
    def read(self,infile):
        self.dcdfile=open(infile,"rb")
        self._readHeader()
        

    def writeToMovie(self,outfile):
        pass


    def _initArg(self):
        parser = argparse.ArgumentParser(description='This scripts defined dcd-style in Cafemol.')
        parser.add_argument('inputfile',nargs='?',help="input-file[.dcd]")
        parser.add_argument('-o','--output',nargs='?',help="output-file[.json]",default='out.json')
        
        self.dcdfile=parser.parse_args().inputfile

    def _readHeader(self):
        self.dcdfile.seek(4)
        print struct.unpack('4s',self.dcdfile.read(4))
        
        
        
    def test(self):
        self.read("./test/inp/2gxa.dcd")

if __name__=="__main__":
    test=DcdFile()
    test.test()
