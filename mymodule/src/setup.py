#! /usr/bin/env python
from distutils.core import setup,Extension
import os

from distutils.core import setup,Extension

from distutils.command import build_py, build_ext
from distutils.errors import DistutilsPlatformError
from distutils.unixccompiler import UnixCCompiler

class MyIntelCCompiler(UnixCCompiler):
    compiler_type = "intel"
    executables = dict(UnixCCompiler.executables)
    executables.update({
        "compiler"      : ["icc", "-O3", "-xhost", "-no-prec-div","-fpic"],
        "compiler_so"   : ["icc", "-O3", "-xhost", "-no-prec-div","-fpic"],
        "compiler_cxx"  : ["icc", "-O3", "-xhost", "-no-prec-div","-fpic"],
        "linker_so"     : ["icc", "-shared"],
        "linker_exe"    : ["icc"],
    })

    
class matrix_build_ext(build_ext.build_ext):
    def run(self):
        import distutils.ccompiler
        def wrap_new_compiler(func):
            def _wrap_new_compiler(*args, **kwargs):
                try: return func(*args, **kwargs)
                except DistutilsPlatformError:
                    return MyIntelCCompiler(None, kwargs["dry_run"], kwargs["force"])
            return _wrap_new_compiler
        distutils.ccompiler.new_compiler = wrap_new_compiler(distutils.ccompiler.new_compiler)
        self.compiler = "intel"
        build_ext.build_ext.run(self)
        
module1=Extension("matrixmodule",["cal_matrix.c"],extra_link_args=["-fPIC"])
    
setup(name='matrixmodule',version='1.0',
      cmdclass={"build_ext":matrix_build_ext},
      description='calculate matrix',
      ext_modules=[module1])
