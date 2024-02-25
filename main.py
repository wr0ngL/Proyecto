import pygame
import menu
import random
import sys

pygame.init()

clock = pygame.time.Clock()
fps = 60

# Pantalla
bottom_panel = 150
screen_width = 800
screen_height = 486 + bottom_panel

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Combate')

# Variables del juego
current_fighter = 1
total_fighters = 2
action_cooldown = 0
action_wait_time = 90
attack = False
potion = False
clicked = False
game_over = False  # Variable para controlar el estado del juego

# Imágenes
# Fondo
background_img = pygame.image.load('img/Background/Campo.jpg').convert_alpha()


def draw_bg():
    screen.blit(background_img, (0, 0))


# Panel
panel_img = pygame.image.load('img/Panel/panelaco.png').convert_alpha()

# Cursor ataque
espada_img = pygame.image.load('img/Icons/espada.png').convert_alpha()

# Pocion
potion_img = pygame.image.load('img/Icons/pocion.png').convert_alpha()

# Imagen de "You Win"
you_win_img = pygame.image.load('img/Victoria/victoria.png').convert_alpha()
you_win_rect = you_win_img.get_rect(center=(screen_width // 2, screen_height // 2))

# Cargar música
pygame.mixer.music.load('music/Songs/music.mp3')
pygame.mixer.music.play(-1)

def draw_panel():
    screen.blit(panel_img, (0, screen_height - bottom_panel))
    # Mostrar la HP del guerrero
    draw_text(f'{warrior.name} HP: {warrior.hp}', font, black, 100, screen_height - bottom_panel + 10)
    # Mostrar la HP del goblin
    if goblin.hp > 0:
        draw_text(f'{goblin.name} HP: {goblin.hp}', font, black, 550, screen_height - bottom_panel + 10)
    else:
        draw_text(f'{goblin.name} HP: 0', font, black, 550, screen_height - bottom_panel + 10)


# Definir fuentes
font = pygame.font.SysFont('Times New Roman', 26)
red = (255, 0, 0)
green = (0, 255, 0)
black = (0, 0, 0)


# Función texto
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


# Clases de personajes

# Warrior
class Warrior():
    def __init__(self, x, y, name, strength, potions, max_hp):
        self.name = name
        self.strength = strength
        self.initial_potions = potions
        self.potions = potions
        self.max_hp = max_hp
        self.hp = max_hp
        self.alive = True
        self.animation_list = []
        self.frame_index = 0
        self.action = 0  # 0: Depie, 1: Ataque, 2: Muerte
        self.update_time = pygame.time.get_ticks()
        # Imagenes de pie
        temp_list = []
        for i in range(4):
            img = pygame.image.load(f'img/Characters/Warrior/Depie/{i}.png')
            img = pygame.transform.scale(img, (img.get_width() * 1.2, img.get_height() * 1.2))
            temp_list.append(img)
        self.animation_list.append(temp_list)
        # Imagenes ataque
        temp_list = []
        for i in range(4):
            img = pygame.image.load(f'img/Characters/Warrior/Ataque/{i}.png')
            img = pygame.transform.scale(img, (img.get_width() * 1.2, img.get_height() * 1.2))
            temp_list.append(img)
        self.animation_list.append(temp_list)
        # Imagenes muerte
        temp_list = []
        for i in range(4):
            img = pygame.image.load(f'img/Characters/Warrior/Muerte/{i}.png')
            img = pygame.transform.scale(img, (img.get_width() * 1.2, img.get_height() * 1.2))
            temp_list.append(img)
        self.animation_list.append(temp_list)
        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self):
        animation_cooldown = 175
        self.image = self.animation_list[self.action][self.frame_index]
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        if self.frame_index >= len(self.animation_list[self.action]):
            self.Depie()

    def Depie(self):
        #Variables animación Depie
        self.action = 0
        self.frame_index = 0
        self.update_time = 0


    def attack(self, target):
        #Daño a enemigo
        rand = random.randint(-2, 5)
        damage = self.strength + rand
        target.hp -= damage
        #El objetivo esta muerto?
        if target.hp < 1:
            target.hp = 0
            target.alive = False
        #Variables animacion ataque
        self.action = 1
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

    def draw(self):
        screen.blit(self.image, self.rect)


# Goblin
class Goblin():
    def __init__(self, x, y, name, strength, potions, max_hp):
        self.name = name
        self.strength = strength
        self.initial_potions = potions
        self.potions = potions
        self.max_hp = max_hp
        self.hp = max_hp
        self.alive = True
        self.animation_list = []
        self.frame_index = 0
        self.action = 0  # 0: Depie, 1: Ataque, 2: Muerte
        self.update_time = pygame.time.get_ticks()
        # Imagenes de pie
        temp_list = []
        for i in range(3):
            img = pygame.image.load(f'img/Characters/Goblin/Depie/{i}.png')
            img = pygame.transform.scale(img, (img.get_width() * 1.2, img.get_height() * 1.2))
            temp_list.append(img)
        self.animation_list.append(temp_list)
        # Imagenes ataque
        temp_list = []
        for i in range(3):
            img = pygame.image.load(f'img/Characters/Goblin/Ataque/{i}.png')
            img = pygame.transform.scale(img, (img.get_width() * 1.2, img.get_height() * 1.2))
            temp_list.append(img)
        self.animation_list.append(temp_list)
        # Imagenes muerte
        temp_list = []
        for i in range(3):
            img = pygame.image.load(f'img/Characters/Goblin/Muerte/{i}.png')
            img = pygame.transform.scale(img, (img.get_width() * 1.2, img.get_height() * 1.2))
            temp_list.append(img)
        self.animation_list.append(temp_list)
        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self):
        animation_cooldown = 175
        self.image = self.animation_list[self.action][self.frame_index]
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        if self.frame_index >= len(self.animation_list[self.action]):
            self.Depie()

    def Depie(self):
        #Variables animación Depie
        self.action = 0
        self.frame_index = 0
        self.update_time = 0


    def attack(self, target):
        #Daño a enemigo
        rand = random.randint(-3, 1)
        damage = self.strength + rand
        target.hp -= damage
        #Variables animacion ataque
        self.action = 1
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
    def draw(self):
        screen.blit(self.image, self.rect)


