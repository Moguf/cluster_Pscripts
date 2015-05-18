#!/bin/usr/env python
# coding: utf-8
# editor: ono
import argparse

import numpy as np

import dcdfile



class CalcRMSF:
    def __init__(self):
        self.dcdfile=""
        self.coordinates=[]
        self.natoms=0


    def main(self):
        self._initArg()
        self.read(self.dcdfile,1000)
        self.calcRMSF()


    def read(self,inputfile,start):
        dcd=dcdfile.DcdFile()
        dcd.read(inputfile)
        self.natoms=dcd.dcdheader.natoms
        self.coordinates=np.array(dcd[start:])
        dcd.close()
        

    def doPy(self):
        import prody
        """
        -----
        pip install prody
        or
        http://prody.csb.pitt.edu/index.html
        ------
        RMSF[i]=sqrt(ave((x[i]-average_x[i])**2))
        delta2=(x[i]-average_x[i])**2
        
        B-factor=8*pi**2*RMSF**2/3
        Ref: Willis & Pryor, Thermal vibrations in crystallography, Cambridge Univ. Press, 1975
        unit: Angstrom**2
        """
        
        ave_coordinate=np.average(self.coordinates,axis=0)
        nframes=len(self.coordinates)
        rmsf=np.zeros(self.natoms)

        for j in range(10):
            t=prody.calcTransformation(ave_coordinate,self.coordinates[j])
            for i in range(self.natoms):
                delta2=(self.coordinates[j][i].dot(t.getRotation())-ave_coordinate[i])
                rmsf[i]+=delta2.dot(delta2)
                
        return np.sqrt(rmsf/nframes)**2*8*np.pi**2/3
        

    def doC(self):
        pass


    def _initArg(self):
        parser = argparse.ArgumentParser(description='This scripts calculate RMSF from dcd-file.')
        parser.add_argument('inputfile',nargs='?',help="input-file[.dcd]")
        
        self.dcdfile=parser.parse_args().inputfile


    def test(self):
        self.read("./test/inp/m21z14t300n1.dcd",1000)
        #self.read("./test/inp/2gxa.dcd",100)
        self.doPy()
        

        
if __name__=="__main__":
    test=CalcRMSF()
    test.test()
    #test.main()

