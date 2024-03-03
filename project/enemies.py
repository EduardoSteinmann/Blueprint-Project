from PIL import Image
import pygame
import common
from common import *

class Enemy:
    def __init__(self, position: tuple[float], path: str, bounds: tuple[float], player_health: list[float]) -> None:
        image = pygame.image.load(path)
        self.position = position
        self.sprite = image
        self.bounding_box = image.get_rect().move(position[0], position[1])
        self.range = 0.6
        self.health = 20
        self.velocity = 0.1
        self.bounds = bounds
        self.health_ref = player_health
        
    
    def take_damage(self):
        self.health -= 10

    def is_dead(self) -> bool:
        return self.health <= 0
    
    def move(self, offset: tuple[float]) -> None:
        self.position = [self.position[0] + offset[0], self.position[1] + offset[1]]
        self.bounding_box.move_ip(offset)
        if self.velocity > 0:
            if self.bounds[1] - self.position[0] < 5:
                self.velocity *= -1
        else:
            if self.position[0] - self.bounds[0] < 5:
                self.velocity *= -1

    def update_position(self, delta_time: float):
        offset = (delta_time * self.velocity, 0)
        self.move(offset)