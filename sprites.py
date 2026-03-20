import pygame
from pygame.examples.grid import TILE_SIZE
import random
import math

from config import *
from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self, game, x, y, spritesheet, controls, velocity):
        self.game = game
        self.controls = controls
        self._layer = player_layer
        self.velocity = velocity
        self.spritesheet = spritesheet
        self.speedpickup_time = None
        self.x_change = 0
        self.y_change = 0
        self.bomb_count = bomb_count_start
        self.bomb_timer = bomb_timer_start
        self.explosion_range = explosion_range_start
        self.groups = self.game.all_sprites, self.game.players
        
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.image = spritesheet.get_sprite(16, 143, 32, 48)
        self.player_size = int(self.game.tilesize * 2/3)
        self.image = pygame.transform.scale(self.image, (self.player_size, self.player_size * 1.5))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.hitbox = pygame.Rect(0, 0, int(self.player_size * 0.6), int(self.player_size * 1.05))
        self.hitbox.center = self.rect.center
        self.player_facing = "down"
        self.animation_loop = 1
        self.animation_speed = 0.25

    def update(self):
        self.movement()
        self.animate()
        self.hitbox.x += self.x_change
        self.rect.center = self.hitbox.center
        self.collide_blocks("x")
        self.hitbox.y += self.y_change
        self.rect.center = self.hitbox.center
        self.collide_blocks("y")
        self.rect.center = self.hitbox.center

        self.x_change = 0
        self.y_change = 0
        
        if self.speedpickup_time is not None:
            if pygame.time.get_ticks() - self.speedpickup_time > powerup_duration:
                self.velocity -= 2
                self.animation_speed -= 0.125
                self.speedpickup_time = None
        
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
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False,
                                               collided=lambda a, b: a.hitbox.colliderect(b.rect))
            if hits:
                if self.x_change > 0:
                    self.hitbox.x = hits[0].rect.left - self.hitbox.width
                    self.rect.center = self.hitbox.center
                if self.x_change < 0:
                    self.hitbox.x = hits[0].rect.right
                    self.rect.center = self.hitbox.center

        if direction == "y":
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False,
                                               collided=lambda a, b: a.hitbox.colliderect(b.rect))
            if hits:
                if self.y_change > 0:
                    self.hitbox.y = hits[0].rect.top - self.hitbox.height
                    self.rect.center = self.hitbox.center
                if self.y_change < 0:
                    self.hitbox.y = hits[0].rect.bottom
                    self.rect.center = self.hitbox.center

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
                
    
    def animate(self):
        down_animations = [self.spritesheet.get_sprite(16, 143, 32, 48),
                           self.spritesheet.get_sprite(80, 143, 32, 48),
                           self.spritesheet.get_sprite(144, 143, 32, 48),
                           self.spritesheet.get_sprite(208, 143, 32, 48),
                           self.spritesheet.get_sprite(272, 143, 32, 48),
                           self.spritesheet.get_sprite(336, 143, 32, 48),
                           self.spritesheet.get_sprite(400, 143, 32, 48),
                           self.spritesheet.get_sprite(464, 143, 32, 48)]
        
        up_animations = [self.spritesheet.get_sprite(16, 13, 32, 48),
                         self.spritesheet.get_sprite(80, 13, 32, 48),
                         self.spritesheet.get_sprite(144, 13, 32, 48),
                         self.spritesheet.get_sprite(208, 13, 32, 48),
                         self.spritesheet.get_sprite(272, 13, 32, 48),
                         self.spritesheet.get_sprite(336, 13, 32, 48),
                         self.spritesheet.get_sprite(400, 13, 32, 48),
                         self.spritesheet.get_sprite(464, 13, 32, 48)]
        
        left_animations = [self.spritesheet.get_sprite(16, 80, 32, 48),
                           self.spritesheet.get_sprite(80, 80, 32, 48),
                           self.spritesheet.get_sprite(144, 80, 32, 48),
                           self.spritesheet.get_sprite(208, 80, 32, 48),
                           self.spritesheet.get_sprite(272, 80, 32, 48),
                           self.spritesheet.get_sprite(336, 80, 32, 48),
                           self.spritesheet.get_sprite(400, 80, 32, 48),
                           self.spritesheet.get_sprite(464, 80, 32, 48)]
        
        right_animations = [self.spritesheet.get_sprite(16, 208, 32, 48),
                            self.spritesheet.get_sprite(80, 208, 32, 48),
                            self.spritesheet.get_sprite(144, 208, 32, 48),
                            self.spritesheet.get_sprite(208, 208, 32, 48),
                            self.spritesheet.get_sprite(272, 208, 32, 48),
                            self.spritesheet.get_sprite(336, 208, 32, 48),
                            self.spritesheet.get_sprite(400, 208, 32, 48),
                            self.spritesheet.get_sprite(464, 208, 32, 48)]
        
        if self.player_facing == "down":
            if self.y_change == 0:
                self.image = self.spritesheet.get_sprite(16, 143, 32, 48)
            else:
                self.image = down_animations[math.floor(self.animation_loop)]
                self.animation_loop += self.animation_speed
                if self.animation_loop >= 8:
                    self.animation_loop = 1

        if self.player_facing == "up":
            if self.y_change == 0:
                self.image = self.spritesheet.get_sprite(16, 13, 32, 48)
            else:
                self.image = up_animations[math.floor(self.animation_loop)]
                self.animation_loop += self.animation_speed
                if self.animation_loop >= 8:
                    self.animation_loop = 1

        if self.player_facing == "left":
            if self.x_change == 0:
                self.image = self.spritesheet.get_sprite(16, 80, 32, 48)
            else:
                self.image = left_animations[math.floor(self.animation_loop)]
                self.animation_loop += self.animation_speed
                if self.animation_loop >= 8:
                    self.animation_loop = 1

        if self.player_facing == "right":
            if self.x_change == 0:
                self.image = self.spritesheet.get_sprite(16, 208, 32, 48)
            else:
                self.image = right_animations[math.floor(self.animation_loop)]
                self.animation_loop += self.animation_speed
                if self.animation_loop >= 8:
                    self.animation_loop = 1

        self.image = pygame.transform.scale(self.image, (self.player_size, int(self.player_size * 1.5)))

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

        self.image = pygame.image.load("img/Indestructible.png").convert_alpha()
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
        
class SpeedUp(PowerUp):
    def collect(self, player):
        player.speedpickup_time = pygame.time.get_ticks()
        player.velocity += 2
        player.animation_speed += 0.125
        self.kill()
        
            
        