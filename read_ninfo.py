#!/usr/bin/env python2.7
import re
import argparse

import numpy as np

class ReadNinfo:
    def __init__(self):
        self.data={}
        for ikey in ["bond","angl","aicg13","aicgdih","dihd","contact"]:
            self.data[ikey]=[]
        self.filename=""
        self.bond_format="%-7s%7d%7d%7d%7d%7d%7d%7d    %8.4f    %7.4f    %7.4f    %7.4f %7s\n"
        self.angl_format="%-7s%7d%7d%7d%7d%7d%7d%7d%7d%7d    %8.4f    %7.4f    %7.4f    %7.4f %7s\n"
        self.aicg13_format="%-7s%7d%7d%7d%7d%7d%7d%7d%7d%7d    %8.4f    %7.4f    %7.4f    %7.4f    %7.4f %7s\n"
        self.dihd_format="%-7s%7d%7d%7d%7d%7d%7d%7d%7d%7d%7d%7d    %9.4f    %7.4f    %7.4f    %7.4f    %7.4f %7s\n"
        self.aicgdih_format="%-7s%7d%7d%7d%7d%7d%7d%7d%7d%7d%7d%7d    %9.4f    %7.4f    %7.4f    %7.4f    %7.4f %7s\n"
        self.contact_format="%-7s%7d%7d%7d%7d%7d%7d%7d     %8.4f    %7.4f%7d    %7.4f %4s\n"

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
            ostr+="<<<<\n"
            for ilist in self.data[ikey]:
                #                _tmp=[str(i) for i in ilist]

                if ikey=="bond":
                    ostr+=self.bond_format % (ikey,ilist[0],ilist[1],ilist[2]
                                              ,ilist[3],ilist[4],ilist[5],ilist[6]
                                              ,ilist[7],ilist[8],ilist[9],ilist[10]
                                              ,ilist[11])
                elif ikey=="angl":
                    ostr+=self.angl_format % (ikey,ilist[0],ilist[1],ilist[2]
                                              ,ilist[3],ilist[4],ilist[5],ilist[6]
                                              ,ilist[7],ilist[8],ilist[9],ilist[10]
                                              ,ilist[11],ilist[12],ilist[13])
                elif ikey=="aicg13":
                    ostr+=self.aicg13_format % (ikey,ilist[0],ilist[1],ilist[2]
                                                ,ilist[3],ilist[4],ilist[5],ilist[6]
                                                ,ilist[7],ilist[8],ilist[9],ilist[10]
                                                ,ilist[11],ilist[12],ilist[13],ilist[14])
                elif ikey=="dihd":
                    ostr+=self.dihd_format % (ikey,ilist[0],ilist[1],ilist[2]
                                              ,ilist[3],ilist[4],ilist[5],ilist[6]
                                              ,ilist[7],ilist[8],ilist[9],ilist[10]
                                              ,ilist[11],ilist[12],ilist[13],ilist[14]
                                              ,ilist[15],ilist[16])
                elif ikey=="aicgdih":
                    ostr+=self.aicgdih_format % (ikey,ilist[0],ilist[1],ilist[2]
                                                ,ilist[3],ilist[4],ilist[5],ilist[6]
                                                ,ilist[7],ilist[8],ilist[9],ilist[10]
                                                ,ilist[11],ilist[12],ilist[13],ilist[14]
                                                ,ilist[15],ilist[16])
                elif ikey=="contact":
                    ostr+=self.contact_format % (ikey,ilist[0],ilist[1],ilist[2]
                                                ,ilist[3],ilist[4],ilist[5],ilist[6]
                                                ,ilist[7],ilist[8],ilist[9],float(ilist[10])
                                                ,ilist[11])
            ostr+="<<<<\n\n"

        wfile.write(ostr)

    def _num(self,s):
        try:
            return int(s)
        except ValueError:
            return float(s)

    def collectContact(self):
        """this method returns contacts matrix([[unti1 unit2 num1 num2 length] ...]
        ,type=numpy.array,value-type=float)."""

        return np.array(self.data['contact'])[:,np.array([1,2,3,4,7])].astype(np.float)

    def _initArg(self):
        parser = argparse.ArgumentParser(description='This script make json-style of cafemol-ninfo')
        parser.add_argument('inputfile',nargs='?',help="input-file[.ninfo]")
        parser.add_argument('-o','--output',nargs='?',help="output-file[.ninfo]",default='out.ninfo')
        self.filename=parse.parse_args().inputfile

    def close(self):
        self.data={}        
        
            
if __name__=="__main__":
    test=ReadNinfo()
    test.main()
