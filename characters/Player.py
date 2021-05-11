import math
import pygame

class Player():
    """
    Represents a player character in the pygame
    """

    def __init__(self, image_path: str, x_start: int, y_start: int, start_scrolling_pos_x: int, stage_width: int, game_width: int, y_top_threshold: int, y_bottom_threshold: int, health: int):
        """
        Initialize a player character
        :param image_path: file path of player image
        :param x_start:
        :param y_start:
        :param start_scrolling_pos_x: point at which background scrolls/moves, not the player
        :param stage_width: width of stage (a few times the background image)
        :param game_width: width of game window itself
        :param y_top_threshold: top threshold where character cannot go above
        :param y_bottom_threshold: bottom threshold where character cannot go below
        :param health: hit points of character
        """
        self.image = pygame.image.load(image_path)
        self.image_width = self.image.get_width()

        self.x = x_start
        self.y = y_start
        self.x_velocity = 0.0
        self.y_velocity = 0.0
        self.real_x_position = self.image_width

        self.start_scrolling_pos_x = start_scrolling_pos_x
        self.stage_width = stage_width
        self.game_width = game_width

        self.y_top_threshold = y_top_threshold
        self.y_bottom_threshold = y_bottom_threshold

        self.health = health

        self.is_left_facing = False

    def draw(self, screen) -> None:
        """
        draws player onto the pygame window, changing orientation if necessary
        :param screen: pygame display
        :return: None
        """
        if self.is_left_facing: screen.blit(self.image, (self.real_x_position, self.y))
        else: screen.blit(pygame.transform.flip(self.image, True, False), (self.real_x_position, self.y))

    def set_x_velocity(self, new_velocity: float) -> None:
        """
        Changes x velocity field
        :param new_velocity:
        :return:
        """
        self.x_velocity = new_velocity
        
        # change player's orientation/direction
        if self.x_velocity == 0: return
        else: self.is_left_facing = False if self.x_velocity > 0 else True

    def set_y_velocity(self, new_velocity: float) -> None:
        """
        Changes y velocity field
        :param new_velocity:
        :return:
        """
        self.y_velocity = new_velocity

    def move(self) -> None:
        """
        Moves player character according to current position and velocities
        This was super helpful: https://www.youtube.com/watch?v=AX8YU2hLBUg
        :return:
        """
        self.x += self.x_velocity
        self.y += self.y_velocity

        # makes sure player doesn't go beyond stage to the right
        if self.x > self.stage_width - self.image_width: self.x = self.stage_width - self.image_width
        # makes sure player doesn't go beyond stage to the left
        if self.x < 0: self.x = 0
        # makes sure player doesn't go above top threshold
        if self.y < self.y_top_threshold: self.y = self.y_top_threshold
        # makes sure player doesn't go below bottom threshold
        if self.y > self.y_bottom_threshold: self.y = self.y_bottom_threshold


        # where x position of player is less than scrolling threshold
        if self.x < self.start_scrolling_pos_x:
            self.real_x_position = self.x
        # where stage no longer scrolls, but the player moves to the end
        elif self.x > self.stage_width - self.start_scrolling_pos_x:
            self.real_x_position = self.x - self.stage_width + self.game_width
        # scroll stage (handled elsewhere), but keep player "still" in the middle area
        else:
            self.real_x_position = self.start_scrolling_pos_x

    def is_collision(self, enemy, threshold: float) -> bool:
        """
        Determines whether the player
        :param enemy: enemy character object
        :param threshold: below or equal to which is considered a collision
        :return:
        """
        return True if math.dist([self.x, self.y], [enemy.x, enemy.y]) <= threshold else False