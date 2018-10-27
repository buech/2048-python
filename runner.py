#!/usr/bin/env python

"""
Common run script to apply algorithm to solve 2048 puzzle.
Algorithms are read from subdirectory algorithms and have to supply a function getNextMoves(matrix), which should return a list of next moves.
"""

from __future__ import division, print_function
import os, sys
import logging
import argparse
import importlib
import time
import numpy as np
try:
    input = raw_input
except NameError:
    pass

import puzzle

def initializeGame(seed = None, showGUI = True):
    return puzzle.GameGrid(is_ai_game=True, useSeed = seed, showGUI = showGUI)

def printSummary(results):
    order = list(results.keys())
    order.sort(key = lambda x: results[x]["Nmoves"], reverse=True)
    order.sort(key = lambda x: results[x]["maxTile"],  reverse=True)
    order.sort(key = lambda x: results[x]["score"],  reverse=True)
    header = ["Algorithm", "Score", "Tile", "Moves", "Elapsed", "Mps"]
    lines = []
    for alg in order:
        res = results[alg]
        lines.append([alg, res["score"], res["maxTile"], res["Nmoves"], res["total_time"], res["mps"]])
    line_format = ""
    for val, head in zip(lines[0], header):
        line_format += ("{:<" if line_format=="" else "{:>") + str(max(len(str(val)), len(head)) + 2) + "}"
    print(line_format.format(*header))
    for line in lines:
        print(line_format.format(*line))

def print_gamegrid(matrix):
    print(4 * "+-----" + "+")
    for row in matrix:
        print((4 * "|{:5d}" + "|").format(*row))
        print(4 * "+-----" + "+")

def main(argv):
    parser = argparse.ArgumentParser( description = 'Script that applies a provided algorithm to solve 2048 puzzle.' ,
                                      formatter_class = argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument( "-d", '--debug',       default = False, action='store_true', help = 'Print in debug output' )
    parser.add_argument(       "--gui",         default = False, action="store_true", help = "Shows graphical interface with current status")
    parser.add_argument(       "--ascii",       default = False, action="store_true", help = "Prints current status to terminal")
    parser.add_argument(       "--sleep",       default = 0,  type=float,             help = "Time to wait between moves [s].")
    parser.add_argument( "-s", "--seed",        default = None,                       help = "Set seed to fixed value.")
    parser.add_argument( "-a", "--algorithm",   default = "example",                  help = "Which algorithms to run. multiple algorithms can be split by ','.")
    args = parser.parse_args(argv)

    if args.debug:
        logging.basicConfig(level=logging.DEBUG)
        #logging.info("Set log level to DEBUG")
    else:
        logging.basicConfig(level=logging.INFO)
        #logging.info("Set log level to INFO")

    results = {}

    total_time = 0
    for algorithm in args.algorithm.split(","):

        logging.debug("Initializing game")
        gamegrid = initializeGame(seed = args.seed, showGUI = args.gui)

        logging.debug("loading algorithm " + algorithm)
        alg = importlib.import_module("algorithms."+algorithm)

        logging.debug("starting loop")
        total_start = time.time()
        time_per_move = 0
        done = False
        Nmoves = 0
        NnoMoves = 0
        while (not done):
            logging.debug("Getting next move from algorithm")
            move_start = time.time()
            moves = alg.getNextMoves(gamegrid.matrix)
            move_stop = time.time()
            if not type(moves) == list:
                moves = [moves]
            time_per_move += (move_stop - move_start) / len(moves)
            for move in moves:
                didMove = gamegrid.ai_move(move)
                if not didMove:
                    NnoMoves += 1
                    if NnoMoves > 4:
                        done = True
                        break
                    continue

                Nmoves += 1
                NnoMoves = 0

                time.sleep(args.sleep)

                # update game grid
                if args.gui:
                    gamegrid.update()
                if args.ascii:
                    print("status: (Score = {})".format(gamegrid.calc_score()))
                    print_gamegrid(gamegrid.matrix)

                if gamegrid.game_over():
                    done = True
                    break

        total_stop = time.time()
        total_time = round(total_stop - total_start, 3)
        mps = round(Nmoves / time_per_move, 3)
        score = gamegrid.calc_score()
        maxTile = np.max(gamegrid.matrix)
        results[algorithm] = {"score": score, "maxTile": maxTile, "Nmoves": Nmoves, "mps": mps, "total_time": total_time}
        #print("GAME OVER. Final score: {:8.0f} after {:5.0f} moves (algorithm: {}).".format(score, Nmoves, algorithm))
        if args.gui:
            input("Press Enter to terminate.")

    printSummary(results)

if __name__ == "__main__":
    main( sys.argv[1:] )
