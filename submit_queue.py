#!/usr/bin/env python2.7
#coding:utf-8
#editor:ono
#This script makes input files and submits queue.

from json_to_cafeinp import JsonToCafeinp

class SubmitQueue:
    def __init__(self,inpfile):
        self.injson=inpfile


    def main(self):
        makeinputs=JsonToCafeinp(self.injson)
        makeinputs.read()
        makeinputs.makeInps()


        self.__makeQueue()
        self._submitQueue()

    def _makeQueue(self):
        pass
        
    def _submitQueue(self):
        pass

if __name__ == "__main__":
    test=SubmitQueue('./test/inp/inp.json')
    test.main()
    
