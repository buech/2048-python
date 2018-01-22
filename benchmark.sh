#!/usr/bin/env sh

NGAMES=8
NTHREADS=2
NLOOPS=$(expr $NGAMES / $NTHREADS)

if grep -P > /dev/null 2>&1; then
	GREP='grep -P'
else
	GREP='pcregrep'
fi

echo "Running $(expr $NLOOPS \* $NTHREADS) games in $NTHREADS threads, behold!"

for i in $(seq 1 $NLOOPS); do
	parallel -n0 python runner.py -a $1 -s'$(od -An -N2 -tu2 /dev/urandom)' ::: $(seq 1 $NTHREADS) | $GREP '^(?!(Algorithm|\-\-))'
done
