#!/usr/bin/env python2.7
import re
import argparse

class ReadNinfo:
    def __init__(self):
        self.data={}
        for ikey in ["bond","angl","aicg13","aicgdih","dihd","contact"]:
            self.data[ikey]=[]
        self.filename=""

    def main(self):
        self._initArg()
        self.read(self.filename)
        

    def read(self,filename):
        rfile=open(filename,'r')
        for iline in rfile.readlines():
            ilist=iline.strip().split()
            if not ilist:
                continue
            if ilist[0] in self.data.keys():
                self.data[ilist[0]].append([self._num(i) for i in ilist[1:-1]]+[ilist[-1]])
                # ilist[0] is key, ilist[-1] is string( 'pp', 'p-p' )
                # 'int' -> int , 'float' -> float


    def write(self,filename):
        wfile=open(filename,'w')
        ostr=""
        for ikey in ["bond","angl","aicg13","aicgdih","dihd","contact"]:#self.data.keys():
            # This for-loop is not good.
            for ilist in self.data[ikey]:
                _tmp=[str(i) for i in ilist]
                ostr+=ikey+" "+" ".join(_tmp)+"\n"
            ostr+="\n"
        
        wfile.write(ostr)

    def _num(self,s):
        try:
            return int(s)
        except ValueError:
            return float(s)

    def _initArg(self):
        parser = argparse.ArgumentParser(description='This script make json-style of cafemol-ninfo')
        parser.add_argument('inputfile',nargs='?',help="input-file[.ninfo]")
        parser.add_argument('-o','--output',nargs='?',help="output-file[.ninfo]",default='out.ninfo')
        self.filename=parse.parse_args().inputfile
        

        
            
if __name__=="__main__":
    test=ReadNinfo()
    test.main()
