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
        self.scores = {}
        
        self.player1_spritesheet = Spritesheet("img/Character.png")
        self.player2_spritesheet = Spritesheet("img/Character.png")
        self.player3_spritesheet = Spritesheet("img/Character.png")
        self.player4_spritesheet = Spritesheet("img/Character.png")
        self.bomb_image = pygame.image.load("img/bomb.png").convert_alpha()
        self.explosion_image = pygame.image.load("img/explosion.png").convert_alpha()
        self.bombpowerup_image = pygame.image.load("img/bombpowerup.png").convert_alpha()
        self.rangepowerup_image = pygame.image.load("img/rangepowerup.png").convert_alpha()
        self.speedpowerup_image = pygame.image.load("img/speedpowerup.png").convert_alpha()
        self.background_image = pygame.image.load("img/ground.png").convert_alpha()
        self.background_image = pygame.transform.scale(self.background_image, (self.tilesize * column_count, self.tilesize * row_count))
    
    def createmap(self):
        tilemap = create_map1()
        for row in range(len(tilemap)):
            for column in range(len(tilemap[row])):
                map_code = tilemap[row][column]
                x = column * self.tilesize + self.map_offset_x
                y = row * self.tilesize
                if map_code == empty:
                    continue
                elif map_code == destructible:
                    Destructible(self,x,y)
                elif map_code == indestructible:
                    Indestructible(self,x,y)
                elif map_code == player1:
                    Player(self, x ,y ,self.player1_spritesheet, controls_wasd, player_velocity, 1)
                elif map_code == player2:
                    Player(self, x ,y ,self.player2_spritesheet, controls_arrows, player_velocity, 2)
                elif map_code == player3:
                    Player(self, x ,y ,self.player3_spritesheet, controls_ijkl, player_velocity, 3)
                elif map_code == player4:
                    Player(self, x ,y ,self.player4_spritesheet, controls_numpad, player_velocity, 4)
                    
    def new(self):
        self.playing = True
        self.round_over = False
        self.game_over = False
        self.round_start_time = pygame.time.get_ticks()
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.destructibles = pygame.sprite.LayeredUpdates()
        self.indestructibles = pygame.sprite.LayeredUpdates()
        self.blocks = pygame.sprite.LayeredUpdates()
        self.bomb = pygame.sprite.LayeredUpdates()
        self.explosion = pygame.sprite.LayeredUpdates()
        self.players = pygame.sprite.LayeredUpdates()
        self.powerup = pygame.sprite.LayeredUpdates()
        self.last_powerup_spawn = pygame.time.get_ticks()
        self.createmap()
        self.playing = True
    
    def updates(self):
        self.all_sprites.update()
        if pygame.time.get_ticks() - self.last_powerup_spawn > spawn_interval:
            self.last_powerup_spawn = pygame.time.get_ticks()
            rnd = random.randint(1,6)
            if rnd == 1:
                attempts = 20
                while attempts != 0:
                    x = random.randint(1, column_count - 2) * self.tilesize + self.map_offset_x
                    y = random.randint(1, row_count - 2) * self.tilesize
                    test_rect = pygame.Rect(x, y, self.tilesize, self.tilesize)
                    if not any(s.rect.colliderect(test_rect) for s in self.all_sprites):
                        SpeedUp(self, self.speedpowerup_image, x, y)
                        break
                    attempts -= 1
                    
        if len(self.players) == 1 and not self.round_over and pygame.time.get_ticks() - self.round_start_time > 2000:
            self.round_over = True
            for player in self.players:                
                self.scores[player.player_id] += 1                
                if self.scores[player.player_id] >= rounds_to_win:
                    self.running = False
                    self.playing = False
                    self.game_over = True
                else:
                    self.playing = False               
                    
    
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
        self.window.fill((205, 179, 139, 255))
        self.window.blit(self.background_image, (self.map_offset_x, 0))
        self.all_sprites.draw(self.window)
        self.clock.tick(fps)
        pygame.display.update()
    def main(self):
        while self.playing:
            self.events()
            self.updates()
            self.draw()
            
    
    def intro_screen(self):
        pass
    
    def round_end_screen(self):
        waiting = True
        while waiting:
            self.window.fill((205, 201, 165, 255))
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        waiting = False
                    elif event.key == pygame.K_ESCAPE:
                        self.running = False
                        waiting = False
    def winner_screen(self):
        waiting = True
        while waiting:
            self.window.fill((238, 220, 130, 255))
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        waiting = False
                    elif event.key == pygame.K_ESCAPE:
                        self.running = False
                        waiting = False
    
    
g = Game()
g.intro_screen()
g.new()
while g.running:
    g.main()
    if g.running and not g.game_over:
        g.round_end_screen()
        g.new()
    elif g.game_over:
        g.winner_screen()
                
            

pygame.quit()