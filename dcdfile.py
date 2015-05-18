#! /usr/bin/env python
# -*- coding: utf-8 -*-
#editor: ono

import os 
import sys
import struct
import argparse

from my_error import MyError



class DcdHeader:
    def __init__(self):
        self.nset = None
        self.istart = None
        self.nstep_save = None
        self.nstep = None
        self.nunit_real = None
        self.delta = None
        self.title = None
        self.tempk = None
        self.lunit2mp = []
        self.natoms = None
        self.blocksize=0


    def show(self):
        for ikey in self.__dict__.keys():
            print ikey,self.__dict__[ikey]



class DcdFile(object):
    def __init__(self):
        self.dcdfile=False
        self.dcdheader=DcdHeader()
        self.nframes=0  
        self.iterValue=0


    def __getitem__(self,item):
        tmp_cordinates=[]

        try:
            if isinstance(item,slice):
                indices=item.indices(self.nframes)
                
                for i in range(*indices):
                    self.dcdfile.seek(self.dcdheader.blocksize+i*12*(self.dcdheader.natoms+2))
                    tmp_cordinates.append(self.readOneStep())

                self.dcdfile.seek(0)
                return tmp_cordinates
            if item>=0:
                self.dcdfile.seek(self.dcdheader.blocksize+item*12*(self.dcdheader.natoms+2))
                tmp_cordinates= self.readOneStep()        
                self.dcdfile.seek(0)
            else:
                item=self.nframes+item
                self.dcdfile.seek(self.dcdheader.blocksize+item*12*(self.dcdheader.natoms+2))
                tmp_cordinates= self.readOneStep()        
                self.dcdfile.seek(0)
        except:
            errormsg="There is no %dth frame"%(item)
            raise MyError(errormsg)
            
        return tmp_cordinates


    def __iter__(self):
        self.dcdfile.seek(self.dcdheader.blocksize)
        return self
        

    def __len__(self):
        return self.nframes


    def next(self):
        self.iterValue+=1
        if self.nframes < self.iterValue:
            raise StopIteration
        return self.readOneStep()


    def main(self):
        self._initArg()
        self.read(self.inputfile)

        
    def read(self,inputfile):
        print "read:",inputfile
        self.inputfile=inputfile
        self.dcdfile=open(self.inputfile,"rb")
        self._readHeader()


    def readOneStep(self):
        coord_matrix = []
        
        b = self._pickData()
        x = struct.unpack('f' * self.dcdheader.natoms, b)
        b = self._pickData()
        y = struct.unpack('f' * self.dcdheader.natoms, b)
        b = self._pickData()
        z = struct.unpack('f' * self.dcdheader.natoms, b)
        
        for i in xrange(self.dcdheader.natoms) :
            xyz = [x[i], y[i], z[i]]
            coord_matrix.append(xyz)
            
        return coord_matrix


    def writeToMovie(self,outfile):
        pass


    def _readHeader(self):
        ### read first line
        b=self._pickData()
        header=struct.unpack('4s9if10i',b)

        if header[0].strip() != "CORD":
            raise MyError('Input Error:','Inpug file is not dcd-format.')

        self.dcdheader.nset = header[1]
        self.dcdheader.istart = header[2]
        self.dcdheader.nstep_save = header[3]
        self.dcdheader.nstep = header[4]
        self.dcdheader.nunit_real = header[5]
        self.dcdheader.delta = header[10]
        
        self.nframes=self.dcdheader.nstep/self.dcdheader.nstep_save+1
        ## initial struture and step = 1 sturecture are contained in dcd-file.
        ###

        ### read title block
        b=self._pickData()
        titleblock=struct.unpack('i'+'80s'*(3+self.dcdheader.nunit_real),b)
        self.dcdheader.title=titleblock[1]+titleblock[2]
        self.dcdheader.tempk=float(titleblock[3])

        for i in xrange(self.dcdheader.nunit_real) :
            self.dcdheader.lunit2mp.append(int(titleblock[i + 4]))

        b = self._pickData()
        self.dcdheader.natoms = struct.unpack('i', b)[0]
        ###         

        ### read header block_size
        self.dcdfile.seek(0)
        for i in range(3):
            size1= struct.unpack("i",self.dcdfile.read(4))[0]
            self.dcdfile.seek(size1,os.SEEK_CUR)
            struct.unpack("i",self.dcdfile.read(4))[0]
        
        self.dcdheader.blocksize=self.dcdfile.tell()
        ### 
        
        self.dcdfile.seek(self.dcdheader.blocksize)
        self._checkData()


    def _checkData(self):
        file_size=os.stat(self.inputfile).st_size
        header_size=self.dcdheader.blocksize
        coordinate_size=12*(self.dcdheader.natoms+2)
        total_steps=(file_size-header_size)/coordinate_size
        
        if total_steps==self.nframes:
            print total_steps,"steps in this file"
        else:
            print "-"*20,"CAUTION:!!!","-"*20
            print "\t\tIN header:total steps",self.nframes
            print "\t\tThis file size:total steps",total_steps
            print "-"*53
            
        self.nframes=total_steps
        
        return True

            
    def _pickData(self):
        num = struct.unpack('i', self.dcdfile.read(4))[0]
        b=self.dcdfile.read(num)
        self.dcdfile.seek(4, os.SEEK_CUR)
        return b
        

    def _initArg(self):
        parser = argparse.ArgumentParser(description='This scripts defined dcd-style in Cafemol.')

        parser.add_argument('inputfile',nargs='?',help="input-file[.dcd]")
        parser.add_argument('-o','--output',nargs='?',help="output-file[.json]",default='out.json')

        self.inputfile=parser.parse_args().inputfile


    def test(self):
        self.read("./test/inp/2gxa.dcd")
        ### broken file(2gxa.dcd)
        #self.read("./test/inp/test.dcd")
        """
        print "test.dcd case"
        print "10000 frames"
        print "587 atoms"
        """
        print "%%% my function test---"
        initdata=self.readOneStep()
        initdata=self.readOneStep()
        print initdata

        print "%%% __len__ test---"
        print len(self)

        print "%%% __getitem__ test---"
        print len(self[0:10])
        print len(self[0:10:2])
        print len(self[::-100])

        print "%%% __iter__ test---"
        for i,frame in enumerate(self[:5]):
            print i,len(frame)


        
if __name__=="__main__":
    test=DcdFile()
    test.test()
    
