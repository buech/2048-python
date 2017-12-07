#!/usr/bin/env sh

parallel -n0 'python runner.py -a expecti_fort -s$RANDOM' ::: {1..4}
