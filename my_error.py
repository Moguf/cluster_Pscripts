#! /usr/bin/env python
# -*- coding: utf-8 -*-
#editor: ono

class MyError(Exception) :
    def __init__(self, expr='myerror.expr',msg='myerror.msg'):
        self.expr = expr
        self.msg = msg
        
    def __str__(self):
        print self.expr,self.msg,


class InputError(Exception):
    """Exception raised for errors in the input.

    Attributes:
        expr -- input expression in which the error occurred
        msg  -- explanation of the error
    """

    def __init__(self, expr, msg):
        self.expr = expr
        self.msg = msg
    def __str__(self):
        print self.expr,
        print self.msg,
