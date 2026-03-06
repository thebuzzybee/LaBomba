import pygame
from config import *

class Player1(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self._layer = player1_layer
        self.groups =self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.x = x * tilesize
        self.y = y * tilesize
        self.player1_sprite = pygame.image.load("Player1_sprite.png")
        self.player1_sprite = pygame.transform.scale(self.player1_sprite, (tilesize, tilesize))
        self.player1_rect = self.player1_image.get_rect()
        self.player1_rect.x = self.x
        self.player1_rect.y = self.y
        
    def update(self):
        pass