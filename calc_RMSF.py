#!/bin/usr/env python
# coding: utf-8
# editor: ono

import prody
import argparse


class CalcRMSF:
    def __init__(self):
        self.dcdfile=""


    def main(self):
        self._initArg()
        self.read(self.dcdfile)


    def read(self,inputfile):
        self.dcddata=prody.DCDFile('./test/inp/2gxa.dcd',mode='rb')
        

    def _initArg(self):
        parser = argparse.ArgumentParser(description='This scripts calculate RMSF from dcd-file.')
        parser.add_argument('inputfile',nargs='?',help="input-file[.dcd]")
        
        self.dcdfile=parser.parse_args().inputfile

        
    def test(self):
        self.read("./test/inp/2gxa.dcd")


if __name__=="__main__":
    test=CalcRMSF()
    #test.test()
    test.main()

