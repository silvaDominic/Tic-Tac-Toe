"""
------------------- Monte Carlo Tic-Tac-Toe -------------------

How to start and stop the game:

Click the 'play' button at the top left corner of
CodeSkulptor to start the game. A popout window will appear
with a menu. Simply click the menu to begin.

To stop, exit the popout window and click the 'reset'
button (to the right of the folder icon).

Controls:

Use mouse to click on empty grid spaces.
Reset game by clicking 'New Game'.

For the curious:
    Feel free to skim over the code and see what's going on.
    If you'd like to change the code up be sure to save
    your work by clicking the floppy disk in the left
    corner of CodeSkulptor and then saving the url somewhere.
    This will NOT affect the version that is presented to you
    from the website.

    - Adjusting NTRIALS constant will essentially change the difficulty
     (don't go over 100)
    - Adjusting TTT_SIZE constant will change size of grid (not advised)
"""

import random
import poc_ttt_gui
import poc_ttt_provided as provided

# Constants for Monte Carlo simulator

NTRIALS = 50 	# Number of trials to run
SCORE_CURRENT = 1.0 	# Score for squares played by the current player
SCORE_OTHER = 1.0 	# Score for squares played by the other player
TTT_SIZE = 3 	# Height/Width of board (anything over 3 isn't much fun)

def mc_trial(board, player):
    """
    Using the currnet board determine next move through random selection of
    of empty cells. Completed the move, switch players and
    continues until one of the players wins.

    Arguments:
    board (list): a 2D array representing the game board
    player (int): represents the AI player
    """
    while board.check_win() == None:

        # Find all empty squares
        available_moves = board.get_empty_squares()

        # Randomly select an available position
        next_move = random.choice(available_moves)

        # Make the move for current player
        board.move(next_move[0], next_move[1], player)

        # Switch players
        player = provided.switch_player(player)

        # Check for win, end game if true
        if board.check_win() != None:
            break

def mc_update_scores(scores, board, player):
    """
    Updates the scores based on player and outcome of previous move

    Arguments:
    scores (list): a 2D array representation of the score computed scores
                   for each square.
    board (list): a 2D array representing the game board
    player (int): represents the AI player
    """
    # Move through TTT board
    for row in range(board.get_dim()):
        for col in range(board.get_dim()):

            current_square = board.square(row, col)

            # If current player got the win, update scores.
            # Current player +1, other player -1
            if board.check_win() == player:
                if current_square == player:
                    scores[row][col] += SCORE_CURRENT
                elif current_square == provided.EMPTY:
                    scores[row][col] += 0
                else:
                    scores[row][col] -= SCORE_OTHER

            # If the other player got the win, update scores.
            # Current player -1, other palyer +1
            elif board.check_win() == provided.switch_player(player):
                if current_square == player:
                    scores[row][col] -= SCORE_CURRENT
                elif current_square == provided.EMPTY:
                    scores[row][col] += 0
                else:
                    scores[row][col] += SCORE_OTHER

            # If a tie, update scores with 0
            elif board.check_win() == provided.DRAW:
                    scores[row][col] += 0


def get_best_move(board, scores):
    """
    Calculates the 'best' move based on number of available squares.

    Arguments:
    board (list): a 2D array representing the game board
    scores (list): a 2D array representation of the score computed scores
                   for each square.

    Returns:
    random.choice(available_moves) (tuple): random max scoring position
    """
    square_values = {}
    available_moves = []

    # Find all empty squares
    available_squares = board.get_empty_squares()

    # Set score for each available square
    for square in available_squares:
        square_values[square] = scores[square[0]][square[1]]

    # Determine if value is a max value and add to available moves if it is
    for value in square_values:
        if square_values[value] == max(square_values.values()):
            available_moves.append(value)

    # Randomly (hence 'best') select next move if available
    if len(available_moves) > 0:
        return random.choice(available_moves)

def mc_move(board, player, trials):
    '''
    Determine next position for the machine player using the current board.

    Arguments:
    board (list): a 2D array representing the game board
    player (int): represents the AI player
    trials (int): the number of trials to be run for calculating the next move

    Returns:
    get_best_move(board, scores) (tuple): the position of the next best move for the AI
    '''
    # Reset all scores to 0
    scores = [[0 for dummy_col in range(board.get_dim())] for dummy_row in range(board.get_dim())]

    # Create the starting score board
    for dummy_index in range(trials):

        # Clone original board
        dummy_board = board.clone()

        # Start trial with AI player going first
        mc_trial(dummy_board, player)

        mc_update_scores(scores, dummy_board, player)

    return get_best_move(board, scores)

poc_ttt_gui.run_gui(TTT_SIZE, provided.PLAYERX, mc_move, NTRIALS, False)