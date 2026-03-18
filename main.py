import pygame
from pygame.examples.cursors import image

from sprites import *
from config import *
from map import create_map1
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
        self.window = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        pygame.display.set_caption("LaBomba")
        screen_height = self.window.get_height()
        screen_width = self.window.get_width()
        self.clock = pygame.time.Clock()
        self.running = True
        self.tilesize = screen_height // row_count
        self.map_offset_x = (screen_width - column_count * self.tilesize) // 2
        
        self.player1_spritesheet = Spritesheet("img/Character.png")
        self.player2_spritesheet = Spritesheet("img/Character.png")
        self.player3_spritesheet = Spritesheet("img/Character.png")
        self.player4_spritesheet = Spritesheet("img/Character.png")
        self.bomb_image = pygame.image.load("img/bomb.png").convert_alpha()
        self.explosion_image = pygame.image.load("img/explosion.png").convert_alpha()
        self.bombpowerup_image = pygame.image.load("img/bombpowerup.png").convert_alpha()
        self.rangepowerup_image = pygame.image.load("img/rangepowerup.png").convert_alpha()
    
    def createmap(self):
        for row in range(len(create_map1())):
            for column in range(len(create_map1()[row])):
                map_code = create_map1()[row][column]
                x = column * self.tilesize + self.map_offset_x
                y = row * self.tilesize
                if map_code == empty:
                    continue
                elif map_code == destructible:
                    Destructible(self,x,y)
                elif map_code == indestructible:
                    Indestructible(self,x,y)
                elif map_code == player1:
                    Player(self, x ,y ,self.player1_spritesheet, controls_wasd, player_velocity)
                elif map_code == player2:
                    Player(self, x ,y ,self.player2_spritesheet, controls_arrows, player_velocity)
                elif map_code == player3:
                    Player(self, x ,y ,self.player3_spritesheet, controls_ijkl, player_velocity)
                elif map_code == player4:
                    Player(self, x ,y ,self.player4_spritesheet, controls_numpad, player_velocity)
                    
    def new(self):
        self.playing = True
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.destructibles = pygame.sprite.LayeredUpdates()
        self.indestructibles = pygame.sprite.LayeredUpdates()
        self.blocks = pygame.sprite.LayeredUpdates()
        self.bomb = pygame.sprite.LayeredUpdates()
        self.explosion = pygame.sprite.LayeredUpdates()
        self.players = pygame.sprite.LayeredUpdates()
        self.powerup = pygame.sprite.LayeredUpdates()
        self.createmap()
        self.playing = True
    
    def updates(self):
        self.all_sprites.update()
    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                    self.playing = False
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