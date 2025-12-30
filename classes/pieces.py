from utils.functions import *


class Pieces:
    def __new__(cls,game, color = int, x = int, y = int, type_piece = int):
        if type_piece == PAWN:
            return super().__new__(Pawn)
        elif type_piece == KNIGHT:
            return super().__new__(Knight)
        elif type_piece == BISHOP:
            return super().__new__(Bishop)
        elif type_piece == ROOK:
            return super().__new__(Rook)
        elif type_piece == KING:
            return super().__new__(King)
        elif type_piece == QUEEN:
            return super().__new__(Queen)
    def __init__(self,game,color,x,y,type_piece):
        self.game = game
        self.color = color
        self.type_piece = type_piece
        self.nb_move = 0
        self.x = x
        self.y = y
        self.nb_possible_move = 0
        self.path = game.path

    def promotion(self,des_x,des_y):
        if self.type_piece == PAWN and self.color == WHITE and des_y == 0:
            self._promote_to_queen()
            self.game.update()
            return True
        elif self.type_piece == PAWN and self.color == BLACK and des_y == 7:
            self._promote_to_queen()
            self.game.update()
            return True

        return False
    def demotion(self):
        self.__class__ = Pawn
        self.type_piece = PAWN

        if self.color == WHITE:
            self.image = pygame.image.load(f"assets/{self.path}/white-pawn.png")
            self.movement = DIRECTIONS_WHITE_PAWN
            self.movement_1 = DIRECTIONS_WHITE_PAWN_1
            self.movement_2 = DIRECTIONS_WHITE_PAWN_2
        else:
            self.image = pygame.image.load(f"assets/{self.path}/black-pawn.png")
            self.movement = DIRECTIONS_BLACK_PAWN
            self.movement_1 = DIRECTIONS_BLACK_PAWN_1
            self.movement_2 = DIRECTIONS_BLACK_PAWN_2

        self.image = pygame.transform.smoothscale(self.image, (SIZE_PIECES, SIZE_PIECES))
        self.rect = self.image.get_rect(center=(chess_to_xy((self.x, self.y))))
        self.movement_type = JUMPING
        self.game.update()
        return

    def _promote_to_queen(self):
        self.__class__ = Queen
        self.type_piece = QUEEN

        if self.color == WHITE:
            self.image = pygame.image.load(f"assets/{self.path}/white-queen.png")

        else:
            self.image = pygame.image.load(f"assets/{self.path}/black-queen.png")
        self.image = pygame.transform.smoothscale(self.image, (SIZE_PIECES, SIZE_PIECES))

        self.movement = QUEEN_DIRECTION
        self.movement_type = SLIDING

        self.rect = self.image.get_rect(center=(chess_to_xy((self.x, self.y))))
        self.game.update()

    def count_possible_move(self):
        nb_possible_move = 0
        for y in range(8):
            for x in range(8):
                legal = is_legal_move(self.game, self.x, self.y, x, y,True)
                safe = is_safe_move(self.game, self.x, self.y, x, y,self.color)
                if legal and safe:
                    nb_possible_move += 1
        return nb_possible_move



    def reinitialise_possible_move(self):
        self.nb_possible_move = 0









class Pawn(Pieces):
    def __init__(self,game,color,x,y,type_piece):
        super().__init__(game,color,x,y,type_piece)
        self.game = game
        if self.color == WHITE :
            self.image = pygame.image.load(f"assets/{self.path}/white-pawn.png").convert_alpha()
            self.movement = DIRECTIONS_WHITE_PAWN
            self.movement_1 = DIRECTIONS_WHITE_PAWN_1
            self.movement_2 = DIRECTIONS_WHITE_PAWN_2
        else:
            self.image = pygame.image.load(f"assets/{self.path}/black-pawn.png").convert_alpha()
            self.movement = DIRECTIONS_BLACK_PAWN
            self.movement_1 = DIRECTIONS_BLACK_PAWN_1
            self.movement_2 = DIRECTIONS_BLACK_PAWN_2

        self.image = pygame.transform.smoothscale(self.image,(SIZE_PIECES,SIZE_PIECES))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.rect = self.image.get_rect(center=(chess_to_xy((self.rect.x,self.rect.y))))
        self.movement_type = JUMPING


