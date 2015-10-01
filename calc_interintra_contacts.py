#!/usr/bin/env python

import subprocess
import argparse
import multiprocessing as mp

import numpy as np
import scipy.spatial.distance as scidist
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
        self._initArg()
        self._read()
        self._preCalc()
        self._checkMemory()

    def _read(self):
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
        self.dcddata = DcdFile()
        self.dcddata.read(dcdfile)

        
    def readNinfo(self,ninfofile):
        print '@NINFO:\t'+ninfofile
        tklass = ReadNinfo()
        tklass.read(ninfofile)
        self.contacts = tklass.collectContact()
        print '@@NINFO:MEMORY: %7.2lfMb' % (self.contacts.nbytes/1024.0**2)
        tklass = None


    def _preCalc(self):
        print '@CONTACTS:\t\t'+" ".join(self.contact_group)
        if len(self.contact_group) == 1:
            if self.contact_group[0] == 'all':
                self.calcInterIntraContacts(self.dcddata[-4:],self.contacts)
                self.dcddata = None


    def calcInterIntraContacts(self,coordinates,contacts):
        coordinates = np.array(coordinates)
        print '@@CALCULATING:MEMORY: %7.2lfMb' % ((coordinates.nbytes+contacts.nbytes)/1024.0**2)
        self.doPyCalc(coordinates,contacts)



    def doPyCalc(self,coordinates,contacts):
        distmat = scidist.cdist(coordinates[-1],coordinates[-1])
        atommat = np.zeros_like(distmat)
        num_subunits = 60  ## for virus capsid
        total_cmat = np.zeros((num_subunits,num_subunits))
        now_cmat = np.zeros((num_subunits,num_subunits))
        hex_cmat = np.zeros((num_subunits/5,num_subunits/5))
        tri_cmat = np.zeros((num_subunits/3,num_subunits/3))

        print '@@DIST:MEMORY: %7.2lfMb' % (distmat.nbytes/1024.0**2)

        for icon in contacts:
            total_cmat[int(icon[0])-1,int(icon[1])-1] += 1
            if distmat[int(icon[2])-1,int(icon[3])-1] < 1.2*icon[4]:
                now_cmat[int(icon[0])-1,int(icon[1])-1] += 1

        rows,cols = np.where(total_cmat==729)
        print rows,cols

        total_cmat[total_cmat<40] = 0
        distmat = None
                
        qmat = now_cmat/total_cmat

        ###plot
        fig = plt.figure()
        ax = fig.add_subplot(111)
        cax = ax.matshow(qmat,interpolation='nearest')
        ax.grid(True)
        fig.colorbar(cax)
        ###text
        ind_array = np.arange(60)
        x,y = np.meshgrid(ind_array, ind_array)
        #for x_val,y_val in zip(x.flatten(), y.flatten()):
        for x_val,y_val in zip(cols,rows):
            #ax.text(x_val, y_val, '3' , va='center', ha='center')
            ax.scatter(x_val, y_val,marker='p',s=60,facecolors='none', edgecolors='b')
        print 352<=total_cmat + 355>=total_cmat
        rows,cols = np.where(*(352<=total_cmat and total_cmat<=355))
        for x_val,y_val in zip(cols,rows):
            #ax.text(x_val, y_val, '5' , va='center', ha='center')
            ax.scatter(x_val, y_val,marker='^',s=60,facecolors='none', edgecolors='b')
        rows,cols = np.where(total_cmat==208)
        for x_val,y_val in zip(cols,rows):
            #ax.text(x_val, y_val, '5' , va='center', ha='center')
            ax.scatter(x_val, y_val,marker='d',s=60,facecolors='none', edgecolors='b')
            

        plt.show()

        
    def _checkMemory(self):
        from guppy import hpy
        h = hpy() 
        print h.heap()


    def _initArg(self):
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
        
if __name__ == "__main__":
    test=CalcInterIntraContacts()
    test.main()
