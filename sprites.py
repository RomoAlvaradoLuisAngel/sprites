import pygame
pygame.init()

# Pantalla
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

# Cargar imagen
jugador = pygame.image.load("personaje1/frame1_001.png").convert_alpha()
jugador_rect = jugador.get_rect()
jugador_rect.topleft = (100, 100)

# Bucle del juego
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Movimiento con teclas
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        jugador_rect.x -= 5
    if keys[pygame.K_RIGHT]:
        jugador_rect.x += 5

    # Dibujar
    screen.fill((0, 0, 0))
    screen.blit(jugador, jugador_rect)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()