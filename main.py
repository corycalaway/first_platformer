import pygame, sys, os, random

clock = pygame.time.Clock()

from pygame.locals import *
pygame.mixer.pre_init(44100, -16, 2, 512)

pygame.init() # initiate pygame
pygame.mixer.set_num_channels(69)

pygame.display.set_caption('My Pygame Window')

WINDOW_SIZE = (1200,800)

screen = pygame.display.set_mode(WINDOW_SIZE,0,32) # initiate window

display = pygame.Surface((600,400))

# player_image = pygame.image.load('player_animations/run/run_0.png')



grass_image = pygame.image.load('basic.png')
TILE_SIZE = grass_image.get_width()
grass2_image = pygame.image.load('grass.png')
plant_image = pygame.image.load('grass2.png')

tile_index = {1: grass_image,
              2: grass2_image,
              3: plant_image
              }

jump_sound = pygame.mixer.Sound('jump.wav')
grass_sounds = [pygame.mixer.Sound('grass_0.wav'), pygame.mixer.Sound('grass_1.wav')]
grass_sounds[0].set_volume(0.5)
pygame.mixer.music.load('music.wav')
pygame.mixer.music.play(-1)


# movement
moving_right = False
moving_left = False

# player_location = [150,50]
player_y_momentum = 0
air_timer = 0

true_scroll = [0,0]

background_objects = [[0.25,[120,10,70,400]],[0.25,[280,30,40,400]],[0.25,[560,30,40,400]],[0.5,[30,40,40,400]],[0.5,[130,90,100,400]],[0.5,[300,80,120,400]]]

CHUNK_SIZE = 9


def generate_chunk(x,y):
    chunk_data = []
    for y_pos in range(CHUNK_SIZE):
        for x_pos in range(CHUNK_SIZE):
            target_x = x * CHUNK_SIZE + x_pos
            target_y = y * CHUNK_SIZE + y_pos
            tile_type = 0
            if target_y > 10:
                if random.randint(1,3) == 1:

                    tile_type = 2
            elif target_y == 10:
                if random.randint(1, 3) == 1:
                    tile_type = 1
            elif target_y == 9:
                if random.randint(1,5) == 1:
                    tile_type = 3
            if tile_type != 0:
                chunk_data.append([[target_x,target_y], tile_type])

    return chunk_data





# old map
# def load_map(path):
#     print('here')
#     f = open(path + '.txt', 'r')
#     data = f.read()
#     f.close()
#     data = data.split('\n')
#     game_map = []
#     for row in data:
#         game_map.append(list(row))
#     return game_map

global animation_frames
animation_frames = {}

def load_animation(path, frame_durations):
    global animation_frames
    animation_name = path.split('/') [-1]
    animation_frame_data = []
    n = 0
    for frame in frame_durations:
        animation_frame_id = animation_name + '_' + str(n)
        img_loc = path + '/' + animation_frame_id + '.png'
        print(img_loc)
        animation_image = pygame.image.load(img_loc)
        # animation_image.set_colorkey((255,255,255))
        animation_frames[animation_frame_id] = animation_image.copy()
        for i in range(frame):
            animation_frame_data.append(animation_frame_id)
        n += 1
    return animation_frame_data

def change_action(action_var, frame, new_value):
    if action_var != new_value:
        action_var = new_value
        frame = 0
    return action_var,frame

# print(load_animation('player_animations/run',[7,7]))

animation_database = {}

animation_database['run'] = load_animation('player_animations/run', [7,7])
animation_database['idle'] = load_animation('player_animations/idle',[7,7])

player_action = 'idle'
player_frame = 0
player_flip = False

grass_sound_timer = 0



# game_map = load_map('map')
game_map = { }


def collision_test(rect, tiles):
    hit_list = []
    for tile in tiles:
        if rect.colliderect(tile):
            hit_list.append(tile)
    return hit_list


