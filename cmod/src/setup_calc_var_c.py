from distutils.core import setup, Extension
import os

os.environ['CC'] = 'icc -pthread'
module1 = Extension('calcVarC',
                    sources = ['calc_var_c.cpp'])

setup(name = 'calcVarC',
      version = '1.0',
      description = 'Caluclating Variance from Trajctory-File.',
      ext_modules = [module1])

