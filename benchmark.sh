#!/usr/bin/env sh

NGAMES=${NGAMES:-8}
NTHREADS=${NTHREADS:-2}

printf "Running $NGAMES games in $NTHREADS threads\n"

seq $NGAMES | xargs -I% -P$NTHREADS sh -c 'python runner.py -a '$1' -s$(od -An -N2 -tu2 /dev/random)' | grep -v '^\(Algorithm\|\-\+\)'
