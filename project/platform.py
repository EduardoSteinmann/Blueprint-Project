import pygame

class Platform:
    def __init__(self, position, sprite_path) -> None:
        image = pygame.image.load(sprite_path)
        self.position: tuple[float] = position
        self.sprite = image
        self.bounding_box = image.get_rect().move(position[0], position[1])
        self.velocity = 0.05
        self.bounds = [self.position[0]-100, self.position[0] + self.bounding_box.w + 100]

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