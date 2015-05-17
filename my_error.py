#! /usr/bin/env python
# -*- coding: utf-8 -*-
#editor: ono

class MyError(Exception) :
    def __init__(self, expr='myerror.expr',msg='myerror.msg'):
        self.expr = expr
        self.msg = msg
        
    def __str__(self):
        print self.expr,self.msg,

