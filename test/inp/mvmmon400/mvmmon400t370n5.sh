#!/bin/sh

#$ -S /bin/sh
#$ -cwd
#$ -V
#$ -N mvmmon400t370n5
#$ -o /home/ono/misc/cluster_pscripts/test/inp/mvmmon400/log/mvmmon400t370n5.log
#$ -e /home/ono/misc/cluster_pscripts/test/inp/mvmmon400/err/mvmmon400t370n5.err
#$ -q all.q
#$ -pe smp 1

OMP_NUM_THREADS=1
/home/ono/misc/cluster_pscripts/test/cafemol /home/ono/misc/cluster_pscripts/test/inp/mvmmon400/mvmmon400t370n5.inp
