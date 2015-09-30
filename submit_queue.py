#!/rei_fs1/ono/python/bin/python
####!/home/ono/Python-2.7.9/python
#coding:utf-8
#editor:ono
#This script makes input files and submits queue.

import json
import subprocess
import sys
import argparse

from json_to_cafeinp import JsonToCafeinp
from make_queues import MakeQueues

class SubmitQueue:
    def __init__(self):
        self.injson=""
        self.WORKDIR=""
        self.INPDIR=""
        self.loadjson=""

    def main(self):
        self._initArg()
        self.loadjson=json.load(open(self.injson))
        inputs=JsonToCafeinp(self.injson)
        inputs.read()
        inputs.makeInps()
        self.BASEDIR=inputs.BASEDIR
        self.INPDIR=inputs.INPDIR

        self._makeQueue()
        self.submitQueue()

    def _makeQueue(self):
        queues=MakeQueues()
        queues.setQueue(self.loadjson["queue"]["6"][-1])
        queues.setCore(self.loadjson["queue"]["8"][-1])
        queues.main(self.INPDIR,self.BASEDIR)
        
    def submitQueue(self):
        filename=self.loadjson["inputfile"]["filenames"]["filename"]["name"]
        cmdline="ls %s/*%s*.sh" % (self.INPDIR,filename)
        print cmdline
        qsublist=subprocess.check_output(cmdline,shell=True).split()
        
        for iqsub in qsublist:
            exe=["qsub",iqsub]
            #print " ".join(exe)
            #print exe
            subprocess.Popen(exe)

    def _initArg(self):
        parser=argparse.ArgumentParser(description='This script submits torque-queue from cafe-json')
        parser.add_argument('inputfile',nargs='?',help="input-file[.json]")
        self.injson=parser.parse_args().inputfile


if __name__ == "__main__":
    test=SubmitQueue()
    test.main()
    
