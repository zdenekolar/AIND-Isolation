"""This file contains all the classes you must complete for this project.

You can use the test cases in agent_test.py to help during development, and
augment the test suite with your own test cases to further test your code.

You must test your agent's strength against a set of agents with known
relative strength using tournament.py and include the results in your report.
"""
import random
from math import sqrt
import sys

class Timeout(Exception):
    """Subclass base exception for code clarity."""
    pass


def custom_score(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """


    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    # Check if we can win in one move.
    # if one_step_ko(game, player):
    #     return float('inf')

    return heuristic_three(game, player)



def heuristic_one(game, player):
    '''
    This heuristic considers the next steps, i.e. if we make a move what is our situation.
    Further it calculates the difference in available moves for both players.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    '''

    score = 0
    for move in game.get_legal_moves():
        next_step = game.forecast_move(move)
        my_moves = len(next_step.get_legal_moves(player))
        opponent_moves = len(next_step.get_legal_moves(game.get_opponent(player)))
        score += my_moves - opponent_moves
    return score


def heuristic_two(game, player):
    '''
    Chase the opponent and minimize his options. 64.29%

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    '''

    score = 0
    my_moves_total = 0
    for move in game.get_legal_moves():
        next_step = game.forecast_move(move)
        my_moves = len(next_step.get_legal_moves(player))
        opponent_moves = len(next_step.get_legal_moves(game.get_opponent(player)))
        score -= opponent_moves
        my_moves_total += my_moves

    if my_moves_total > 0:
        return score
    else:
        return float('-inf')


def heuristic_three(game, player):
    '''
    Combines heuristic one and two and with decreasing number of blank spaces we aim to block the opponent.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    '''
    total_spaces = 7*7
    remaining_spaces = len(game.get_blank_spaces())
    coefficient = remaining_spaces / total_spaces
    return coefficient * heuristic_one(game, player) + (1 - coefficient) * heuristic_two(game, player)

def heuristic_four(game, player):
    '''
    Return weighted average of scores, similar to F1 score.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    '''

    legal_moves = game.get_legal_moves()
    my_moves = 0
    blocked_opp_moves = 0
    for move in legal_moves:
        next_step = game.forecast_move(move)
        my_moves += len(next_step.get_legal_moves(player))/8
        blocked_opp_moves += (8-len(next_step.get_legal_moves(game.get_opponent(player))))/8
    score = 2*(my_moves * blocked_opp_moves) / (my_moves + blocked_opp_moves)
    return score

def heuristic_five(game, player):
    '''
    Check positions that are awkward for the opponent and pick the one that gives you most steps.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    '''

    return calculate_distance(game, player)


def calculate_distance(game, player):
    '''

    Return euclidian or manhattan distance.
    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    '''

    my_location = game.get_player_location(player)
    opponent_location = game.get_player_location(game.get_opponent(player))
    distance_x = abs(my_location[0] - opponent_location[0])
    distance_y = abs(my_location[1] - opponent_location[1])

    euclidean = sqrt(distance_x^2 + distance_y^2)
    manhattan = distance_x + distance_y

    return -euclidean

def one_step_ko(game, player):
    '''
    Checks if we can kill the oponent in one move.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    '''
    for move in game.get_legal_moves(player):
        next_step = game.forecast_move(move)
        opponent_moves = len(next_step.get_legal_moves(next_step.get_opponent(player)))
        if opponent_moves == 0:
            return True
    return False

class CustomPlayer:
    """Game-playing agent that chooses a move using your evaluation function
    and a depth-limited minimax algorithm with alpha-beta pruning. You must
    finish and test this player to make sure it properly uses minimax and
    alpha-beta to return a good move before the search time limit expires.

    Parameters
    ----------
    search_depth : int (optional)
        A strictly positive integer (i.e., 1, 2, 3,...) for the number of
        layers in the game tree to explore for fixed-depth search. (i.e., a
        depth of one (1) would only explore the immediate sucessors of the
        current state.)

    score_fn : callable (optional)
        A function to use for heuristic evaluation of game states.

    iterative : boolean (optional)
        Flag indicating whether to perform fixed-depth search (False) or
        iterative deepening search (True).

    method : {'minimax', 'alphabeta'} (optional)
        The name of the search method to use in get_move().

    timeout : float (optional)
        Time remaining (in milliseconds) when search is aborted. Should be a
        positive value large enough to allow the function to return before the
        timer expires.
    """

    def __init__(self, search_depth=3, score_fn=custom_score,
                 iterative=True, method='minimax', timeout=10.):
        self.search_depth = search_depth
        self.iterative = iterative
        self.score = score_fn
        self.method = method
        self.time_left = None
        self.TIMER_THRESHOLD = timeout

    def get_move(self, game, legal_moves, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        This function must perform iterative deepening if self.iterative=True,
        and it must use the search method (minimax or alphabeta) corresponding
        to the self.method value.

        **********************************************************************
        NOTE: If time_left < 0 when this function returns, the agent will
              forfeit the game due to timeout. You must return _before_ the
              timer reaches 0.
        **********************************************************************

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        legal_moves : list<(int, int)>
            A list containing legal moves. Moves are encoded as tuples of pairs
            of ints defining the next (row, col) for the agent to occupy.

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """

        self.time_left = time_left

        # Perform any required initializations, including selecting an initial
        # move from the game board (i.e., an opening book), or returning
        # immediately if there are no legal moves
        if not legal_moves:
            return (-1, -1)

        # Variable to store the best move so far
        move = None

        try:
            # Iterative deepening
            if self.iterative:
                if self.method == 'minimax':
                    for depth in range(sys.maxsize):
                        _, move = self.minimax(game, depth, maximizing_player=True)
                elif self.method == 'alphabeta':
                    for depth in range(sys.maxsize):
                        _, move = self.alphabeta(game, depth, maximizing_player=True)
                else:
                    raise ValueError('Unknown method {}'.format(self.method))
                    # return move
            # Breadth search
            else:
                if self.method == 'minimax':
                    _, move = self.minimax(game, self.search_depth)
                elif self.method == 'alphabeta':
                    _, move = self.alphabeta(game, self.search_depth)
                else:
                    raise ValueError('Unknown method {}'.format(self.method))

        except Timeout:
            # Handle any actions required at timeout, if necessary
            pass

        # Return the best move from the last completed search iteration
        return move

    def minimax(self, game, depth, maximizing_player=True):
        """Implement the minimax search algorithm as described in the lectures.

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        maximizing_player : bool
            Flag indicating whether the current search depth corresponds to a
            maximizing layer (True) or a minimizing layer (False)

        Returns
        -------
        float
            The score for the current search branch

        tuple(int, int)
            The best move for the current branch; (-1, -1) for no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project unit tests; you cannot call any other
                evaluation function directly.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise Timeout()

        # START
        legal_moves = game.get_legal_moves()

        if depth == 0:
            return self.score(game, self), (-1, -1)

        if not legal_moves:
            return game.utility(self), (-1, -1)

        best_move = None
        if maximizing_player:
            best_score = float('-inf')
            for move in legal_moves:
                score, _ = self.minimax(game.forecast_move(move), depth-1, maximizing_player=False)
                if score > best_score:
                    best_score, best_move = score, move

        else:
            best_score = float('inf')
            for move in legal_moves:
                score, _= self.minimax(game.forecast_move(move), depth-1, maximizing_player=True)
                if score < best_score:
                    best_score, best_move = score, move

        return best_score, best_move
        # END


    def alphabeta(self, game, depth, alpha=float("-inf"), beta=float("inf"), maximizing_player=True):
        """Implement minimax search with alpha-beta pruning as described in the
        lectures.

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        alpha : float
            Alpha limits the lower bound of search on minimizing layers

        beta : float
            Beta limits the upper bound of search on maximizing layers

        maximizing_player : bool
            Flag indicating whether the current search depth corresponds to a
            maximizing layer (True) or a minimizing layer (False)

        Returns
        -------
        float
            The score for the current search branch

        tuple(int, int)
            The best move for the current branch; (-1, -1) for no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project unit tests; you cannot call any other
                evaluation function directly.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise Timeout()

        # START
        if depth == 0:
            return self.score(game, self), (-1, -1)

        legal_moves = game.get_legal_moves()

        if not legal_moves:
            return game.utility(self), (-1, -1)

        best_move = None

        if maximizing_player:
            best_score = float('-inf')
            for move in legal_moves:
                score, _ = self.alphabeta(game.forecast_move(move), depth-1, alpha=alpha, beta=beta, maximizing_player=False)
                if score > best_score:
                    best_score, best_move = score, move
                # Prune if possible
                if best_score >= beta:
                    return best_score, best_move
                alpha = max(alpha, best_score)
        else:
            best_score = float('inf')
            for move in legal_moves:
                score, _ = self.alphabeta(game.forecast_move(move), depth-1, alpha=alpha, beta=beta, maximizing_player=True)
                if score < best_score:
                    best_score, best_move = score, move
                # Prune if possible
                if best_score <= alpha:
                    return best_score, best_move
                beta = min(beta, best_score)
        return best_score, best_move
        # END

