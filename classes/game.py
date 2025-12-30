
from classes.pieces import Pieces

from classes.interface import *
from classes.AI import*
from classes.stack import *



class Game:
    def __init__(self):
        self.running = True
        self.is_playing = False
        self.in_menu = True
        self.in_mode_selection = False
        self.in_ath_selection = False
        self.in_opponent_selection = False
        self.screen = None
        self.bord = []
        self.bord_color = CLASSICAL_BORD
        self.path = "pieces"
        self.state = {}
        self.time_is_stop = False
        self.is_increment = False
        self.increment_time = 0
        self.white_time = None
        self.black_time = None
        self.time = None
        self.turn = WHITE
        self.nb_turn = 1
        self.check = None
        self.checkmate = None
        self.stalemate = None
        self.last_move = None
        self.list_move = Stack()
        self.white_roque = True
        self.black_roque = True
        self.game_start_sound = pygame.mixer.Sound(f"assets/sounds/game-start.mp3")
        self.game_end_sound = pygame.mixer.Sound(f"assets/sounds/game-end.mp3")
        self.move_self_sound = pygame.mixer.Sound(f"assets/sounds/move-self.mp3")
        self.move_check_sound = pygame.mixer.Sound("assets/sounds/move-check.mp3")
        self.move_illegal_sound = pygame.mixer.Sound("assets/sounds/illegal.mp3")
        self.capture_sound = pygame.mixer.Sound("assets/sounds/capture.mp3")
        self.castle_sound = pygame.mixer.Sound("assets/sounds/castle.mp3")
        self.ai = AI(self)
        self.ai_enabled = True



    def set_screen(self,screen):
        self.screen = screen

    def set_bord(self,bord=PLATEAU_INITIAL):
        for y in range(len(bord)):
            row = []
            for x in range(len(bord[y])):
                pieces = bord[y][x]
                if pieces != EMPTY:
                    obj = Pieces(self,pieces[0], x, y, pieces[1])
                    row.append(obj)
                else: row.append(None)
            self.bord.append(row)

    def reinitialise_game(self):
        self.bord = []
        self.turn = WHITE
        self.nb_turn = 1
        self.white_roque = True
        self.black_roque = True
        self.checkmate = False
        self.check = False
        self.stalemate = False
        self.set_time(self.time)


    def update(self):
        """
        Update the position of the pieces in the bord to their coordinate
        :return:
        """
        for y in range(8):
            for x in range(8):
                if self.bord[y][x] is not None:
                    self.bord[y][x].rect = self.bord[y][x].image.get_rect(center=(chess_to_xy((x,y))))
                    self.bord[y][x].x = x
                    self.bord[y][x].y = y
                    self.screen.blit(self.bord[y][x].image, self.bord[y][x].rect)


    def switch_turn(self):
        self.turn = -self.turn
        display_current_player(self)
        if self.turn == WHITE:
            self.nb_turn += 1
        return self.turn

    def copy(self):
        bord = self.bord
        grid = []
        for y in range(8):
            row = []
            for x in range(8):
                piece = bord[y][x]
                if piece is None:
                    row.append(None)
                else:
                    row.append((piece.type_piece,piece.color,piece.movement_type,piece.nb_move))
            grid.append(row)

        if self.last_move:
            last_move_info = (self.last_move['piece_type'],
                              self.last_move['from_x'],
                              self.last_move['from_y'],
                              self.last_move['to_x'],
                              self.last_move['to_y'])
        else :
            last_move_info = None
        state = {'bord':grid,
                 'last_move_info':last_move_info,
                 'turn':self.turn,
                 'nb_turn':self.nb_turn
                 }
        return state

    def is_checkmate(self,color):
        if not self.check:
            return False
        for y in range(8):
            for x in range(8):
                piece = self.bord[y][x]
                if piece is not None and piece.color == color:
                    if piece.count_possible_move() != 0:
                        return False
        return True

    def is_stalemate(self, color):
        if self.is_pat(color):
            return True

        remaining = self.pieces_remaining()
        if sorted(remaining) == sorted([KING,KING]):
            return True
        if sorted(remaining) == sorted([KING,KING,BISHOP]):
            return True
        if sorted(remaining) == sorted([KING,KING,KNIGHT]):
            return True
        if sorted(remaining) == sorted([KING,BISHOP,KING,BISHOP]):
            return True
        return False

    def is_pat(self,color):
        if  self.check:
            return False
        for y in range(8):
            for x in range(8):
                piece = self.bord[y][x]
                if piece is not None and piece.color == color:
                    if piece.count_possible_move() != 0:
                        return False
        return True


    def set_time(self,time):
        self.white_time = time
        self.black_time = time
        self.time = time

    def set_increment_time(self,time):

        self.increment_time = time

    def decrement_time(self,color,dt):
        if color == WHITE and self.white_time > 1:
            self.white_time -= dt
        elif color == BLACK and self.black_time > 1:
            self.black_time -= dt

    def increment(self,color,time):
        if color == WHITE:
            self.white_time += time
        else:
            self.black_time += time

    def set_mode(self, time, increment_time=0):
        self.set_time(time)
        self.set_increment_time(increment_time)

    def stop_time(self):
        self.time_is_stop = True
    def start_time(self):
        self.time_is_stop = False




    def start_game(self):

        self.screen.fill(BACKGROUND_COLOR)
        display_current_player(self)
        draw_bord(self.screen,self)
        clock = pygame.time.Clock()
        selected_square = None
        self.game_start_sound.play()
        self.update()
        coup = []
        list_coup = []
        if self.time is not None:
            self.start_time()
        while self.is_playing:

            if self.end_game():
                self.is_playing = False


            dt = clock.tick(30) / 1000
            if self.time is not None:
                display_timer(self)
                if not self.time_is_stop:
                    self.decrement_time(self.turn, dt)

            if self.ai_enabled  and not self.end_game():
                # On rafraîchit l'écran pour voir le dernier
                pygame.display.flip()
                if self.turn == WHITE:
                    print("The White AI is thinking ...")

                    coup_ia = self.ai.get_best_move(depth=2)
                #else:
                #   print("The Black AI is thinking ...")
                #   coup_ia = self.ai.get_best_move(depth=2)

                    if coup_ia:
                        # On joue le coup avec la fonction normale qui gère l'affichage et le son
                        movement = move(self, coup_ia[0], coup_ia[1], coup_ia[2], coup_ia[3])

                        if movement is not None:
                            if self.turn == BLACK:
                                coup.append(movement)

                            else:
                                coup.append(movement)
                                list_coup.append(coup)
                                coup = []


            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_playing = False

                if event.type == pygame.MOUSEBUTTONUP:
                    self.update()
                    if selected_square is None:
                        selected_square = is_select(self, event)
                    else:
                        start_x, start_y = selected_square[0], selected_square[1]
                        if xy_to_chess(event.pos) is not None:
                            end_x, end_y = xy_to_chess(event.pos)
                            movement = move(self, start_x, start_y, end_x, end_y)

                            if movement is not None:
                                if self.turn == BLACK:
                                    coup.append(movement)

                                else:
                                    coup.append(movement)
                                    list_coup.append(coup)
                                    coup = []

                        selected_square = None
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.is_playing = False
                        self.reinitialise_game()
                    if event.key == pygame.K_t:
                        print(is_endgame(self.copy()))
                    if event.key == pygame.K_c:
                        cancel_move(self)



            pygame.display.flip()
        if coup:
            list_coup.append(coup)
        create_pgn(list_coup, -self.turn, self)
        self.stop_time()


    def set_bord_color(self,color):
        self.bord_color = color

    def set_piece(self,path):
        self.path = path

    def end_game(self):
        end = False
        if self.time is not None:
            if self.white_time < 1:
                end = True
            elif self.black_time < 1:
                end = True
        elif self.checkmate:
            end = True
        elif self.stalemate:
            end = True
        return end

    def pieces_remaining(self):
        pieces = []
        for y in range(8):
            for x in range(8):
                piece = self.bord[y][x]
                if piece is not None:
                    pieces.append(piece.type_piece)
        return pieces