def move(rect, movement, tiles):

    collision_types = {'top': False, 'bottom': False, 'right': False, 'left': False}
    rect.x += movement[0]
    hit_list = collision_test(rect, tiles)
    for tile in hit_list:
        if movement[0] > 0:
            rect.right = tile.left
            collision_types['right'] = True
        elif movement[0] < 0:
            rect.left = tile.right
            collision_types['left'] = True

    rect.y += movement[1]
    hit_list = collision_test(rect, tiles)

    for tile in hit_list:
        if movement[1] > 0:
            rect.bottom = tile.top
            collision_types['bottom'] = True
        elif movement[1] < 0:
            rect.top = tile.bottom
            collision_types['top'] = True
    return rect, collision_types





player_rect = pygame.Rect(50, 50, 25,25) # player hitbox/collision
test_rect = pygame.Rect(100,100,100,50)

while True: # game loop
    display.fill((146,244,255))

    if grass_sound_timer > 0:
        grass_sound_timer -= 1


    # Auto scroll
    # scroll[0] += 1
    # Scroll with player
    true_scroll[0] += (player_rect.x - true_scroll[0] - 304)/10
    true_scroll[1] += (player_rect.y - true_scroll[1] - 212)/10
    scroll = true_scroll.copy()
    scroll[0] = int(scroll[0])
    scroll[1] = int(scroll[1])

    pygame.draw.rect(display,(7,80,75),pygame.Rect(0, 120, 650, 400))

    for background_object in background_objects:
        obj_rect = pygame.Rect(background_object[1][0] - scroll[0] * background_object[0],background_object[1][1]-scroll[1]* background_object[0],background_object[1][2],background_object[1][3])
        if background_object[0] == 0.5:
            pygame.draw.rect(display,(14,22,150), obj_rect)
        else:
            pygame.draw.rect(display,(9,91,85),obj_rect)

    tile_rects = []

    for y in range(3):
        for x in range(4):
            target_x = x - 1  + int(scroll[0] / (CHUNK_SIZE * 32))
            target_y = y  + int(scroll[1] / (CHUNK_SIZE * 32))
            target_chunk = str(target_x) +';' +str(target_y)
            if target_chunk not in game_map:
                game_map[target_chunk] = generate_chunk(target_x,target_y)
            for tile in game_map[target_chunk]:
                display.blit(tile_index[tile[1]], (tile[0][0]*32-scroll[0], tile[0][1]*32-scroll[1]))
                if tile[1] in [1,2,3]:
                    tile_rects.append(pygame.Rect(tile[0][0]*32, tile[0][1]*32,32,32,) )

    #old tile rendering
    # y = 0
    # for row in game_map:
    #     x = 0
    #     for tile in row:
    #         if tile == '1':
    #             display.blit(grass2_image, (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))
    #         if tile == '2':
    #             display.blit(grass_image, (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))
    #         if tile != '0':
    #             tile_rects.append(pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
    #         x += 1
    #     y += 1

    # player_rect, collisions = move(player_rect, player_movement, tile_rects)
    # display.blit(player_image1, (player_rect.x, player_rect.y))
    # display.blit(player_image1, player_location)

    player_movement = [0, 0]
    if moving_right:
        player_movement[0] += 2
    if moving_left:
        player_movement[0] -= 2
    player_movement[1] += player_y_momentum
    player_y_momentum += 0.2
    if player_y_momentum > 3:
        player_y_momentum = 3

    if player_movement[0] > 0:
        player_action,player_frame = change_action(player_action,player_frame,'run')
        player_flip = False

    if player_movement[0] == 0:
        player_action, player_frame = change_action(player_action, player_frame, 'idle')

    if player_movement[0] < 0:
        player_action,player_frame = change_action(player_action,player_frame,'run')
        player_flip = True

    player_rect, collisions = move(player_rect, player_movement, tile_rects)

    if collisions['bottom']:
        player_y_momentum = 0
        air_timer = 0
        if player_movement[0] !=0:
            if grass_sound_timer == 0:
                grass_sound_timer = 30
                random.choice(grass_sounds).play()


    else:
        air_timer += 1

    # Cycles through animation images for player
    player_frame += 1
    if player_frame >= len(animation_database[player_action]):
        player_frame = 0
    # Checks for frame in animation database
    player_img_id = animation_database[player_action][player_frame]
    player_img = animation_frames[player_img_id]
    print(player_img_id)

    display.blit(pygame.transform.flip(player_img,player_flip,False), (player_rect.x - scroll[0], player_rect.y - scroll[1]))

    # Bouncing
    # if player_location[1] > WINDOW_SIZE[1]-player_image1.get_height():
    #     player_y_momentum = -player_y_momentum
    # else:
    #     player_y_momentum += .2
    # player_location[1] += player_y_momentum


    # player_location[1] += player_y_momentum

    # player_movement = [0,0]
    # if moving_right:
    #     player_movement[0] += 2
    # if moving_left:
    #     player_movement[0] -= 2
    # player_movement[1] += player_y_momentum
    # player_y_momentum += 0.2
    # if player_y_momentum > 3:
    #     player_y_momentum = 3
    #
    # player_rect, collisions = move(player_rect, player_movement, tile_rects)
    #
    # display.blit(player_image1, (player_rect.x, player_rect.y))


    # if moving_right == True:
    #     print(player_location)
    #     player_location[0] += 4
    # if moving_left == True:
    #     player_location[0] -= 4
    #
    # player_rect.x = player_location[0]
    # player_rect.y = player_location[1]

    # if player_rect.colliderect(test_rect):
    #     print('hit')
    #     pygame.draw.rect(screen,(255,0,0),test_rect)
    # else:
    #     pygame.draw.rect(screen,(0,255,0), test_rect)

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()


        # movement keys
        if event.type == KEYDOWN:
            print('key down')

            if event.key == K_w:
                pygame.mixer.music.fadeout(1000)

            if event.key == K_RIGHT:
                moving_right = True

            if event.key == K_LEFT:
                moving_left = True

            if event.key == K_UP:
                if air_timer < 100:
                    jump_sound.play()
                    player_y_momentum = -5


        if event.type == KEYUP:
            print('key up')
            print(moving_right)
            if event.key == K_RIGHT:
                moving_right = False
            if event.key == K_LEFT:
                moving_left = False

    surf = pygame.transform.scale(display, WINDOW_SIZE)
    screen.blit(surf,(0,0))
    pygame.display.update()
    clock.tick(60)



