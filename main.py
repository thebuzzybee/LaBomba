import pygame
from pygame.examples.cursors import image

from sprites import *
from config import *
pygame.init()


class Spritesheet:
    def __init__(self, filename):
        self.sheet = pygame.image.load(filename).convert()
        
    def get_sprite(self, x, y, width, height):
        sprite = pygame.Surface((width, height))
        sprite.blit(self.sheet, (0,0),(x, y, width, height))
        sprite.set_colorkey((0,0,0))
        return sprite
      
        
class Game:
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode((width, height))
        pygame.display.set_caption("LaBomba")
        self.clock = pygame.time.Clock()
        self.running = True
        
        self.player1_spritesheet = Spritesheet("player1_spritesheet.png")
        
    
    def createmap(self):
        for row in range(len(game_map1)):
            for column in range(len(game_map1[row])):
                map_code = game_map1[row][column]
                x = column * tilesize
                y = row * tilesize
                if map_code == empty:
                    continue
                elif map_code == destructible:
                    Destructible(self,x,y)
                elif map_code == indestructible:
                    Indestructible(self,x,y)
                elif map_code == player1:
                    Player1(self,x,y)
                    
    def new(self):
        self.playing = True
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.destructibles = pygame.sprite.LayeredUpdates()
        self.indestructibles = pygame.sprite.LayeredUpdates()
        self.createmap()
        self.playing = True
    
    def updates(self):
        self.all_sprites.update()
    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False

    def draw(self):
        self.window.fill((255,255,255))
        self.all_sprites.draw(self.window)
        self.clock.tick(fps)
        pygame.display.update()
    def main(self):
        while self.playing:
            self.events()
            self.updates()
            self.draw()
        self.running = False    
    
    def intro_screen(self):
        pass
    
    
g = Game()
g.intro_screen()
g.new()
while g.running:
    g.main()

                
            

pygame.quit()