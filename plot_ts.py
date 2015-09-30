#!/usr/bin/env python2.7
"""
I need to change scripts to treat multiple data.
Key Ideas: pdf

"""
import argparse
import sys
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from read_ts import ReadTs


class PlotTs(ReadTs):
    def __init__(self):
        ReadTs.__init__(self)
        self.args=[]
        self.inputfile=""            ### you need to input "ts-file".
        self.outfilename="ouput"     ### default is ouput
        self.outfiletype=""          ### for example [png,eps,both]
        self.datatype=['qscore']     ### for example [qsocre,local, ...]
        self._initArg()


    def main(self):
        self.read(self.inputfile)   ### ReadTs
        self.plotTs()

        
    def plotTs(self):
        fig=plt.figure()
        self.ax=fig.add_subplot(111)
        self._setPlotInit()

        #for idatatype in self.outdata:
        #I need to change to treat multiple data in future. ex qscore and radg , ..
        index=self.data['unit'].index(self.datatype[0])
        #dict[key] -> list[index]
        
        self.ax.plot(self.data['all'][0],self.data['all'][index],lw=3)
        self._saveFig()

        
    def _setPlotInit(self):
        for idatatype in self.datatype:
            if idatatype=="qscore":
                self.ax.set_ylim([0,1])

        self.ax.set_xlabel("Step")
        self.ax.set_ylabel(self.datatype[0])
        self.ax.set_title(self.inputfile.split("/")[-1])
        

    def _saveFig(self):
        if self.outfilesuffix=="both":
            plt.savefig(self.outfilename+".eps",fortmat="eps")
            plt.savefig(self.outfilename+".png",fortmat="png")
        else:
            print self.outfilename+"."+self.outfilesuffix
            plt.savefig(self.outfilename+"."+self.outfilesuffix,fortmat=self.outfilesuffix)

                
    def _initArg(self):
        parser = argparse.ArgumentParser(description='plot ts-data')
        parser.add_argument('inputfile',nargs='?',help="input-file[.ts]")
        parser.add_argument('-o',type=str,choices=["eps","png","both"],help="ex:output[.eps, .png  ,.png and .eps]",default="png")
        parser.add_argument('output',nargs='?',const="output",help="ex:[output].png",default="output")
        parser.add_argument('-t',nargs="*",help="qscore,radg,etot,rmsd,local,go,repul,elect",default=['qscore'])
        self.args = parser.parse_args()

        self.inputfile=self.args.inputfile
        self.outfilename=self.args.output
        self.outfilesuffix=self.args.o
        self.datatype=self.args.t

        
if __name__=="__main__":
    # test command
    # python plot_ts.py ./test/inp/test.ts ./test/out/test -o eps -t rmsd
    test=PlotTs()
    test.main()

