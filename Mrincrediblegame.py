import pygame, sys, os, random, noise
import math 
from random import randrange
import pygame.sprite as sprite
clock = pygame.time.Clock()

from pygame.locals import *
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init() # initiates pygame
pygame.mixer.set_num_channels(64)

SCREEN_WIDTH = 1900
SCREEN_HEIGHT = 1060

pygame.display.set_caption('Pygame Mrincredible')

WINDOW_SIZE = (SCREEN_WIDTH,SCREEN_HEIGHT)
  
screen = pygame.display.set_mode(WINDOW_SIZE) # initiate the window

display = pygame.Surface((300,200))# used as the surface for rendering, which is scaled

moving_right = False
moving_left = False
vertical_momentum = 0
air_timer = 0

true_scroll = [0,0]

CHUNK_SIZE = 16

def generate_chunk(x,y):
    chunk_data = []
    for y_pos in range(CHUNK_SIZE):
        for x_pos in range(CHUNK_SIZE):
            target_x = x * CHUNK_SIZE + x_pos
            target_y = y * CHUNK_SIZE + y_pos
            tile_type = 0 # nothing
            height = int(noise.pnoise1(target_x * 0.1, repeat=9999999) * 5)
            if target_y > 8 - height:
                tile_type = 2 # dirt
            elif target_y == 8 - height:
                tile_type = 1 # grass
            elif target_y == 8 - height - 1:
                if random.randint(1,5) == 1:       
                    tile_type = 3 # plant
            elif target_y == 1 - height - 1:        
                if random.randint(1,16) == 1:
                    tile_type = 4
            elif target_y == 3 - height - 1:
                if random.randint(1,16) == 1:
                    tile_type = 5  
            elif target_y == 0 - height - 1:
                if random.randint(1,10) == 1:            
                    tile_type = 6              
            if tile_type != 0:
                chunk_data.append([[target_x,target_y],tile_type])
    return chunk_data

global animation_frames
animation_frames = {}

def load_animation(path,frame_durations):
    global animation_frames
    animation_name = path.split('/')[-1]
    animation_frame_data = []
    n = 0
    for frame in frame_durations:
        animation_frame_id = animation_name + '_' + str(n)
        img_loc = path + '/' + animation_frame_id + '.png'
        # player_animations/idle/idle_0.png
        animation_image = pygame.image.load(img_loc).convert()
        animation_image.set_colorkey((0,0,0))
        animation_frames[animation_frame_id] = animation_image.copy()
        for i in range(frame):
            animation_frame_data.append(animation_frame_id)
        n += 1
    return animation_frame_data

def change_action(action_var,frame,new_value):
    if action_var != new_value:
        action_var = new_value
        frame = 0
    return action_var,frame
 
animation_database = {}

animation_database['run'] = load_animation('player_animations/run',[7,7])
animation_database['idle'] = load_animation('player_animations/idle',[7,7,40])

game_map = {}


grass_img = pygame.image.load('grass.png')
dirt_img = pygame.image.load('dirt.png')
largetree_img = pygame.image.load('Largetree1.png')
smalltree_img = pygame.image.load('Smalltree1.png')
cloud_img = pygame.image.load('cloud.png')
plant_img = pygame.image.load('plant.png').convert()
plant_img.set_colorkey((255,255,255))

tile_index = {1:grass_img,
            2:dirt_img,
            3:plant_img,
            4:largetree_img,
            5:smalltree_img,
            6:cloud_img
            }

jump_sound = pygame.mixer.Sound('jump.wav')
grass_sounds = [pygame.mixer.Sound('grass_0.wav'),pygame.mixer.Sound('grass_1.wav')]
grass_sounds[0].set_volume(0.2)
grass_sounds[1].set_volume(0.2)

pygame.mixer.music.load('music.wav')
pygame.mixer.music.play(-1)

game_music = pygame.mixer.Sound('music.wav')
game_music.set_volume(0.002)

player_action = 'idle'
player_frame = 0
player_flip = False

grass_sound_timer = 0

player_rect = pygame.Rect(100,100,5,22)

