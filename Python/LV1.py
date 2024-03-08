import pygame
import sys
from PIL import Image
import time
import math

pygame.init()
pygame.mixer.init()
pygame.mixer.music.load("/Users/i589040/Documents/GitHub/Spiel-Info-Q11-2022/Sounds/Background/696485__gis_sweden__minimal-tech-background-music-mtbm02.wav") 
pygame.mixer.music.play(-1,0.0)
# pygame.mouse.set_visible(False)
info_object = pygame.display.Info()
screen_size = (info_object.current_w, info_object.current_h)

SPEED_LATERAL = 5

display = pygame.display.set_mode(screen_size, pygame.FULLSCREEN | pygame.SCALED, vsync=True)

background = pygame.image.load('/Users/i589040/Documents/GitHub/Spiel-Info-Q11-2022/Bilder/Level 1/Level1_11200x1080_V3.1_hintergrund_1.png').convert()
background_foreground = pygame.image.load('/Users/i589040/Documents/GitHub/Spiel-Info-Q11-2022/Bilder/Level 1/Level1_11200x1080_V3.3_vordergrund.png').convert_alpha()
background_middle_foreground = pygame.image.load('/Users/i589040/Documents/GitHub/Spiel-Info-Q11-2022/Bilder/Level 1/Level1_11200x1080_V3.2_hintergrund_2.png').convert_alpha()

level1_enemys_positiones = [(1000,250)]

class enemy:
    enemies = []
    def __init__(self,coordinates) -> None:
        enemy.enemies.append(self)
        self.coordinates = coordinates
        self.image = pygame.image.load("/Users/i589040/Documents/GitHub/Spiel-Info-Q11-2022/Bilder/Objekte/PNG/Foreground/Hindernisse/Container_Side_1.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (200, 400))


    def draw(self, surface:pygame.surface):
        surface.blit(self.image, (self.coordinates[0] + world.x,self.coordinates[1]))

for e in level1_enemys_positiones:
    enemy(e)

class GameState:
    def __init__(self):
        self.running = True
        self.dt_last_frame = 1

class ObstacleMap:
    def __init__(self, image_path):
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (11200, 1080))

    def collides_horizontally_right(self, rect:pygame.Rect):
        for y in range(rect.y+25, rect.y + rect.h-25):
            try:
                if self.image.get_at((rect.x + rect.w, y)) != (0, 0, 0, 0):
                    return True
            except IndexError:
                pass
        return False
    
    def collides_horizontally_left(self, rect:pygame.Rect):
        for y in range(rect.y+25, rect.y + rect.h-25):
            try:
                if self.image.get_at((rect.x, y)) != (0, 0, 0, 0):
                    return True

            except IndexError:
                pass
        return False

    def collides_vertically_top(self, rect):
        for x in range(rect.x+4, rect.x + rect.w-4):
            try:
                if self.image.get_at((x, rect.y)) != (0, 0, 0, 0):
                    return True

            except IndexError:
                pass
        return False
    
    def collides_vertically_bottom(self, rect):
        for x in range(rect.x+4, rect.x + rect.w-4):
            try: 
                if self.image.get_at((x, rect.y + rect.h)) != (0, 0, 0, 0):
                    for y in range(int(rect.y+rect.h*0.5), rect.y + rect.h):
                            if self.image.get_at((rect.x+rect.w-10, y)) != (0, 0, 0, 0):
                                player.y = y-rect.h
                                break
                            if self.image.get_at((rect.x+10, y)) != (0, 0, 0, 0):
                                player.y = y-rect.h
                                break
                    return True
            except IndexError:
                pass
        return False
    
    def collides(self, rect:pygame.Rect):
        for y in range(rect.y, rect.y + rect.h):
            try:
                if self.image.get_at((rect.x, y)) != (0, 0, 0, 0):
                    return True

            except IndexError:
                pass

        for x in range(rect.x, rect.x + rect.w):
            try: 
                if self.image.get_at((x, rect.y)) != (0, 0, 0, 0):
                    return True
            except IndexError:
                pass

        return False
    
obstacle_map = ObstacleMap("/Users/i589040/Documents/GitHub/Spiel-Info-Q11-2022/Bilder/Level 1/Level1_11200x1080_V1_Collisions_kopie-auflösung niedrig.png")

