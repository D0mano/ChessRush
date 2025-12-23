from utils.functions import *
from utils.constante import *
import random


def is_safe_move_simu(board, original_x, original_y, des_x, des_y, color):
    """
    Check if a move is safe (doesn't leave the king in check) in a simulated board state.
    Uses a shallow copy to prevent modifying the actual simulation board during the check.

    Args:
        board (list): A list representing the board
        original_x (int): Origin x coordinate
        original_y (int): Origin y coordinate
        des_x (int): Destination x coordinate
        des_y (int): Destination y coordinate
        color (int): Color of the player making the move

    Returns:
        bool: True if the move is safe, False otherwise
    """
    # Create a shallow copy of the board rows (faster than deepcopy for tuples)
    temp_board = [row[:] for row in board]

    # Execute the move on the temporary board
    move_simu(temp_board, original_x, original_y, des_x, des_y)

    # Check if the king is in check after the move
    return not is_check_simu(temp_board, color)


def can_en_passant_simu(state, orig_x, orig_y, des_x, des_y):
    """
    Check if an 'en passant' capture is possible.
    """
    board = state['bord']
    pawn = board[orig_y][orig_x]

    # Basic validation: Piece must be a pawn
    if pawn is None or pawn[PIECE_TYPE] != PAWN:
        return False

    color = pawn[PIECE_COLOR]

    # Pawn must be on the correct rank (row 3 for White, row 4 for Black - depending on indexing)
    if (color == WHITE and orig_y != 3) or (color == BLACK and orig_y != 4):
        return False

    dx = des_x - orig_x
    dy = des_y - orig_y

    # Validate diagonal movement direction
    # Note: Ensure DIRECTIONS_BLACK_PAWN_2 corresponds to capture diagonals for black
    if (color == WHITE and (dx, dy) not in DIRECTIONS_WHITE_PAWN_2) or \
            (color == BLACK and (dx, dy) not in DIRECTIONS_BLACK_PAWN_2):
        return False

    # Check for the adjacent opponent pawn
    adjacent_pawn = board[orig_y][des_x]
    if adjacent_pawn is None or adjacent_pawn[PIECE_TYPE] != PAWN or adjacent_pawn[PIECE_COLOR] == color:
        return False

    # Check history: The opponent pawn must have just moved two squares
    if state['last_move_info'] is None:
        return False

    last_move = state['last_move_info']
    # Check if last move was a double pawn push to the adjacent square
    if (last_move[PIECE_TYPE] == PAWN and
            last_move[TO_X] == des_x and
            last_move[TO_Y] == orig_y and
            abs(last_move[FROM_Y] - last_move[TO_Y]) == 2):
        return True

    return False


def execute_en_passant_simu(state, orig_x, orig_y, des_x, des_y):
    """
    Execute the 'en passant' capture on the simulated board.
    """
    board = state['bord']
    pawn = board[orig_y][orig_x]

    # Create new tuple for the pawn with updated move count
    new_pawn = (pawn[PIECE_TYPE], pawn[PIECE_COLOR], pawn[PIECE_MOVEMENT], pawn[PIECE_NB_MOVEMENT] + 1)

    # Move pawn to destination
    board[des_y][des_x] = new_pawn
    # Remove pawn from origin
    board[orig_y][orig_x] = None
    # Remove the captured pawn (which is 'behind' the destination)
    board[orig_y][des_x] = None


def execute_castle_simu(state, color, king_side=True):
    """
    Execute castling on the simulated board.
    """
    board = state['bord']
    king_row = 7 if color == WHITE else 0

    if king_side:
        # King-side castling coordinates
        king_new_x, rook_old_x, rook_new_x = 6, 7, 5
    else:
        # Queen-side castling coordinates
        king_new_x, rook_old_x, rook_new_x = 2, 0, 3

    # Move the King
    king = board[king_row][4]
    if king:
        new_king = (king[0], king[1], king[2], king[3] + 1)
        board[king_row][king_new_x] = new_king
        board[king_row][4] = None

    # Move the Rook
    rook = board[king_row][rook_old_x]
    if rook:
        new_rook = (rook[0], rook[1], rook[2], rook[3] + 1)
        board[king_row][rook_new_x] = new_rook
        board[king_row][rook_old_x] = None


def generate_legal_moves(board: list, color: int) -> list:
    """
    Generate all legal moves for a specific color on the given board.

    Args:
        board: The simulated board (list of lists of tuples)
        color: The color of the player (WHITE or BLACK)
    Returns:
        list: A list of moves in format [start_x, start_y, end_x, end_y]
    """
    legal_moves = []

    for o_y in range(len(board)):
        for o_x in range(len(board[o_y])):
            piece = board[o_y][o_x]
            if piece is not None:
                if piece[PIECE_COLOR] == color:
                    # Check all possible squares on the board
                    for d_y in range(len(board)):
                        for d_x in range(len(board[o_y])):
                            # Check geometry and safety (King not in check)
                            if is_legal_move_simu(board, o_x, o_y, d_x, d_y) and \
                                    is_safe_move_simu(board, o_x, o_y, d_x, d_y, color):
                                legal_moves.append([o_x, o_y, d_x, d_y])
    return legal_moves