def collision_test(rect,tiles):
    hit_list = []
    for tile in tiles:
        if rect.colliderect(tile):
            hit_list.append(tile)
    return hit_list

def move(rect,movement,tiles):
    collision_types = {'top':False,'bottom':False,'right':False,'left':False}
    rect.x += movement[0]
    hit_list = collision_test(rect,tiles)
    for tile in hit_list:
        if movement[0] > 0:
            rect.right = tile.left
            collision_types['right'] = True
        elif movement[0] < 0:
            rect.left = tile.right
            collision_types['left'] = True
    rect.y += movement[1]
    hit_list = collision_test(rect,tiles)
    for tile in hit_list:
        if movement[1] > 0:
            rect.bottom = tile.top
            collision_types['bottom'] = True
        elif movement[1] < 0:
            rect.top = tile.bottom
            collision_types['top'] = True
    return rect, collision_types

while True: # game loop
        
    display.fill((135,206,235))# clear screen by filling it with sky blue
    
    if grass_sound_timer > 0:
           grass_sound_timer -= 1    

    true_scroll[0] += (player_rect.x-true_scroll[0]-152)/20
    true_scroll[1] += (player_rect.y-true_scroll[1]-106)/20
    scroll = true_scroll.copy()
    scroll[0] = int(scroll[0])
    scroll[1] = int(scroll[1])

    tile_rects = []
    for y in range(3):
        for x in range(4):
            target_x = x - 1 + int(round(scroll[0]/(CHUNK_SIZE*16)))
            target_y = y - 1 + int(round(scroll[1]/(CHUNK_SIZE*16)))
            target_chunk = str(target_x) + ';' + str(target_y)
            if target_chunk not in game_map:
                game_map[target_chunk] = generate_chunk(target_x,target_y)
            for tile in game_map[target_chunk]:
                display.blit(tile_index[tile[1]],(tile[0][0]*16-scroll[0],tile[0][1]*16-scroll[1]))
                if tile[1] in [1,2]:
                    tile_rects.append(pygame.Rect(tile[0][0]*16,tile[0][1]*16,16,16))    

    player_movement = [0,0]
    if moving_right == True:
        player_movement[0] += 2
    if moving_left == True:
        player_movement[0] -= 2
    player_movement[1] += vertical_momentum
    vertical_momentum += 0.2
    if vertical_momentum > 3:
        vertical_momentum = 3

    if player_movement[0] == 0:
        player_action,player_frame = change_action(player_action,player_frame,'idle')
    if player_movement[0] > 0:
        player_flip = False
        player_action,player_frame = change_action(player_action,player_frame,'run')
    if player_movement[0] < 0:
        player_flip = True
        player_action,player_frame = change_action(player_action,player_frame,'run')

    player_rect,collisions = move(player_rect,player_movement,tile_rects)

    if collisions['bottom'] == True:
        air_timer = 0
        vertical_momentum = 0
        if player_movement[0] != 0:
            if grass_sound_timer == 0:
                grass_sound_timer = 30
                random.choice(grass_sounds).play()
    else:
        air_timer += 1

    player_frame += 1
    if player_frame >= len(animation_database[player_action]):
        player_frame = 0
    player_img_id = animation_database[player_action][player_frame]
    player_img = animation_frames[player_img_id]
    display.blit(pygame.transform.flip(player_img,player_flip,False),(player_rect.x-scroll[0],player_rect.y-scroll[1]))


    for event in pygame.event.get(): # event loop
        if event.type == pygame.QUIT:sys.exit()
       
    if event.type == KEYDOWN:
            if event.key == K_RIGHT:
                moving_right = True
            if event.key == K_LEFT:
                moving_left = True
            if event.key == K_UP:
                if air_timer < 6:
                    vertical_momentum = -5
    if event.type == KEYUP:
            if event.key == K_RIGHT:
                moving_right = False
            if event.key == K_LEFT:
                moving_left = False
         
    screen.blit(pygame.transform.scale(display,WINDOW_SIZE),(0,0))
    pygame.display.update()
    clock.tick(60)
    
    

    

