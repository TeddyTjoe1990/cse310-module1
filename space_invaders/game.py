import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Create screen
screen = pygame.display.set_mode((800, 600))

# Title and Icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load("assets/spaceship.png")
pygame.display.set_icon(icon)

# Background music
pygame.mixer.music.load("assets/background.mp3")
pygame.mixer.music.play(-1)  # Loop music forever

# Player
player_img = pygame.image.load("assets/player.png")
player_x = 370
player_y = 480
player_x_change = 0

# Enemy
enemy_img = []
enemy_x = []
enemy_y = []
enemy_x_change = []
enemy_y_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemy_img.append(pygame.image.load("assets/enemy.png"))
    enemy_x.append(random.randint(0, 736))
    enemy_y.append(random.randint(50, 150))
    enemy_x_change.append(2)
    enemy_y_change.append(40)

# Bullet
bullet_img = pygame.image.load("assets/bullet.png")
bullet_x = 0
bullet_y = 480
bullet_y_change = 10
bullet_state = "ready"  # "ready" = you can't see the bullet, "fire" = bullet is moving

# Score
score_value = 0
font = pygame.font.Font(None, 32)
text_x = 10
text_y = 10

# Game Over font
over_font = pygame.font.Font(None, 64)

# Sounds
bullet_sound = pygame.mixer.Sound("assets/laser.wav")
explosion_sound = pygame.mixer.Sound("assets/explosion.wav")

def show_score(x, y):
    score = font.render(f"Score : {score_value}", True, (255, 255, 255))
    screen.blit(score, (x, y))

def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 0, 0))
    screen.blit(over_text, (250, 250))

def player(x, y):
    screen.blit(player_img, (x, y))

def enemy(x, y, i):
    screen.blit(enemy_img[i], (x, y))

def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bullet_img, (x + 16, y + 10))

def is_collision(enemy_x, enemy_y, bullet_x, bullet_y):
    distance = math.sqrt((enemy_x - bullet_x) ** 2 + (enemy_y - bullet_y) ** 2)
    return distance < 27

def main_menu():
    menu_font = pygame.font.Font(None, 48)
    title_text = menu_font.render("Press ENTER to Play", True, (255, 255, 255))
    screen.fill((0, 0, 0))
    screen.blit(title_text, (250, 300))
    pygame.display.update()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    waiting = False

# Main loop
main_menu()

running = True
while running:
    screen.fill((0, 0, 0))  # Black background
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Keystroke check (left/right and space)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_x_change = -5
            if event.key == pygame.K_RIGHT:
                player_x_change = 5
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_sound.play()
                    bullet_x = player_x
                    fire_bullet(bullet_x, bullet_y)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player_x_change = 0

    # Player movement
    player_x += player_x_change
    if player_x <= 0:
        player_x = 0
    elif player_x >= 736:
        player_x = 736

    # Enemy movement
    for i in range(num_of_enemies):

        # Game Over condition
        if enemy_y[i] > 440:
            for j in range(num_of_enemies):
                enemy_y[j] = 2000  # Move enemies off screen
            game_over_text()
            pygame.display.update()
            pygame.time.wait(3000)
            main_menu()
            # Reset game state
            player_x = 370
            score_value = 0
            bullet_y = 480
            bullet_state = "ready"
            for j in range(num_of_enemies):
                enemy_x[j] = random.randint(0, 736)
                enemy_y[j] = random.randint(50, 150)
            break

        enemy_x[i] += enemy_x_change[i]
        if enemy_x[i] <= 0:
            enemy_x_change[i] = abs(enemy_x_change[i])
            enemy_y[i] += enemy_y_change[i]
        elif enemy_x[i] >= 736:
            enemy_x_change[i] = -abs(enemy_x_change[i])
            enemy_y[i] += enemy_y_change[i]

        # Collision detection
        if is_collision(enemy_x[i], enemy_y[i], bullet_x, bullet_y):
            explosion_sound.play()
            bullet_y = 480
            bullet_state = "ready"
            score_value += 1
            enemy_x[i] = random.randint(0, 736)
            enemy_y[i] = random.randint(50, 150)

            # Increase difficulty every 10 points
            if score_value % 10 == 0:
                for k in range(num_of_enemies):
                    enemy_x_change[k] = 2 + (score_value // 10)

        enemy(enemy_x[i], enemy_y[i], i)

    # Bullet movement
    if bullet_state == "fire":
        fire_bullet(bullet_x, bullet_y)
        bullet_y -= bullet_y_change
    if bullet_y <= 0:
        bullet_y = 480
        bullet_state = "ready"

    player(player_x, player_y)
    show_score(text_x, text_y)

    pygame.display.update()
