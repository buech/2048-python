#!/usr/bin/env sh

NGAMES=${NGAMES:-8}
NTHREADS=${NTHREADS:-2}

printf "Running $NGAMES games in $NTHREADS threads\n"

for i in $(seq 1 $NGAMES); do printf "$RANDOM\n"; done | xargs -I% -P$NTHREADS python runner.py -a $1 -s% | grep -v '^\(Algorithm\|\-\+\)'
