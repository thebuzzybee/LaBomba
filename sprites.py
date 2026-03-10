import pygame
from pygame.examples.grid import TILE_SIZE

from config import *

class Player1(pygame.sprite.Sprite):
    def __init__(self, game, player1_x, player1_y):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self._layer = player1_layer
        self.x_change = 0
        self.y_change = 0
        self.bomb_count = 2
        self.bomb_timer = 3000
        self.explosion_range = 2
        self.groups = self.game.all_sprites, self.game.players
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.image = self.game.player1_spritesheet.get_sprite(0, 0, tilesize, tilesize)
        player1_size = int(tilesize * 2/3)
        self.image = pygame.transform.scale(self.image, (player1_size, player1_size))
        self.rect = self.image.get_rect()
        self.rect.x = player1_x
        self.rect.y = player1_y
        self.player1_facing = "down"
        
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
        if keys[pygame.K_a]:
            self.x_change -= player1_velocity
            self.player1_facing = "left"
        if keys[pygame.K_d]:
            self.x_change += player1_velocity
            self.player1_facing = "right"
        if keys[pygame.K_w]:
            self.y_change -= player1_velocity
            self.player1_facing = "up"
        if keys[pygame.K_s]:
            self.y_change += player1_velocity
            self.player1_facing = "down"
        if keys[pygame.K_q]:
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
        x = int(self.rect.centerx / tilesize) * tilesize
        y = int(self.rect.centery / tilesize) * tilesize
        if self.bomb_count > len(self.game.bomb):
            Bomb(self.game, self.bomb_timer, self.explosion_range, x, y)
    
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
        self.width = tilesize
        self.height = tilesize
        
        self.image = pygame.image.load("img/brown_square.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
    def destroy(self):
        self.kill()
        
class Indestructible(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = indestructible_layer
        self.groups = self.game.all_sprites, self.game.indestructibles, self.game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x
        self.y = y
        self.width = tilesize
        self.height = tilesize

        self.image = pygame.image.load("img/black_square.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        
class Bomb(pygame.sprite.Sprite):
    def __init__(self, game, bomb_timer, explosion_range, x, y):
        self.game = game
        self.bomb_timer = bomb_timer
        self.explosion_range = explosion_range
        self.time_placed = pygame.time.get_ticks()
        self._layer = bomb_layer
        self.groups = self.game.all_sprites, self.game.bomb
        pygame.sprite.Sprite.__init__(self, self.groups)
        
        self.x = x
        self.y = y
        self.width = tilesize
        self.height = tilesize
        
        
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
        for i in directions:
            for j in range(self.explosion_range):
                explosion_x = self.rect.x + i[0] * j * tilesize
                explosion_y = self.rect.y + i[1] * j * tilesize
                explosion_rect = pygame.Rect(explosion_x, explosion_y, tilesize, tilesize)
                for sprite in self.game.blocks:
                    if explosion_rect.colliderect(sprite.rect) and isinstance(sprite, Destructible):
                        sprite.destroy()
                        break
                    elif explosion_rect.colliderect(sprite.rect) and isinstance(sprite, Indestructible):
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
        self.width = tilesize
        self.height = tilesize

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