"""
Tic Tac Toe Player with Minimax and Alpha-Beta Pruning
"""

import math
import copy

# Constants for players
X = "X"
O = "O"
EMPTY = None

def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]

def player(board):
    """
    Returns player who has the next turn on a board.
    """
    x_count = sum(row.count(X) for row in board)
    o_count = sum(row.count(O) for row in board)
    return X if x_count <= o_count else O

def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    return {(i, j) for i in range(3) for j in range(3) if board[i][j] == EMPTY}

def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if action not in actions(board):
        raise ValueError("Invalid move")

    new_board = copy.deepcopy(board)
    new_board[action[0]][action[1]] = player(board)
    return new_board

def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    for i in range(3):
        # Check rows and columns
        if board[i][0] == board[i][1] == board[i][2] and board[i][0] is not None:
            return board[i][0]
        if board[0][i] == board[1][i] == board[2][i] and board[0][i] is not None:
            return board[0][i]
    
    # Check diagonals
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] is not None:
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] is not None:
        return board[0][2]

    return None

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    return winner(board) is not None or all(cell is not EMPTY for row in board for cell in row)

def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    win = winner(board)
    if win == X:
        return 1
    elif win == O:
        return -1
    return 0

def minimax(board, alpha=-math.inf, beta=math.inf):
    """
    Returns the optimal action for the current player using Alpha-Beta Pruning.
    """
    if terminal(board):
        return None

    def max_value(board, alpha, beta):
        if terminal(board):
            return utility(board)

        v = -math.inf
        for action in actions(board):
            move_score = min_value(result(board, action), alpha, beta)  # Only return integer scores
            v = max(v, move_score)
            alpha = max(alpha, v)
            if alpha >= beta:
                break  # Prune
        return v  # Return only the score

    def min_value(board, alpha, beta):
        if terminal(board):
            return utility(board)

        v = math.inf
        for action in actions(board):
            move_score = max_value(result(board, action), alpha, beta)  # Only return integer scores
            v = min(v, move_score)
            beta = min(beta, v)
            if alpha >= beta:
                break  # Prune
        return v  # Return only the score

    current_player = player(board)
    best_move = None
    if current_player == X:
        best_score = -math.inf
        for action in actions(board):
            move_score = min_value(result(board, action), alpha, beta)  # Get score
            if move_score > best_score:
                best_score = move_score
                best_move = action
            alpha = max(alpha, best_score)
    else:  # O's turn
        best_score = math.inf
        for action in actions(board):
            move_score = max_value(result(board, action), alpha, beta)  # Get score
            if move_score < best_score:
                best_score = move_score
                best_move = action
            beta = min(beta, best_score)

    return best_move  # Return the best move, not the score