# Boss
class Boss():
    def __init__(self, x, y, name, strength, potions, max_hp):
        self.name = name
        self.strength = strength
        self.initial_potions = potions
        self.potions = potions
        self.max_hp = max_hp
        self.hp = max_hp
        self.alive = True
        self.animation_list = []
        self.frame_index = 0
        self.action = 0  # 0: Depie, 1: Ataque, 2: Muerte
        self.update_time = pygame.time.get_ticks()
        # Imagenes de pie
        temp_list = []
        for i in range(4):
            img = pygame.image.load(f'img/Characters/Boss/Depie/{i}.png')
            img = pygame.transform.scale(img, (img.get_width() * 1.2, img.get_height() * 1.2))
            temp_list.append(img)
        self.animation_list.append(temp_list)
        # Imagenes ataque
        temp_list = []
        for i in range(4):
            img = pygame.image.load(f'img/Characters/Boss/Ataque/{i}.png')
            img = pygame.transform.scale(img, (img.get_width() * 1.2, img.get_height() * 1.2))
            temp_list.append(img)
        self.animation_list.append(temp_list)
        # Imagenes muerte
        temp_list = []
        for i in range(4):
            img = pygame.image.load(f'img/Characters/Boss/Muerte/{i}.png')
            img = pygame.transform.scale(img, (img.get_width() * 1.2, img.get_height() * 1.2))
            temp_list.append(img)
        self.animation_list.append(temp_list)
        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self):
        animation_cooldown = 250
        self.image = self.animation_list[self.action][self.frame_index]
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        if self.frame_index >= len(self.animation_list[self.action]):
            self.frame_index = 0


warrior = Warrior(150, 383, 'Warrior', 50, 3, 50)
goblin = Goblin(630, 410, 'Goblin', 10, 0, 300)
boss = Boss(150, 390, 'Boss', 30, 0, 150)

run = True
while run:
    clock.tick(fps)
    draw_bg()
    draw_panel()
    warrior.update()
    warrior.draw()
    goblin.update()
    goblin.draw()

    # Acciones control jugador
    # Variables accion reset
    attack = False
    potion = False
    target = None

    # Acciones del jugador
    if warrior.alive and current_fighter == 1:
        action_cooldown += 1
        if action_cooldown >= action_wait_time:
            if attack:
                warrior.attack(goblin)
                current_fighter = 2  # Cambiar al turno del Goblin
                action_cooldown = 0

    # Acciones del Goblin
    elif goblin.alive and current_fighter == 2:
        action_cooldown += 1
        if action_cooldown >= action_wait_time:
            goblin.attack(warrior)
            current_fighter = 1  # Cambiar al turno del Warrior
            action_cooldown = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Si se hace clic, establecer el ataque en True
            attack = True
            pos = pygame.mouse.get_pos()
            # Si se hace clic en el área del goblin, ataque
            if goblin.rect.collidepoint(pos):
                warrior.attack(goblin)
                current_fighter = 2  # Cambiar al turno del Goblin
        else:
            # Si no se hace clic, el ataque es False
            attack = False

    # Detección de colisión y visualización del cursor de la espada
    pos = pygame.mouse.get_pos()
    if goblin.rect.collidepoint(pos):
        pygame.mouse.set_visible(False)
        screen.blit(espada_img, pos)
    else:
        pygame.mouse.set_visible(True)

    # Verificar si el goblin está muerto para mostrar "You Win"
    if not goblin.alive:
        screen.blit(you_win_img, you_win_rect)
        pygame.display.update()
        pygame.time.delay(2000)  # Retraso de 2 segundos
        run = False

    pygame.display.update()

pygame.quit()