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


    if pygame.key.get_pressed()[pygame.K_KP8]:
        player2_y -= player2_velocity
    if pygame.key.get_pressed()[pygame.K_KP5]:
        player2_y += player2_velocity
    if pygame.key.get_pressed()[pygame.K_KP4]:
        player2_x -= player2_velocity
    if pygame.key.get_pressed()[pygame.K_KP6]:
        player2_x += player2_velocity
    if pygame.key.get_pressed()[pygame.K_KP7]:
        print("7")
    if pygame.key.get_pressed()[pygame.K_KP9]:
        print("9")

    if pygame.key.get_pressed()[pygame.K_w]:
        player1_y -= player1_velocity
    if pygame.key.get_pressed()[pygame.K_s]:
        player1_y += player1_velocity
    if pygame.key.get_pressed()[pygame.K_a]:
        player1_x -= player1_velocity
    if pygame.key.get_pressed()[pygame.K_d]:
        player1_x += player1_velocity
    if pygame.key.get_pressed()[pygame.K_q]:
        print("q")
    if pygame.key.get_pressed()[pygame.K_e]:
        print("e")
    pygame.display.update()
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