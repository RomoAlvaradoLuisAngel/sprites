import pygame

# Inicializar Pygame
pygame.init()

# Configuración de la pantalla
ANCHO, ALTO = 800, 600  # Dimensiones de la ventana
pantalla = pygame.display.set_mode((ANCHO, ALTO))  # Crear la ventana del juego
pygame.display.set_caption("Juego marcianito")  # Título de la ventana

# Cargar sprites del personaje (animación de caminar)
sprites_caminar = [
    pygame.image.load("personaje1/frame1_001.png").convert_alpha(),
    pygame.image.load("personaje1/frame2_002.png").convert_alpha(),
    pygame.image.load("personaje1/frame3_003.png").convert_alpha(),
    pygame.image.load("personaje1/frame4_004.png").convert_alpha(),
    pygame.image.load("personaje1/frame5_005.png").convert_alpha(),
    pygame.image.load("personaje1/frame6_006.png").convert_alpha(),
]

# Cargar sprite de ataque (puedes agregar más sprites para una animación completa)
sprites_ataque = [
    pygame.image.load("personaje1/frame1_001.png").convert_alpha()
]

# Cargar sprites del enemigo (animación de caminar)
sprites_enemigo = [
    pygame.image.load("personaje2/frame1_001.png").convert_alpha(),
    pygame.image.load("personaje2/frame2_002.png").convert_alpha()
]

# Cargar imagen de la bala
bala_img = pygame.image.load("items/fireball.png").convert_alpha()

# Variables del personaje
altura_personaje = sprites_caminar[0].get_height() #Altura del sprite del personaje
pos_x, pos_y = 100, 0  # Posición inicial del personaje (x, y)
velocidad = 5  # Velocidad de movimiento horizontal del personaje
indice_sprite = 0  # Índice del sprite actual del personaje
contador = 0  # Contador para controlar la animación del personaje
retraso_animacion = 10  # Retraso entre cambios de sprite del personaje

# Variables para el salto del personaje
saltando = False  # Indica si el personaje está en el aire
vel_salto = 0  # Velocidad vertical durante el salto
gravedad = 1  # Aceleración debido a la gravedad
salto_inicial = -15  # Velocidad inicial del salto (negativa para subir)

# Definir el suelo
suelo_rect = pygame.Rect(0, 550, ANCHO, 50)  # Rectángulo que representa el suelo
suelo_y = suelo_rect.top - altura_personaje  # Posición vertical del personaje sobre el suelo
pos_y = suelo_y  # Ajustar la posición inicial del personaje al suelo

# Variables para el disparo
balas = []  # Lista para almacenar las balas activas
bala_velocidad = 10  # Velocidad de las balas
atacando = False  # Indica si el personaje está atacando

# Variables para los enemigos
enemigos = []  # Lista para almacenar los enemigos activos
enemigo_timer = 0  # Temporizador para controlar la aparición de enemigos
ENEMIGO_INTERVALO = 2000  # Intervalo entre la aparición de enemigos (en milisegundos)
retraso_enemigo = 10  # Retraso entre cambios de sprite del enemigo (velocidad de animación)

# Crear un reloj para controlar la velocidad de fotogramas
reloj = pygame.time.Clock()

# Variable para controlar el bucle principal del juego
jugando = True

