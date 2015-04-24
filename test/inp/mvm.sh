#!/bin/sh

#$ -S /bin/sh
#$ -cwd
#$ -V
#$ -N mvm
#$ -o /rei_fs1/ono/mvmtrunk/log/mvm.log -e /rei_fs1/ono/mvmtrunk/mvm.err
#$ -q all.q
#$ -pe smp  4


OMP_NUM_THREADS=4
/rei_fs1/ono/mvmtrunk/cafemol /rei_fs1/ono/mvmtrunk/inp/mvm_mon.inp

