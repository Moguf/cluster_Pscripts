#! /usr/bin/env python
from distutils.core import setup,Extension
import os

#os.environ["CC"] = "icc -pthread"
#args=["-O3"]
#link=["static"]
#module=Extension("myadd",["rmsf.c"],extra_compile_args=args,extra_link_args=link)
module=Extension("myadd",["rmsf.c"])#,extra_compile_args=args,extra_link_args=link)


setup(name='myadd',
      version='1.0',
      ext_modules=[module]
      )

