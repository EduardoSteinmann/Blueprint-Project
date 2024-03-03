from PIL import Image
import pygame
import common

class Enemy:
    def __init__(self, position: tuple[float], path: str) -> None:
        image = pygame.image.load(path)
        self.position = position
        self.sprite = image
        self.bounding_box = image.get_rect()
        self.range = 0.6*common.METER
        self.health = 20
    
    def take_damage(self):
        self.health -= 10

    def is_dead(self) -> bool:
        return self.health <= 0
    
    def move(self, pos: tuple[float]) -> None:
        self.bounding_box.move(pos)
        self.position = pos

    def attack(self, player):
        pass