class Knight(Pieces):
    def __init__(self,game,color,x,y,type_piece):
        super().__init__(game,color,x,y,type_piece)
        self.game = game
        if self.color == 1 :self.image = pygame.image.load(f"assets/{self.path}/white-knight.png").convert_alpha()
        else: self.image = pygame.image.load(f"assets/{self.path}/black-knight.png").convert_alpha()

        self.image = pygame.transform.smoothscale(self.image,(SIZE_PIECES,SIZE_PIECES))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.rect = self.image.get_rect(center=(chess_to_xy((self.rect.x, self.rect.y))))
        self.movement = KNIGHT_DIRECTION
        self.movement_type = JUMPING

class Bishop(Pieces):
    def __init__(self,game,color,x,y,type_piece):
        super().__init__(game,color,x,y,type_piece)
        self.game = game
        if self.color == 1 :self.image = pygame.image.load(f"assets/{self.path}/white-bishop.png").convert_alpha()
        else: self.image = pygame.image.load(f"assets/{self.path}/black-bishop.png").convert_alpha()

        self.image = pygame.transform.smoothscale(self.image,(SIZE_PIECES,SIZE_PIECES)).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.rect = self.image.get_rect(center=(chess_to_xy((self.rect.x, self.rect.y))))
        self.movement = BISHOP_DIRECTION
        self.movement_type = SLIDING

class Rook(Pieces):
    def __init__(self,game,color,x,y,type_piece):
        super().__init__(game,color,x,y,type_piece)
        self.game = game
        if self.color == WHITE :self.image = pygame.image.load(f"assets/{self.path}/white-rook.png").convert_alpha()
        else: self.image = pygame.image.load(f"assets/{self.path}/black-rook.png").convert_alpha()

        self.image = pygame.transform.smoothscale(self.image,(SIZE_PIECES,SIZE_PIECES))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.rect = self.image.get_rect(center=(chess_to_xy((self.rect.x, self.rect.y))))
        self.movement = ROOK_DIRECTION
        self.movement_type = SLIDING

class Queen(Pieces):
    def __init__(self,game,color,x,y,type_piece):
        super().__init__(game,color,x,y,type_piece)
        self.game = game
        if self.color == 1 :self.image = pygame.image.load(f"assets/{self.path}/white-queen.png").convert_alpha()
        else: self.image = pygame.image.load(f"assets/{self.path}/black-queen.png").convert_alpha()

        self.image = pygame.transform.smoothscale(self.image,(SIZE_PIECES,SIZE_PIECES))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.rect = self.image.get_rect(center=(chess_to_xy((self.rect.x, self.rect.y))))
        self.movement = QUEEN_DIRECTION
        self.movement_type = SLIDING

class King(Pieces):
    def __init__(self,game,color,x,y,type_piece):
        super().__init__(game,color,x,y,type_piece)
        self.game = game
        if self.color == 1 :self.image = pygame.image.load(f"assets/{self.path}/white-king.png").convert_alpha()
        else: self.image = pygame.image.load(f"assets/{self.path}/black-king.png").convert_alpha()

        self.image = pygame.transform.smoothscale(self.image,(SIZE_PIECES,SIZE_PIECES))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.rect = self.image.get_rect(center=(chess_to_xy((self.rect.x, self.rect.y))))
        self.movement = KING_DIRECTION
        self.movement_type = JUMPING
        self.queen_castle = (2,0) if color == BLACK else (2,7)
        self.king_castle = (6,0) if color == BLACK else (6,7)

