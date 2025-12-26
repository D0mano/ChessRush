import pygame
import math

from classes.AI import *
from utils.constante import *

# Global variable to track selected squares on the chessboard
selected_case = [[False for _ in range(8)] for _ in range(8)]


def chess_to_xy(pos):
    """
    Convert chess board coordinates to pixel coordinates on screen.

    Args:
        pos (tuple): Chess board coordinates (x, y) where (0,0) is top-left

    Returns:
        tuple: Pixel coordinates (x, y) for the center of the square, or None if pos is None
    """
    if pos is not None:
        pos_x = pos[0] * CASE_SIZE + OFFSET_PLATEAU_X + CASE_SIZE // 2
        pos_y = pos[1] * CASE_SIZE + OFFSET_PLATEAU_Y + CASE_SIZE // 2
        return pos_x, pos_y
    return


def xy_to_chess(pos):
    """
    Convert pixel coordinates to chess board coordinates.

    Args:
        pos (tuple): Pixel coordinates (x, y) on the screen

    Returns:
        tuple: Chess board coordinates (x, y) if within bounds, None otherwise
    """
    pos_x = (pos[0] - OFFSET_PLATEAU_X) // CASE_SIZE
    pos_y = (pos[1] - OFFSET_PLATEAU_Y) // CASE_SIZE

    if (0 <= pos_x <= 7) and (0 <= pos_y <= 7):
        return pos_x, pos_y
    return


