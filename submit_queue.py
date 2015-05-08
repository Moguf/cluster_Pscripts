#!/usr/bin/env python2.7
#coding:utf-8
#editor:ono
#This script makes input files and submits queue.
import json

from json_to_cafeinp import JsonToCafeinp
from make_queues import MakeQueues

class SubmitQueue:
    def __init__(self,inpfile):
        self.injson=inpfile
        self.WORKDIR=""
        self.INPDIR=""

    def main(self):
        inputs=JsonToCafeinp(self.injson)
        inputs.read()
        inputs.makeInps()
        self.BASEDIR=inputs.BASEDIR
        self.INPDIR=inputs.INPDIR
        
        self._makeQueue()

        self.submitQueue()

    def _makeQueue(self):
        loadjson=json.load(open(self.injson))
        queues=MakeQueues()
        queues.main(self.INPDIR,self.BASEDIR)
        queues.setQueue(loadjson["queue"]["6"][-1])
        queues.setCore(loadjson["queue"]["8"][-1])
        
    def submitQueue(self):
        pass

if __name__ == "__main__":
    test=SubmitQueue('./test/inp/inp.json')
    test.main()
    
