
from utils.constante import *
import random

# --- POSITIONAL EVALUATION TABLES (PST) ---
# These tables define where pieces prefer to be (from WHITE's perspective).
# The Y index is inverted for Black.
# Values are small to avoid exceeding the value of a pawn (often 10 or 100).

# Pawns want to advance (Y=0 is the top of the screen, promotion for White)
PAWN_TABLE = [
    [0,  0,  0,  0,  0,  0,  0,  0],
    [50, 50, 50, 50, 50, 50, 50, 50],
    [10, 10, 20, 30, 30, 20, 10, 10],
    [5,  5, 10, 25, 25, 10,  5,  5],
    [0,  0,  0, 20, 20,  0,  0,  0],
    [5, -5,-10,  0,  0,-10, -5,  5],
    [5, 10, 10,-20,-20, 10, 10,  5],
    [0,  0,  0,  0,  0,  0,  0,  0]
]

KNIGHT_TABLE = [
    [-50,-40,-30,-30,-30,-30,-40,-50],
    [-40,-20,  0,  0,  0,  0,-20,-40],
    [-30,  0, 10, 15, 15, 10,  0,-30],
    [-30,  5, 15, 20, 20, 15,  5,-30],
    [-30,  0, 15, 20, 20, 15,  0,-30],
    [-30,  5, 10, 15, 15, 10,  5,-30],
    [-40,-20,  0,  5,  5,  0,-20,-40],
    [-50,-40,-30,-30,-30,-30,-40,-50]
]

BISHOP_TABLE = [
    [-20,-10,-10,-10,-10,-10,-10,-20],
    [-10,  0,  0,  0,  0,  0,  0,-10],
    [-10,  0,  5, 10, 10,  5,  0,-10],
    [-10,  5,  5, 10, 10,  5,  5,-10],
    [-10,  0, 10, 10, 10, 10,  0,-10],
    [-10, 10, 10, 10, 10, 10, 10,-10],
    [-10,  5,  0,  0,  0,  0,  5,-10],
    [-20,-10,-10,-10,-10,-10,-10,-20]
]

ROOK_TABLE = [
    [0,  0,  0,  0,  0,  0,  0,  0],
    [5, 10, 10, 10, 10, 10, 10,  5],
    [-5,  0,  0,  0,  0,  0,  0, -5],
    [-5,  0,  0,  0,  0,  0,  0, -5],
    [-5,  0,  0,  0,  0,  0,  0, -5],
    [-5,  0,  0,  0,  0,  0,  0, -5],
    [-5,  0,  0,  0,  0,  0,  0, -5],
    [0,  0,  0,  5,  5,  0,  0,  0]
]

QUEEN_TABLE = [
    [-20,-10,-10, -5, -5,-10,-10,-20],
    [-10,  0,  0,  0,  0,  0,  0,-10],
    [-10,  0,  5,  5,  5,  5,  0,-10],
    [-5,  0,  5,  5,  5,  5,  0, -5],
    [0,  0,  5,  5,  5,  5,  0, -5],
    [-10,  5,  5,  5,  5,  5,  0,-10],
    [-10,  0,  5,  0,  0,  0,  0,-10],
    [-20,-10,-10, -5, -5,-10,-10,-20]
]

KING_MIDDLE_GAME_TABLE = [
    [-30,-40,-40,-50,-50,-40,-40,-30],
    [-30,-40,-40,-50,-50,-40,-40,-30],
    [-30,-40,-40,-50,-50,-40,-40,-30],
    [-30,-40,-40,-50,-50,-40,-40,-30],
    [-20,-30,-30,-40,-40,-30,-30,-20],
    [-10,-20,-20,-20,-20,-20,-20,-10],
    [20, 20,  0,  0,  0,  0, 20, 20],
    [20, 30, 10,  0,  0, 10, 30, 20]
]

KING_END_GAME_TABLE = [
    [-50,-40,-30,-20,-20,-30,-40,-50],
    [-30,-20,-10,  0,  0,-10,-20,-30],
    [-30,-10, 20, 30, 30, 20,-10,-30],
    [-30,-10, 30, 40, 40, 30,-10,-30],
    [-30,-10, 30, 40, 40, 30,-10,-30],
    [-30,-10, 20, 30, 30, 20,-10,-30],
    [-30,-30,  0,  0,  0,  0,-30,-30],
    [-50,-30,-30,-30,-30,-30,-30,-50]
]

