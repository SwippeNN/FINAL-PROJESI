from os import stat_result
import pygame, sys
from pygame.font import Font



class Menu():
    def __init__(self, game):
        self.game = game
        self.mid_w, self.mid_h, = self.game.DISPLAY_W/2, self.game.DISPLAY_H/2
        self.run_display = True
        self.crusor_rect = pygame.Rect(0, 0, 20, 20)
        self.offset = - 100

    def draw_cursor(self):
        self.game.draw_text('-->', 15, self.crusor_rect.x, self.crusor_rect.y)


    def blit_screen(self):
        # bg =  pygame.image.load("bg.png")   
        # self.game.window.blit(bg, (0,0))
        
        self.game.window.blit(self.game.display, (0,0))
        
        pygame.display.update()
        self.game.reset_keys()
class MainMenu(Menu):
    def __init__(self, game):
        Menu. __init__(self, game)
        self.state = "Start"
        self.startx, self.starty = self.mid_w, self.mid_h + 30
        self.optionsx, self.optionsy = self.mid_w, self.mid_h + 50
        self.creditsx, self.creditsy = self.mid_w, self.mid_h + 70
        self.Quitax, self.Quitay = self.mid_w, self.mid_h + 90
        self.crusor_rect.midtop = (self.startx + self.offset, self.starty)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.fill(self.game.BLACK)
            self.game.draw_text('Main Menu', 20, self.game.DISPLAY_W/2, self.game.DISPLAY_H/2 - 20)
            self.game.draw_text("Start Game", 20, self.startx, self.starty)
            self.game.draw_text("Options", 20, self.optionsx, self.optionsy)
            self.game.draw_text("Credits", 20, self.creditsx, self.creditsy)
            self.game.draw_text("Quit", 20, self.Quitax, self.Quitay)
            self.draw_cursor()
            self.blit_screen()

    def move_cursor(self):
        if self.game.DOWN_KEY:
            if self.state == 'Start':
                self.crusor_rect.midtop = (self.optionsx + self.offset, self.optionsy)
                self.state = 'Options'
            elif self.state == 'Options':
                self.crusor_rect.midtop = (self.creditsx + self.offset, self.creditsy)
                self.state = 'Credits'
            elif self.state == 'Credits':
                self.crusor_rect.midtop = (self.Quitax + self.offset, self.Quitay)
                self.state = 'Quit'
            elif self.state == 'Quit':
                self.crusor_rect.midtop = (self.startx + self.offset, self.starty)
                self.state = 'Start'
        elif self.game.UP_KEY:
            if self.state == 'Start':
                self.crusor_rect.midtop = (self.Quitax + self.offset, self.Quitay)
                self.state = 'Quit'
            elif self.state == 'Options':
                self.crusor_rect.midtop = (self.startx + self.offset, self.starty)
                self.state = 'Start'
            elif self.state == 'Credits':
                self.crusor_rect.midtop = (self.optionsx + self.offset, self.optionsy)
                self.state = 'Options'   
            elif self.state == 'Quit':
                self.crusor_rect.midtop = (self.creditsx + self.offset, self.creditsy)
                self.state = 'Credits'

    def check_input(self):
        self.move_cursor()
        if self.game.START_KEY:
            if self.state == 'Start':
                self.game.playing = True
            elif self.state == 'Options':
                self.game.curr_menu = self.game.options
            elif self.state == 'Credits':
                self.game.curr_menu = self.game.credits
                pass
            elif self.state == 'Quit':
                self.game.curr_menu = self.game.Quitt
            self.run_display = False
            
        
            
class CreditsMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            if self.game.START_KEY or self.game.BACK_KEY:
                self.game.curr_menu = self.game.main_menu
                self.run_display = False
            self.game.display.fill(self.game.BLACK)
            self.game.draw_text('Credits', 20, self.game.DISPLAY_W/2, self.game.DISPLAY_H/2 - 20)
            self.game.draw_text('Made by BERİBOSİNALPS', 15, self.game.DISPLAY_W/2, self.game.DISPLAY_H/2 +10)
            self.blit_screen()

