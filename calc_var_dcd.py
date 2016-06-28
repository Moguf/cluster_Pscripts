#!/usr/bin/env python
# coding:utf-8

import argparse
import json
import sys

import numpy as np
import scipy.spatial as sp

from dcdfile import DcdFile
from read_ninfo import ReadNinfo
from calc_var_c import calcVarC


class CalcVarDcd:
    def __init__(self):
        self.inputfile = ''
        self.natoms = 0
        self.stepsize = 1
        self.begin_step = 0
        self.deltalist = []
        self.result = {}
        self.contact_data = {}
        self.dcddata = 'dcdFileClass'

    def main(self):
        self._initArg()
        self.readDcd(self.inputfile)
        self.readNinfo(self.ninfofile)
        self.calcVar()
        #self.writeJson()
        
    def printInfo(self):
        pass

    def calcVar(self):
        sys.stdout.write('Now Calculating!!\r')
        sys.stdout.flush()
        tstep = self.nstep/self.nstep_save
        if self.begin_step > tstep:
            print('Error:: Start Step < Step Size!!')
            print('Start Step = %d\nStep Size = %d' % (self.begin_step, tstep))
            sys.exit()

        for i,xyz in enumerate(self.dcddata[self.begin_step:]):
            sys.stdout.write('%4d/%4d\r' % (i+self.begin_step+1,tstep))
            for icon in self.contact_data:
                imp = icon[0,0]-1
                jmp = icon[0,1]-1
                key = "%d-%d" % (imp,jmp)
                if not key in self.result.keys():
                    self.result[key] = []
                self.result[key].append(sp.distance.euclidean(xyz[imp],xyz[jmp]))
            sys.stdout.flush()
        print('Done!!!')

    def calcVarC(self):
        sys.stdout.write('Now Calculating in C!!\r')

    def writeJson(self):
        with open(self.output,'w') as f:
            json.dump(self.result,f,indent=4)
        
    def readDcd(self,dcdfile):
        dcd=DcdFile()
        dcd.read(dcdfile)
        self.natoms=dcd.dcdheader.natoms
        self.nstep_save = dcd.dcdheader.nstep_save
        self.nstep = dcd.dcdheader.nstep
        self.dcddata = dcd
        print('========== Dcd file ==========')
        print('FILE: ', dcdfile)
        print('ATOMS: ',self.natoms)
        print('Total_Step: ',self.nstep)
        print('Step_Save: ',self.nstep_save)
        print('==============================')

    def readNinfo(self,ninfofile):
        tmp = ReadNinfo()
        tmp.read(ninfofile)
        print('========= Ninfo file =========')
        print('FILE: ', ninfofile)
        print('==============================')
        self.contact_data = np.matrix(tmp.data['contact'])
        self.contact_data = self.contact_data[:,np.array([3,4])].astype(int)
        # Selecting contact numbers.
        # For example
        # "[[1,5],[15,19],...,]" -> "[[1st atom,5th atom],[15th atom,19th atom],...,]"
        tmp = 0
        
    def _initArg(self):
        parser = argparse.ArgumentParser(description='This script calculates variances from dcd-file and ninfo-file.')
        parser.add_argument('inputfile',nargs='?',help="input-file[.dcd]")
        parser.add_argument('-n','--ninfo',nargs='?',help="input-file[.ninfo]")
        parser.add_argument('-s','--stepsize',type=int,help='choice stepsize[int]',default=1)
        parser.add_argument('-b','--begin',type=int,help='choice the start step[int]',default=0)
        self.inputfile=parser.parse_args().inputfile
        parser.add_argument('-o','--output',type=str,help='output-filename[json]',default='var_'+self.inputfile.split(".")[0]+".json")
        
        if not (self.inputfile):
            print("[CAUTION!!] Please check 'calc_var_dcd.py -h'")
            sys.exit()
        self.ninfofile = parser.parse_args().ninfo
        self.begin_step = parser.parse_args().begin - 1
        self.stepsize = parser.parse_args().stepsize
        self.output = parser.parse_args().output

if __name__=='__main__':
    tmp=CalcVarDcd()
    tmp.main()
    
