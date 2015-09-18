#!/usr/bin/env python
# coding: utf-8
# editor: ono
import argparse
import json

import numpy as np
import matplotlib.pyplot as plt

import dcdfile

class CalcRMSF:
    def __init__(self):
        self.dcdfile=""
        self.coordinates=[]
        self.natoms=0
        self.bfactor=[]
        self.cal_bfactor=[]
        self.inputfile=""


    def main(self):
        self._initArg()
        self.read(self.dcdfile,100)
        self.doPyForCapsid()


    def read(self,inputfile,start=0,unit='all'):
        self.inputfile=inputfile
        dcd=dcdfile.DcdFile()
        dcd.read(inputfile)
        self.natoms=dcd.dcdheader.natoms
        self.coordinates=np.array(dcd[start:])
        dcd.close()
        

    def doPy(self):
        print "calculating ...."
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
        
        tmpcoord=[]
        nframes=len(self.coordinates)
        ave_coordinate=np.average(self.coordinates,axis=0)
        
        rmsf=np.zeros(len(self.coordinates[0]))

        for j in range(nframes):
            t=prody.calcTransformation(ave_coordinate,self.coordinates[j])
            for i in range(self.natoms):
                delta2=(self.coordinates[j][i].dot(t.getRotation())-ave_coordinate[i])
                rmsf[i]+=delta2.dot(delta2)

                
        self.cal_bfactor=np.sqrt(rmsf/nframes)**2*8*np.pi**2/3
        print "done!!"
        return np.sqrt(rmsf/nframes)**2*8*np.pi**2/3
        

    def doPyForCapsid(self,resides=0,subunit=60):
        print "for mvm capsid"
        print "calculating ...."
        import prody
        resides=587
        tmpcoord=[]
        nframes=len(self.coordinates)
        ignore_residue=38


        self.subunits_coord=[]
        
        for i in range(nframes):
            for k in range(subunit):
                self.subunits_coord.append(self.coordinates[i][k*587+ignore_residue:587*(k+1)])
                
        self.subunits_coord=np.array(self.subunits_coord)
        ensemble=prody.Ensemble()
        ensemble.addCoordset(self.subunits_coord)
        rmsf=ensemble.getRMSFs()
        bfactor=8/3*np.pi**2*rmsf**2
        self.cal_bfactor=[0 for i in range(ignore_residue)]+bfactor.tolist()

    def doC(self):
        pass

    def _initArg(self):
        parser = argparse.ArgumentParser(description='This scripts calculate RMSF from dcd-file.')
        parser.add_argument('inputfile',nargs='?',help="input-file[.dcd]")
        self.dcdfile=parser.parse_args().inputfile


    def test(self):
        #self.read("./test/inp/m21z14t300n1.dcd",1000) ## monomer
        self.read("./test/inp/mc1z14t300n1.dcd",1000) ## capsid
        #self.read("./test/inp/2gxa.dcd",100)
        self.doPy()
        

    def plot(self):
        fig=plt.figure()
        ax=fig.add_subplot(111)
        ax.plot(self.cal_bfactor)
        plt.show()
        
    def writeJson(self):
        jsondata={"cal_BFACTOR":self.cal_bfactor}
        filename="bfac_"+self.inputfile.split(".")[0]+".json"
        f=open(filename,'w')
        json.dump(jsondata,f)
        f.close()
        
if __name__=="__main__":
    test=CalcRMSF()
    #test.test()
    test.main()
    test.writeJson()
  



