
from gameee import Game

# from pygame_animation import Game

g = Game()


while g.running:
    # g.pygame_animation() == time.sleep(4)
    g.curr_menu.display_menu()
    g.game_loop()