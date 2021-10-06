import pygame, sys

clock = pygame.time.Clock()

from pygame.locals import *

pygame.init() # initiate pygame

pygame.display.set_caption('My Pygame Window')

WINDOW_SIZE = (1200,800)

screen = pygame.display.set_mode(WINDOW_SIZE,0,32) # initiate window

display = pygame.Surface((600,400))

player_image1 = pygame.image.load('knight.png')
# player_image2 = pygame.image.load('dagger.png')
grass_image = pygame.image.load('grass.png')
TILE_SIZE = grass_image.get_width()
grass2_image = pygame.image.load('grass2.png')


game_map = [['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0'],
            ['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0'],
            ['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0'],
            ['0','0','2','2','2','0','0','0','0','0','0','0','0','0','0','0','0','2','2','2'],
            ['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0'],
            ['0','0','0','0','0','0','0','2','2','2','2','0','0','0','0','0','0','0','0','0'],
            ['2','2','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0'],
            ['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0'],
            ['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0'],
            ['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0'],
            ['0','1','1','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0'],
            ['0','1','1','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0'],
            ['1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1'],
            ['1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1'],
            ['1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1']]

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



# movement
moving_right = False
moving_left = False

# player_location = [150,50]
player_y_momentum = 0
air_timer = 0

player_rect = pygame.Rect(50, 50, player_image1.get_width(), player_image1.get_height()) # player hitbox/collision
test_rect = pygame.Rect(100,100,100,50)

while True: # game loop
    display.fill((146,244,255))

    tile_rects = []
    y = 0
    for row in game_map:
        x = 0
        for tile in row:
            if tile == '1':
                display.blit(grass2_image, (x * TILE_SIZE, y * TILE_SIZE))
            if tile == '2':
                display.blit(grass_image, (x * TILE_SIZE, y * TILE_SIZE))
            if tile != '0':
                tile_rects.append(pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
            x += 1
        y += 1

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

    player_rect, collisions = move(player_rect, player_movement, tile_rects)

    if collisions['bottom']:
        player_y_momentum = 0
        air_timer = 0
    else:
        air_timer += 1

    display.blit(player_image1, (player_rect.x, player_rect.y))

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

            if event.key == K_RIGHT:
                moving_right = True

            if event.key == K_LEFT:
                moving_left = True

            if event.key == K_UP:
                if air_timer < 100:
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