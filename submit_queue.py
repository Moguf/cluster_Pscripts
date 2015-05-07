#!/usr/bin/env python2.7
#coding:utf-8
#editor:ono
#This script makes input files and submits queue.

import sys
import subprocess
import json
import os

from cafemol_style import CafemolStyleInp

class SubmitQueue:
    def __init__(self,inpfile):
        _jdata=open(inpfile,"r")
        self.jsondata=json.load(_jdata)
        
        self.iterlist=[]
        #This list is needed to make input file on many value.
        #If there is a list in json, iterlist.the list).
        
        self.basedir=""


    def main(self):
        self._makeInputFile()
        self._submitQueue()


    def _makeInputFile(self):
        self.jsondata["inputfile"]
        self.template_file=CafemolStyleInp()

        self._checkBlock()
        self._checkDir()

        self._readFilenames()
        self._readJobCntl()
        self._readEnergyFunction()
        self._readUnitAndState()
        self._readMdInformation()
        self._readOptionalBlock()


        
    def _readFilenames(self):
        txtlist=[]
        self.template_file.filename=self.jsondata["inputfile"]["filenames"]["filename"]
        self.template.path = self.jsondata["inputfile"]["filenames"]["path"]
        self.template.output = self.jsondata["inputfile"]["filenames"]["output"]
        self.template.path_pdb = self.jsondata["inputfile"]["filenames"]["path_pdb"]
        self.template.path_ini = self.jsondata["inputfile"]["filenames"]["path_ini"]
        self.template.path_natinfo = self.jsondata["inputfile"]["filenames"]["path_natinfo"]
        self.template.path_aicg = self.jsondata["inputfile"]["filenames"]["path_aicg"]
        self.template.path_para = self.jsondata["inputfile"]["filenames"]["path_para"]
        self.template.path_msf = self.jsondata["inputfile"]["filenames"]["path_msf"]
        

    def _readJobCntl(self):
        pass

    def _readEnergyFunction(self):
        pass

    def _readUnitAndState(self):
        pass

    def _readMdInformation(self):
        pass

    def _readOptionalBlock(self):
        pass
        
    def _makeShFile(self):
        _shfdata=self.jsondata["queue"]


    def _checkBlock(self):
        pass
        
    def _checkDir(self):
        pass

    def _submitQueue(self):
        pass
    
    def _determineCount(self):
        
        pass


if __name__ == "__main__":
    test=SubmitQueue('./test/inp/inp.json')
    test.main()
    
