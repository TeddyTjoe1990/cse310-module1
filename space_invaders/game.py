import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Create screen
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

# Title and Icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load("assets/spaceship.png")
pygame.display.set_icon(icon)

# Background music
pygame.mixer.music.load("assets/background.mp3")
pygame.mixer.music.play(-1)

# Resize helper
def load_and_scale(path, size):
    return pygame.transform.scale(pygame.image.load(path), size)

# Player
player_img = load_and_scale("assets/player.png", (48, 48))
player_x = 370
player_y = 480
player_x_change = 0

# Bullet (player)
bullet_img = load_and_scale("assets/bullet.png", (12, 24))
bullet_x = 0
bullet_y = 480
bullet_y_change = 10
bullet_state = "ready"
last_bullet_time = 0
bullet_delay = 250  # milliseconds

# Enemy bullet (enemy laser) 
enemy_bullet_img = load_and_scale("assets/enemy_laser.png", (8, 20))
enemy_bullets = []
enemy_bullet_y_change = 1  # enemy bullets are slower than 3 to 1
enemy_bullet_delay = 2000  # delay between enemy shots becomes 2000 ms (2 seconds)
last_enemy_shot_time = 0

# Score and Level
score_value = 0
level = 1
level_threshold = 10  # Score needed to level up
last_level_up_score = 0
font = pygame.font.Font(None, 32)
text_x = 10
text_y = 10

# Game Over font
over_font = pygame.font.Font(None, 64)

# Sounds
bullet_sound = pygame.mixer.Sound("assets/laser.wav")
explosion_sound = pygame.mixer.Sound("assets/explosion.wav")
enemy_shoot_sound = pygame.mixer.Sound("assets/enemy_shoot.mp3")

# Pause
paused = False