# Bucle principal del juego
while jugando:
    # Manejar eventos
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            jugando = False  # Salir del bucle si se cierra la ventana
            
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_a:
                atacando = True  # Activar el estado de ataque
                # Crear una nueva bala
                bala = {
                    "rect": bala_img.get_rect(midleft=(pos_x + 60, pos_y + 40)),  # Posición inicial de la bala
                    "activa": True  # Estado de la bala
                }
                balas.append(bala)  # Agregar la bala a la lista

    # Obtener el estado de las teclas
    teclas = pygame.key.get_pressed()
    moviendo = False  # Indica si el personaje se está moviendo

    # Mover al personaje hacia la derecha
    if teclas[pygame.K_RIGHT]:
        pos_x += velocidad
        moviendo = True

    # Mover al personaje hacia la izquierda
    if teclas[pygame.K_LEFT]:
        pos_x -= velocidad
        moviendo = True

    # Iniciar el salto si se presiona la barra espaciadora y no está saltando
    if teclas[pygame.K_SPACE] and not saltando:
        saltando = True
        vel_salto = salto_inicial

    # Lógica del salto
    if saltando:
        pos_y += vel_salto  # Actualizar la posición vertical
        vel_salto += gravedad  # Aplicar la gravedad
        if pos_y >= suelo_y:
            pos_y = suelo_y  # Asegurar que el personaje no caiga por debajo del suelo
            saltando = False  # Terminar el salto

    # Animación del personaje
    if moviendo and not atacando:
        contador += 1
        if contador >= retraso_animacion:
            indice_sprite = (indice_sprite + 1) % len(sprites_caminar)  # Cambiar al siguiente sprite
            contador = 0
    elif not atacando:
        indice_sprite = 0  # Usar el sprite inicial si no se está moviendo ni atacando

    # Crear nuevos enemigos
    ahora = pygame.time.get_ticks()  # Obtener el tiempo actual
    if ahora - enemigo_timer > ENEMIGO_INTERVALO:
        nuevo_enemigo = {
            "x": ANCHO,  # Posición horizontal inicial del enemigo (fuera de la pantalla)
            "y": suelo_rect.top - sprites_enemigo[0].get_height(),  # Posición vertical del enemigo sobre el suelo
            "indice": 0,  # Índice del sprite actual del enemigo
            "contador": 0  # Contador para controlar la animación del enemigo
        }
        enemigos.append(nuevo_enemigo)  # Agregar el nuevo enemigo a la lista
        enemigo_timer = ahora  # Reiniciar el temporizador

    # Mover enemigos y detectar colisiones con balas
    for enemigo in enemigos[:]:
        enemigo["x"] -= 2  # Mover al enemigo hacia la izquierda
        enemigo["contador"] += 1
        if enemigo["contador"] >= retraso_enemigo:
            enemigo["indice"] = (enemigo["indice"] + 1) % len(sprites_enemigo)  # Cambiar al siguiente sprite
            enemigo["contador"] = 0

        # Eliminar al enemigo si sale de la pantalla
        if enemigo["x"] + sprites_enemigo[0].get_width() < 0:
            enemigos.remove(enemigo)

        # Detectar colisión con balas
        enemigo_rect = sprites_enemigo[enemigo["indice"]].get_rect(topleft=(enemigo["x"], enemigo["y"]))
        for bala in balas:
            if bala["activa"] and bala["rect"].colliderect(enemigo_rect):
                enemigos.remove(enemigo)  # Eliminar al enemigo
                bala["activa"] = False  # Desactivar la bala
                break  # Salir del bucle de balas para evitar errores

    # Mover balas
    for bala in balas[:]:
        if bala["activa"]:
            bala["rect"].x += bala_velocidad  # Mover la bala hacia la derecha
            if bala["rect"].x > ANCHO:
                bala["activa"] = False  # Desactivar la bala si sale de la pantalla

    # Dibujar elementos en la pantalla
    pantalla.fill((255, 255, 255))  # Rellenar la pantalla con color blanco
    pygame.draw.rect(pantalla, (120, 120, 120), suelo_rect)  # Dibujar el suelo

    # Dibujar al personaje
    if atacando:
        pantalla.blit(sprites_ataque[0], (pos_x, pos_y))  # Dibujar el sprite de ataque
        atacando = False  # Restablecer el estado de ataque
    else:
        pantalla.blit(sprites_caminar[indice_sprite], (pos_x, pos_y))  # Dibujar el sprite de caminar

    # Dibujar enemigos
    for enemigo in enemigos:
        sprite = sprites_enemigo[enemigo["indice"]]
        pantalla.blit(sprite, (enemigo["x"], enemigo["y"]))

    # Dibujar balas
    for bala in balas:
        if bala["activa"]:
            pantalla.blit(bala_img, bala["rect"])

    # Actualizar la pantalla
    pygame.display.flip()

    # Controlar la velocidad de fotogramas
    reloj.tick(60)  # Limitar a 60 fotogramas por segundo

# Salir de Pygame
pygame.quit()