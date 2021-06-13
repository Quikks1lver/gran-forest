import pygame
import math
import random

from .Enemy import Enemy

class EnemyFactory():
    """
    A way to easily create pre-set enemies
    """

    def __init__(self, stage_width: int, game_width: int, y_start: int, y_top_threshold: int, y_bottom_threshold: int, start_scrolling_pos_x: int):
        """
        Creates an EnemyFactory object
        """
        self.stage_width = stage_width
        self.game_width = game_width
        self.y_start = y_start
        self.y_top_threshold = y_top_threshold
        self.y_bottom_threshold = y_bottom_threshold
        self.start_scrolling_pos_x = start_scrolling_pos_x

    def create_basic_enemy(self) -> Enemy:
        """
        Returns a random-looking basic enemy
        """
        health = 50
        x_velocity, y_velocity = 0.4, 0.1
        enemy_img = "gingerbread-man" if random.randint(0, 1) == 0 else "cupcake"
        enemy_start = self.stage_width + 200 if random.randint(0, 1) == 0 else -200

        return Enemy(f"images/{enemy_img}.png", enemy_start, self.y_start, self.start_scrolling_pos_x,
                     self.stage_width, self.game_width, self.y_top_threshold, self.y_bottom_threshold, health, x_velocity, y_velocity)