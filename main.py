import pygame
pygame.font.init()
window = pygame.display.set_mode((1000, 600))
pygame.display.set_caption("nombre")
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
         
    def update(self, keys):   
        if self.player == 1:
            if not self.esta_saltando:
                if keys[pygame.K_a] and self.rect.x > 0:
                    self.rect.x -= self.speed
                    self.image = self.images[0]
                    self.direccion = 1
                if keys[pygame.K_s] and self.rect.y < 550:
                    self.rect.y += self.speed
                if keys[pygame.K_d] and self.rect.x < 950:
                    self.rect.x += self.speed
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
                    self.salto_presionado = True
            else:
                self.salto_presionado = False
                
        if self.player == 2:
            if not self.esta_saltando:
                if keys[pygame.K_LEFT] and self.rect.x > 0:
                   self.rect.x -= self.speed
                   self.image = self.images[0]
                   self.direccion = 1
                if keys[pygame.K_DOWN] and self.rect.y < 550:
                   self.rect.y += self.speed
                if keys[pygame.K_RIGHT] and self.rect.x < 950:
                   self.rect.x += self.speed
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
                    self.salto_presionado = True
            else:
                self.salto_presionado = False
                
        if self.esta_saltando:
            self.rect.y += self.velocidad_y
            self.velocidad_y += self.gravedad
            self.rect.x += self.velocidad_x_salto

            if self.rect.x < 0:
                self.rect.x = 0
            elif self.rect.x > 950:
                self.rect.x = 950
            
            if self.rect.y >= self.y_inicial:
                self.rect.y = self.y_inicial
                self.esta_saltando = False
                self.velocidad_y = 0
                self.velocidad_x_salto = 0 
    
izq = Player("ranaverde.png", 50, 50, 300, 559, 1, SALTO_VERDE, SALTO_VERDE_IZQ)
der = Player("morada.png", 45, 40, 300, 565, 1, SALTO_MORADA, SALTO_MORADA_IZQ)
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
        font = pygame.font.SysFont("Arial", 36)
        text = font.render("Presiona ESPACIO para jugar", True, (255, 255, 255))
        img = pygame.image.load("historia.jpg")
        window.blit(img, (0, 0))
        window.blit(text, (250, 500))
        if keys[pygame.K_SPACE]:
            play = True 

    if play:
        izq.draw()
        izq.update(keys)
        der.draw()
        der.update(keys)
    
    pygame.display.update()
    clock.tick(700)
                
            
            

