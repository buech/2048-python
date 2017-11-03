import puzzle
import time

UP = 1
DOWN= 2
RIGHT = 3
LEFT = 4

SHOW_GUI = True

gamegrid = puzzle.GameGrid(is_ai_game=True)

while (True):
    # AI logic
    done = gamegrid.ai_move(RIGHT) 
    if not done:
        done = gamegrid.ai_move(DOWN)
    if not done:
        done = gamegrid.ai_move(LEFT)
    if not done:
        gamegrid.ai_move(UP)
        gamegrid.ai_move(DOWN)

    # update game grid
    if SHOW_GUI: 
        gamegrid.update()
        # time.sleep(0.005)

        print "status: (Score = {})".format(gamegrid.calc_score())
        for line in gamegrid.matrix:
            print line
    if gamegrid.game_over():
        print "Final score: " + str(gamegrid.calc_score())
        break

if SHOW_GUI:
    gamegrid.update()
    raw_input("Press Enter to terminate.")
