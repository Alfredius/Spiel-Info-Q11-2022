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
        self.level = "exit"
        self.Options_prototype = {
            "master volume":1,
            "jump volume":1,
            "shot volume":1,
        }


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


class Slider():
    def __init__(self, display, x, y, width, height, color, min_val, max_val, start_val):
        """defines an instance of a Slider. 
        
         display: pygame instance of the display to draw on.
         x,y: x- and y coordinates of the slider.
         width: width of the slider.
         height: height of the slider.
         color: color of the slider (R,G,B).
         min_val: minimum value.
         max_value: maximum value.
         start_val: presest starting value.
        """
        self.display = display
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color 
        self.min_val = min_val
        self.max_val = max_val
        self.start_val = start_val
        self.current_val = start_val
        self.rect = pygame.Rect(x, y, width, height)
        self.dragging = False
        self.dragging_pos = 0
    
    def draw(self):
        """draws the paddle."""
        pygame.draw.rect(self.display, self.color, self.rect)
        pygame.draw.rect(self.display, (255, 255, 255), self.rect, 2)
        pygame.draw.rect(self.display, (255, 255, 255), (self.x + self.current_val/self.max_val * self.width - 5, self.y - 5, 10, self.height + 10))
        font = pygame.font.SysFont(None, 36)
        text = font.render(str(self.current_val), True, (255, 255, 255))
        self.display.blit(text, (self.x + self.current_val/self.max_val * self.width - 10, self.y + self.height + 10))
    
    def check_input(self, events):
        """checks the inputs to the slider.
        events: pygame.event"""
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if self.rect.collidepoint(mouse_pos): 
                    self.dragging = True
                    self.dragging_pos = mouse_pos[0] - self.x
                    self.current_val = (mouse_pos[0] - self.x) / self.width * self.max_val
                    self.current_val = int(max(self.min_val, min(self.current_val, self.max_val)))
            elif event.type == pygame.MOUSEBUTTONUP:
                mouse_pos = pygame.mouse.get_pos()
                if self.dragging: 
                    # pygame.mixer.Sound.play(gs.click_sound)
                    pass
                self.dragging = False
            elif event.type == pygame.MOUSEMOTION:
                if self.dragging:
                    mouse_pos = pygame.mouse.get_pos()
                    self.current_val = (mouse_pos[0] - self.x) / self.width * self.max_val
                    self.current_val = int(max(self.min_val, min(self.current_val, self.max_val)))



class Startmenu():
    def __init__(self, display):
        """defines a new startmenu.
        display: instance of the display to draw on."""
        self.display = display
        self.font_size = 18
        self.font = pygame.font.SysFont(None, self.font_size) 
        self.color_l = (0,0,0)
        self.color_r = (0,0,0)
        self.y = 200
        self.x = screen_size[0]//2
        self.s1 = Slider(display,self.x-100,self.y,200,20,(50,50,50),0,100,100)
        self.s2 = Slider(display,self.x-100,self.y+100,200,20,(50,50,50),0,100,100)
        self.s3 = Slider(display,self.x-100,self.y+200,200,20,(50,50,50),0,100,100)
        


    def draw(self):
        """draws the startmenue to the display"""

        pygame.draw.rect(self.display, (150, 0, 0), (screen_size[0]-150, 70, 70, 30), 0)
        text = self.font.render(f"Beenden", True, (200, 200, 200))
        self.display.blit(text, (screen_size[0]-145, 80))
        text = pygame.font.SysFont(None, 36).render(f"Master Volume", True, (200, 200, 200))
        self.display.blit(text, (self.x-text.get_width()//2, self.y-50))
        self.s1.draw()
        text = pygame.font.SysFont(None, 36).render(f"Jump Volume", True, (200, 200, 200))
        self.display.blit(text, (self.x-text.get_width()//2, self.y+50))
        self.s2.draw()
        text = pygame.font.SysFont(None, 36).render(f"Shot Volume", True, (200, 200, 200))
        self.display.blit(text, (self.x-text.get_width()//2, self.y+150))
        self.s3.draw()
        

        
    def check_input(self, events):
        """checks input to the startmenue.
        events: pygame.event"""
        

        options.check_input(events)
        self.s1.check_input(events)
        self.s2.check_input(events)
        self.s3.check_input(events)
        gs.Options_prototype["master volume"] = self.s1.current_val/100
        gs.Options_prototype["jump volume"] = self.s2.current_val/100
        gs.Options_prototype["shot volume"] = self.s3.current_val/100

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()

                if pygame.Rect(screen_size[0]-150, 70, 70, 30).collidepoint(mouse_pos): 
                    print('click')
                    gs.level = "exit"
                    gs.running = False


class Options():
    def __init__(self) -> None:
        self.x = screen_size[0]//2 + 100
        self.y = screen_size[1]//2 + 200
        self.w = 90
        self.h = 35
        self.font_size = 24
        self.font = pygame.font.SysFont(None, self.font_size) 

    def draw(self, surface):
        pygame.draw.rect(surface, (255, 0, 0), (self.x, self.y, self.w, self.h))
        text = self.font.render(f"Zurück", True, (255, 255, 255))
        surface.blit(text, (self.x+10, self.y+10))

    def check_input(self, events):
        """checks input to the startmenue.
        events: pygame.event"""
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()

                if pygame.Rect(self.x-5, self.y-5, self.w+10, self.h+10).collidepoint(mouse_pos): 
                    print('click')
                    gs.running = False
                    

start_menu = Startmenu(display)
options = Options()


gs = gamestate()
def main(optionen):
    gs.Options_prototype = optionen
    start_menu.s1.current_val = optionen["master volume"]*100
    start_menu.s2.current_val = optionen["jump volume"]*100
    start_menu.s3.current_val = optionen["shot volume"]*100

    # pygame.mixer.init()
    # pygame.mixer.music.load("/Users/i589040/Documents/GitHub/Spiel-Info-Q11-2022/Sounds/Background/696485__gis_sweden__minimal-tech-background-music-mtbm02.wav") 
    # pygame.mixer.music.play(-1,0.0)
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
                    gs.level = "exit"
        options.draw(display)
        start_menu.check_input(events)
        for texts in PulsatingText.Texts:
            texts.update()
            texts.draw()
        start_menu.draw()
        pygame.display.flip()
    # pygame.mixer.pause()
    return gs.Options_prototype

if __name__ == '__main__':
    main(gs.Options_prototype)