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
        self.loop=[]

        

    def main(self):
        self._makeInputFile()
        self._submitQueue()


    def _makeInputFile(self):

        _inpdata=self.jsondata["inputfile"]
        _cafe_style=CafemolStyleInp()



        
    def _makeShFile(self):
        _shfdata=self.jsondata["queue"]


    def _submitQueue(self):
        pass
    
    def _determineCount(self):
        
        pass


if __name__ == "__main__":
    test=SubmitQueue('./test/inp/inp.json')
    test.main()
    
