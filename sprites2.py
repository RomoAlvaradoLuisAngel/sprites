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
indice_sprite = 0 #inicializacion de lista de imagenes
retraso_animacion = 10  # Cambiar sprite cada 10 fotogramas
contador = 0 #
pos_x, pos_y = 500,500
velocidad = 5

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

    # Animación
    if moviendo:
        contador += 1
        if contador >= retraso_animacion:
            indice_sprite = (indice_sprite + 1) % len(sprites_caminar)#cambia el indice de la lista de imagens
            contador = 0
    else:
        indice_sprite = 0  # Imagen quieta si no se mueve


    # Dibujar
    pantalla.fill((255, 255, 255))
    pantalla.blit(sprites_caminar[indice_sprite], (pos_x, pos_y))
    pygame.display.flip()
    reloj.tick(60)

pygame.quit()