class OptionsMenu(Menu):
    def __init__(self, game):
        Menu. __init__(self, game)
        self.state = "Volume"
        self.volx, self.voly = self.mid_w, self.mid_h + 20
        self.controlsx, self.controlsy = self.mid_w, self.mid_h + 40
        self.crusor_rect.midtop = (self.volx + self.offset, self.voly)
    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.fill((0, 0, 0))
            self.game.draw_text('Options', 20, self.game.DISPLAY_W/2, self.game.DISPLAY_H/2 - 30)
            self.game.draw_text("Volume", 15, self.volx, self.voly)
            self.game.draw_text("Controls", 15, self.controlsx, self.controlsy)
            self.draw_cursor()
            self.blit_screen()
    def check_input(self):
        if self.game.BACK_KEY:
            self.game.curr_menu = self.game.main_menu
            self.run_display = False
        elif self.game.UP_KEY or self.game.DOWN_KEY:
            if self.state == 'Volume':
                self.state = 'Controls'
                self.crusor_rect.midtop = (self.controlsx + self.offset, self.controlsy)
                
            elif self.state == 'Controls':
                self.crusor_rect.midtop = (self.volx + self.offset, self.voly)
                self.state = 'Volume'
                self.crusor_rect.midtop = (self.volx + self.offset, self.voly)
        elif self.game.START_KEY:
            pass


# class QuitMenu(Menu):
#     def __init__(self, game):
#         Menu.__init__(self, game)

#     def display_menu(self):
#         self.run_display =  True
#         while self.run_display:
#             self.game.check_events()
#             if self.game.START_KEY or self.game.BACK_KEY:
#                 self.game.curr_menu = self.game.main_menu
#                 self.run_display = False
#             self.game.display.fill(self.game.BLACK)
#             self.game.draw_text('Quit', 20, self.game.DISPLAY_W/2, self.game.DISPLAY_H/2 - 20)
#             self.game.draw_text('Made by BERİBOSİNALPS', 15, self.game.DISPLAY_W/2, self.game.DISPLAY_H/2 +10)
#             self.blit_screen() 

            
#     def display_menu(self):
#         self.run_display = True
#         while self.run_display:
#             self.game.check_events()
#             if self.game.START_KEY or self.game.BACK_KEY:
#                 self.game.curr_menu = self.game.main_menu
#                 self.run_display = False
#             self.game.display.fill(self.game.BLACK)
#             self.game.draw_text('Credits', 20, self.game.DISPLAY_W/2, self.game.DISPLAY_H/2 - 30)
#             self.game.draw_text('Made by BERİBOSİNALPS', 15, self.game.DISPLAY_W/2, self.game.DISPLAY_H/2 +10)
#             self.blit_screen()




# class volumeMenu(Menu):
#     def __init__(self, game):
#         Menu. __init__(self, game)
#         self.state = "on"
#         self.onx, self.ony = self.mid_w, self.mid_h + 20
#         self.offx, self.offy = self.mid_w, self.mid_h + 40
#         self.crusor_rect.midtop = (self.onx + self.offset, self.ony)
#     def display_menu(self):
#         self.run_display = True
#         while self.run_display:
#             self.game.check_events()
#             self.check_input()
#             self.game.display.fill(self.game.BLACK)
#             self.game.draw_text('Volume', 20, self.game.DISPLAY_W/2, self.game.DISPLAY_H/2 - 30)
#             self.game.draw_text("on", 20, self.onx, self.ony)
#             self.game.draw_text("off", 20, self.offx, self.offy)
#             self.draw_cursor()
#             self.blit_screen()
#     def check_input(self):
#         if self.game.BACK_KEY:
#             self.game.curr_menu = self.game.main_menu
#             self.run_display = False
#         elif self.game.UP_KEY or self.game.DOWN_KEY:
#             if self.state == 'on':
#                 self.state = 'off'
#                 self.crusor_rect.midtop = (self.offx + self.offset, self.offy)
                
#             elif self.state == 'off':
#                 self.crusor_rect.midtop = (self.onx + self.offset, self.ony)
#                 self.state = 'on'
#                 self.crusor_rect.midtop = (self.onx + self.offset, self.ony)

class Quitmenu(Menu):
    pygame.quit()
    
    
    
    
    
    