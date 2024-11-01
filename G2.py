import pygame
import random
import sys

# Inicializar Pygame
pygame.init()

# Configuración de pantalla
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Shooter")

#Fondo
bg_img= pygame.image.load("assets/bg.png")
bg_img=pygame.transform.scale(bg_img, (800,int(WIDTH*0.8)))
# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Jugador
class Player:
    def __init__(self):
        self.image = pygame.image.load("assets/player.png")
        self.image = pygame.transform.scale(self.image, (80, 80))
        self.rect = self.image.get_rect(center=(WIDTH // 2, HEIGHT - 50))
        self.speed = 5
        self.lives = 3
        self.score = 0
        self.triple_shot = False  # Estado del power-up de triple disparo
        self.triple_shot_timer = 0  # Duración del power-up

    def move(self, keys):
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.x += self.speed

    def draw(self):
        screen.blit(self.image, self.rect)

    def shoot(self):
        if self.triple_shot:
            bullets.append(Bullet(self.rect.centerx - 20, self.rect.top))
            bullets.append(Bullet(self.rect.centerx, self.rect.top))
            bullets.append(Bullet(self.rect.centerx + 20, self.rect.top))
        else:
            bullets.append(Bullet(self.rect.centerx, self.rect.top))

# Enemigo
class Enemy:
    def __init__(self, enemies):
        self.image = pygame.image.load("assets/enemy.png")
        self.image = pygame.transform.scale(self.image, (50, 50))
        while True:
            self.rect = self.image.get_rect(center=(random.randint(50, WIDTH - 50), -50))
            if not any(self.rect.colliderect(e.rect) for e in enemies):
                break
        self.speed = random.randint(1, 2)

    def move(self):
        self.rect.y += self.speed

    def draw(self):
        screen.blit(self.image, self.rect)

# Bala
class Bullet:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 5, 10)
        self.speed = 10

    def move(self):
        self.rect.y -= self.speed

    def draw(self):
        pygame.draw.rect(screen, WHITE, self.rect)

# Power-up
class PowerUp:
    def __init__(self):
        self.image = pygame.image.load("assets/powerup.png")
        self.image = pygame.transform.scale(self.image, (30, 30))
        self.rect = self.image.get_rect(center=(random.randint(50, WIDTH - 50), -50))
        self.speed = 3

    def move(self):
        self.rect.y += self.speed

    def draw(self):
        screen.blit(self.image, self.rect)

# Funciones principales
def main_menu():
    font = pygame.font.Font(None, 74)
    text = font.render("Space Shooter", True, WHITE)
    text2 = font.render("Presiona Enter para comenzar", True, WHITE)
    #Dibujado
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height()))
    #Texto abajo
    screen.blit(text2, (WIDTH // 2 - text2.get_width() // 2, HEIGHT // 2 + 30))
    pygame.display.flip()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    waiting = False

def game():
    player = Player()
    enemies = []
    powerups = []
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 36)

    global bullets
    bullets = []
    powerup_spawn_time = 0

    running = True
    while running:
        screen.fill(BLACK)
        #Dibujar el fondo
        screen.blit(bg_img, (0,0))
        #Manejo de teclas 
        keys = pygame.key.get_pressed()

        # Eventos de salida
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.shoot()

        # Movimiento y dibujado del jugador
        player.move(keys)
        player.draw()

        # Generar enemigos
        if random.randint(1, 30) == 1:
            enemies.append(Enemy(enemies))

        # Generar power-up
        if pygame.time.get_ticks() - powerup_spawn_time > 5000:  # cada 5 segundos
            powerups.append(PowerUp())
            powerup_spawn_time = pygame.time.get_ticks()

        # Movimiento y dibujado de enemigos
        for enemy in enemies[:]:
            enemy.move()
            enemy.draw()
            if enemy.rect.top > HEIGHT:
                enemies.remove(enemy)
                player.lives -= 1
                if player.lives <= 0:
                    game_over(player.score)

        # Movimiento y dibujado de balas
        for bullet in bullets[:]:
            bullet.move()
            bullet.draw()
            if bullet.rect.bottom < 0:
                bullets.remove(bullet)

        # Movimiento y dibujado de power-ups
        for powerup in powerups[:]:
            powerup.move()
            powerup.draw()
            if powerup.rect.top > HEIGHT:
                powerups.remove(powerup)
            elif powerup.rect.colliderect(player.rect):
                powerups.remove(powerup)
                player.triple_shot = True
                player.triple_shot_timer = pygame.time.get_ticks()

        # Colisiones
        for enemy in enemies[:]:
            for bullet in bullets[:]:
                if bullet.rect.colliderect(enemy.rect):
                    bullets.remove(bullet)
                    enemies.remove(enemy)
                    player.score += 10
                    break
            if player.rect.colliderect(enemy.rect):
                enemies.remove(enemy)
                player.lives -= 1
                if player.lives <= 0:
                    game_over(player.score)

        # Desactivar triple disparo después de un tiempo
        if player.triple_shot and pygame.time.get_ticks() - player.triple_shot_timer > 5000:  # dura 5 segundos
            player.triple_shot = False

        # Mostrar puntaje y vidas
        score_text = font.render(f"Puntaje: {player.score}", True, WHITE)
        lives_text = font.render(f"Vidas: {player.lives}", True, RED)
        
        #Dibujado
        screen.blit(score_text, (10, 10))
        screen.blit(lives_text, (WIDTH - 100, 10))

        # Actualizar pantalla y limitar FPS
        pygame.display.flip()
        clock.tick(60)

def game_over(score):
    font = pygame.font.Font(None, 74)
    small_font = pygame.font.Font(None, 36)
    screen.fill(BLACK)
    
    #Definición de los textos
    text = font.render("Game Over", True, WHITE)
    score_text = small_font.render(f"Puntaje: {score}", True, WHITE)
    restart_text = small_font.render("Presiona R para reiniciart", True, WHITE)
    
    #Dibujo de los textos
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - 50))
    screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2 + 20))
    screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 60))
    
    pygame.display.flip()
    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    waiting = False
                    game()

main_menu()
game()
pygame.quit()
