#!/usr/bin/env python2.7
#coding:utf-8
#editor:ono
#This script makes input files and submits queue.
import json
import subprocess
import sys

from json_to_cafeinp import JsonToCafeinp
from make_queues import MakeQueues

class SubmitQueue:
    def __init__(self,inpfile):
        self.injson=inpfile
        self.WORKDIR=""
        self.INPDIR=""
        self.loadjson=json.load(open(self.injson))

    def main(self):
        inputs=JsonToCafeinp(self.injson)
        inputs.read()
        inputs.makeInps()
        self.BASEDIR=inputs.BASEDIR
        self.INPDIR=inputs.INPDIR
        
        self._makeQueue()

        self.submitQueue()

    def _makeQueue(self):

        queues=MakeQueues()
        queues.main(self.INPDIR,self.BASEDIR)
        queues.setQueue(self.loadjson["queue"]["6"][-1])
        queues.setCore(self.loadjson["queue"]["8"][-1])
        
    def submitQueue(self):
        filename=self.loadjson["inputfile"]["filenames"]["filename"]["name"]
        cmdline="ls %s/*%s*.sh" % (self.INPDIR,filename)
        print cmdline
        qsublist=subprocess.check_output(cmdline,shell=True).split()
        
        for iqsub in qsublist:
            exe=["qsub",iqsub]
            print " ".join(exe)
            #subprocess.Popen(exe)

if __name__ == "__main__":
    test=SubmitQueue(sys.argv[1])
    test.main()
    
