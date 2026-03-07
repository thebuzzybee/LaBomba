import pygame
from sprites import *
from config import *
pygame.init()

class Game:
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode((width, height))
        pygame.display.set_caption("LaBomba")
        self.clock = pygame.time.Clock()
        self.running = True
    
    def new(self):
        self.playing = True
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.destructibles = pygame.sprite.LayeredUpdates()
        self.indestructibles = pygame.sprite.LayeredUpdates()
        self.playing = True
        self.player1 = Player1(self, 1, 2)
    
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