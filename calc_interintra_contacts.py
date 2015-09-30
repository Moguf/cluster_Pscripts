#!/usr/bin/env python

import subprocess
import argparse
import multiprocessing
import numpy as np
import scipy
#import matplotlib 
#matplotlib.use('Agg')
import matplotlib.pyplot as plt

from dcdfile import DcdFile
from read_ninfo import ReadNinfo
from my_error import InputError

class CalcInterIntraContacts(object):
    def __init__(self):
        self.dcdfile = ''
        self.ninfofile = ''
        self.pdbfile = ''
        self.contact_group=[]

    def main(self):
        self.__initArg()
        self.read()
        self.calcInterIntraContacts()

    def read(self):
        if self.dcdfile:
            self.readDcd(self.dcdfile)
        elif self.pdbfile:
            self.readPDB(self.pdbfile)
        else:
            errormsg = 'Can\'t find pdbfile or dcdfile.'
            raise InputError('in read::',errormsg)
            
        if self.ninfofile:
            self.readNinfo(self.ninfofile)


    def readPDB(self,pdbfile):
        print '@PDB:\t'+pdbfile


    def readDcd(self,dcdfile):
        print '@DCD:\t'+dcdfile
        self.dcddata=DcdFile()
        self.dcddata.read(dcdfile)


    def readNinfo(self,ninfofile):
        print '@NINFO:\t'+ninfofile
        tklass=ReadNinfo()
        tklass.read(ninfofile)
        self.ninfodata=tklass.data


    def _preCalc(self):
        print '@CALCULATEING:\t'+" ".join(self.contact_group)
        if len(self.contact_group) == 1:
            if self.contact_group[0] == 'all':
                print self.ninfodata['contact']


    def calcInterIntraContacts(self):
        self._preCalc()
        
    def __initArg(self):
        scriptusage = '%(prog)s [-d] [-p] [-n]'
        description = ('''\
===================================================================
===     Calculating qscores of monomer and inter-monomer.       ===
===================================================================

 [EXAMLE] %(prog)s -d cafemol.dcd -n cafemol.ninfo -o png(default)
 [EXAMLE] %(prog)s -p protein.pdb -n cafemol.ninfo -o png eps json

===================================================================\
        ''')
        parser = argparse.ArgumentParser(description=description,usage=scriptusage,formatter_class=argparse.RawTextHelpFormatter)
        parser.add_argument('-d','--dcd',type=str,help='Cordinate file from cafemol software.',default=None)
        parser.add_argument('-p','--pdb',type=str,help='Protein structure file ,PDB style.',default=None)
        parser.add_argument('-n','--ninfo',type=str,help='Native Info file from cafemol software.',required=True)
        parser.add_argument('-o','--output',nargs='*',help='Output type, png, eps, json(default).',default=['json'])
        parser.add_argument('-c','--contact',nargs='*',help='Output type, png, eps, json(default).',default=['all'])
        
        args = parser.parse_args()
        self.dcdfile=args.dcd
        self.ninfofile=args.ninfo
        self.pdbfile=args.pdb
        self.contact_group=args.contact
        print self.__dict__
        
if __name__ == "__main__":
    test=CalcInterIntraContacts()
    test.main()
