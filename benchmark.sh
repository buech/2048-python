#!/usr/bin/env sh

NGAMES=8
NTHREADS=2

echo "Running $NGAMES games in $NTHREADS threads, behold!"

#parallel -j$NTHREADS -n0 python runner.py -a $1 -s'$(od -An -N2 -tu2 /dev/urandom)' ::: $(seq 1 $NGAMES) | grep -v '^\(Algorithm\|\-\+\)'
parallel -j$NTHREADS -n0 python runner.py -a $1 -s'$(od -An -N2 -tu2 /dev/urandom)' ::: $(seq 1 $NGAMES) | awk '!/^(Algorithm|-+)/' -