def draw_pause():
    pause_font = pygame.font.Font(None, 72)
    text = pause_font.render("PAUSED", True, (255, 255, 255))
    text_rect = text.get_rect(center=(screen_width // 2, screen_height // 2 - 40))
    screen.blit(text, text_rect)

    sub_font = pygame.font.Font(None, 36)
    sub_text = sub_font.render("Press P to Resume", True, (255, 255, 255))
    sub_rect = sub_text.get_rect(center=(screen_width // 2, screen_height // 2 + 20))
    screen.blit(sub_text, sub_rect)

# Lives
life_img = load_and_scale("assets/heart.png", (32, 32))
lives = 3

# Enemies
enemy_img = load_and_scale("assets/enemy.png", (40, 40))
fast_enemy_img = load_and_scale("assets/enemy2.png", (40, 40))
tank_enemy_img = load_and_scale("assets/enemy3.png", (60, 60))

enemies = []
for _ in range(6):
    enemies.append({"type": "normal", "img": enemy_img, "x": random.randint(0, 760), "y": random.randint(50, 150), "x_change": 0.5, "y_change": 30})

fast_enemies = []
tank_enemies = []

bullet_power = 1

def increase_difficulty():
    global level, bullet_power
    level += 1
    bullet_power += 1

def show_score(x, y):
    score = font.render(f"Score : {score_value}  Level : {level}", True, (255, 255, 255))
    screen.blit(score, (x, y))

def show_lives(lives):
    for i in range(lives):
        screen.blit(life_img, (10 + i*40, 50))

def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 0, 0))
    screen.blit(over_text, (250, 250))

def player(x, y):
    screen.blit(player_img, (x, y))

def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bullet_img, (x + 18, y))

def fire_enemy_bullet(x, y):
    screen.blit(enemy_bullet_img, (x + 16, y + 40))  # offset to bottom-center of enemy

def is_collision(x1, y1, x2, y2, threshold=27):
    distance = math.sqrt((x1 - x2)**2 + (y1 - y2)**2)
    return distance < threshold

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

main_menu()

running = True
while running:
    screen.fill((0, 0, 0))

    if paused:
        draw_pause()
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    paused = False
        continue

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_x_change = -3
            if event.key == pygame.K_RIGHT:
                player_x_change = 3
            if event.key == pygame.K_p:
                paused = True
        if event.type == pygame.KEYUP:
            if event.key in [pygame.K_LEFT, pygame.K_RIGHT]:
                player_x_change = 0

    keys = pygame.key.get_pressed()
    current_time = pygame.time.get_ticks()
    if keys[pygame.K_SPACE] and bullet_state == "ready" and (current_time - last_bullet_time > bullet_delay):
        bullet_sound.play()
        bullet_x = player_x
        fire_bullet(bullet_x, bullet_y)
        last_bullet_time = current_time

    player_x += player_x_change
    player_x = max(0, min(player_x, 752))

    # Normal enemies move and can shoot randomly (not too frequent)
    for enemy in enemies:
        enemy["x"] += enemy["x_change"]
        if enemy["x"] <= 0 or enemy["x"] >= 760:
            enemy["x_change"] *= -1
            enemy["y"] += enemy["y_change"]

        # Enemy shooting logic with slower bullet and longer delay
        if current_time - last_enemy_shot_time > enemy_bullet_delay:
            if random.random() < 0.002:  # peluang tembakan lebih kecil
                enemy_bullets.append({"x": enemy["x"], "y": enemy["y"] + 40, "y_change": enemy_bullet_y_change})
                enemy_shoot_sound.play()
                last_enemy_shot_time = current_time

        # Bullet collision with enemy
        if is_collision(enemy["x"], enemy["y"], bullet_x, bullet_y):
            explosion_sound.play()
            bullet_y = 480
            bullet_state = "ready"
            score_value += 1
            enemy["x"] = random.randint(0, 760)
            enemy["y"] = random.randint(50, 150)

        screen.blit(enemy["img"], (enemy["x"], enemy["y"]))

    # Fast enemies logic - no shooting
    if random.randint(0, 300) == 1:
        fast_enemies.append({"x": random.randint(0, 760), "y": 50, "x_change": 0.8})

    for fe in fast_enemies[:]:
        fe["x"] += fe["x_change"]
        if fe["x"] <= 0 or fe["x"] >= 760:
            fe["x_change"] *= -1
            fe["y"] += 30

        if is_collision(fe["x"], fe["y"], bullet_x, bullet_y):
            explosion_sound.play()
            score_value += 2
            bullet_y = 480
            bullet_state = "ready"
            fast_enemies.remove(fe)

        if is_collision(fe["x"], fe["y"], player_x, player_y):
            lives -= 1
            fast_enemies.remove(fe)

        screen.blit(fast_enemy_img, (fe["x"], fe["y"]))

    # Tank enemies logic - no shooting
    if random.randint(0, 800) == 1:
        tank_enemies.append({"x": random.randint(0, 740), "y": 50, "x_change": 0.2, "health": 3})

    for te in tank_enemies[:]:
        te["x"] += te["x_change"]
        if te["x"] <= 0 or te["x"] >= 740:
            te["x_change"] *= -1
            te["y"] += 20

        if is_collision(te["x"], te["y"], bullet_x, bullet_y):
            te["health"] -= bullet_power
            bullet_y = 480
            bullet_state = "ready"
            if te["health"] <= 0:
                explosion_sound.play()
                score_value += 3
                tank_enemies.remove(te)

        if is_collision(te["x"], te["y"], player_x, player_y):
            lives -= 1
            tank_enemies.remove(te)

        screen.blit(tank_enemy_img, (te["x"], te["y"]))

    # Player bullet movement
    if bullet_state == "fire":
        fire_bullet(bullet_x, bullet_y)
        bullet_y -= bullet_y_change
    if bullet_y <= 0:
        bullet_y = 480
        bullet_state = "ready"

    # Enemy bullets movement and collision with player
    for eb in enemy_bullets[:]:
        eb["y"] += eb["y_change"]
        fire_enemy_bullet(eb["x"], eb["y"])
        if eb["y"] > screen_height:
            enemy_bullets.remove(eb)
        elif is_collision(eb["x"], eb["y"], player_x, player_y, threshold=30):
            lives -= 1
            enemy_bullets.remove(eb)

    # Level up logic
    if score_value - last_level_up_score >= level_threshold:
        last_level_up_score = score_value
        increase_difficulty()

    player(player_x, player_y)
    show_score(text_x, text_y)
    show_lives(lives)

    if lives <= 0:
        game_over_text()
        pygame.display.update()
        pygame.time.wait(3000)
        main_menu()
        player_x = 370
        score_value = 0
        bullet_y = 480
        bullet_state = "ready"
        level = 1
        bullet_power = 1
        lives = 3
        enemies.clear()
        fast_enemies.clear()
        tank_enemies.clear()
        enemy_bullets.clear()
        for _ in range(6):
            enemies.append({"type": "normal", "img": enemy_img, "x": random.randint(0, 760), "y": random.randint(50, 150), "x_change": 0.5, "y_change": 30})

    pygame.display.update()
