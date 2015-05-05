#!/usr/bin/env python2.7
import argparse
import sys

import matplotlib.pyplot as plt

from read_ts import ReadTs


class PlotTs(ReadTs):
    def __init__(self):
        ReadTs.__init__(self)
        self.args=[]
        self._initArg()


    def main(self):
        self.read(self.args.inputfile)
        self.transposeData()
        self.plotTs()

        
    def plotTs(self,**args):
        pass

        
    def _initArg(self):
        parser = argparse.ArgumentParser(description='plot ts-data')
        parser.add_argument('inputfile',nargs='?',help="input-file[.ts]")
        parser.add_argument('outtype',type=str,choices=["eps","png","both"],help="ex:output[.eps, .png  ,.png and .eps]")
        parser.add_argument('output',nargs='?',help="ex:[output].png")
        parser.add_argument('-t',nargs="*",help="qscore,radg,etot,rmsd,local,go,repul,elect")
        self.args = parser.parse_args()
        print self.args.inputfile

if __name__=="__main__":
    test=PlotTs()
    test.main()#sys.argv[1],sys.argv[2])
    #test.main("./test/inp/test.ts")
