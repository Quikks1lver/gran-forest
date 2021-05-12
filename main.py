# Adam Fernandes
# May 2021
# My first pygame!

import pygame
import random
from typing import List

import background.Background_Methods as bg_methods
from characters.Player import Player
from characters.Enemy import Enemy, Enemy_Collision
from weapons.Weapon import Weapon

# constants
WIDTH, HEIGHT = 800, 600

NUM_ENEMIES = 5
ENEMY_HIT = .5
ENEMY_HEALTH = 50
ENEMY_X_VELOCITY, ENEMY_Y_VELOCITY = 0.4, 0.1
ENEMY_HIT_SCORE = 1
ENEMY_DEFEATED_SCORE = 11

PLAYER_HEALTH = 100
PLAYER_X_START, PLAYER_Y_START = 50, 460
PLAYER_X_VELOCITY, PLAYER_Y_VELOCITY = 1.5, 0.5

AMMO_COST, AMMO_GAIN = 75, 25
STARTING_WEAPON_VELOCITY = 4
STARTING_WEAPON_DAMAGE = 10
STARTING_WEAPON_AMMO = 50

Y_TOP_THRESHOLD, Y_BOTTOM_THRESHOLD = 440, 530
COLLISION_THRESHOLD = 25

# initialize the pygame & create screen
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# background and stage
background = pygame.image.load("images/background.png").convert()
background_width, background_height = background.get_rect().size
stage_width = background_width * 2
stage_pos_x = 0
start_scrolling_pos_x = WIDTH / 2
background_collision = pygame.image.load("images/background_collision.png").convert()

# sounds
explosion_sound = pygame.mixer.Sound("sounds/explosion.wav")

# init player and enemy characters
player = Player("images/ghost.png", PLAYER_X_START, PLAYER_Y_START, start_scrolling_pos_x,
                stage_width, WIDTH, Y_TOP_THRESHOLD, Y_BOTTOM_THRESHOLD, PLAYER_HEALTH)
player.add_weapon(Weapon("images/revolver.png",  "sounds/weapon.wav", "images/bullet.png", player, STARTING_WEAPON_VELOCITY,
                         STARTING_WEAPON_DAMAGE, STARTING_WEAPON_AMMO))
enemies: List[Enemy] = []
for i in range(NUM_ENEMIES):
    enemy_img = "gingerbread-man.png" if random.randint(0, 1) == 0 else "cupcake.png"
    enemy_start = stage_width + 200 if random.randint(0, 1) == 0 else -200
    enemies.append(Enemy(f"images/{enemy_img}", enemy_start, PLAYER_Y_START, start_scrolling_pos_x,
                         stage_width, WIDTH, Y_TOP_THRESHOLD, Y_BOTTOM_THRESHOLD, ENEMY_HEALTH, ENEMY_X_VELOCITY, ENEMY_Y_VELOCITY))

# important flags and variables for main game loop
collision = False
running = True
died = False
final_score = 0
enemies_defeated = 0

# game loop
while running:
    collision = False
    trying_to_buy_ammo = False

    # event handlers
    for event in pygame.event.get():
        # break out of game loop if user quits
        if event.type == pygame.QUIT:
            running = False

        # key presses
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT: player.set_x_velocity(-PLAYER_X_VELOCITY)
            if event.key == pygame.K_RIGHT: player.set_x_velocity(PLAYER_X_VELOCITY)
            if event.key == pygame.K_UP: player.set_y_velocity(-PLAYER_Y_VELOCITY)
            if event.key == pygame.K_DOWN: player.set_y_velocity(PLAYER_Y_VELOCITY)
            if event.key == pygame.K_SPACE: player.fire_current_weapon()
            if event.key == pygame.K_b: trying_to_buy_ammo = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT: player.set_x_velocity(0)
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN: player.set_y_velocity(0)

    # move all characters
    player.move()
    for e in enemies:
        e.move(player)
        if e.has_collision_with_player(player, COLLISION_THRESHOLD):
            player.take_damage(ENEMY_HIT)
            collision = True

    # move stage if need be
    stage_pos_x += bg_methods.determine_stage_change(player)

    # draw everything to screen; also, check for bullet collisions here
    bg_methods.draw_background(screen, background_collision if collision else background, stage_pos_x, background_width, WIDTH)
    bg_methods.draw_ammo_box(screen, player, AMMO_COST, AMMO_GAIN, trying_to_buy_ammo)
    player.draw(screen)
    for e in enemies:
        e.draw(screen, player)

        collision_type = e.check_for_bullet_collision(player.get_current_weapon().bullet, COLLISION_THRESHOLD)
        if collision_type == Enemy_Collision.HIT:
            player.add_score(ENEMY_HIT_SCORE)
        elif collision_type == Enemy_Collision.DEFEATED:
            player.add_score(ENEMY_DEFEATED_SCORE)
            explosion_sound.play()
            enemies_defeated += 1

    # draw score & ammo metadata
    bg_methods.display_points(screen, player.score)
    bg_methods.display_ammo(screen, player.get_current_weapon().ammo)

    # game over screen
    if player.health <= 0:
        if not died:
            final_score = enemies_defeated
            died = True
        bg_methods.game_over(screen, enemies_defeated, WIDTH, HEIGHT)

    # update display
    pygame.display.update()