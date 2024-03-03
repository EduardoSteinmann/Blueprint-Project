import pygame
import common

class Player:
    def __init__(self, position: tuple[float], sprite_path: str, move_keys: list[int]) -> None:
        image = pygame.image.load(sprite_path)
        self.position = position
        self.sprite = image
        self.bounding_box = image.get_rect()
        self.is_performing_action = False
        self.range = common.METER
        self.teleport_cooldown = 0
        self.falling = True 
        self.velocity = (0, 0)
        self.move_keys = move_keys
        
    def get_position(self) -> int:
        return self.position

    def move(self, offset: tuple[float]) -> None:
        self.position = [self.position[0] + offset[0], self.position[1] + offset[1]]
        self.bounding_box.move_ip(offset)
        
    # def attack(self, enemies]) -> None:
    #     pass

    def gravity(self, delta_time: float) -> None:
        if self.falling:
            # Going down is positive (top left of screen is (0,0))
            self.velocity = (self.velocity[0], self.velocity[1]+ common.GRAVITY * delta_time) # delta_time = time between frames
        
    
    def jump(self) -> None:
        if not self.falling and not self.is_performing_action:
            self.velocity = (self.velocity[0], - common.JUMP_MODIFIER)

    def thrown(self) -> None:
        #self.velocity = [self.velocity[0] - common.THROW_MODIFIER]
        self.velocity = (self.velocity[0], - common._MODIFIER)

    def move_horizontal(self, isLeftPressed: bool, isRightPressed: bool):
        if self.is_performing_action:
            return
        if isLeftPressed and isRightPressed:
            return
        if isRightPressed:
            self.velocity = (common.JUMP_MODIFIER, self.velocity[1])
        if isLeftPressed:
            self.velocity = (-common.JUMP_MODIFIER, self.velocity[1])
    
    def update_position(self, delta_time: float):
        offset = (delta_time * self.velocity[0], delta_time * self.velocity[1])
        self.move(offset)

    def reset_horizontal(self, key):
        if key == self.move_keys[common.RIGHT]:
            self.velocity = (0, self.velocity[1])
        elif key == self.move_keys[common.LEFT]:
            self.velocity = (0, self.velocity[1])
    
    def set_x_vel(self, new_x):
        self.velocity = [new_x, self.velocity[1]]