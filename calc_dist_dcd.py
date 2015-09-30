#!/usr/bin/env python

import argparse
import json
import sys

import numpy as np

from dcdfile import DcdFile

class CalcDist:
    def __init__(self):
        self.inputfile=''
        self.atom1=0
        self.atom2=0
        self.natoms=0
        self.stepsize=1
        self.deltalist=[]
        self.result={}

    def main(self):
        self._initArg()
        self.readDcd(self.inputfile)
        self.calcDist()
        self.writeJson()
        
    def printInfo(self):
        pass

    def calcDist(self):
        dstep=self.nstep/(self.nstep_save*self.stepsize)
        for i,delta in enumerate(self.deltalist):
            self.result[dstep*i]=np.linalg.norm(delta)

    def writeJson(self):
        with open(self.output,'w') as f:
            json.dump(self.result,f,indent=4)
        
    def readDcd(self,dcdfile):
        dcd=DcdFile()
        dcd.read(dcdfile)
        self.natoms=dcd.dcdheader.natoms
        self.nstep_save = dcd.dcdheader.nstep_save
        self.nstep = dcd.dcdheader.nstep

        self.deltalist=np.array(np.array(dcd)[::self.stepsize,self.atom1,:]-np.array(dcd)[::self.stepsize,self.atom2,:])
        # This line means stepsize is "::2" and self.atom1 and self.atom2 is choisend.
        print 'ATOMS ',self.natoms
        print 'Total_Step ',self.nstep
        print 'Step_Save ',self.nstep_save
        dcd.close()

    def _initArg(self):
        parser = argparse.ArgumentParser(description='This script calculates a distance between atom1 and atom2.')
        parser.add_argument('inputfile',nargs='?',help="input-file[.dcd]")
        parser.add_argument('-a1','--atom1',type=int,help='choice atom1[int]',default=0,required=True)
        parser.add_argument('-a2','--atom2',type=int,help='choice atom2[int]',default=0,required=True)
        parser.add_argument('-s','--stepsize',type=int,help='choice stepsize[int]',default=1)
        self.inputfile=parser.parse_args().inputfile
        if not (self.inputfile):
            print "[CAUTION!!] Please check 'calc_dist_dcd.py -h'"
            sys.exit()
        parser.add_argument('-o','--output',type=str,help='output-filename[json]',default='dist_'+self.inputfile.split(".")[0]+".json")
        self.atom1=parser.parse_args().atom1-1
        self.atom2=parser.parse_args().atom2-1
        self.stepsize=parser.parse_args().stepsize
        self.output=parser.parse_args().output

if __name__=='__main__':
    tmp=CalcDist()
    tmp.main()
    
