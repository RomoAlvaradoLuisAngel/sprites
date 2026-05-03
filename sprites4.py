import pygame

pygame.init()

# Configuración
ANCHO, ALTO = 800, 600
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Juego marcianito")
# Cargar sprites del personaje
sprites_caminar = [
    pygame.image.load("personaje1/frame1_001.png").convert_alpha(),
    pygame.image.load("personaje1/frame2_002.png").convert_alpha(),
    pygame.image.load("personaje1/frame3_003.png").convert_alpha(),
    pygame.image.load("personaje1/frame4_004.png").convert_alpha(),
    pygame.image.load("personaje1/frame5_005.png").convert_alpha(),
    pygame.image.load("personaje1/frame6_006.png").convert_alpha(),
]

# Altura del personaje y suelo
altura_personaje = sprites_caminar[0].get_height()
suelo_rect = pygame.Rect(0, 550, ANCHO, 50)
suelo_y = suelo_rect.top - altura_personaje
pos_x, pos_y = 100, suelo_y
velocidad = 5

# Cargar sprites del enemigo
sprites_enemigo = [
    pygame.image.load("personaje2/frame_001.png").convert_alpha(),
    pygame.image.load("personaje2/frame_002.png").convert_alpha(),
    pygame.image.load("personaje2/frame_003.png").convert_alpha(),
    pygame.image.load("personaje2/frame_004.png").convert_alpha(),
    pygame.image.load("personaje2/frame_005.png").convert_alpha(),
    pygame.image.load("personaje2/frame_006.png").convert_alpha(),
]
altura_enemigo = sprites_enemigo[0].get_height()
enemigo_x = 700
enemigo_y = suelo_rect.top - altura_enemigo
indice_enemigo = 0
contador_enemigo = 0
retraso_enemigo = 10  # velocidad de animación

# Variables del personaje
indice_sprite = 0
retraso_animacion = 10
contador = 0

# Variables del salto
saltando = False
vel_salto = 0
gravedad = 1
salto_inicial = -15

# Reloj
reloj = pygame.time.Clock()
jugando = True

while jugando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            jugando = False

    teclas = pygame.key.get_pressed()
    moviendo = False

    if teclas[pygame.K_RIGHT]:
        pos_x += velocidad
        moviendo = True
    if teclas[pygame.K_LEFT]:
        pos_x -= velocidad
        moviendo = True
    if teclas[pygame.K_SPACE] and not saltando:
        saltando = True
        vel_salto = salto_inicial

    # Lógica de salto
    if saltando:
        pos_y += vel_salto
        vel_salto += gravedad
        if pos_y >= suelo_y:
            pos_y = suelo_y
            saltando = False

    # Animación del personaje
    if moviendo:
        contador += 1
        if contador >= retraso_animacion:
            indice_sprite = (indice_sprite + 1) % len(sprites_caminar)
            contador = 0
    else:
        indice_sprite = 0

    # Movimiento del enemigo
    enemigo_x -= 2
    if enemigo_x + sprites_enemigo[0].get_width() < 0:
        enemigo_x = ANCHO

    # Animación del enemigo
    contador_enemigo += 1
    if contador_enemigo >= retraso_enemigo:
        indice_enemigo = (indice_enemigo + 1) % len(sprites_enemigo)
        contador_enemigo = 0

    # Detección de colisión
    personaje_rect = sprites_caminar[indice_sprite].get_rect(topleft=(pos_x, pos_y))
    enemigo_rect = sprites_enemigo[indice_enemigo].get_rect(topleft=(enemigo_x, enemigo_y))
    if personaje_rect.colliderect(enemigo_rect):
        print("¡Colisión con enemigo!")

    # Dibujar
    pantalla.fill((255, 255, 255))
    pygame.draw.rect(pantalla, (120, 120, 120), suelo_rect)  # Suelo
    pantalla.blit(sprites_caminar[indice_sprite], (pos_x, pos_y))  # Personaje
    pantalla.blit(sprites_enemigo[indice_enemigo], (enemigo_x, enemigo_y))  # Enemigo

    pygame.display.flip()
    reloj.tick(60)

pygame.quit()