# <div>Icons made by <a href="https://www.freepik.com" title="Freepik">Freepik</a> from <a href="https://www.flaticon.com/" title="Flaticon">www.flaticon.com</a></div>
# <div>Icons made by <a href="https://www.freepik.com" title="Freepik">Freepik</a> from <a href="https://www.flaticon.com/" title="Flaticon">www.flaticon.com</a></div>
# <div>Icons made by <a href="https://www.freepik.com" title="Freepik">Freepik</a> from <a href="https://www.flaticon.com/" title="Flaticon">www.flaticon.com</a></div>
# <div>Icons made by <a href="https://www.freepik.com" title="Freepik">Freepik</a> from <a href="https://www.flaticon.com/" title="Flaticon">www.flaticon.com</a></div>
# <div>Icons made by <a href="https://www.flaticon.com/authors/smashicons" title="Smashicons">Smashicons</a> from <a href="https://www.flaticon.com/" title="Flaticon">www.flaticon.com</a></div>
# <div>Icons made by <a href="https://www.freepik.com" title="Freepik">Freepik</a> from <a href="https://www.flaticon.com/" title="Flaticon">www.flaticon.com</a></div>
# <div>Icons made by <a href="https://www.freepik.com" title="Freepik">Freepik</a> from <a href="https://www.flaticon.com/" title="Flaticon">www.flaticon.com</a></div>