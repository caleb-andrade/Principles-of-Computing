"""
Monte Carlo Tic-Tac-Toe Player
"""

import random
import poc_ttt_gui
import poc_ttt_provided as provided
#import user40_bUjUwEE3EI_29 as testsuite

# Constants for Monte Carlo simulator
# You may change the values of these constants as desired, but
#  do not change their names.
NTRIALS = 10      # Number of trials to run
SCORE_CURRENT = 1 # Score for squares played by the current player
SCORE_OTHER = 1   # Score for squares played by the other player
    
# Add your functions here.

def mc_trial(board, player):
    """ 
    takes a current board and the next player to move
    """
    while board.check_win() == None:
        [row, col] = random.choice(board.get_empty_squares()) 
        board.move(row, col, player)
        player = provided.switch_player(player)

# test visually mc_trial 10 times
#testsuite.mc_trial_run_suite(mc_trial, 10)

def mc_update_scores(scores, board, player):
    """ 
    takes a grid of scores, a board from a completed game,
    which player the machine player is and scores the completed
    board and updates the scores grid 
    """
    value = [SCORE_CURRENT, SCORE_OTHER]
    winner = board.check_win()
    if winner == provided.DRAW:
        return None
    elif winner == player:
        p_val = value[player-2]
        np_val = -value[player-3]
    else:
        p_val = -value[player-2]
        np_val = value[player-3]
        
    for row in range(board.get_dim()):
        for col in range(board.get_dim()):
            if board.square(row, col) == player:
                scores[row][col] += p_val
            elif board.square(row, col) != provided.EMPTY:
                scores[row][col] += np_val
                    
# test mc_update_scores function
# testsuite.mc_update_scores_run_suite(mc_update_scores, SCORE_OTHER, SCORE_CURRENT)

def get_best_move(board, scores):
    """
    takes a board and a grid of scores, determining all the empty
    squares with maximum value, and returning randomly one of them
    """
    empty = board.get_empty_squares()
    if len(empty) > 0:
        random.shuffle(empty)
        temp = empty[0]
        for idx in range(len(empty)):
            if scores[empty[idx][0]][empty[idx][1]] > scores[temp[0]][temp[1]]:
                temp = empty[idx]
        return temp
    else:
        pass

# test mc_get_best_move function
#testsuite.mc_get_best_move_run_suite(mc_get_best_move)

def mc_move(board, player, ntrials):
    """
    Takes a current board, machine player and number of trials to run,
    it returns a move (row, col) for the machine to play, using Monte
    Carlo simulation
    """
    dim = board.get_dim()
    scores = [[0 for dummy_row in range(dim)] for dummy_col in range(dim)]
    if len(board.get_empty_squares()) > 0:
        for dummy_trial in range(ntrials):
            tboard = board.clone()
            mc_trial(tboard, player)
            mc_update_scores(scores, tboard, player)
        return get_best_move(board, scores)
         
    else:
        pass

# test mc_move function
# testsuite.mc_move_run_suite(mc_move)

# Test game with the console or the GUI.  Uncomment whichever 
# you prefer.  Both should be commented out when you submit 
# for testing to save time.

#provided.play_game(mc_move, NTRIALS, False)        
#poc_ttt_gui.run_gui(3, provided.PLAYERX, mc_move, NTRIALS, False)
