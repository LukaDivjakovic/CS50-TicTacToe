"""
Tic Tac Toe Player
"""
import copy
import math


class ImpossibleActionError(Exception):
    pass


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

    cX = 0
    cO = 0
    cE = 0
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == X:
                cX += 1
            if board[i][j] == O:
                cO += 1
    if cX > cO:
        return O
    else:
        return X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    set_actions = set()
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == EMPTY:
                set_actions.add((i, j))

    return set_actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """

    new_board = copy.deepcopy(board)

    try:
        if new_board[action[0]][action[1]] is not EMPTY:
            raise ImpossibleActionError
        else:
            new_board[action[0]][action[1]] = player(board)
    except ImpossibleActionError:
        print("Invalid action on board")
        return board
    finally:
        return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # horizontal
    for i in range(len(board)):
        if board[i][0] == board[i][1] == board[i][2] and not EMPTY:
            return board[i][0]
    # vertical
    for j in range(len(board)):
        if board[0][j] == board[1][j] and board[0][j] == board[2][j] and not EMPTY:
            return board[0][j]

    # diagonal
    if board[0][0] == board[1][1] == board[2][2] and not EMPTY:
        return board[0][0]
    # diagonal
    if board[2][0] == board[1][1] == board[0][2] and not EMPTY:
        return board[2][0]
    else:
        return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """

    if winner(board) is not None or (not any(EMPTY in sublist for sublist in board) and winner(board) is None):
        return True
    else:
        return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) is X:
        return 1
    if winner(board) is O:
        return -1
    else:
        return 0


def max_value(board):
    if terminal(board):
        return utility(board), None

    value = float('-inf')
    move = None

    for action in actions(board):
        tempValue, tempMove = min_value(result(board, action))

        if tempValue > value:
            value = tempValue
            move = action
            if value == 1:
                return value, move

    return value, move


def min_value(board):
    if terminal(board):
        return utility(board), None

    value = float('inf')
    move = None

    for action in actions(board):
        tempValue, tempMove = max_value(result(board, action))
        if tempValue < value:
            value = tempValue
            move = action
            if value == -1:
                return value, move

    return value, move


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """

    if terminal(board):
        return None

    if player(board) == X:
        value, move = max_value(board)
        return move
    else:
        value, move = min_value(board)
        return move
