import pygame
pygame.init()

window = pygame.display.set_mode((1024, 800))
pygame.display.set_caption("LaBomba")

player1_x = 10
player1_y = 10
player2_x = 300
player2_y = 300
player1_velocity = 0.5
player2_velocity = 0.5
player1_sprite = pygame.image.load(r"Player1_sprite.png")
player2_sprite = pygame.image.load(r"Player2_sprite.png")
player1_sprite = pygame.transform.scale(player1_sprite, (100, 100))
player2_sprite = pygame.transform.scale(player2_sprite, (100, 100))
player1_hitbox = player1_sprite.get_rect()
player1_hitbox.center = (player1_x, player1_y)
player2_hitbox = player2_sprite.get_rect()
player2_hitbox.center = (player2_x, player2_y)

running = True
while running:
    window.fill((255,255,255))
    window.blit(player1_sprite, (player1_x, player1_y))
    window.blit(player2_sprite, (player2_x, player2_y))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        
    if pygame.key.get_pressed()[pygame.K_KP8]:
                player2_y -= player2_velocity
    elif pygame.key.get_pressed()[pygame.K_KP5]:
                player2_y += player2_velocity
    elif pygame.key.get_pressed()[pygame.K_KP4]:
                player2_x -= player2_velocity
    elif pygame.key.get_pressed()[pygame.K_KP6]:
                player2_x += player2_velocity
    elif pygame.key.get_pressed()[pygame.K_KP7]:
                print("7")
    elif pygame.key.get_pressed()[pygame.K_KP9]:
                print("9")
                
    elif pygame.key.get_pressed()[pygame.K_w]:
                player1_y -= player1_velocity
    elif pygame.key.get_pressed()[pygame.K_s]:
                player1_y += player1_velocity
    elif pygame.key.get_pressed()[pygame.K_a]:
                player1_x -= player1_velocity
    elif pygame.key.get_pressed()[pygame.K_d]:
                player1_x += player1_velocity
    elif pygame.key.get_pressed()[pygame.K_q]:
                print("q")
    elif pygame.key.get_pressed()[pygame.K_e]:
                print("e")
    pygame.display.update()        
                
            

pygame.quit()