def is_collinear(v1, v2):
    """
    Check if two vectors are collinear (parallel or anti-parallel).

    Args:
        v1 (tuple): First vector (dx, dy)
        v2 (tuple): Second vector (dx, dy)

    Returns:
        bool: True if vectors are collinear, False otherwise
    """
    # Cross product is zero for collinear vectors
    return v1[0] * v2[1] - v1[1] * v2[0] == 0


def is_legal_move_simu(board, o_x, o_y, d_x, d_y):
    """
    Check if a move is legal in a simulated board state (used for move validation).

    Args:
        board (list): 2D list representing the board state
        o_x (int): Origin x coordinate
        o_y (int): Origin y coordinate
        d_x (int): Destination x coordinate
        d_y (int): Destination y coordinate

    Returns:
        bool: True if the move is legal, False otherwise
    """
    case_sta = board[o_y][o_x]
    case_end = board[d_y][d_x]
    distance_x = d_x - o_x
    distance_y = d_y - o_y
    valid_direction = False

    if case_sta[PIECE_TYPE] == KING:
        if (distance_x,distance_y) not in KING_DIRECTION:
            if (case_sta[PIECE_COLOR] == WHITE and (d_x, d_y) == QUEEN_SIDE_CASTLE[1]) or (case_sta[PIECE_COLOR] == BLACK and (d_x, d_y) == QUEEN_SIDE_CASTLE[0])  and case_sta[PIECE_NB_MOVEMENT] == 0:
                    return can_castle_queen_side_simu(board, case_sta[PIECE_COLOR])
            elif (case_sta[PIECE_COLOR] == WHITE and (d_x, d_y) == KING_SIDE_CASTLE[1]) or (case_sta[PIECE_COLOR] == BLACK and (d_x, d_y) == KING_SIDE_CASTLE[0]) and case_sta[PIECE_NB_MOVEMENT] == 0:
                    return can_castle_king_side_simu(board, case_sta[PIECE_COLOR])

    # Handle non-pawn pieces
    if case_sta[0] != PAWN:
        if case_sta[2] == SLIDING:
            # Check if move direction is valid for sliding pieces
            for direct in MOVEMENT[case_sta[0]]:
                if is_collinear((distance_x, distance_y), direct):
                    valid_direction = True
                    break

            # Check if path is clear
            if valid_direction:
                step_x = (distance_x // abs(distance_x)) if distance_x != 0 else 0
                step_y = (distance_y // abs(distance_y)) if distance_y != 0 else 0
                x, y = o_x + step_x, o_y + step_y
                while (x, y) != (d_x, d_y):
                    if board[y][x] is not None:
                        return False
                    x += step_x
                    y += step_y
        else:
            # For non-sliding pieces
            valid_direction = (distance_x, distance_y) in MOVEMENT[case_sta[0]]

        # Check destination
        if case_end is None:
            return valid_direction

        # Cannot capture own piece
        if case_sta[1] == case_end[1]:
            return False
        elif valid_direction:
            return True
    else:
        # Handle pawn moves
        return is_legal_move_pawn_simu(board, o_x, o_y, d_x, d_y)


def is_legal_move_pawn_simu(board, o_x, o_y, d_x, d_y):
    """
    Check if a pawn move is legal in a simulated board state.

    Args:
        board (list): 2D list representing the board state
        o_x (int): Origin x coordinate
        o_y (int): Origin y coordinate
        d_x (int): Destination x coordinate
        d_y (int): Destination y coordinate

    Returns:
        bool: True if the pawn move is legal, False otherwise
    """
    original = board[o_y][o_x]
    destination = board[d_y][d_x]
    color = original[1]

    # Calculate movement vector
    distance_x = d_x - o_x
    distance_y = d_y - o_y

    # Check diagonal capture moves based on color
    if color == WHITE:
        if (distance_x, distance_y) in DIRECTIONS_WHITE_PAWN_2 and destination is not None and destination[PIECE_COLOR] == BLACK:
            return True
        # Check forward moves
        if original[3] == 0:  # Pawn hasn't moved
            valid_direction = (distance_x, distance_y) in DIRECTIONS_WHITE_PAWN_1
        else:
            valid_direction = (distance_x, distance_y) in DIRECTIONS_WHITE_PAWN
    else:  # BLACK
        if (distance_x, distance_y) in DIRECTIONS_BLACK_PAWN_2 and destination is not None and destination[PIECE_COLOR] == WHITE:
            return True
        # Check forward moves
        if original[3] == 0:  # Pawn hasn't moved
            valid_direction = (distance_x, distance_y) in DIRECTIONS_BLACK_PAWN_1
        else:
            valid_direction = (distance_x, distance_y) in DIRECTIONS_BLACK_PAWN

    # Check if path is clear
    if valid_direction:
        step_x = (distance_x // abs(distance_x)) if distance_x != 0 else 0
        step_y = (distance_y // abs(distance_y)) if distance_y != 0 else 0
        x, y = o_x + step_x, o_y + step_y
        while (x, y) != (d_x, d_y):
            if board[y][x] is not None:
                return False
            x += step_x
            y += step_y

    # Pawn can only move to empty square (for non-capture moves)
    if destination is None:
        return valid_direction

    return False


def is_safe_move_simu(board, original_x, original_y, des_x, des_y, color):
    # Shallow copy for speed
    temp_board = [row[:] for row in board]
    move_simu(temp_board, original_x, original_y, des_x, des_y)
    return not is_check_simu(temp_board, color)


def move_simu(board,o_x,o_y,d_x,d_y):

    piece = board[o_y][o_x]
    board[d_y][d_x] = piece
    board[o_y][o_x] = None


def pieces_remaining_simu(board):
    pieces = []
    for y in range(8):
        for x in range(8):
            piece = board[y][x]
            if piece is not None:
                pieces.append(piece[PIECE_COLOR])
    return pieces


def is_check_simu(board, color):
    """
    Check if the king is in check in a simulated board state.

    Args:
        board (list): 2D list representing the board state
        color (int): Color of the king we are checking

    Returns:
        bool: True if the king is in check, False otherwise
    """
    pos = king_pos_simu(board, color)
    if pos is None:
        return False

    # Check if any opponent piece can attack the king
    adversary_color = -color
    for y in range(8):
        for x in range(8):
            piece = board[y][x]
            if piece is not None and piece[1] == adversary_color:
                if is_legal_move_simu(board, x, y, pos[0], pos[1]):
                    return True
    return False


def is_stalemate_simu(state,is_check,color):
    if is_check:
        return False
    if not generate_legal_moves(state['board'], color):
        return True
    return False


def insufficient_material_simu(state):
    remaining = pieces_remaining_simu(state['board'])
    if sorted(remaining) == sorted([KING, KING]):
        return True
    if sorted(remaining) == sorted([KING, KING, BISHOP]):
        return True
    if sorted(remaining) == sorted([KING, KING, KNIGHT]):
        return True
    if sorted(remaining) == sorted([KING, KING, BISHOP, BISHOP]):
        return True
    return False


def threefold_repetition_simu(state):
    last_index = len(state['move_history'])-1
    if last_index >= 9:
        if (state['last_move_info'] == state['move_history'][last_index - 4]) and (state['move_history'][last_index - 1] == state['move_history'][last_index - 5]):
            if (state['last_move_info'] == state['move_history'][last_index - 8]) and (state['move_history'][last_index - 1] == state['move_history'][last_index - 9]):
                return True

    return False


def is_draw_simu(state,color,is_check=False):
    if is_stalemate_simu(state,is_check,color):
        return True
    elif insufficient_material_simu(state):
        return True
    elif threefold_repetition_simu(state):
        return True
    return False


def outcome_simu(state,color):
    if is_check_simu(state['board'],color):
        return CHECK
    elif is_draw_simu(state,color):
        return DRAW
    return None


def king_pos_simu(board, color):
    """
    Find the position of the king in a simulated board state.

    Args:
        board (list): 2D list representing the simulated board state
        color (int): Color of the king to find

    Returns:
        tuple: Position (x, y) of the king, or None if not found
    """
    for y in range(8):
        for x in range(8):
            piece = board[y][x]
            if piece is not None:
                if piece[0] == KING and piece[1] == color:
                    return x, y


def can_en_passant_simu(state, orig_x, orig_y, des_x, des_y):
    board = state['board']
    pawn = board[orig_y][orig_x]
    if pawn is None or pawn[PIECE_TYPE] != PAWN:
        return False
    color = pawn[PIECE_COLOR]
    # Check Ranks
    if (color == WHITE and orig_y != 3) or (color == BLACK and orig_y != 4):
        return False
    dx = des_x - orig_x
    dy = des_y - orig_y
    # Directions
    if (color == WHITE and (dx, dy) not in DIRECTIONS_WHITE_PAWN_2) or \
            (color == BLACK and (dx, dy) not in DIRECTIONS_BLACK_PAWN_2):
        return False
    # Opponent pawn existence
    adjacent_pawn = board[orig_y][des_x]
    if adjacent_pawn is None or adjacent_pawn[PIECE_TYPE] != PAWN or adjacent_pawn[PIECE_COLOR] == color:
        return False
    # History check
    if state['last_move_info'] is None:
        return False
    last_move = state['last_move_info']
    if (last_move[PIECE_TYPE] == PAWN and last_move[TO_X] == des_x and
            last_move[TO_Y] == orig_y and abs(last_move[FROM_Y] - last_move[TO_Y]) == 2):
        return True
    return False


def can_castle_king_side_simu(board, color):
    """
    Vérify if the king side castle is possible
    """
    if color == WHITE:
        if board[7][4] is None:
            return False
        elif board[7][4][PIECE_TYPE] != KING or board[7][4][PIECE_COLOR] != WHITE:
            return False
        else:
            king = board[7][4]
            king_row = 7
            king_x = 4
            rook = board[7][7]
    else:
        if board[0][4] is None:
            return False
        elif board[0][4][PIECE_TYPE] != KING or board[0][4][PIECE_COLOR] != BLACK:
            return False
        else:
            king = board[0][4]
            king_row = 0
            king_x = 4
            rook = board[0][7]

    if king[PIECE_NB_MOVEMENT] > 0:
        return False
    if rook is None or rook[PIECE_TYPE] != ROOK or rook[PIECE_COLOR] != color or rook[PIECE_NB_MOVEMENT] > 0:
        return False

    # Check that the squares between the king and the rook are empty
    for x in range(5, 7):
        if board[king_row][x] is not None:
            return False

    # Check that the king is not in check and does not pass through an attacked square.
    if is_check_simu(board, color):
        return False

    # Simulate the king's movement square by square
    for x in range(4, 7):
        if not is_safe_move_simu(board, king_x, king_row, x, king_row, color):
            return False

    return True


def can_castle_queen_side_simu(board, color):
    """
    Vérify if the king side castle is possible
    """
    if color == WHITE:
        if board[7][4] is None:
            return False
        elif board[7][4][PIECE_TYPE] != KING or board[7][4][PIECE_COLOR] != WHITE:
            return False
        else:
            king = board[7][4]
            king_row = 7
            king_x = 4
            rook = board[7][0]
    else:
        if board[0][4] is None:
            return False
        elif board[0][4][PIECE_TYPE] != KING or board[0][4][PIECE_COLOR] != BLACK:
            return False
        else:
            king = board[0][4]
            king_row = 0
            king_x = 4
            rook = board[0][0]

    if king[PIECE_NB_MOVEMENT] > 0:
        return False
    if rook is None or rook[PIECE_TYPE] != ROOK or rook[PIECE_COLOR] != color or rook[PIECE_NB_MOVEMENT] > 0:
        return False

    # Check that the squares between the king and the rook are empty

    for x in range(1, 4):
        if board[king_row][x] is not None:
            return False

    # Check that the king is not in check and does not pass through an attacked square.

    if is_check_simu(board, color):
        return False

    # Simulate the king's movement square by square

    for x in range(4, 1, -1):
        if not is_safe_move_simu(board, king_x, king_row, x, king_row, color):
            return False

    return True


def execute_en_passant_simu(state, orig_x, orig_y, des_x, des_y):
    board = state['board']
    pawn = board[orig_y][orig_x]
    new_pawn = (pawn[PIECE_TYPE], pawn[PIECE_COLOR], pawn[PIECE_MOVEMENT], pawn[PIECE_NB_MOVEMENT] + 1)
    board[des_y][des_x] = new_pawn
    board[orig_y][orig_x] = None
    board[orig_y][des_x] = None


def execute_castle_simu(state, color, king_side=True):
    board = state['board']
    king_row = 7 if color == WHITE else 0
    if king_side:
        king_new_x, rook_old_x, rook_new_x = 6, 7, 5
    else:
        king_new_x, rook_old_x, rook_new_x = 2, 0, 3
    king = board[king_row][4]
    if king:
        new_king = (king[0], king[1], king[2], king[3] + 1)
        board[king_row][king_new_x] = new_king
        board[king_row][4] = None
    rook = board[king_row][rook_old_x]
    if rook:
        new_rook = (rook[0], rook[1], rook[2], rook[3] + 1)
        board[king_row][rook_new_x] = new_rook
        board[king_row][rook_old_x] = None


def generate_legal_moves(board: list, color: int) -> list:
    legal_moves = []
    for o_y in range(len(board)):
        for o_x in range(len(board[o_y])):
            piece = board[o_y][o_x]
            if piece is not None and piece[PIECE_COLOR] == color:
                for d_y in range(len(board)):
                    for d_x in range(len(board[o_y])):
                        if is_legal_move_simu(board, o_x, o_y, d_x, d_y) and \
                                is_safe_move_simu(board, o_x, o_y, d_x, d_y, color):
                            legal_moves.append((o_x, o_y, d_x, d_y))
    return legal_moves


def score_move(board:list , move : tuple ) -> int :
    target = board[move[2]][move[3]]
    if target is None:
        return 0
    else:
        return PIECE_VALUE[target[PIECE_TYPE]]



def move_simu_ai(state: dict, o_x: int, o_y: int, d_x: int, d_y: int):
    board = state['board']
    if can_en_passant_simu(state, o_x, o_y, d_x, d_y):
        execute_en_passant_simu(state, o_x, o_y, d_x, d_y)
        state['last_move_info'] = (PAWN, o_x, o_y, d_x, d_y)
        state['turn'] = -state['turn']
        state['move_history'].append(state['last_move_info'])

        return

    piece = board[o_y][o_x]
    king_castle = (6, 0) if state['turn'] == BLACK else (6, 7)
    queen_castle = (2, 0) if state['turn'] == BLACK else (2, 7)

    if piece[PIECE_TYPE] == KING and (d_x, d_y) == queen_castle and piece[PIECE_NB_MOVEMENT] == 0:
        execute_castle_simu(state, piece[PIECE_COLOR], False)
        state['last_move_info'] = (KING, o_x, o_y, d_x, d_y)
        state['turn'] = -state['turn']
        state['move_history'].append(state['last_move_info'])
        return
    elif piece[PIECE_TYPE] == KING and (d_x, d_y) == king_castle and piece[PIECE_NB_MOVEMENT] == 0:
        execute_castle_simu(state, piece[PIECE_COLOR], True)
        state['last_move_info'] = (KING, o_x, o_y, d_x, d_y)
        state['turn'] = -state['turn']
        state['move_history'].append(state['last_move_info'])
        return


    if piece[PIECE_TYPE] == PAWN and piece[PIECE_COLOR] == WHITE and d_y == 0:
        new_piece = (QUEEN, piece[PIECE_COLOR], SLIDING, piece[PIECE_NB_MOVEMENT] + 1)
    elif piece[PIECE_TYPE] == PAWN and piece[PIECE_COLOR] == BLACK and d_y == 7:
        new_piece = (QUEEN, piece[PIECE_COLOR], SLIDING, piece[PIECE_NB_MOVEMENT] + 1)
    else:
        new_piece = (piece[0], piece[1], piece[2], piece[3] + 1)

    board[o_y][o_x] = None
    board[d_y][d_x] = new_piece
    state['last_move_info'] = (new_piece[PIECE_TYPE], o_x, o_y, d_x, d_y)
    state['turn'] = -state['turn']
    state['move_history'].append(state['last_move_info'])


def material_eval(state):
    """
    Evaluates the board.
    Returns: Material Score
    Positive = White Advantage, Negative = Black Advantage
    """
    board = state['board']
    score_mat = 0
    for y in range(8):
        for x in range(8):
            piece = board[y][x]
            if piece is not None:
                if piece[PIECE_COLOR] == WHITE:
                    score_mat += PIECE_VALUE[piece[PIECE_TYPE]]
                else:
                    score_mat -= PIECE_VALUE[piece[PIECE_TYPE]]

    return score_mat


def total_material(state):
    board = state['board']
    total_mat = 0
    for y in range(8):
        for x in range(8):
            piece = board[y][x]
            if piece is not None and piece[PIECE_TYPE] != KING:
                total_mat += PIECE_VALUE[piece[PIECE_TYPE]]
    return total_mat


def is_endgame(state):
    return total_material(state) < 1300


def mobility_eval(board):
    white_moves = len(generate_legal_moves(board, WHITE))
    black_moves = len(generate_legal_moves(board, BLACK))
    return (white_moves - black_moves) * 5


def get_position_value(piece,x,y, is_endgame=False):
    """
    Obtains the positional value of a piece
    """
    piece_type = piece[PIECE_TYPE]
    color = piece[PIECE_COLOR]

    if piece_type == KING and is_endgame:
        table = KING_END_GAME_TABLE
    elif piece_type == KING:
        table = KING_MIDDLE_GAME_TABLE
    elif piece_type == QUEEN:
        table = QUEEN_TABLE
    elif piece_type == ROOK:
        table = ROOK_TABLE
    elif piece_type == PAWN:
        table = PAWN_TABLE
    elif piece_type == KNIGHT:
        table = KNIGHT_TABLE
    elif piece_type == BISHOP:
        table = BISHOP_TABLE
    else:
        return 0

    # Pour les pièces noires, on inverse le tableau
    if color == BLACK:
        y = 7 - y

    return table[y][x]


def positional_eval(state,is_endgame=False):
    board = state['board']
    pos_eval = 0
    for y in range(8):
        for x in range(8):
            piece = board[y][x]
            if piece is not None:
                if piece[PIECE_COLOR] == WHITE:
                    pos_eval += get_position_value(piece,x,y,is_endgame)
                else:
                    pos_eval -= get_position_value(piece,x,y,is_endgame)
    return pos_eval



class AI:
    def __init__(self, game):
        self.game = game

    def evaluate(self, state):
        """
        Evaluates the board.
        Returns: Material Score + Positional Score + Mobility score
        Positive = White Advantage, Negative = Black Advantage
        """
        board = state['board']
        value = 0

        material_score = material_eval(state)

       # mobility_score = mobility_eval(board)

        positional_score = positional_eval(state,is_endgame(state))

       # value += material_score + mobility_score + positional_score
        value += material_score +  positional_score

        outcome_white = outcome_simu(state,WHITE)
        outcome_black = outcome_simu(state,BLACK)
        if outcome_white == CHECK:
            value-= 100
        elif outcome_black == CHECK:
            value+= 100
        elif outcome_black or outcome_white == DRAW:
            value = 0



        #value += random.randint(-5, 5)

        return value



    def minimax(self, state, depth, alpha, beta, maximizing_player):
        current_color = state['turn']
        possible_moves = generate_legal_moves(state['board'], current_color)
        possible_moves.sort(key=lambda m:score_move(state['board'],m), reverse=True)

        if not possible_moves:
            if is_check_simu(state['board'], current_color):
                return (-1000000 if maximizing_player else 1000000), None
            else:
                return 0, None

        if depth == 0:
            return self.evaluate(state), None

        best_move = None
        # Shuffle so the AI isn't too predictable at equal levels
        random.shuffle(possible_moves)

        if maximizing_player:
            max_eval = -float('inf')
            for move in possible_moves:
                ox, oy, dx, dy = move
                new_board = [row[:] for row in state['board']]
                new_state = {
                    'board': new_board,
                    'turn': state['turn'],
                    'last_move_info': state['last_move_info'],
                    'move_history' : state['move_history']
                }
                move_simu_ai(new_state, ox, oy, dx, dy)
                eval, _ = self.minimax(new_state, depth - 1, alpha, beta, False)
                if eval > max_eval:
                    max_eval = eval
                    best_move = move
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval, best_move
        else:
            min_eval = float('inf')
            for move in possible_moves:
                ox, oy, dx, dy = move
                new_board = [row[:] for row in state['board']]
                new_state = {
                    'board': new_board,
                    'turn': state['turn'],
                    'last_move_info': state['last_move_info'],
                    'move_history': state['move_history']
                }
                move_simu_ai(new_state, ox, oy, dx, dy)
                eval, _ = self.minimax(new_state, depth - 1, alpha, beta, True)
                if eval < min_eval:
                    min_eval = eval
                    best_move = move
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval, best_move



    def get_best_move(self, depth=2):
        state = self.game.copy()
        is_white_turn = (self.game.turn == WHITE)
        _, move = self.minimax(state, depth, -float('inf'), float('inf'), is_white_turn)
        return move
