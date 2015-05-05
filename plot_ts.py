#!/usr/bin/env python2.7
import argparse
import sys

import matplotlib.pyplot as plt

from read_ts import ReadTs


class PlotTs(ReadTs):
    def __init__(self):
        ReadTs.__init__(self)
        self.args=[]
        self.inputfile=""           ### you need to input "ts-file".
        self.outfilename="ouput"    ### default is ouput
        self.outfiletype=""         ### for example [png,eps,both]
        self.outdata=['qscore']     ### for example [qsocre,local, ...]
        self._initArg()


    def main(self):
        self.read(self.inputfile)
        self.transposeData()
        self.plotTs()

        
    def plotTs(self):
        fig=plt.figure()
        ax=fig.add_subplot(111)
        print self.data
        for datatype in self.outdata:
            print self.outdata
            index=self.data['unit'].index(datatype)
            print self.data['all'][0]
            ax.plot(self.data['all'][0],self.data['all'][index])

        plt.show()


    def _initArg(self):
        parser = argparse.ArgumentParser(description='plot ts-data')
        parser.add_argument('inputfile',nargs='?',help="input-file[.ts]")
        parser.add_argument('-o',type=str,choices=["eps","png","both"],help="ex:output[.eps, .png  ,.png and .eps]",default="png")
        parser.add_argument('output',nargs='?',const="output",help="ex:[output].png",default="output")
        parser.add_argument('-t',nargs="*",help="qscore,radg,etot,rmsd,local,go,repul,elect",default=['qscore'])
        self.args = parser.parse_args()

        self.inputfile=self.args.inputfile
        self.outfilename=self.args.output
        self.outfiletype=self.args.o
        self.outdata=self.args.t

        
if __name__=="__main__":
    test=PlotTs()
    test.main()#sys.argv[1],sys.argv[2])
    #test.main("./test/inp/test.ts")
