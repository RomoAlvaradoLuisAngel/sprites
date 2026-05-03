import pygame

pygame.init()

# Configuración
ANCHO, ALTO = 800, 600
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Juego marcianito")

# Cargar imágenes de caminar
sprites_caminar = [
    pygame.image.load("personaje1/frame1_001.png").convert_alpha(),
    pygame.image.load("personaje1/frame2_002.png").convert_alpha(),
    pygame.image.load("personaje1/frame3_003.png").convert_alpha(),
    pygame.image.load("personaje1/frame4_004.png").convert_alpha(),
    pygame.image.load("personaje1/frame5_005.png").convert_alpha(),
    pygame.image.load("personaje1/frame6_006.png").convert_alpha(),
]

# Inicialización
indice_sprite = 0
retraso_animacion = 10
contador = 0
pos_x, pos_y = 100, 500
velocidad = 5

# Variables del salto
saltando = False
velocidad_salto = 0
gravedad = 1
salto_inicial = -15
suelo = 500  # Y del suelo (la altura original del personaje)

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

    #define la tecla del salto
    if teclas[pygame.K_SPACE] and not saltando:
        saltando = True
        velocidad_salto = salto_inicial

    # Lógica de salto
    if saltando:
        pos_y += velocidad_salto
        velocidad_salto += gravedad
        if pos_y >= suelo:
            pos_y = suelo
            saltando = False

    # Animación
    if moviendo:
        contador += 1
        if contador >= retraso_animacion:
            indice_sprite = (indice_sprite + 1) % len(sprites_caminar)
            contador = 0
    else:
        indice_sprite = 0

    # Dibujar
    pantalla.fill((255, 255, 255))
    pantalla.blit(sprites_caminar[indice_sprite], (pos_x, pos_y))
    pygame.display.flip()
    reloj.tick(60)

pygame.quit()