class World:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.background_rect = background.get_rect()
        self.background_foreground_rect = background_foreground.get_rect()
        self.background_middle_foreground_rect = background_middle_foreground.get_rect()
        self.background = background
        self.background_foreground = background_foreground
        self.background_middle_foreground = background_middle_foreground

    def draw(self, surface):
        surface.blit(self.background, self.background_rect)
        surface.blit(self.background_middle_foreground, self.background_middle_foreground_rect)
        surface.blit(self.background_foreground, self.background_foreground_rect)

    def move(self, dx):
        if(self.x <= 0 or dx < 0):
            self.x += dx
            self.background_foreground_rect = self.background_foreground_rect.move(dx,0)
            self.background_middle_foreground_rect = self.background_middle_foreground_rect.move(dx/2,0)
            self.background_rect = self.background_rect.move(dx/4,0)


        

class Player:
    def __init__(self):
        self.x, self.y = screen_size[0] // 2, screen_size[1] // 2
        self.dy = 0
        self.jump_enabled = True
        self.gravity = 0.3
        self.jump_height = 12
        self.scale = 0.15
        self.animation_frames = self.load_gif("/Users/i589040/Documents/GitHub/Spiel-Info-Q11-2022/Bilder/Objekte/Test 2 Animation running 1.gif",self.scale)
        self.animation_frames_jumping_up = self.load_gif("/Users/i589040/Documents/GitHub/Spiel-Info-Q11-2022/Bilder/Objekte/Test 2 Animation running 1.gif",self.scale)
        self.animation_frames.pop(0)
        self.current_frame = 0
        self.rect = self.animation_frames[0].get_rect()
        self.walking_right = False
        self.walking_left = False
        self.crouch = False
        self.jumping_sound = pygame.mixer.Sound("/Users/i589040/Documents/GitHub/Spiel-Info-Q11-2022/Sounds/Player/399095__plasterbrain__8bit-jump.flac")
        self.jumping_sound.set_volume(0.8)
        self.last_jump = time.time()

    @staticmethod
    def load_gif(path, scale):
        img = Image.open(path)
        frames = []
        try:
            while True:
                frame = pygame.image.fromstring(img.tobytes(), img.size, img.mode).convert_alpha()
                frame = pygame.transform.scale(frame, (frame.get_width() * scale, frame.get_height() * scale))
                frame.set_colorkey((255,255,255))  # Make white (also the default) color transparent
                frames.append(frame)
                img.seek(len(frames))
        except EOFError:
            pass
        return frames

    def draw(self, surface):
        image = self.animation_frames[int(self.current_frame)]
        if self.dy < 0:
            image = self.animation_frames_jumping_up[1]
            image = pygame.transform.scale(image, (image.get_width(), image.get_height()))
            image.set_colorkey((255,255,255))
        current_width, current_height = image.get_size()
        if self.walking_left:
            image = pygame.transform.flip(image, True, False)
            image.set_colorkey((255,255,255))
        if self.crouch:
            image = pygame.transform.scale(image, (current_width, current_height*0.5))
            image.set_colorkey((255,255,255))  # Make white (also the default) color transparent
        self.rect = image.get_rect()

        surface.blit(image, (self.x, self.y))  

    def jump(self):
        test_rect = pygame.Rect(player.x - world.x, player.y, player.rect.w, player.rect.h).move(0, 2*self.dy)
        if obstacle_map.collides_vertically_bottom(test_rect) and self.jump_enabled:
            self.dy -= self.jump_height
            if (time.time() - self.last_jump) > 0.3:
                self.last_jump = time.time()
                pygame.mixer.Sound.play(self.jumping_sound)

    def update(self):
        self.prev_x, self.prev_y = self.x, self.y  # Remember previous position
       # Inside Player.update() method before applying gravity
        self.dy += self.gravity
        test_rect = pygame.Rect(player.x - world.x, player.y, player.rect.w, player.rect.h).move(0, self.dy)
        
        if obstacle_map.collides_vertically_top(test_rect) and self.dy < 0:
            self.dy = 0

        if not obstacle_map.collides_vertically_bottom(test_rect):
            self.y += self.dy
        elif not self.dy < 0:
            self.dy = 0

        if(self.walking_right):
            self.current_frame = (self.current_frame + gs.dt_last_frame/4 * 1) % (len(self.animation_frames))
        elif(self.walking_left):
            self.current_frame = (self.current_frame + gs.dt_last_frame/4 * 1) % (len(self.animation_frames))
        else:
            self.current_frame = 3

