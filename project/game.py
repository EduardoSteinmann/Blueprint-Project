import pygame as pg
from common import *
import sys
from player import Player
from enemies import Enemy
import platform
import time

class Game:
    def __init__(self) -> None:
        pg.init()
        self.screen = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock = pg.time.Clock()
        self.is_running = False
        player1_keys = [pg.K_w, pg.K_a, pg.K_s, pg.K_d]
        player2_keys = [pg.K_UP, pg.K_LEFT, pg.K_DOWN, pg.K_RIGHT]
        self.players: tuple[Player] = (Player((50,300), "assets/Player1.png", player1_keys), Player((200, 300), "assets/Player2.png", player2_keys))
        self.player_shared_health: float = PLAYER_HEALTH
        self.delta_time = 0
        self.enemies = []
        self.platforms = []
        self.last_frame_time = Game.current_milli_time()
        self.create_platforms()

    def display_background(self):
        self.screen.fill("blue")

    def player_on_platform(self, player) -> bool:
        # print("midtop: ", player.bounding_box.midtop)
        if player.position[1] + player.bounding_box.h >= WINDOW_HEIGHT:
            player.falling = False
            player.position = [player.position[0], WINDOW_HEIGHT - player.bounding_box.h]
            return True
        for platform in self.platforms:
            if (platform.bounding_box.colliderect(player.bounding_box)
                and (platform.position[1] - (player.position[1] + player.bounding_box.h - COLLISION_DEPTH)) >= 0):
                player.falling = False
                return True
        player.falling = True
        return False
    
    def current_milli_time():
        return round(time.time() * 1000)

    def game_loop(self):
        self.is_running = True
        while self.is_running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.quit()
                elif event.type == pg.KEYDOWN:
                    self.check_keys(event)
                elif event.type == pg.KEYUP:
                    for player in self.players:
                        player.reset_horizontal(event.key)

            now = Game.current_milli_time()
            self.delta_time =  now - self.last_frame_time
            self.display_background()
            self.display_players()

            pg.display.update()
            self.clock.tick(FPS)
            self.last_frame_time = now
            for player in self.players:
                player.gravity(self.delta_time)
                player.update_position(self.delta_time)
                if self.player_on_platform(player):
                    player.velocity = (player.velocity[0], 0)
                print(player.position, player.bounding_box.topleft)

    def display_players(self):
        for player in self.players:
            self.screen.blit(player.sprite, player.position)

    def check_keys(self, event):        
        for player in self.players:
            left_key_pressed = False
            right_key_pressed = False
            if event.key == player.move_keys[UP]:
                print("Pressed up!")
                player.jump()
            elif event.key == player.move_keys[DOWN]:
                print("Pressed down!")
                player.down()
            elif event.key == player.move_keys[LEFT]:
                print("Pressed left!")
                left_key_pressed = True
            elif event.key == player.move_keys[RIGHT]:
                print("Pressed right")
                right_key_pressed = True
            player.move_horizontal(left_key_pressed, right_key_pressed)

    def create_platforms(self):
        self.platforms = [
            platform.Platform((100,100), "assets/Game.png"),
            platform.Platform((100,100), "assets/Game.png")
        ]

    def create_enemies(self):
        pass
    
    def quit(self):
        pg.quit()
        sys.exit()