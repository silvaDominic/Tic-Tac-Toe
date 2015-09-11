"""
Monte Carlo Tic-Tac-Toe Player
"""

import random
import poc_ttt_gui
import poc_ttt_provided as provided

# Constants for Monte Carlo simulator
# You may change the values of these constants as desired, but
# do not change their names.
NTRIALS = 20        # Number of trials to run
SCORE_CURRENT = 2.0 # Score for squares played by the current player
SCORE_OTHER = 1.0   # Score for squares played by the other player

board = provided.TTTBoard(3)

# Add your functions here.
def mc_trial(board, player):
    empty_square = []
    trial_board = board.clone()
    while trial_board.check_win() == None:
        empty_squares = trial_board.get_empty_squares()
        current_square = empty_squares.pop(random.randrange(len(empty_squares)))
        trial_board.move(current_square[0], current_square[1], player)
        player = provided.switch_player(player)
    
    print "TRIAL BOARD:"
    print trial_board
    return trial_board


def mc_update_scores(scores, board, player):
    for row in range(board.get_dim()):
        for col in range(board.get_dim()):
            if board.check_win() == provided.PLAYERX:
                if board.square(row, col) == provided.PLAYERX:
                    scores[row][col] += SCORE_CURRENT 
                elif board.square(row, col) == provided.PLAYERO:
                    scores[row][col] -= SCORE_OTHER 
            elif board.check_win() == provided.PLAYERO:
                if board.square(row, col) == provided.PLAYERO:
                    scores[row][col] += SCORE_CURRENT
                elif board.square(row, col) == provided.PLAYERX:
                    scores[row][col] -= SCORE_OTHER
                    
def get_best_score(board, scores):
    best_move = []
    max_score = 0
    for row in range(board.get_dim()):
        for col in range(board.get_dim()):
            if board.square(row, col) == provided.EMPTY:
                max_score += scores[row][col]
                best_move.append([row, col])

                
    print "BEST MOVE:"            
    print max_score_loc
    print "MAX SCORE"
    print max_score
    
    return random.choice(best_move)


def mc_move(board, player, trials):
    scores = [[0 for col in range(board.get_dim())]for row in range(board.get_dim())]
    for trials in range(trials):
        dummy_board = mc_trial(board, player)
        if board.check_win() == None:
            mc_update_scores(scores, dummy_board, player)
            best_move = get_best_score(board, scores)          

        elif board.check_win() == provided.DRAW:
            return provided.DRAW
        
    return best_move


# Test game with the console or the GUI.  Uncomment whichever 
# you prefer.  Both should be commented out when you submit 
# for testing to save time.

provided.play_game(mc_move, NTRIALS, False)        
poc_ttt_gui.run_gui(3, provided.PLAYERX, mc_move, NTRIALS, False)