def move_simu_ai(state: dict, o_x: int, o_y: int, d_x: int, d_y: int):
    """
    Execute a move on the simulated state, handling special moves (Castling, En Passant, Promotion).
    Updates the board, turn, and last_move_info in place.
    """
    board = state['bord']

    # 1. Handle En Passant
    if can_en_passant_simu(state, o_x, o_y, d_x, d_y):
        execute_en_passant_simu(state, o_x, o_y, d_x, d_y)
        state['last_move_info'] = (PAWN, o_x, o_y, d_x, d_y)
        state['turn'] = -state['turn']
        return  # Move is finished

    piece = board[o_y][o_x]
    king_castle = (6, 0) if state['turn'] == BLACK else (6, 7)
    queen_castle = (2, 0) if state['turn'] == BLACK else (2, 7)

    # 2. Handle Castling
    if piece[PIECE_TYPE] == KING and (d_x, d_y) == queen_castle and piece[PIECE_NB_MOVEMENT] == 0:
        execute_castle_simu(state, piece[PIECE_COLOR], False)
        state['last_move_info'] = (KING, o_x, o_y, d_x, d_y)
        state['turn'] = -state['turn']
        return  # Move is finished

    elif piece[PIECE_TYPE] == KING and (d_x, d_y) == king_castle and piece[PIECE_NB_MOVEMENT] == 0:
        execute_castle_simu(state, piece[PIECE_COLOR], True)
        state['last_move_info'] = (KING, o_x, o_y, d_x, d_y)
        state['turn'] = -state['turn']
        return  # Move is finished

    # 3. Handle Pawn Promotion & Standard Moves
    new_piece = None
    if piece[PIECE_TYPE] == PAWN and piece[PIECE_COLOR] == WHITE and d_y == 0:
        # Promote to Queen
        new_piece = (QUEEN, piece[PIECE_COLOR], SLIDING, piece[PIECE_NB_MOVEMENT] + 1)
    elif piece[PIECE_TYPE] == PAWN and piece[PIECE_COLOR] == BLACK and d_y == 7:
        # Promote to Queen
        new_piece = (QUEEN, piece[PIECE_COLOR], SLIDING, piece[PIECE_NB_MOVEMENT] + 1)
    else:
        # Standard move: just increment move count
        new_piece = (piece[0], piece[1], piece[2], piece[3] + 1)

    # Apply move to board
    board[o_y][o_x] = None
    board[d_y][d_x] = new_piece

    # Update State
    state['last_move_info'] = (new_piece[PIECE_TYPE], o_x, o_y, d_x, d_y)
    state['turn'] = -state['turn']


class AI:
    def __init__(self, game):
        self.game = game

    def evaluate(self, state):
        """
        Evaluate the board state.
        Returns a score: Positive for White advantage, Negative for Black advantage.
        """
        board = state['bord']
        value = 0

        # Iterate over the 8x8 grid (FIXED: do not iterate directly over board list)
        for y in range(8):
            for x in range(8):
                piece = board[y][x]
                if piece is not None:
                    # Calculate absolute score (White - Black)
                    piece_val = PIECE_VALUE[piece[PIECE_TYPE]]

                    # Optional: Add positional bonuses here (e.g., center control)
                    if 2 < x < 5 and 2 < y < 5:
                        piece_val += 1

                    if piece[PIECE_COLOR] == WHITE:
                        value += piece_val
                    else:
                        value -= piece_val

        return value

    def minimax(self, state, depth, alpha, beta, maximizing_player):
        """
        Minimax algorithm with Alpha-Beta pruning.
        """
        current_color = state['turn']

        # 1. Generate all possible moves
        possible_moves = generate_legal_moves(state['bord'], current_color)

        # 2. Check for End Game (Mat or Pat)
        if not possible_moves:
            # If the current player is in check and has no moves -> Checkmate
            if is_check_simu(state['bord'], current_color):
                # If maximizing_player (White) is mated, return -infinity
                # If minimizing_player (Black) is mated, return +infinity
                return (-1000000 if maximizing_player else 1000000), None
            else:
                # Stalemate (Pat) -> Draw
                return 0, None

        # 3. Depth limit reached
        if depth == 0:
            return self.evaluate(state), None

        best_move = None

        if maximizing_player:  # WHITE's turn (maximize score)
            max_eval = -float('inf')

            # Optional: Shuffle moves to add variety
            # random.shuffle(possible_moves)

            for move in possible_moves:
                ox, oy, dx, dy = move

                # Create a DEEP copy of the state manually for performance
                new_board = [row[:] for row in state['bord']]
                new_state = {
                    'bord': new_board,
                    'turn': state['turn'],
                    'last_move_info': state['last_move_info']
                }

                # Simulate the move
                move_simu_ai(new_state, ox, oy, dx, dy)

                # Recursive call
                eval, _ = self.minimax(new_state, depth - 1, alpha, beta, False)

                if eval > max_eval:
                    max_eval = eval
                    best_move = move

                alpha = max(alpha, eval)
                if beta <= alpha:
                    break  # Beta Pruning
            return max_eval, best_move

        else:  # BLACK's turn (minimize score)
            min_eval = float('inf')

            # random.shuffle(possible_moves)

            for move in possible_moves:
                ox, oy, dx, dy = move

                # Create a DEEP copy of the state
                new_board = [row[:] for row in state['bord']]
                new_state = {
                    'bord': new_board,
                    'turn': state['turn'],
                    'last_move_info': state['last_move_info']
                }

                # Simulate the move
                move_simu_ai(new_state, ox, oy, dx, dy)

                # Recursive call
                eval, _ = self.minimax(new_state, depth - 1, alpha, beta, True)

                if eval < min_eval:
                    min_eval = eval
                    best_move = move

                beta = min(beta, eval)
                if beta <= alpha:
                    break  # Alpha Pruning
            return min_eval, best_move

    def get_best_move(self, depth=2):
        """
        Main entry point for the AI.
        Called by the game loop to get the AI's move.
        """
        # Create the initial simulation state from the real game object
        # Ensure game.copy() returns the dict {bord, turn, last_move_info}
        state = self.game.copy()

        is_white_turn = (self.game.turn == WHITE)

        # Run Minimax
        _, move = self.minimax(state, depth, -float('inf'), float('inf'), is_white_turn)

        return move