#!/usr/bin/env sh

NGAMES=8
NTHREADS=2

echo "Running $NGAMES games in $NTHREADS threads"

for i in $(seq 1 $NGAMES); do echo $RANDOM; done | xargs -I% -P$NTHREADS python runner.py -a $1 -s% | grep -v '^\(Algorithm\|\-\+\)'
#parallel -j$NTHREADS -n0 python runner.py -a $1 -s'$RANDOM' ::: $(seq 1 $NGAMES) | grep -v '^\(Algorithm\|\-\+\)'
#parallel -j$NTHREADS -n0 python runner.py -a $1 -s'$RANDOM' ::: $(seq 1 $NGAMES) | awk '!/^(Algorithm|-+)/' -
# alternative to $RANDOM : $(od -An -N2 -tu2 /dev/urandom)
