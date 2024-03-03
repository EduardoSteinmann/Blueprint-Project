import pygame

class Platform:
    def __init__(self, position1, sprite_path) -> None:
        # Center of platform object
        image = pygame.image.load(sprite_path)
        self.position: tuple[float] = position1
        self.sprite = pygame.image.load(sprite_path)
        self.bounding_box = image.get_rect()

    

    
