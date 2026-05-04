import pygame
import os
import sys
#esto es de chat gpt, no me quiere correr el ejecutable jaja
def ruta_archivo(ruta):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, ruta)
    return ruta


# Inicialización de Pygame
pygame.init()
pygame.mixer.init()
# Configuración de la pantalla
ANCHO, ALTO = 800, 600
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Juego marcianito")

# Cargar y ajustar la imagen de fondo
fondo = pygame.image.load(ruta_archivo("assets/items/fondo.jpg")).convert()
fondo = pygame.transform.scale(fondo, (ANCHO, ALTO))  # Ajusta al tamaño de la pantalla

fondo_menu = pygame.image.load((ruta_archivo("assets/items/menusito.png"))).convert()
fondo_menu = pygame.transform.scale(fondo_menu, (ANCHO, ALTO))


# Cargar sprites del personaje para animación de caminar
sprites_caminar = [
    pygame.image.load(ruta_archivo("assets/personaje1/frame1_001.png")).convert_alpha(),
    pygame.image.load(ruta_archivo("assets/personaje1/frame2_002.png")).convert_alpha(),
    pygame.image.load(ruta_archivo("assets/personaje1/frame3_003.png")).convert_alpha(),
    pygame.image.load(ruta_archivo("assets/personaje1/frame4_004.png")).convert_alpha(),
    pygame.image.load(ruta_archivo("assets/personaje1/frame5_005.png")).convert_alpha(),
    pygame.image.load(ruta_archivo("assets/personaje1/frame6_006.png")).convert_alpha(),
]

# Sprite para animación de ataque
sprites_ataque = [
    pygame.image.load(ruta_archivo("assets/personaje1/frame1_001.png")).convert_alpha()
]

# Cargar sprites del enemigo para su animación
sprites_enemigo = [
    pygame.image.load(ruta_archivo("assets/personaje2/frame_001.png")).convert_alpha(),
    pygame.image.load(ruta_archivo("assets/personaje2/frame_002.png")).convert_alpha()
]

# Cargar imagen de la bala
bala_img = pygame.image.load(ruta_archivo("assets/items/fireball.png")).convert_alpha()
bala_img = pygame.transform.scale(bala_img, (40, 40))

# Configuración de fuentes para mostrar texto en pantalla
fuente = pygame.font.SysFont(None, 36)
fuente_grande = pygame.font.SysFont(None, 72)

# Variables del jugador
altura_personaje = sprites_caminar[0].get_height()
pos_x, pos_y = 100, 0  # Posición inicial del personaje
velocidad = 5  # Velocidad de movimiento
indice_sprite = 0  # Índice para la animación
contador = 0  # Contador para controlar la velocidad de la animación
retraso_animacion = 10  # Retraso entre frames de animación

# Variables para el salto
saltando = False
vel_salto = 0
gravedad = 1
salto_inicial = -15  # Velocidad inicial del salto

# Definición del suelo
suelo_rect = pygame.Rect(0, 550, ANCHO, 50)  # Rectángulo que representa el suelo
suelo_y = suelo_rect.top - altura_personaje  # Posición Y del personaje sobre el suelo
pos_y = suelo_y  # Posición inicial en Y del personaje

# Variables para el disparo
balas = []  # Lista para almacenar las balas activas
bala_velocidad = 10  # Velocidad de las balas
atacando = False  # Estado de ataque del personaje

# Variables para los enemigos
enemigos = []  # Lista para almacenar los enemigos
enemigo_timer = 0  # Temporizador para controlar la aparición de enemigos
ENEMIGO_INTERVALO = 2000  # Intervalo de tiempo entre la aparición de enemigos (en milisegundos)
retraso_enemigo = 10  # Retraso entre frames de animación del enemigo

# Sistema de vidas
vidas = 3  # Vidas del jugador
game_over = False  # Estado del juego

# Control del reloj
reloj = pygame.time.Clock()
jugando = True  # Estado principal del juego

menu = True
musica_activa = True

#sonidos
sonido_disparo = pygame.mixer.Sound(ruta_archivo("assets/sonidos/pluh.mp3"))
pygame.mixer.music.load(ruta_archivo("assets/sonidos/white_records-dark-gladiator-epic-background-music-for-video-stories-37-second-490015.mp3"))
sonido_golpe = pygame.mixer.Sound(ruta_archivo("assets/sonidos/fahhhhhhhhhhhhhh.mp3"))


roca = pygame.image.load(ruta_archivo("assets/items/roca-removebg-preview.png")).convert_alpha()
roca = pygame.transform.scale(roca, (80, 80))

goku = pygame.image.load(ruta_archivo("assets/items/goku_volando-removebg-preview.png")).convert_alpha()
goku = pygame.transform.scale(goku, (100, 80))
goku_x = 0

pygame.mixer.music.play(-1)
while menu:
    pantalla.blit(fondo_menu, (0, 0))

    texto_inicio = fuente.render("ENTER para iniciar", True, (255,255,255))
    texto_musica = fuente.render("M para musica ON/OFF", True, (255,255,255))
    texto_salir = fuente.render("ESC para salir", True, (255,255,255))

    pantalla.blit(texto_inicio, (250, 200))
    pantalla.blit(texto_musica, (250, 250))
    pantalla.blit(texto_salir, (250, 300))

    pygame.display.flip()

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            menu = False
            jugando = False
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_RETURN:
                pygame.mixer.music.stop() 
                menu = False
            if evento.key == pygame.K_m:
                musica_activa = not musica_activa

                if musica_activa:
                    pygame.mixer.music.play(-1)
                else:
                    pygame.mixer.music.stop()
            if evento.key == pygame.K_ESCAPE:
                menu = False
                jugando = False

