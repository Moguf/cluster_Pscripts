#!/bin/usr/env python2.7
#coding:utf-8
#editor:ono
#this scirpt is utility script
import re

def mySplit(string,spliter=""):
    #This function remain spliter in result list.
    rematch=re.search(spliter,string)
        
    if rematch:
        string_no_space=re.sub(r' ','',string)
        #remove space.
        _tmptxt=""
        for ichar in string_no_space:
            if spliter==ichar:
                _tmptxt+=" "
                _tmptxt+=ichar
                _tmptxt+=" "
            else:
                _tmptxt+=ichar
        outlist=_tmptxt.split()
        return outlist
    else:
        return string.split()
            
            
if __name__  ==  "__main__":
    print mySplit("test=hello","=")
    print mySplit("    test     =hello","=")
    print mySplit("    test     ==hello    ","=")
    print mySplit("    test     ==hello    ")
    print mySplit("    test     ==hello    ")

    
