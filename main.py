from classes.interface import *
from classes.game import Game
from utils.constante import *

pygame.init()
game = Game()


screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.NOFRAME)
pygame.display.set_caption("ChessRush")

while game.running:

    if game.in_menu:
        main_menu(game, screen)

    elif game.in_opponent_selection:
        opponent_selecting(game,screen)
    
    elif game.in_mode_selection:
        mode_selecting(game, screen)
        
    elif game.in_ath_selection:
        ATH_selecting(game, screen)

    elif game.is_playing:


        if screen.get_width() != GAME_WINDOW_WIDTH:
            screen = pygame.display.set_mode((GAME_WINDOW_WIDTH, GAME_WINDOW_HEIGHT),pygame.FULLSCREEN | pygame.NOFRAME )
        game.set_screen(screen)
            
        game.set_board(PLATEAU_INITIAL)
        game.start_game()
        # Après le jeu, on affiche la bannière
        End_banner(game, screen)
        # Si on quitte la bannière, on remet la taille normale pour le menu
        screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.NOFRAME)

pygame.quit()

