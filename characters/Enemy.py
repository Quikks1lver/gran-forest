import math
import pygame
from .Player import Player
import random

class Enemy(Player):
    """
    Represents an enemy character in the pygame
    """

    def __init__(self, image_path: str, x_start: int, y_start: int, start_scrolling_pos_x: int, stage_width: int, game_width: int, y_top_threshold: int, y_bottom_threshold: int, health: int, x_velocity: float, y_velocity: float):
        """
        Initialize an enemy character
        :param image_path: file path of player image
        :param x_start:
        :param y_start:
        :param start_scrolling_pos_x: point at which background scrolls/moves, not the player
        :param stage_width: width of stage (a few times the background image)
        :param game_width: width of game window itself
        :param y_top_threshold: top threshold where character cannot go above
        :param y_bottom_threshold: bottom threshold where character cannot go below
        :param health: hit points of character
        :param x_velocity:
        :param y_velocity:
        """
        super().__init__(image_path, x_start, y_start, start_scrolling_pos_x, stage_width,
                         game_width, y_top_threshold, y_bottom_threshold, health)

        self.x_velocity = x_velocity
        self.y_velocity = y_velocity

    def move(self, player: Player) -> None:
        """
        Moves enemy according to current position and player's position
        Also has some random movement to simulate being crazy
        :param player: player object
        :return:
        """
        # inject some randomness
        self.x += random.randint(-1, 1)
        self.y += random.randint(-1, 1)

        # track player's x position
        if self.x > player.x: self.x -= self.x_velocity
        elif self.x < player.x: self.x += self.x_velocity
        else: pass

        # track player's y position
        if self.y > player.y: self.y -= self.y_velocity
        elif self.y < player.y: self.y += self.y_velocity
        else: pass

        # make sure enemy doesn't go above y thresholds; it can go past x-thresholds, though
        if self.y < self.y_top_threshold: self.y = self.y_top_threshold
        if self.y > self.y_bottom_threshold: self.y = self.y_bottom_threshold

        # refer to Player file for comments on these lines
        if self.x < self.start_scrolling_pos_x:
            self.real_x_position = self.x
        elif self.x > self.stage_width - self.start_scrolling_pos_x:
            self.real_x_position = self.x - self.stage_width + self.game_width
        else:
            self.real_x_position = self.start_scrolling_pos_x