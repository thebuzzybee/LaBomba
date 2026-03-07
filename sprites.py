import pygame
from config import *

class Player1(pygame.sprite.Sprite):
    def __init__(self, game, player1_x, player1_y):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self._layer = player1_layer
        self.groups =self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.image = pygame.image.load("Player1_sprite.png")
        player1_size = int(tilesize * 2/3)
        self.image = pygame.transform.scale(self.image, (player1_size, player1_size))
        self.rect = self.image.get_rect()
        self.rect.x = player1_x * tilesize
        self.rect.y = player1_y * tilesize
        self.player1_facing = "down"
        
    def update(self):
        self.movement()
            
    
    def movement(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.rect.x -= player1_velocity
            self.player1_facing = "left"
        if keys[pygame.K_d]:
            self.rect.x += player1_velocity
            self.player1_facing = "right"
        if keys[pygame.K_w]:
            self.rect.y -= player1_velocity
            self.player1_facing = "up"
        if keys[pygame.K_s]:
            self.rect.y += player1_velocity
            self.player1_facing = "down"
            