# Bucle principal del juego
while jugando:
    # Manejo de eventos
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            jugando = False  # Salir del juego
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_a and not game_over:
                atacando = True  # Activar estado de ataque
                sonido_disparo.play()  # Reproducir sonido de disparo
                # Crear una nueva bala
                bala = {
                    "rect": bala_img.get_rect(midleft=(pos_x + 60, pos_y + 40)),
                    "activa": True
                }
                balas.append(bala)  # Agregar la bala a la lista

    teclas = pygame.key.get_pressed()  # Obtener las teclas presionadas

    # Mostrar pantalla de Game Over
    if game_over:
        pantalla.fill((0, 0, 0))

        texto_final = fuente_grande.render("GAME OVER", True, (255, 0, 0))
        pantalla.blit(texto_final, (250, 200))

        texto_reiniciar = fuente.render("Presiona R para reiniciar", True, (255,255,255))
        pantalla.blit(texto_reiniciar, (250, 300))

        texto_salir = fuente.render("ESC para salir", True, (255,255,255))
        pantalla.blit(texto_salir, (250, 350))

        pygame.display.flip()

        if teclas[pygame.K_ESCAPE]:
            jugando = False

        if teclas[pygame.K_r]:
            vidas = 3
            enemigos.clear()
            balas.clear()
            pos_x = 100
            pos_y = suelo_y
            game_over = False

        continue
        # Salir del juego al presionar ESC
        if teclas[pygame.K_ESCAPE]:
            jugando = False
        continue  # Saltar el resto del bucle si el juego ha terminado

    moviendo = False  # Estado de movimiento del personaje

    # Movimiento del personaje
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
    if moviendo and not atacando:
        contador += 1
        if contador >= retraso_animacion:
            indice_sprite = (indice_sprite + 1) % len(sprites_caminar)
            contador = 0
    elif not atacando:
        indice_sprite = 0  # Sprite estático si no se mueve ni ataca

    # Generar nuevos enemigos
    ahora = pygame.time.get_ticks()
    if ahora - enemigo_timer > ENEMIGO_INTERVALO:
        nuevo_enemigo = {
            "x": ANCHO,
            "y": suelo_rect.top - sprites_enemigo[0].get_height(),
            "indice": 0,
            "contador": 0
        }
        enemigos.append(nuevo_enemigo)
        enemigo_timer = ahora

    # Mover enemigos y detectar colisiones
    personaje_rect = sprites_caminar[0].get_rect(topleft=(pos_x, pos_y))
    for enemigo in enemigos[:]:
        enemigo["x"] -= 2  # Movimiento hacia la izquierda
        enemigo["contador"] += 1
        if enemigo["contador"] >= retraso_enemigo:
            enemigo["indice"] = (enemigo["indice"] + 1) % len(sprites_enemigo)
            enemigo["contador"] = 0

        enemigo_rect = sprites_enemigo[enemigo["indice"]].get_rect(topleft=(enemigo["x"], enemigo["y"]))

        # Colisión con bala
        for bala in balas:
            if bala["activa"] and bala["rect"].colliderect(enemigo_rect):
                sonido_golpe.play()  # Reproducir sonido de golpe
                enemigos.remove(enemigo)
                bala["activa"] = False
                break

        # Colisión con el personaje
        if personaje_rect.colliderect(enemigo_rect):
            sonido_golpe.play()  # Reproducir sonido de golpe
            vidas -= 1
            enemigos.remove(enemigo)
            print(f"Vidas restantes: {vidas}")
            if vidas <= 0:
                game_over = True

        # Eliminar enemigo si sale de la pantalla
        if enemigo["x"] + sprites_enemigo[0].get_width() < 0:
            enemigos.remove(enemigo)

    # Mover balas
    for bala in balas:
        if bala["activa"]:
            bala["rect"].x += bala_velocidad
            if bala["rect"].x > ANCHO:
                bala["activa"] = False

    # Dibujar fondo y suelo
    pantalla.blit(fondo, (0, 0))
    pygame.draw.rect(pantalla, (120, 120, 120), suelo_rect)
    pantalla.blit(roca, (400, suelo_y))
    goku_x += 3  # velocidad

    if goku_x > ANCHO:
        goku_x = -100

    pantalla.blit(goku, (goku_x, 100))

    # Dibujar personaje
    if atacando:
        pantalla.blit(sprites_ataque[0], (pos_x, pos_y))
        atacando = False  # Restablecer estado de ataque
    else:
        pantalla.blit(sprites_caminar[indice_sprite], (pos_x, pos_y))

    # Dibujar enemigos
    for enemigo in enemigos:
        sprite = sprites_enemigo[enemigo["indice"]]
        pantalla.blit(sprite, (enemigo["x"], enemigo["y"]))

    # Dibujar balas
    for bala in balas:
        if bala["activa"]:
            pantalla.blit(bala_img, bala["rect"])

    # Dibujar vidas
    texto_vidas = fuente.render(f"Vidas: {vidas}", True, (255, 255, 255))
    pantalla.blit(texto_vidas, (10, 10))

    # Actualizar pantalla y controlar la velocidad de fotogramas
    pygame.display.flip()
    reloj.tick(60)

# Salir del juego
pygame.quit()
