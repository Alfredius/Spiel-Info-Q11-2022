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

SPEED_LATERAL = 10

UI_X = 30
UI_Y = 850
MARGIN = 20

display = pygame.display.set_mode(screen_size, pygame.FULLSCREEN | pygame.SCALED, vsync=True)

background = pygame.image.load('/Users/i589040/Documents/GitHub/Spiel-Info-Q11-2022/Bilder/Level 1/Level1_11200x1080_V3.1_hintergrund_1.png').convert()
background_foreground = pygame.image.load('/Users/i589040/Documents/GitHub/Spiel-Info-Q11-2022/Bilder/Level 1/Level1_11200x1080_V3.3_vordergrund.png').convert_alpha()
background_middle_foreground = pygame.image.load('/Users/i589040/Documents/GitHub/Spiel-Info-Q11-2022/Bilder/Level 1/Level1_11200x1080_V3.2_hintergrund_2.png').convert_alpha()

level1_enemys_positiones = [[(1000,250),(100,200),1,2],[(1500,250),(100,200),2,1],[(2000,250),(100,200),5,0.5]]

class enemy:
    enemies = []
    def __init__(self,coordinates,size, hp, shots_per_seconds) -> None:
        enemy.enemies.append(self)
        self.last_shot_fired = 0
        self.shots_per_seconds = shots_per_seconds
        self.coordinates = coordinates
        self.x, self.y = coordinates
        self.max_health = hp
        self.health = hp
        self.image = pygame.image.load("/Users/i589040/Documents/GitHub/Spiel-Info-Q11-2022/Bilder/Objekte/PNG/Foreground/Hindernisse/Container_Side_1.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, size)


    def draw(self, surface:pygame.surface):
       surface.blit(self.image, (self.coordinates[0] + world.x,self.coordinates[1]))
       self.display_health_bar()

    def check_for_hit(self, coordinates) -> bool:
        x,y = coordinates
        if x > self.x and x < self.x+self.image.get_width():
            if y > self.y and y < self.y + self.image.get_height():
                return True
        return False

    
    def is_hit(self):
        self.health -= 1
        if self.health <= 0:
            enemy.enemies.remove(self)
            Collectable(self.x+self.image.get_width()//2, self.y+ self.image.get_height()//2)

    def display_health_bar(self):
        color = (int(255-255*(self.health/self.max_health)),int(255*(self.health/self.max_health)),0)
        pygame.draw.rect(display, color,pygame.Rect(self.coordinates[0] + world.x,self.coordinates[1]-25,100,20),3)
        pygame.draw.rect(display, color,pygame.Rect(self.coordinates[0] + world.x,self.coordinates[1]-25,100*(self.health/self.max_health),20))

    def fire_shot(self):
        if (time.time() - self.last_shot_fired) > (1/self.shots_per_seconds) and abs(player.x + player.rect.w/2 - world.x - self.x) < 1000:
            dx = player.x - (self.coordinates[0] + world.x)
            dy = player.y - self.coordinates[1]
            shot([player.x + player.rect.w/2 - world.x, player.y + player.rect.h/2],[self.x, self.y],False)
            self.last_shot_fired = time.time()

for e in level1_enemys_positiones:
    enemy(*e) 

class DialogBox:
    boxes = []
    def __init__(self, messages, cords, font=pygame.font.SysFont('Comic Sans MS', 30), color=(255, 255, 255)):
        self.coordinates = cords
        self.messages = messages
        self.current_message = 0
        self.font = font
        self.color = color
        self.text_surfaces = [font.render(msg, False, self.color) for msg in messages]
        DialogBox.boxes.append(self)

    def next_message(self):
        # No need to check bounds here, the draw method handles the case where we are out of bounds
        self.current_message += 1

    def draw(self, win):
        # If we are out of messages, don't draw anything
        if self.current_message >= len(self.messages):
            gs.shooting_enebled = True
            gs.movement_enebled  = True
            DialogBox.boxes.remove(self)
            if gs.end_of_game:
                gs.running = False
            return

        text_surface = self.text_surfaces[self.current_message]
        text_rect = text_surface.get_rect(center=self.coordinates)
        bubble_rect = text_rect.inflate(2*MARGIN, MARGIN)
        pygame.draw.rect(win, self.color, bubble_rect, 2)  # Speech bubble
        pygame.draw.polygon(win, self.color, [(bubble_rect.bottomleft[0], bubble_rect.bottomleft[1]-10),
                                               (bubble_rect.bottomleft[0]-5, bubble_rect.bottomleft[1] + 5),
                                               (bubble_rect.bottomleft[0]+10, bubble_rect.bottomleft[1])])  # Little triangle
        win.blit(text_surface, text_rect)  # Text

class Collectable:
    collectables = []
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.img_frames = []
        self.load("coins")
        self.current_frame = 0
        self.last_frame_time = time.time()
        Collectable.collectables.append(self)

    def draw(self, surface):
        surface.blit(self.img_frames[self.current_frame], (self.x + world.x - self.img_frames[self.current_frame].get_width()//2,self.y))
        if time.time() - self.last_frame_time > 0.1:
            self.current_frame = (self.current_frame + 1)%len(self.img_frames)
            self.last_frame_time = time.time()
    
    def load(self, path):
        filenames = sorted(os.listdir(path))
        print(filenames)
        for filename in filenames:
            filepath = os.path.join(path, filename)
            if filepath.endswith((".png")):
                # Lädt das Bild und fügt es zur Liste hinzu
                self.img_frames.append(pygame.image.load(filepath))

    def collision_with_player(self):
        if self.x > -world.x + player.x and self.x < -world.x + + player.x + player.rect.width and self.y > player.y and self.y < player.y + player.rect.height:
            Collectable.collectables.remove(self)
            player.coin_count += 1
                


class GameState:
    def __init__(self):
        self.running = False
        self.dt_last_frame = 1
        self.dead = False
        self.shooting_enebled = False
        self.movement_enebled = False
        self.end_of_game = False

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
        for x in range(rect.x, rect.x + rect.w-10):
            try:
                if self.image.get_at((x, rect.y)) != (0, 0, 0, 0):
                    return True

            except IndexError:
                pass
        return False
    
    def collides_vertically_bottom(self, rect):
        for x in range(rect.x+4, rect.x + rect.w-10):
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
    
obstacle_map = ObstacleMap("Bilder/Level 1/Level1_11200x1080_V1_Collisions.png")

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

        # self.font = pygame.font.SysFont(None, 18) 
        # text = self.font.render(f"Wo bin ich? {self.x}", True, (200, 200, 200))
        # display.blit(text, (screen_size[0]-145, 80))

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
        self.gravity = 0.5
        self.jump_height = 17
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

        self.inventory = []
        self.coin_count = 0
        self.health = 7
        self.health_bar_current_frame = 0
        self.health_bar_gif_folder_path = "Bilder/IO/Health_gifs"
        self.haelth_bar_gifs = self.load_gifs(self.health_bar_gif_folder_path)

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

    def damage(self, damage):
        self.health -= damage
        pygame.draw.rect(display, (255,0,0),pygame.Rect(0,0,screen_size[0],screen_size[1]),4)
        if self.health < 0:
            self.health = 0
            gs.dead = True
            world.__init__()
            gs.dead = False
            self.health = 7

    def display_health(self, surface):
        if self.health == 7:
            img = pygame.image.load("Bilder/IO/Health_gifs/Health8.png")
            img = pygame.transform.scale(img, (img.get_width() * 2, img.get_height() * 2))
            surface.blit(img, (UI_X+170, UI_Y+50))
        else: 
            surface.blit(self.haelth_bar_gifs[self.health][int(self.health_bar_current_frame)], (UI_X+170, UI_Y+50))
            self.health_bar_current_frame = (self.health_bar_current_frame + 0.25) % 7
    
    def load_gifs(self, path):
        all_gifs = []
        filenames = sorted(os.listdir(path))
        print(filenames)
        for filename in filenames:
            filepath = os.path.join(path, filename)
            if filepath.endswith((".gif")):
                # Lädt das Bild und fügt es zur Liste hinzu
                gif = self.load_gif(filepath,2)
                gif.pop(0)
                all_gifs.append(gif)
        return all_gifs
    
    def check_for_hit(self, coordinates) -> bool:
        image = self.animation_frames[1]
        x,y = coordinates
        if x > self.x-world.x and x < self.x - world.x + image.get_width():
            if y > self.y and y < self.y + image.get_height():
                return True
        return False
                

    def update(self):
        self.prev_x, self.prev_y = self.x, self.y  # Remember previous position
        self.dy += self.gravity
        test_rect = pygame.Rect(self.x - world.x, self.y, self.rect.w, self.rect.h).move(0, self.dy)
        
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
        if -world.x + player.x >= 10800:
            gs.movement_enebled = False
            if DialogBox.boxes == []:
                gs.end_of_game = True
                DialogBox(["Wow, du hast es geschafft!", "Bist du bereit weiter zu gehen?"],(player.x+100, 700))

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
    last_shot_fired = 0
    shots_left = 4
    is_reloading = False
    animation_frames = Player.load_gif("Bilder/IO/reload.webp",0.1)
    current_frame = 0
    last_frame_time = 0
    def __init__(self, cords_target, coordinates_origin, shot_by_player):
        if (time.time() - shot.last_shot_fired) > 0.2 and shot.shots_left > 0 and shot_by_player and gs.shooting_enebled:
            shot.shots_list.append(self)
            self.shot_by_player = shot_by_player
            self.image = pygame.image.load("/Users/i589040/Documents/GitHub/Spiel-Info-Q11-2022/Bilder/Objekte/PNG/Foreground/Hindernisse/Container_Side_1.png")
            self.image = pygame.transform.scale(self.image, (50,10))
            self.velocity = self.set_velocities(cords_target, coordinates_origin)
            v = -get_rotation_angle(self.velocity)
            self.image = pygame.transform.rotate(self.image,v)
            self.coordinates = coordinates_origin
            shot.last_shot_fired = time.time()
            shot.shots_left -= 1
        elif not shot_by_player and gs.shooting_enebled:
            shot.shots_list.append(self)
            self.shot_by_player = shot_by_player
            self.image = pygame.image.load("/Users/i589040/Documents/GitHub/Spiel-Info-Q11-2022/Bilder/Objekte/PNG/Foreground/Hindernisse/Container_Side_1.png")
            self.image = pygame.transform.scale(self.image, (50,10))
            self.velocity = self.set_velocities(cords_target, coordinates_origin)
            v = -get_rotation_angle(self.velocity)
            self.image = pygame.transform.rotate(self.image,v)
            self.coordinates = coordinates_origin
        elif shot.shots_left <= 0 and shot.is_reloading == False and (time.time() - shot.last_shot_fired) > 0.2:
            shot.is_reloading = True
    
    def move(self):
        self.coordinates[0] += self.velocity[0]
        self.coordinates[1] += self.velocity[1]

        test_rect = pygame.Rect(self.coordinates[0], self.coordinates[1], 5, 5)
        for enem in enemy.enemies:
            if enem.check_for_hit(self.coordinates) and self.shot_by_player:
                shot.shots_list.remove(self)
                enem.is_hit()
        if obstacle_map.collides(test_rect):
            shot.shots_list.remove(self)
        if abs(self.coordinates[1]) > 1080:
            shot.shots_list.remove(self)
        if player.check_for_hit(self.coordinates) and not self.shot_by_player:
            player.damage(1)
            shot.shots_list.remove(self)

    def reload_animation(surface):
        surface.blit(shot.animation_frames[shot.current_frame], (UI_X, UI_Y))
        if time.time() - shot.last_frame_time > 0.2:
            shot.current_frame = (shot.current_frame + 1)%len(shot.animation_frames)
            if shot.current_frame % len(shot.animation_frames) == 0:
                shot.is_reloading = False
                shot.shots_left = 4
            shot.last_frame_time = time.time()

    def display_magazine(surface):
        if shot.shots_left > 0:
            surface.blit(shot.animation_frames[int(shot.shots_left * 3)-2], (UI_X, UI_Y))
        elif shot.is_reloading == False:
            surface.blit(shot.animation_frames[0], (UI_X, UI_Y))
            if (time.time() - shot.last_shot_fired) > 0.5:
                shot.is_reloading = True
        else:
            shot.reload_animation(surface)


    def set_velocities_mouse(self) -> list:
        x,y = pygame.mouse.get_pos()
        v = [x - (player.x + player.rect.w/2), y - (player.y + player.rect.h/2)]
        v_l = math.sqrt(v[0]**2 + v[1]**2)
        v = [(i/v_l)*10 for i in v]
        return v
    
    def set_velocities(self, coords_origin, cords_target) -> list:
        x,y = coords_origin
        v = [x - cords_target[0], y - cords_target[1]]
        v_l = math.sqrt(v[0]**2 + v[1]**2)
        v = [(i/v_l)*10 for i in v]
        return v
    
    def draw(self,surface):
        surface.blit(self.image, (self.coordinates[0] + world.x, self.coordinates[1]))



world = World()
gs = GameState()
player = Player()
FPS = pygame.time.Clock()
DialogBox(["Hello!", "How are you?", "Good Luck!"], (screen_size[0]//2 + 200,700))

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
                if event.key == pygame.K_SPACE:
                    dialog.next_message()

            if event.type == pygame.MOUSEBUTTONUP:
                cords = pygame.mouse.get_pos()
                shot([cords[0] - world.x, cords[1]],[player.x + player.rect.w/2 - world.x, player.y + player.rect.h/2],True)
        # In the game loop
        if keys[pygame.K_SPACE] and gs.movement_enebled:
            if not player.dy < 0:
                player.jump()

        if keys[pygame.K_d] and gs.movement_enebled:
                test_rect = pygame.Rect(player.x - world.x, player.y, player.rect.w, player.rect.h).move(1, 0)
                if not obstacle_map.collides_horizontally_right(test_rect):
                    world.move(-SPEED_LATERAL)
                    player.walking_right = True
        else:
            player.walking_right = False

        if keys[pygame.K_a] and gs.movement_enebled:

                test_rect = pygame.Rect(player.x - world.x, player.y, player.rect.w, player.rect.h).move(-1, 0)
                if not obstacle_map.collides_horizontally_left(test_rect):
                    world.move(SPEED_LATERAL)
                    player.walking_left = True
        else:
            player.walking_left = False

        if keys[pygame.K_LSHIFT] and gs.movement_enebled:
            player.crouch = True
            player.jump_enabled = False
        elif player.crouch == True:
            player.jump_enabled = True
            player.y -= player.rect.size[1]
            player.crouch = False


        player.update()
        world.draw(display)
        player.draw(display)
        shot.display_magazine(display)
        player.display_health(display)
        for dialog in DialogBox.boxes:
            dialog.draw(display)
        for item in Collectable.collectables:
            item.collision_with_player()
            item.draw(display)
        for shots in shot.shots_list:
            shots.move()
            shots.draw(display)
        
        for e in enemy.enemies:
            e.fire_shot()
            e.draw(display)

        pygame.display.flip()
        gs.dt_last_frame = FPS.tick()/17
    pygame.mixer.pause()

if __name__ == "__main__":
    gs.running = True
    main()