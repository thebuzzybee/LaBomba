import pygame
pygame.init()

window = pygame.display.set_mode((1024, 800))
pygame.display.set_caption("LaBomba")

player1_x = 10
player1_y = 10
player2_x = 30
player2_y = 30
player1_velocity = 10
player2_velocity = 10
player1_sprite = pygame.image.load(r"Player1_sprite.png")
player2_sprite = pygame.image.load(r"Player2_sprite.png")


running = True
while running:
    window.fill((255,255,255))
    window.blit(player1_sprite, (player1_x, player1_y))
    window.blit(player2_sprite, (player2_x, player2_y))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_KP8:
                player2_y -= player2_velocity
            elif event.key == pygame.K_KP5:
                player2_y += player2_velocity
            elif event.key == pygame.K_KP4:
                player2_x -= player2_velocity
            elif event.key == pygame.K_KP6:
                player2_x += player2_velocity
            elif event.key == pygame.K_KP7:
                print("7")
            elif event.key == pygame.K_KP9:
                print("9")
                
            elif event.key == pygame.K_w:
                player1_y -= player1_velocity
            elif event.key == pygame.K_s:
                player1_y += player1_velocity
            elif event.key == pygame.K_a:
                player1_x -= player1_velocity
            elif event.key == pygame.K_d:
                player1_x += player1_velocity
            elif event.key == pygame.K_q:
                print("q")
            elif event.key == pygame.K_e:
                print("e")
        pygame.display.update()        
                
            

pygame.quit()