def get_rotation_angle(velocity):
    # velocity[0] is horizontal speed
    # velocity[1] is vertical speed
    if velocity[0]==0: # this conditional logic is done in order to handle the case whenever horizontal speed becomes zero to avoid zero division error
        return 90 if velocity[1]>0 else 270
    angle_in_radians = math.atan(velocity[1]/velocity[0])
    # convert radian to degree
    angle_in_degree = math.degrees(angle_in_radians)
    #Finding appropriate quadrant of angle
    if velocity[0]>0 and velocity[1]>0:
        final_angle = angle_in_degree
    elif velocity[0]<0 and velocity[1]>0:
        final_angle = 180 + angle_in_degree
    elif velocity[0]<0 and velocity[1]<0:
        final_angle = 180 + angle_in_degree
    elif velocity[0]>0 and velocity[1]<0:
        final_angle = 360 + angle_in_degree
    else:
        final_angle = angle_in_degree
    return final_angle

class shot:
    shots_list = []
    def __init__(self):
        shot.shots_list.append(self)
        self.image = pygame.image.load("/Users/i589040/Documents/GitHub/Spiel-Info-Q11-2022/Bilder/Objekte/PNG/Foreground/Hindernisse/Container_Side_1.png")
        self.image = pygame.transform.scale(self.image, (50,10))
        self.velocity = self.set_velocities()
        v = -get_rotation_angle(self.velocity)
        self.image = pygame.transform.rotate(self.image,v)
        self.coordinates = [player.x + player.rect.w/2 - world.x, player.y + player.rect.h/2]
    
    def move(self):
        self.coordinates[0] += self.velocity[0]
        self.coordinates[1] += self.velocity[1]

        test_rect = pygame.Rect(self.coordinates[0], self.coordinates[1], 5, 5)
        if obstacle_map.collides(test_rect):
            shot.shots_list.remove(self)


        

    def set_velocities(self) -> list:
        x,y = pygame.mouse.get_pos()
        v = [x - (player.x + player.rect.w/2), y - (player.y + player.rect.h/2)]
        v_l = math.sqrt(v[0]**2 + v[1]**2)
        v = [(i/v_l)*10 for i in v]
        return v
    
    def draw(self,surface):
        surface.blit(self.image, (self.coordinates[0] + world.x, self.coordinates[1]))  



world = World()
gs = GameState()
player = Player()
FPS = pygame.time.Clock()

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
                pygame.quit()
                sys.exit()
        if event.type == pygame.MOUSEBUTTONUP:
            shot()
    # In the game loop
    if keys[pygame.K_SPACE]:
        if not player.dy < 0:
            player.jump()

    if keys[pygame.K_d]:
            test_rect = pygame.Rect(player.x - world.x, player.y, player.rect.w, player.rect.h).move(1, 0)
            if not obstacle_map.collides_horizontally_right(test_rect):
                world.move(-SPEED_LATERAL)
                player.walking_right = True
    else:
        player.walking_right = False

    if keys[pygame.K_a]:

            test_rect = pygame.Rect(player.x - world.x, player.y, player.rect.w, player.rect.h).move(-1, 0)
            if not obstacle_map.collides_horizontally_left(test_rect):
                world.move(SPEED_LATERAL)
                player.walking_left = True
    else:
        player.walking_left = False

    if keys[pygame.K_LSHIFT]:
        player.crouch = True
        player.jump_enabled = False
    elif player.crouch == True:
        player.jump_enabled = True
        player.y -= player.rect.size[1]
        player.crouch = False



    player.update()
    world.draw(display)
    player.draw(display)
    for shots in shot.shots_list:
        shots.move()
        shots.draw(display)
    
    for e in enemy.enemies:
        e.draw(display)

    pygame.display.flip()
    gs.dt_last_frame = FPS.tick()/17

pygame.quit()
sys.exit()