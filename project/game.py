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
        self.players: tuple[Player] = (Player((50, 100), "assets/Player1.png", player1_keys), Player((200, 100), "assets/Player2.png", player2_keys))
        self.player_shared_health = [PLAYER_HEALTH]
        self.delta_time = 0
        self.enemies = []
        self.platforms = []
        self.last_frame_time = Game.current_milli_time()

        self.create_platforms()
        self.create_enemies()

    def better_collision(self, rect1: pg.Rect, rect2: pg.Rect) -> bool:
        rect1corners = [(rect1.x, rect1.y), (rect1.x+rect1.w, rect1.y), (rect1.x, rect1.y+rect1.h), (rect1.x+rect1.w, rect1.y + rect1.h)]
        
        rect2corners = [(rect2.x, rect2.y), (rect2.x + rect2.w, rect2.y), (rect2.x, rect2.y + rect2.h), (rect2.x + rect2.w, rect2.y + rect2.h)]

        for i in rect2corners:
            if i[0] >= rect1corners[0][0] and i[1] >= rect1corners[0][1] and i[0] <= rect1corners[3][0] and i[1] <= rect1corners[3][1]:
                return True

        # if (rect2corners[0][0] > rect1corners[0][0] and rect2corners[0][0] < rect1corners[1][0]) and (rect2corners[0][1] > rect1corners[0][1] and rect2corners[0][1] < rect1corners[1][1]):
        #     return True
        # if (rect2corners[1][0] > rect1corners[0][0] and rect2corners[1][0] < rect1corners[1][0]) and (rect2corners[1][1] > rect1corners[0][1] and rect2corners[1][1] < rect1corners[])
        return False

    def display_background(self):
        self.screen.blit(pg.image.load("assets/Floor 1.png"), (0, 0, WINDOW_WIDTH, WINDOW_HEIGHT))

    def player_on_platform(self, player) -> bool:
        # print("midtop: ", player.bounding_box.midtop)
        if player.position[1] + player.bounding_box.h >= WINDOW_HEIGHT:
            player.falling = False
            player.move((0, WINDOW_HEIGHT - (player.position[1]+player.bounding_box.h)))
            if player.velocity[1] > 0:
                player.set_y_vel(0)
            return True
        for platform in self.platforms:
            # print(platform.bounding_box.topleft)
            if player.position[0] > platform.position[0] and player.position[0] + player.bounding_box.w < platform.position[0] + platform.bounding_box.w:
                offset = platform.position[1] - player.position[1] - player.bounding_box.h
                # print(offset, platform.position[1], player.position[1] + player.bounding_box.h)
                if offset < 0 and offset > - 15:
                    if player.velocity[1] > 0:
                        player.falling = False
                        player.set_y_vel(0)
                        player.move((0, offset))
                    return True
        player.falling = True
        return False
    
    def player_hit_top(self, player):
        if player.position[1] <= 0:
            player.falling = True
            player.move((0, 0 - player.position[1]))
            player.set_y_vel(0)
            return True
        
    def player_left_platform(self, player) -> bool:
        # print("midtop: ", player.bounding_box.midtop)
        if player.position[0] <= 0:
            player.move((0-player.position[0], 0))
            if player.velocity[0] < 0:
                player.set_x_vel(0)
            return True
        for platform in self.platforms:
            if (self.better_collision(player.bounding_box, platform.bounding_box)
                and (player.position[0] - (platform.position[0] + platform.bounding_box.w - COLLISION_DEPTH)) >= 0):
                if player.velocity[0] < 0:
                    player.set_x_vel(0)
                return True
        return False
    
    def player_right_platform(self, player) -> bool:
        if player.position + player.bounding_box.w > WINDOW_WIDTH:
            player.position.move((WINDOW_WIDTH - player.bounding_box.w - player.position[0], 0))
            if player.velocity[0] > 0:
                player.set_x_vel(0)
            return True
        for platform in self.platforms:
            if (self.better_collision(player.bounding_box, platform.bounding_box)
                and (player.position[0] + player.bounding_box.w - COLLISION_DEPTH <= platform.positions)):
                if player.velocity[0] > 0:
                    player.set_x_vel(0)
                return True
        return False
                
    def current_milli_time():
        return round(time.time() * 1000)

    def game_loop(self):
        if self.check_win():
            self.quit()
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
            self.display_platforms()
            self.display_enemies()
            self.display_elevator()
            self.display_players()

            pg.display.update()
            self.last_frame_time = now
            for player in self.players:
                player.gravity(self.delta_time)
                player.update_position(self.delta_time)
                self.player_on_platform(player)
                # self.player_right_platform(player)
                # self.player_left_platform(player)
                self.player_hit_top(player)
                # print(player.velocity)

            for enemy in self.enemies:
                enemy.update_position(self.delta_time)
            self.check_enemy_collisions()
            for platform in self.platforms:
                platform.update_position(self.delta_time)
            self.clock.tick(FPS)

    def display_players(self):
        for player in self.players:
            self.screen.blit(player.sprite, player.position)

    def check_keys(self, event):
        for (i, player) in enumerate(self.players):
            left_key_pressed = False
            right_key_pressed = False
            if event.key == player.move_keys[UP]:
                player.jump()
            elif event.key == player.move_keys[LEFT]:
                left_key_pressed = True
            elif event.key == player.move_keys[RIGHT]:
                right_key_pressed = True
            elif event.key == player.move_keys[DOWN]:
                if i == 0:
                    player.teleport(self.players[1])
                else:
                    player.teleport(self.players[0])
            player.move_horizontal(left_key_pressed, right_key_pressed)

    def create_platforms(self):
        self.platforms = [ 
            platform.Platform((400, 300), "assets/platform.png"),
            platform.Platform((100,400), "assets/platform.png"),
            platform.Platform((900,400), "assets/platform.png"),
            platform.Platform((200, 700), "assets/platform.png"),
            platform.Platform((600, 300), "assets/platform.png"),
            platform.Platform((800, 700), "assets/platform.png"),
            platform.Platform((200, 500), "assets/platform.png"),
            platform.Platform((800, 500), "assets/platform.png"),
            platform.Platform((200, 600), "assets/platform.png"),
            platform.Platform((800, 600), "assets/platform.png"),
        ]
    
    def display_platforms(self):
        for platform in self.platforms:
            self.screen.blit(platform.sprite, platform.position)
   
    def create_enemies(self):
        self.enemies = [
            Enemy((400, WINDOW_HEIGHT - 100), "assets/enemy.png", (WINDOW_WIDTH / 2, WINDOW_WIDTH / 2 + 200), self.player_shared_health),
            Enemy((WINDOW_WIDTH / 2, WINDOW_HEIGHT - 100), "assets/enemy.png", (WINDOW_WIDTH / 2, WINDOW_WIDTH / 2 + 100), self.player_shared_health),
            Enemy((WINDOW_WIDTH / 2, WINDOW_HEIGHT - 300), "assets/enemy.png", (WINDOW_WIDTH / 2, WINDOW_WIDTH / 2 + 300), self.player_shared_health),
            Enemy((WINDOW_WIDTH / 2, WINDOW_HEIGHT - 500), "assets/enemy.png", (WINDOW_WIDTH / 2, WINDOW_WIDTH / 2 - 100), self.player_shared_health),
            Enemy((200, WINDOW_HEIGHT + 100), "assets/enemy.png", (WINDOW_WIDTH / 2, WINDOW_WIDTH / 2 + 200), self.player_shared_health),
            Enemy((100, 100), "assets/enemy.png", (WINDOW_WIDTH / 2, WINDOW_WIDTH / 2 + 100), self.player_shared_health),
            Enemy((WINDOW_WIDTH / 2 + 300, WINDOW_HEIGHT - 600), "assets/enemy.png", (WINDOW_WIDTH / 2, WINDOW_WIDTH / 2 + 300), self.player_shared_health),
            Enemy((WINDOW_WIDTH / 2, WINDOW_HEIGHT - 200), "assets/enemy.png", (WINDOW_WIDTH / 2, WINDOW_WIDTH / 2 - 200), self.player_shared_health),
        ]
    
    def check_win(self):
        for player in self.players:
            if player.position[0] > WINDOW_WIDTH and player.position[1] > WINDOW_HEIGHT - self.elevator.get_rect()[3]:
                return True
        return False
    
    def display_elevator(self):
        self.elevator = pg.image.load("assets/elevator.png")
        elevator = self.elevator
        self.screen.blit(elevator, (WINDOW_WIDTH - elevator.get_rect()[2], WINDOW_HEIGHT - elevator.get_rect()[3]))

    def display_enemies(self):
        for enemy in self.enemies:
            # print("enemy: ", enemy.velocity)
            self.screen.blit(enemy.sprite, enemy.position)
    
    def check_enemy_collisions(self):
        for player in self.players:
            for enemy in self.enemies:
                # print("is robot colliding: ", player.bounding_box.colliderect(enemy.bounding_box))
                if self.better_collision(player.bounding_box, enemy.bounding_box):
                    # print("bounding box: ", enemy.bounding_box.topleft, enemy.bounding_box.bottomright)
                    self.is_running = False
    
    def quit(self):
        pg.quit()
        sys.exit()