def draw_bord(screen, game, miniature=False, offset_x=OFFSET_PLATEAU_X, offset_y=OFFSET_PLATEAU_Y,
              bord_width=BORD_WIDTH, bord_height=BORD_HEIGHT, case_size=CASE_SIZE):
    """
    Draw the chess board with alternating colors and coordinate labels.

    Args:
        screen (pygame.Surface): The surface to draw on
        game (Game): The game instance containing board color settings
        miniature (bool): Whether to draw a miniature version without labels
        offset_x (int): X offset for board position
        offset_y (int): Y offset for board position
        bord_width (int): Width of the board
        bord_height (int): Height of the board
        case_size (int): Size of each square

    Returns:
        pygame.Rect: Rectangle representing the board area
    """
    color = game.bord_color

    # Draw border around the board (only for full-size board)
    if not miniature:
        pygame.draw.rect(screen, TEXT_COLOR,
                         (offset_x - 25, offset_y - 25, bord_width + 50, bord_height + 50))

    # Draw the base board color
    pygame.draw.rect(screen, color[0], (offset_x, offset_y, bord_width, bord_height))

    # Draw alternating colored squares
    for row in range(8):
        for col in range(8):
            if (row + col) % 2 != 0:
                pygame.draw.rect(screen, color[1],
                                 (offset_x + row * case_size, offset_y + col * case_size, case_size, case_size))

    # Draw coordinate labels (only for full-size board)
    font = pygame.font.Font(None, 20)
    if not miniature:
        for i in range(8):
            # Draw row numbers (1-8)
            text_number = font.render(ROWS[i], True, (150, 150, 150))
            rect_number = text_number.get_rect(center=(offset_x - 15, (offset_y + case_size // 2) + (i * case_size)))
            screen.blit(text_number, rect_number)

            # Draw column letters (a-h)
            text_letter = font.render(COLUMNS[i], True, (150, 150, 150))
            rect_letter = text_letter.get_rect(center=((offset_x + case_size // 2) + (i * case_size),
                                                       (offset_y + 8 * case_size) + 10))
            screen.blit(text_letter, rect_letter)

    return pygame.Rect(offset_x, offset_y, bord_width, bord_height)


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


def is_legal_move(game, original_x, original_y, des_x, des_y, ignore_turn=False):
    """
    Check if a move is legal according to chess rules.

    Args:
        game (Game): The game instance
        original_x (int): Starting x coordinate
        original_y (int): Starting y coordinate
        des_x (int): Destination x coordinate
        des_y (int): Destination y coordinate
        ignore_turn (bool): Whether to ignore whose turn it is

    Returns:
        bool: True if the move is legal, False otherwise
    """
    original = game.bord[original_y][original_x]
    destination = game.bord[des_y][des_x]

    # Calculate movement vector
    d_x = des_x - original_x
    d_y = des_y - original_y

    # Check if it's the correct player's turn
    if not ignore_turn:
        if original.color != game.turn:
            return False
    valid_direction = False
    # Check for castling moves
    if original.type_piece == KING:
        if (d_x,d_y) not in original.movement:
            if (original.color == WHITE and (des_x, des_y) == QUEEN_SIDE_CASTLE[1]) or (original.color == BLACK and (des_x, des_y) == QUEEN_SIDE_CASTLE[0])  and original.nb_move == 0:
                    return can_castle_queen_side(game, original.color)
            elif (original.color == WHITE and (des_x, des_y) == KING_SIDE_CASTLE[1]) or (original.color == BLACK and (des_x, des_y) == KING_SIDE_CASTLE[0]) and original.nb_move == 0:
                    return can_castle_king_side(game, original.color)

    valid_direction = False

    # Handle non-pawn pieces
    if original.type_piece != PAWN:
        if original.movement_type == SLIDING:
            # For sliding pieces, check if move direction is valid
            for direct in original.movement:
                if is_collinear((d_x, d_y), direct):
                    valid_direction = True
                    break

            # Check if path is clear for sliding pieces
            if valid_direction:
                step_x = (d_x // abs(d_x)) if d_x != 0 else 0
                step_y = (d_y // abs(d_y)) if d_y != 0 else 0
                x, y = original_x + step_x, original_y + step_y
                while (x, y) != (des_x, des_y):
                    if game.bord[y][x] is not None:
                        return False
                    x += step_x
                    y += step_y
        else:
            # For non-sliding pieces, move must be in allowed movement list
            valid_direction = (d_x, d_y) in original.movement

        # Check destination square
        if destination is None:
            return valid_direction

        # Cannot capture own piece
        if original.color == destination.color:
            return False
        elif valid_direction:
            return True
    else:
        # Handle pawn moves separately
        return is_legal_move_pawn(game, original_x, original_y, des_x, des_y)




def show_possible_move(game, pos):
    """
    Display visual indicators for all legal moves from a given position.

    Args:
        game (Game): The game instance
        pos (tuple): Position (x, y) to show moves from
    """
    orig_x = pos[0]
    orig_y = pos[1]
    piece = game.bord[orig_y][orig_x]

    # Check all squares on the board
    for y in range(8):
        for x in range(8):
            # If move is legal and safe (doesn't leave king in check)
            if is_legal_move(game, orig_x, orig_y, x, y) and is_safe_move(game, orig_x, orig_y, x, y, game.turn):
                piece_2 = game.bord[y][x]
                pos_2 = chess_to_xy((x, y))
                top_left_x = pos_2[0] - CASE_SIZE // 2
                top_left_y = pos_2[1] - CASE_SIZE // 2
                circle_surf = pygame.Surface((CASE_SIZE, CASE_SIZE), pygame.SRCALPHA)

                # Draw different indicators for capture vs normal move
                if piece_2 is not None and piece.color != piece_2.color:
                    # Red circle for capture moves
                    pygame.draw.circle(circle_surf, COLOR_CHECK, (CASE_SIZE / 2, CASE_SIZE / 2), 35, width=3)
                    game.screen.blit(circle_surf, (top_left_x, top_left_y))
                else:
                    # Small dot for normal moves
                    pygame.draw.circle(circle_surf, SELECTION_COLOR_3, (CASE_SIZE / 2, CASE_SIZE / 2), 10)
                    game.screen.blit(circle_surf, (top_left_x, top_left_y))


def is_legal_move_pawn(game, orig_x, orig_y, des_x, des_y):
    """
    Check if a pawn move is legal according to pawn-specific rules.

    Args:
        game (Game): The game instance
        orig_x (int): Origin x coordinate
        orig_y (int): Origin y coordinate
        des_x (int): Destination x coordinate
        des_y (int): Destination y coordinate

    Returns:
        bool: True if the pawn move is legal, False otherwise
    """
    original = game.bord[orig_y][orig_x]
    destination = game.bord[des_y][des_x]

    # Calculate movement vector
    d_x = des_x - orig_x
    d_y = des_y - orig_y

    # Check for en passant
    if can_en_passant(game, orig_x, orig_y, des_x, des_y):
        return True

    # Check for diagonal capture
    if destination is not None and destination.color != original.color:
        if (d_x, d_y) in original.movement_2:
            return True

    # Determine allowed movements based on whether pawn has moved
    if original.nb_move == 0:
        valid_direction = (d_x, d_y) in original.movement_1  # Initial two-square move allowed
    else:
        valid_direction = (d_x, d_y) in original.movement  # Only one square forward

    # Check if path is clear (for forward moves)
    if valid_direction:
        step_x = (d_x // abs(d_x)) if d_x != 0 else 0
        step_y = (d_y // abs(d_y)) if d_y != 0 else 0
        x, y = orig_x + step_x, orig_y + step_y
        while (x, y) != (des_x, des_y):
            if game.bord[y][x] is not None:
                return False
            x += step_x
            y += step_y

    # Pawn can only move to empty square (for non-capture moves)
    if destination is None:
        return valid_direction

    return False





def king_pos(bord, color):
    """
    Find the position of the king of a given color on the board.

    Args:
        bord (list): 2D list representing the board
        color (int): Color of the king to find (WHITE or BLACK)

    Returns:
        tuple: Position (x, y) of the king, or None if not found
    """
    for y in range(8):
        for x in range(8):
            piece = bord[y][x]
            if piece is not None:
                if piece.type_piece == KING and piece.color == color:
                    return x, y



def is_check(game, color):
    """
    Check if the king of a given color is in check.

    Args:
        game (Game): The game instance
        color (int): Color of the king to check

    Returns:
        bool: True if the king is in check, False otherwise
    """
    pos = king_pos(game.bord, color)
    if pos is None:
        return False

    # Visual feedback for check
    pos_xy = chess_to_xy(pos)
    top_left_x = pos_xy[0] - CASE_SIZE // 2
    top_left_y = pos_xy[1] - CASE_SIZE // 2

    # Check if any opponent piece can attack the king
    adversaire_color = -color
    for y in range(8):
        for x in range(8):
            piece = game.bord[y][x]
            if piece is not None and piece.color == adversaire_color:
                if is_legal_move(game, x, y, pos[0], pos[1], True):
                    # Highlight the king in check
                    pygame.draw.rect(game.screen, COLOR_CHECK, (top_left_x, top_left_y, CASE_SIZE, CASE_SIZE))
                    game.update()
                    draw_move_arrow(game.screen, (x, y), pos)
                    return True
    return False




def draw_arrow_filled(surface, color, start_pos, end_pos, arrow_width=5, arrow_head_size=15):
    """
    Draw a filled arrow with elegant appearance.

    Args:
        surface (pygame.Surface): The surface to draw on
        color (tuple): RGB color of the arrow
        start_pos (tuple): Starting position (x, y)
        end_pos (tuple): Ending position (x, y)
        arrow_width (int): Width of the arrow body
        arrow_head_size (int): Size of the arrow head
    """
    # Calculate direction vector
    dx = end_pos[0] - start_pos[0]
    dy = end_pos[1] - start_pos[1]

    # Handle edge case: same start and end position
    if dx == 0 and dy == 0:
        return

    # Normalize the direction vector
    length = math.sqrt(dx * dx + dy * dy)
    unit_x = dx / length
    unit_y = dy / length

    # Calculate perpendicular vector for arrow width
    perp_x = -unit_y * arrow_width / 2
    perp_y = unit_x * arrow_width / 2

    # Calculate where the arrow body ends (before the head)
    body_end_x = end_pos[0] - unit_x * arrow_head_size
    body_end_y = end_pos[1] - unit_y * arrow_head_size

    # Draw the arrow body (rectangle)
    body_points = [
        (start_pos[0] + perp_x, start_pos[1] + perp_y),
        (start_pos[0] - perp_x, start_pos[1] - perp_y),
        (body_end_x - perp_x, body_end_y - perp_y),
        (body_end_x + perp_x, body_end_y + perp_y)
    ]
    pygame.draw.polygon(surface, color, body_points)

    # Draw the arrow head (triangle)
    head_width = arrow_width * 2
    head_perp_x = -unit_y * head_width / 2
    head_perp_y = unit_x * head_width / 2

    head_points = [
        end_pos,
        (body_end_x + head_perp_x, body_end_y + head_perp_y),
        (body_end_x - head_perp_x, body_end_y - head_perp_y)
    ]
    pygame.draw.polygon(surface, color, head_points)


def draw_move_arrow(screen, start_pos, end_pos, color=POSSIBLE_MOVE):
    """
    Draw an arrow to show a possible move or attack.

    Args:
        screen (pygame.Surface): The surface to draw on
        start_pos (tuple): Starting chess position (x, y)
        end_pos (tuple): Ending chess position (x, y)
        color (tuple): RGB color of the arrow
    """
    start_pixel = chess_to_xy(start_pos)
    end_pixel = chess_to_xy(end_pos)
    draw_arrow_filled(screen, color, start_pixel, end_pixel, arrow_width=4, arrow_head_size=12)


def is_safe_move(game, original_x, original_y, des_x, des_y, color):
    """
    Check if a move is safe (doesn't leave the king in check).

    Args:
        game (Game): The game instance
        original_x (int): Origin x coordinate
        original_y (int): Origin y coordinate
        des_x (int): Destination x coordinate
        des_y (int): Destination y coordinate
        color (int): Color of the player making the move

    Returns:
        bool: True if the move is safe, False otherwise
    """
    # Create a copy of the board and simulate the move
    game.bord_copy = game.copy()['bord']
    move_simu(game.bord_copy, original_x, original_y, des_x, des_y)
    # Check if the king would be in check after the move
    return not is_check_simu(game.bord_copy, color)


def is_select(game, event):
    """
    Handle square selection on the chess board and highlight possible moves.

    Args:
        game (Game): The game instance
        event (pygame.Event): Mouse click event

    Returns:
        tuple: Selected position (x, y) or None if no valid selection
    """
    pos = chess_to_xy(xy_to_chess(event.pos))
    if pos is None:
        return

    top_left_x = pos[0] - CASE_SIZE // 2
    top_left_y = pos[1] - CASE_SIZE // 2

    # Clear previous selections
    for y in range(8):
        for x in range(8):
            if selected_case[y][x]:
                selected_case[y][x] = False
                draw_bord(game.screen, game)
                game.update()

    # Check if a piece was clicked
    for y in range(len(game.bord)):
        for x in range(len(game.bord[y])):
            if game.bord[y][x] is not None:
                if game.bord[y][x].rect.collidepoint(event.pos):
                    # Highlight the selected square
                    highlight = pygame.Surface((CASE_SIZE, CASE_SIZE), pygame.SRCALPHA)
                    highlight.fill(SELECTION_COLOR_4)
                    game.screen.blit(highlight, (top_left_x, top_left_y))
                    selected_case[y][x] = True
                    des_x = x
                    des_y = y
                    # Show possible moves for the selected piece
                    show_possible_move(game, (des_x, des_y))
                    game.update()
                    return des_x, des_y


def move(game, original_x, original_y, des_x, des_y):
    """
    Execute a move on the chess board with full validation and game state updates.

    Args:
        game (Game): The game instance
        original_x (int): Origin x coordinate
        original_y (int): Origin y coordinate
        des_x (int): Destination x coordinate
        des_y (int): Destination y coordinate

    Returns:
        str: Algebraic notation of the move, or None if move is invalid
    """
    # Check if move is legal
    if not is_legal_move(game, original_x, original_y, des_x, des_y):
        draw_bord(game.screen, game)
        game.update()
        return

    # Check if move is safe (doesn't leave king in check)
    if not is_safe_move(game, original_x, original_y, des_x, des_y, game.turn):
        draw_bord(game.screen, game)
        game.move_illegal_sound.play()
        game.update()
        return

    capture = False
    capture_piece = None
    if game.bord[des_y][des_x] is not None:
        capture = True
        capture_piece = game.bord[des_y][des_x].type_piece

    # Handle en passant
    if can_en_passant(game, original_x, original_y, des_x, des_y):
        capture = True
        capture_piece = game.bord[original_y][des_x].type_piece
        movement = execute_en_passant(game, original_x, original_y, des_x, des_y)
        draw_bord(game.screen, game)
        game.update()
        game.switch_turn()
        game.capture_sound.play()
        game.last_move = {
            'piece_type': PAWN,
            'from_x': original_x,
            'from_y': original_y,
            'to_x': des_x,
            'to_y': des_y,
            'en_passant': True,
            'castle': False,
            'capture_piece': capture_piece

        }
        return movement

    piece = game.bord[original_y][original_x]

    # Handle castling
    if piece.type_piece == KING and (des_x, des_y) == piece.queen_castle and piece.nb_move == 0:
        movement = execute_castle(game, piece.color, False)
        draw_bord(game.screen, game)
        game.update()
        game.switch_turn()
        game.castle_sound.play()
        game.last_move = {
            'piece_type': KING,
            'from_x': original_x,
            'from_y': original_y,
            'to_x': des_x,
            'to_y': des_y,
            'en_passant': False,
            'castle': True,
            'capture_piece': capture_piece}
        return movement
    elif piece.type_piece == KING and (des_x, des_y) == piece.king_castle and piece.nb_move == 0:
        movement = execute_castle(game, piece.color, True)
        draw_bord(game.screen, game)
        game.update()
        game.switch_turn()
        game.castle_sound.play()
        game.last_move = {
            'piece_type': KING,
            'from_x': original_x,
            'from_y': original_y,
            'to_x': des_x,
            'to_y': des_y,
            'en_passant': False,
            'castle': True,
            'capture_piece': capture_piece}
        return movement

    # Execute normal move
    piece.nb_move += 1
    promotion = game.bord[original_y][original_x].promotion(des_x, des_y)

    # Generate algebraic notation
    notation = algebraic_notation(game, original_x, original_y, des_x, des_y, capture, game.check, game.checkmate,
                                  piece.type_piece, promotion)

    # Update board state
    game.bord[des_y][des_x] = piece
    game.bord[original_y][original_x] = None
    draw_bord(game.screen, game)
    game.update()

    if promotion:
        game.update()

    # Update game state
    game.increment(game.turn, game.increment_time)
    game.switch_turn()
    game.check = is_check(game, game.turn)
    game.checkmate = game.is_checkmate(game.turn)
    game.stalemate = game.is_stalemate(game.turn)

    # Update notation and play sounds
    if game.checkmate:
        game.game_end_sound.play()
        notation += "#"
    elif game.stalemate:
        game.game_end_sound.play()
    elif game.check:
        game.move_check_sound.play()
        notation += "+"
    elif capture:
        game.capture_sound.play()
    else:
        game.move_self_sound.play()

    # Record the move
    game.last_move = {
        'piece_type': piece.type_piece,
        'from_x': original_x,
        'from_y': original_y,
        'to_x': des_x,
        'to_y': des_y,
        'en_passant': False,
        'castle': False,
        'capture_piece': capture_piece
    }
    return notation






def algebraic_notation( game,original_x,original_y, des_x, des_y, capture, check, checkmate, type_piece,promotion):
    other = find_other_piece(game,original_x,original_y,type_piece)

    if capture:
        if promotion:
            notation = COLUMNS[original_x] + "x" + COLUMNS[des_x] + ROWS[des_y] + "=" + PIECE_PGN[type_piece]

        elif type_piece == PAWN :
            notation = COLUMNS[original_x] + "x" + COLUMNS[des_x] + ROWS[des_y]

        elif other is not None and is_legal_move(game,other[0],other[1],des_x, des_y):
            notation = PIECE_PGN[type_piece] + COLUMNS[original_x] + ROWS[original_y] + "x" + COLUMNS[des_x] + ROWS[des_y]

        else:
            notation = PIECE_PGN[type_piece] + "x" + COLUMNS[des_x] + ROWS[des_y]


        return notation
    else:
        if promotion:
            notation = COLUMNS[des_x] + ROWS[des_y] + "=" + PIECE_PGN[type_piece]
        elif type_piece == PAWN :
            notation = COLUMNS[des_x] + ROWS[des_y]

        elif other is not None and is_legal_move(game,other[0],other[1],des_x, des_y):
            notation = PIECE_PGN[type_piece] + COLUMNS[original_x] + ROWS[original_y]  + COLUMNS[des_x] + ROWS[des_y]
        else:
            notation = PIECE_PGN[type_piece] + COLUMNS[des_x] + ROWS[des_y]

        return notation


def create_pgn(list_coup,color,game):
    with open("game_save.txt","w") as file:
        result = ""
        if color == WHITE and game.checkmate:
            result = "0-1"
        elif color == BLACK and game.checkmate:
            result = "1-0"
        elif game.stalemate:
            result = "1/2-1/2"
        else:
            result = "*"
        file.write(f'[Event ""]\n'
                   f'[Site ""]\n'
                   f'[Date ""]\n'
                   f'[Round ""]\n'
                   f'[White "Player_1"]\n'
                   f'[Black "Player_2"]\n'
                   f'[Result "{result}"]\n'
                   f'[FEN "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"]\n')
        for i in range(len(list_coup)):
            file.write(f"{i+1}. ")
            for movement in list_coup[i]:
                file.write(f"{movement} ")
        file.write(result)


def can_castle_king_side(game, color):
    """
    Vérify if the king side castle is possible
    """
    king_x, king_row = king_pos(game.bord,color)
    rook_x = 7

    # We verify is the king and the rook didn't move

    king = game.bord[king_row][king_x]
    rook = game.bord[king_row][rook_x]

    if  king.color != color or king.nb_move > 0:
        return False
    if rook is None or rook.type_piece != ROOK or rook.color != color or rook.nb_move > 0:
        return False

    # Check that the squares between the king and the rook are empty
    for x in range(5, 7):
        if game.bord[king_row][x] is not None:
            return False

    # Check that the king is not in check and does not pass through an attacked square.
    if game.check:
        return False

    # Simulate the king's movement square by square
    for x in range(4, 7):
        if not is_safe_move(game, king_x, king_row, x, king_row, color):
            return False

    return True


def can_castle_queen_side(game, color):
    """
    Vérify if the king side castle is possible
    """
    king_x, king_row = king_pos(game.bord,color)
    rook_x =  0

    # We verify if the king and the rook didn't move

    king = game.bord[king_row][king_x]
    rook = game.bord[king_row][rook_x]

    if  king.color != color or king.nb_move > 0:
        return False
    if rook is None or rook.type_piece != ROOK or rook.color != color or rook.nb_move > 0:
        return False

    # Check that the squares between the king and the rook are empty

    for x in range(1, 4):
        if game.bord[king_row][x] is not None:
            return False

    # Check that the king is not in check and does not pass through an attacked square.

    if game.check:
        return False

    # Simulate the king's movement square by square

    for x in range(4, 1, -1):
        if not is_safe_move(game, king_x, king_row, x, king_row, color):
            return False

    return True


def execute_castle(game, color, king_side=True):
    """
    Exécute le roque
    """
    king_row = 7 if color == WHITE else 0

    if king_side:
        # Roque côté roi
        king_new_x, rook_old_x, rook_new_x = 6, 7, 5
    else:
        # Roque côté dame
        king_new_x, rook_old_x, rook_new_x = 2, 0, 3

    # Déplacer le roi
    king = game.bord[king_row][4]
    game.bord[king_row][king_new_x] = king
    game.bord[king_row][4] = None
    king.nb_move += 1

    # Déplacer la tour
    rook = game.bord[king_row][rook_old_x]
    game.bord[king_row][rook_new_x] = rook
    game.bord[king_row][rook_old_x] = None
    rook.nb_move += 1

    return "O-O" if king_side else "O-O-O"

def can_en_passant(game,orig_x,orig_y,des_x,des_y):
    pawn = game.bord[orig_y][orig_x]
    if pawn is None or pawn.type_piece != PAWN:
        return False
    color = pawn.color
    if (color == WHITE and pawn.y != 3) or (color == BLACK and pawn.y != 4):
        return False
    dx = des_x - orig_x
    dy = des_y - orig_y

    if (dx,dy) not in pawn.movement_2:
        return False

    adjacent_pawn = game.bord[orig_y][des_x]
    if adjacent_pawn is None or adjacent_pawn.type_piece != PAWN or adjacent_pawn.color == color:
        return False

    if game.last_move is None:
        return False

    if (game.last_move["piece_type"] == PAWN and
        game.last_move["to_x"] == des_x and
        game.last_move["to_y"] == orig_y and
        abs(game.last_move['from_y'] - game.last_move['to_y']) == 2):
        return True
    return False

def execute_en_passant(game,orig_x,orig_y,des_x,des_y):
    pawn = game.bord[orig_y][orig_x]
    pawn.nb_move += 1
    game.bord[orig_y][des_x] = None
    game.bord[des_y][des_x] = pawn
    game.bord[orig_y][orig_x] = None
    return f"{COLUMNS[orig_x]}x{COLUMNS[des_x]}{ROWS[des_y]}"


def find_other_piece(game,orig_x,orig_y,type_piece):
    for y in range(8):
        for x in range(8):
            if game.bord[y][x] is not None:
                if game.bord[y][x].type_piece == type_piece and (x,y) != (orig_x,orig_y) and game.bord[y][x].color == game.bord[orig_y][orig_x].color:
                    return x,y
    return

























