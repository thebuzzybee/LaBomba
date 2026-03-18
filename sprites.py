import pygame
from pygame.examples.grid import TILE_SIZE
import random

from config import *
from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self, game, x, y, spritesheet, controls, velocity):
        self.game = game
        self.controls = controls
        self._layer = player_layer
        self.velocity = velocity
        self.x_change = 0
        self.y_change = 0
        self.bomb_count = bomb_count_start
        self.bomb_timer = bomb_timer_start
        self.explosion_range = explosion_range_start
        self.groups = self.game.all_sprites, self.game.players
        
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.image = spritesheet.get_sprite(0, 0, 32, 32)
        player_size = int(self.game.tilesize * 2/3)
        self.image = pygame.transform.scale(self.image, (player_size, player_size))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.player_facing = "down"

    def update(self):
        self.movement()
        self.rect.x += self.x_change
        self.collide_blocks("x")
        self.rect.y += self.y_change
        self.collide_blocks("y")

        self.x_change = 0
        self.y_change = 0
        
    def movement(self):
        keys = pygame.key.get_pressed()
        if keys[self.controls["left"]]:
            self.x_change -= self.velocity
            self.player_facing = "left"
        if keys[self.controls["right"]]:
            self.x_change += self.velocity
            self.player_facing = "right"
        if keys[self.controls["up"]]:
            self.y_change -= self.velocity
            self.player_facing = "up"
        if keys[self.controls["down"]]:
            self.y_change += self.velocity
            self.player_facing = "down"
        if keys[self.controls["bomb"]]:
            self.place_bomb()

    def collide_blocks(self, direction):
        if direction == "x":
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            if hits:
                if self.x_change > 0:
                    self.rect.x = hits[0].rect.left - self.rect.width
                if self.x_change < 0:
                    self.rect.x = hits[0].rect.right

        if direction == "y":
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            if hits:
                if self.y_change > 0:
                    self.rect.y = hits[0].rect.top - self.rect.height
                if self.y_change < 0:
                    self.rect.y = hits[0].rect.bottom

    def place_bomb(self):
        x = int((self.rect.centerx - self.game.map_offset_x) / self.game.tilesize) * self.game.tilesize + self.game.map_offset_x
        y = int(self.rect.centery / self.game.tilesize) * self.game.tilesize
        bomb_rect = pygame.Rect(x, y, self.game.tilesize, self.game.tilesize)
        for sprite in self.game.bomb:
            if bomb_rect.colliderect(sprite.rect):
                break
        else:
            if self.bomb_count > len([b for b in self.game.bomb if b.owner == self]):
                Bomb(self.game, self.bomb_timer, self.explosion_range, self, x, y)

    def destroy(self):
        self.kill()
            
            


class Destructible(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = destructible_layer
        self.groups = self.game.all_sprites, self.game.destructibles, self.game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)
        
        self.x = x
        self.y = y
        self.width = self.game.tilesize
        self.height = self.game.tilesize
        
        self.image = pygame.image.load("img/Destructible.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
    def destroy(self):
        rng = random.randint(1, 100)
        if rng <= 30:
            choice = random.choice([(BombUp, self.game.bombpowerup_image), (RangeUp, self.game.rangepowerup_image)])
            choice[0](self.game, choice[1], self.x, self.y,)
        self.kill()
        
class Indestructible(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = indestructible_layer
        self.groups = self.game.all_sprites, self.game.indestructibles, self.game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x
        self.y = y
        self.width = self.game.tilesize
        self.height = self.game.tilesize

        self.image = pygame.image.load("img/black_square.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        
class Bomb(pygame.sprite.Sprite):
    def __init__(self, game, bomb_timer, explosion_range, player, x, y):
        self.game = game
        self.owner = player
        self.bomb_timer = bomb_timer
        self.explosion_range = explosion_range
        self.time_placed = pygame.time.get_ticks()
        self._layer = bomb_layer
        self.groups = self.game.all_sprites, self.game.bomb
        pygame.sprite.Sprite.__init__(self, self.groups)
        
        self.x = x
        self.y = y
        self.width = self.game.tilesize
        self.height = self.game.tilesize
        
        
        self.image = pygame.transform.scale(self.game.bomb_image, (self.width, self.height))
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        
    def update(self):
        if pygame.time.get_ticks() - self.time_placed > self.bomb_timer:
            self.explosion()
            
    def explosion(self):
        self.kill()
        directions = [(1,0),(-1,0),(0,1),(0,-1)]
        hit = False
        for i in directions:
            for j in range(self.explosion_range):
                explosion_x = self.rect.x + i[0] * j * self.game.tilesize
                explosion_y = self.rect.y + i[1] * j * self.game.tilesize
                explosion_rect = pygame.Rect(explosion_x, explosion_y, self.game.tilesize, self.game.tilesize)
                for sprite in self.game.blocks:
                    if explosion_rect.colliderect(sprite.rect) and isinstance(sprite, Destructible):
                        hit = True
                        sprite.destroy()
                        break
                    elif explosion_rect.colliderect(sprite.rect) and isinstance(sprite, Indestructible):
                        hit = True
                        break
                if hit:
                    hit = False
                    break
                else:
                    Explosion(self.game, explosion_x, explosion_y)
        
class Explosion(pygame.sprite.Sprite):
    def __init__(self, game,  x, y):
        self.game = game
        self.time_placed = pygame.time.get_ticks()
        self._layer = explosion_layer
        self.groups = self.game.all_sprites, self.game.explosion
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x
        self.y = y
        self.width = self.game.tilesize
        self.height = self.game.tilesize

        self.image = pygame.transform.scale(self.game.explosion_image, (self.width, self.height))
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def update(self):
        for sprite in self.game.players:
            if self.rect.colliderect(sprite.rect):
                sprite.destroy()
        
        for sprite in self.game.bomb:
            if self.rect.colliderect(sprite.rect):
                sprite.explosion()
                
        if pygame.time.get_ticks() - self.time_placed > explosion_timer:
            self.kill()
            
class PowerUp(pygame.sprite.Sprite):
    def __init__(self, game, image, x, y):
        self.game = game
        self._layer = powerup_layer
        self.groups = self.game.all_sprites, self.game.powerup
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x
        self.y = y
        self.width = int(self.game.tilesize * 0.9)
        self.height = int(self.game.tilesize * 0.9)
        
        self.image = pygame.transform.scale(image, (self.width, self.height))
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
    
    
    def collect(self, player):
        pass
    def update(self):
        for sprite in self.game.players:
            if self.rect.colliderect(sprite.rect):
                self.collect(sprite)
class BombUp(PowerUp):
    def collect(self, player):
        player.bomb_count += 1
        self.kill()
    
class RangeUp(PowerUp):
    def collect(self, player):
        player.explosion_range += 1
        self.kill()