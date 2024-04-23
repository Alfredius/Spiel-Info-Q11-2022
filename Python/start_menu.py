import pygame
import sys
from PIL import Image
import time
import math
import os

pygame.init()
# pygame.mouse.set_visible(False)
info_object = pygame.display.Info()
screen_size = (info_object.current_w, info_object.current_h)

display = pygame.display.set_mode(screen_size, pygame.FULLSCREEN | pygame.SCALED, vsync=True)

class gamestate:
    def __init__(self):
        self.running = False
        self.level = 0


class PulsatingText:

    Texts = []
    def __init__(self, display, text, center, font_size=36):
        """defines a new pulsating text.
        
        display: pygame instance of the display to draw on.
        text: text the pulsating text should display in game.
        center: list(x-position, y-positio).
        fint_size: default = 36px."""
        self.display = display
        self.text = text
        self.center = center
        self.font_size = font_size
        self.phase = 0
        PulsatingText.Texts.append(self)

    def update(self):
        """updates the phase of the blink."""
        self.phase = (self.phase + 0.04) % (2 * math.pi)

    def draw(self):
        """draws the Text on the display"""
        pulse_val = abs(math.sin(self.phase)) 
        pulse_color = (pulse_val * 255, pulse_val * 255, pulse_val * 255)
        font = pygame.font.SysFont(None, self.font_size) 
        rendered_text = font.render(self.text, True, pulse_color)
        text_rect = rendered_text.get_rect(center=self.center)
        self.display.blit(rendered_text, text_rect)



class Startmenu():
    def __init__(self, display):
        """defines a new startmenu.

        display: instance of the display to draw on."""
        self.display = display
        self.font_size = 15
        self.font = pygame.font.SysFont(None, self.font_size) 
        self.color_l = (0,0,0)
        self.color_r = (0,0,0)
        y = 200
        PulsatingText(display, "Wähle dein Level", (screen_size[0]//2, 100), 36)
        


    def draw(self):
        """draws the startmenue to the display"""
        x = screen_size[0]//2
        y = 200


        text = self.font.render(f"Level: {1}", True, (255, 255, 255))
        self.display.blit(text, (x-15, y+100))


        pygame.draw.rect(self.display, (255, 0, 0), (x-85, y-30, 40, 70), 0)
        

        
    def check_input(self, events):
        """checks input to the startmenue.
        events: pygame.event"""
        x = screen_size[0]//2
        y = 200
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()

                if pygame.Rect(x-85, y-30, 40, 70).collidepoint(mouse_pos): 
                    print('click')
                    gs.level = 1
                    gs.running = False


        


start_menu = Startmenu(display)



gs = gamestate
def main():
    pygame.mixer.init()
    pygame.mixer.music.load("/Users/i589040/Documents/GitHub/Spiel-Info-Q11-2022/Sounds/Background/696485__gis_sweden__minimal-tech-background-music-mtbm02.wav") 
    pygame.mixer.music.play(-1,0.0)
    gs.running = True
    while gs.running:
        display.fill((0,0,0))

        events = pygame.event.get()
        keys = pygame.key.get_pressed()
        for event in events:
            if event.type == pygame.QUIT:
                gs.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    gs.running = False

        start_menu.check_input(events)
        for texts in PulsatingText.Texts:
            texts.update()
            texts.draw()
        start_menu.draw()
        pygame.display.flip()
    pygame.mixer.pause()
    return gs.level

if __name__ == '__main__':
    main()