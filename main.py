import pygame
pygame.font.init()
pygame.mixer.init()
window = pygame.display.set_mode((1000, 600))
pygame.display.set_caption("Ribbit y Frogo")
clock = pygame.time.Clock()

class GameSprite(pygame.sprite.Sprite):
    def __init__(self, img, ancho, alto, x, y, speed):
        pygame.sprite.Sprite.__init__(self)
        self.speed = speed
        self.image = pygame.transform.scale(pygame.image.load(img), (ancho, alto))
        self.imagen2 = pygame.transform.flip(self.image, True, False)
        self.images = [self.image, self.imagen2]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.player = 1
        self.direccion = 0  
        
    def draw(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
        
SALTO_VERDE = pygame.transform.scale(pygame.image.load('ranasaltando.png').convert_alpha(), (50, 50))
SALTO_MORADA = pygame.transform.scale(pygame.image.load('msaltando.png').convert_alpha(), (45, 40))
SALTO_VERDE_IZQ = pygame.transform.flip(SALTO_VERDE, True, False)
SALTO_MORADA_IZQ = pygame.transform.flip(SALTO_MORADA, True, False)

class Player(GameSprite):
    def __init__(self, img, ancho, alto, x, y, speed, img_salto_der, img_salto_izq):
        super().__init__(img, ancho, alto, x, y, speed)
        self.images_salto = [img_salto_der, img_salto_izq]
        self.gravedad = 0.1
        self.altura_salto = 5
        self.velocidad_y = 0
        self.y_inicial = y
        self.esta_saltando = False
        self.salto_presionado = False
        self.velocidad_x_salto = 0
         

    def update(self, keys, walls):
        # Movimiento horizontal y vertical con colisión
        dx, dy = 0, 0
        if self.player == 1:
            if not self.esta_saltando:
                if keys[pygame.K_a] and self.rect.x > 0:
                    dx = -self.speed
                    self.image = self.images[0]
                    self.direccion = 1
                if keys[pygame.K_s] and self.rect.y < 550:
                    dy = self.speed
                if keys[pygame.K_d] and self.rect.x < 950:
                    dx = self.speed
                    self.image = self.images[1]
                    self.direccion = 0
            if keys[pygame.K_w]:
                if not self.salto_presionado and not self.esta_saltando:
                    self.esta_saltando = True
                    self.velocidad_y = -self.altura_salto
                    if keys[pygame.K_d]:
                        self.velocidad_x_salto = self.speed * 2.0
                        self.image = self.images_salto[1]
                        self.direccion = 0
                    elif keys[pygame.K_a]:
                        self.velocidad_x_salto = -self.speed * 2.0
                        self.image = self.images_salto[0]
                        self.direccion = 1
                    else:
                        self.velocidad_x_salto = 0
                        # Usa el sprite de salto derecho por defecto para salto vertical
                        self.image = self.images_salto[1]
                    self.salto_presionado = True
            else:
                self.salto_presionado = False
        if self.player == 2:
            if not self.esta_saltando:
                if keys[pygame.K_LEFT] and self.rect.x > 0:
                    dx = -self.speed
                    self.image = self.images[0]
                    self.direccion = 1
                if keys[pygame.K_DOWN] and self.rect.y < 550:
                    dy = self.speed
                if keys[pygame.K_RIGHT] and self.rect.x < 950:
                    dx = self.speed
                    self.image = self.images[1]
                    self.direccion = 0
            if keys[pygame.K_UP]:
                if not self.salto_presionado and not self.esta_saltando:
                    self.esta_saltando = True
                    self.velocidad_y = -self.altura_salto
                    if keys[pygame.K_RIGHT]:
                        self.velocidad_x_salto = self.speed * 2.0
                        self.image = self.images_salto[0]
                        self.direccion = 0
                    elif keys[pygame.K_LEFT]:
                        self.velocidad_x_salto = -self.speed * 2.0
                        self.image = self.images_salto[1]
                        self.direccion = 1
                    else:
                        self.velocidad_x_salto = 0
                        # Usa el sprite de salto derecho por defecto para salto vertical
                        self.image = self.images_salto[0]
                    self.salto_presionado = True
            else:
                self.salto_presionado = False

        # Movimiento con colisión (solo si no está saltando)
        if not self.esta_saltando:
            # Movimiento horizontal
            if dx != 0:
                self.rect.x += dx
                for w in walls:
                    if self.rect.colliderect(w.rect):
                        if dx > 0:
                            self.rect.right = w.rect.left
                        else:
                            self.rect.left = w.rect.right
                # ...gravedad al caminar lateralmente...
                en_plataforma = False
                for w in walls:
                    if self.rect.bottom == w.rect.top and self.rect.right > w.rect.left and self.rect.left < w.rect.right:
                        en_plataforma = True
                        break
                if not en_plataforma and self.rect.y < self.y_inicial:
                    self.velocidad_y += self.gravedad
                    self.rect.y += self.velocidad_y
                    for w in walls:
                        if self.rect.colliderect(w.rect):
                            self.rect.bottom = w.rect.top
                            self.velocidad_y = 0
            # Movimiento vertical
            if dy != 0:
                self.rect.y += dy
                for w in walls:
                    if self.rect.colliderect(w.rect):
                        if dy > 0:
                            self.rect.bottom = w.rect.top
                        else:
                            self.rect.top = w.rect.bottom
            # Si no hay movimiento ni salto, aplicar gravedad (inactividad)
            if dx == 0 and dy == 0:
                en_plataforma = False
                for w in walls:
                    if self.rect.bottom == w.rect.top and self.rect.right > w.rect.left and self.rect.left < w.rect.right:
                        en_plataforma = True
                        break
                if not en_plataforma and self.rect.y < self.y_inicial:
                    self.velocidad_y += self.gravedad
                    self.rect.y += self.velocidad_y
                    for w in walls:
                        if self.rect.colliderect(w.rect):
                            self.rect.bottom = w.rect.top
                            self.velocidad_y = 0

        # Salto y gravedad
        if self.esta_saltando:
            # Permitir movimiento lateral si el salto es vertical (sin velocidad_x_salto inicial)
            keys_pressed = pygame.key.get_pressed()
            if self.velocidad_x_salto == 0:
                if self.player == 1:
                    if keys_pressed[pygame.K_a] and self.rect.x > 0:
                        self.rect.x -= self.speed
                    if keys_pressed[pygame.K_d] and self.rect.x < 950:
                        self.rect.x += self.speed
                if self.player == 2:
                    if keys_pressed[pygame.K_LEFT] and self.rect.x > 0:
                        self.rect.x -= self.speed
                    if keys_pressed[pygame.K_RIGHT] and self.rect.x < 950:
                        self.rect.x += self.speed
                # Colisión lateral durante salto vertical
                for w in walls:
                    if self.rect.colliderect(w.rect):
                        if self.player == 1:
                            if keys_pressed[pygame.K_a]:
                                self.rect.left = w.rect.right
                            if keys_pressed[pygame.K_d]:
                                self.rect.right = w.rect.left
                        if self.player == 2:
                            if keys_pressed[pygame.K_LEFT]:
                                self.rect.left = w.rect.right
                            if keys_pressed[pygame.K_RIGHT]:
                                self.rect.right = w.rect.left
            # Movimiento en Y (vertical)
            self.rect.y += self.velocidad_y
            contacto_plataforma = False
            for w in walls:
                if self.rect.colliderect(w.rect):
                    contacto_plataforma = True
                    if self.velocidad_y > 0:
                        self.rect.bottom = w.rect.top
                        self.esta_saltando = False
                        self.velocidad_y = 0
                        self.velocidad_x_salto = 0
                    elif self.velocidad_y < 0:
                        self.rect.top = w.rect.bottom
                        self.velocidad_y = 0
            # Movimiento en X (horizontal) para salto diagonal
            if self.velocidad_x_salto != 0:
                self.rect.x += self.velocidad_x_salto
                for w in walls:
                    if self.rect.colliderect(w.rect):
                        if self.velocidad_x_salto > 0:
                            self.rect.right = w.rect.left
                        elif self.velocidad_x_salto < 0:
                            self.rect.left = w.rect.right
                        self.velocidad_x_salto = 0
            # Si no está en contacto con ninguna plataforma, sigue aplicando gravedad
            if not contacto_plataforma:
                self.velocidad_y += self.gravedad
            if self.rect.x < 0:
                self.rect.x = 0
            elif self.rect.x > 950:
                self.rect.x = 950
            if self.rect.y >= self.y_inicial:
                self.rect.y = self.y_inicial
                self.esta_saltando = False
                self.velocidad_y = 0
                self.velocidad_x_salto = 0

class wall():
    def __init__(self, x, y, w, h, color):
        self.color = color
        self.rect = pygame.Rect(x, y, w, h)
    def draw(self):
        pygame.draw.rect(window, self.color , self.rect)
w1 = wall(0, 520, 200 , 10,(255,255,255)) #horizontal
w3 = wall(60,420, 250 , 10,(255,255,255)) #horizontal
w5 = wall(0,300, 30 , 10,(255,255,255)) #horizontal
w6 = wall(60,220, 40 , 10,(255,255,255)) #horizontal
w7 = wall(100,120, 200 , 10,(255,255,255)) #horizontal
w8 = wall(300, 520, 200 , 10,(255,255,255)) #horizontal
w9 = wall(100,120, 200 , 10,(255,255,255)) #horizontal
w12 = wall(100,300, 200 , 10,(255,255,255)) #horizontal
w13 = wall(180,220, 220 , 10,(255,255,255)) #horizontal
w14 = wall(180,220, 220 , 10,(255,255,255)) #horizontal
w15 = wall(470,420, 90, 10,(255,255,255)) #horizontal
w16 = wall(400, 300, 40 , 10,(255,255,255)) #horizontal
w17 = wall(470, 200, 30 , 10,(255,255,255)) #horizontal
w18 = wall(500, 120, 500 , 10,(255,255,255)) #horizontal
w19 = wall(0, 0, 100000000 , 10,(255,255,255)) #horizontal
w20 = wall(670, 510, 40 , 10,(255,255,255)) #horizontal
w22 = wall(570,330, 40, 10,(255,255,255)) #horizontal
w23 = wall(770,320, 40, 10,(255,255,255)) #horizontal
w24 = wall(500,220, 40, 10,(255,255,255)) #horizontal
w25 = wall(630,210, 40, 10,(255,255,255)) #horizontal
w27 = wall(890,410, 40, 10,(255,255,255)) #horizontal
w28 = wall(960,350, 40, 10,(255,255,255)) #horizontal

w2 = wall(300, 300, 10,300,(255,255,255))
w4 = wall(100,120, 10, 300, (255,255,255))
w10 = wall(500, 120, 10,410,(255,255,255))
w11 = wall(400, 0, 10,430,(255,255,255))
w21 = wall(990, 250, 10,590,(255,255,255))
w26 = wall(900, 120, 10, 250,(255,255,255)) 

walls = [w1, w2, w3, w4 ,w5, w6, w7, w8, w9,w10,w11,w12,w14, w13,w15,w16,w17,w18, w19, w20,w21,w22,w23,w24,w25,w26,w27,w28]

izq = Player("ranaverde.png", 50, 50, 0, 559, 2.5, SALTO_VERDE, SALTO_VERDE_IZQ)
der = Player("morada.png", 45, 40, 310, 565, 2.5, SALTO_MORADA, SALTO_MORADA_IZQ)
primer_fondo = pygame.transform.scale(pygame.image.load("fondo1.png"), (1000, 600))
der.player = 2

play = False   
run = True
while run:
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    window.fill((0, 0, 0))
    if not play:
        
        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.load("fondo1.mp3")
            pygame.mixer.music.play(loops=-1)
        font = pygame.font.SysFont("Arial", 36)
        text = font.render("Presiona ESPACIO para jugar", True, (255, 255, 255))
        img = pygame.image.load("historia.jpg")
        window.blit(img, (0, 0))
        window.blit(text, (283, 500))
        if keys[pygame.K_SPACE]:
            play = True 
            pygame.mixer.music.stop() 
    
    if play:
        window.blit(primer_fondo, (0, 0))
        izq.draw()
        izq.update(keys, walls)
        der.draw()
        der.update(keys, walls)
        for w in walls:
            w.draw()

    pygame.display.update()
    clock.tick(100)