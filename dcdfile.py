#! /usr/bin/env python
# -*- coding: utf-8 -*-
#editor: ono

import argparse
import struct
import os 

import numpy as np

from my_error import MyError


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
        self.lunit2mp = []
        self.nmp_real = None

    def show(self):
        for ikey in self.__dict__.keys():
            print ikey,self.__dict__[ikey]


class DcdFile:
    def __init__(self):
        self.dcdfile=False
        self.blocksize=[]
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
        ### read first line
        b=self._pick_data()
        header=struct.unpack('4s9if10i',b)

        if header[0].strip() != "CORD":
            raise MyError('Input Error:','Inpug file is not dcd-format.')

        self.dcdheader.nset = header[1]
        self.dcdheader.istart = header[2]
        self.dcdheader.nstep_save = header[3]
        self.dcdheader.nstep = header[4]
        self.dcdheader.nunit_real = header[5]
        self.dcdheader.delta = header[10]

        ### read title block
        b=self._pick_data()
        titleblock=struct.unpack('i'+'80s'*(3+self.dcdheader.nunit_real),b)
        self.dcdheader.title=titleblock[1]+titleblock[2]
        self.dcdheader.tempk=float(titleblock[3])

        for i in xrange(self.dcdheader.nunit_real) :
            self.dcdheader.lunit2mp.append(int(titleblock[i + 4]))

        ### 
        b = self._pick_data()
        self.dcdheader.nmp_real = struct.unpack('i', b)[0]

        
    def test(self):
        self.read("./test/inp/2gxa.dcd")

    def read_onestep(self):
        pass

    
    def _pick_data(self):
        num = struct.unpack('i', self.dcdfile.read(4))[0]
        b=self.dcdfile.read(num)
        self.dcdfile.seek(4, os.SEEK_CUR)
        return b
        


if __name__=="__main__":
    test=DcdFile()
    test.test()
