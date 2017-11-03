#!/usr/bin/env python

"""
Common run script to apply algorithm to solve 2048 puzzle.
Algorithms are read from subdirectory algorithms and have to supply a function getNextMoves(matrix), which should return a list of next moves.
"""

import os, sys
import logging
import argparse
import importlib
import pprint
import time
import tabulate

import puzzle

def initializeGame():
    return puzzle.GameGrid(is_ai_game=True)

def main(argv):
    parser = argparse.ArgumentParser( description = 'Script that applies a provided algorithm to solve 2048 puzzle.' )
    parser.add_argument( "-d", '--debug',       default = False, action='store_true', help = 'print in debug output' )
    parser.add_argument(       "--gui",         default = False, action="store_true", help = "shows graphical interface with current status")
    parser.add_argument(       "--ascii",       default = False, action="store_true", help = "prints current status to terminal")
    parser.add_argument( "-s", "--sleep",       default = 0,                          help = "time to wait between moves [s].")
    parser.add_argument( "-a", "--algorithm",   default = "example",                  help = "which algorithm to run")
    args = parser.parse_args(argv)

    if args.debug:
        logging.basicConfig(level=logging.DEBUG)
        logging.info("Set log level to DEBUG")
    else:
        logging.basicConfig(level=logging.INFO)
        logging.info("Set log level to INFO")

    logging.debug("Initializing game")
    gamegrid = initializeGame()

    alg = importlib.import_module("algorithms."+args.algorithm)

    done = False
    Nmoves = 0
    while (not done):

        moves = alg.getNextMoves(gamegrid.matrix)
        if not type(moves) == list:
            moves = [moves]
        for move in moves:
            gamegrid.ai_move(move)
            Nmoves += 1

            time.sleep(args.sleep)

            # update game grid
            if args.gui: 
                gamegrid.update()
            if args.ascii:
                print "status: (Score = {})".format(gamegrid.calc_score())
                print tabulate.tabulate(gamegrid.matrix, tablefmt="grid")

            if gamegrid.game_over():
                done = True
                break

    print "Final score: {} after {} moves.".format(gamegrid.calc_score(), Nmoves)
    if args.gui:
        raw_input("Press Enter to terminate.")



if __name__ == "__main__":
    main( sys.argv[1:] )
