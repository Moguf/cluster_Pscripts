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

    def readPDB(self,pdbfile):
        print '@PDB: '+pdbfile


    def readDcd(self,dcdfile):
        print '@DCD: '+dcdfile
        self.dcddata=DcdFile()
        self.dcddata.read(dcdfile)
        print self.dcddata[0]

    def readNinfo(self,ninfofile):
        print '@NINFO: '+ninfofile


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
        
    def calcInterIntraContacts(self):
        pass


    def main(self):
        self.__initArg()
        self.read()

        

    def __initArg(self):
        scriptusage = '%(prog)s [-d] [-p] [-n]'
        description = ('''\
===================================================================
===     Calculating qscores of monomer and inter-monomer.       ===
===     This script is specific for virus structures.           ===

 [EXAMLE] %(prog)s -d cafemol.dcd -n cafemol.ninfo -o png(default)
 [EXAMLE] %(prog)s -p protein.pdb -n cafemol.ninfo -o png eps json

===================================================================\
        ''')
        parser = argparse.ArgumentParser(description=description,usage=scriptusage,formatter_class=argparse.RawTextHelpFormatter)
        parser.add_argument('-d','--dcd',type=str,help='Cordinate file from cafemol software.',default=None)
        parser.add_argument('-p','--pdb',type=str,help='Protein structure file ,PDB style.',default=None)
        parser.add_argument('-n','--ninfo',type=str,help='Native Info file from cafemol software.',required=True)
        parser.add_argument('-o','--output',nargs='*',help='Output type, png, eps, json(default).',default=['json'])
        
        args = parser.parse_args()
        self.dcdfile=args.dcd
        self.ninfofile=args.ninfo
        self.pdvfile=args.pdb

        print self.__dict__
        
if __name__ == "__main__":
    test=CalcInterIntraContacts()
    test.main()
