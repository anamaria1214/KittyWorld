import pygame
import random

pygame.init()

# --- Configuración base ---
width, height = 800, 600
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Kitty World")

PINK = (255, 182, 193)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

font_title = pygame.font.SysFont("Comic Sans MS", 80)
font_button = pygame.font.SysFont("Comic Sans MS", 40)

window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Kitty World")

background_image = pygame.image.load("imagenes/fondohk.png")
player_image = pygame.image.load("imagenes/cohete.png")
bat_image = pygame.image.load("imagenes/murcielago.png")
laser_image = pygame.image.load("imagenes/laser.png")

background_image = pygame.transform.scale(background_image, (width, height))
player_image = pygame.transform.scale(player_image, (80, 60))
bat_image = pygame.transform.scale(bat_image, (60, 40))
laser_image = pygame.transform.scale(laser_image, (10, 30))

player_pos_x = width // 2
player_pos_y = height - 100
player_speed = 5
player_health = 40
score = 0
bat_speed = 2
bat_spawn_delay = 30
bat_spawn_timer = bat_spawn_delay

font = pygame.font.SysFont("Comic Sans MS", 40)

def show_menu():
    while True:
        window.blit(background_image, (0, 0))
        mouse_pos = pygame.mouse.get_pos()

        title_text = font_title.render("Kitty World", True, PINK)
        title_rect = title_text.get_rect(center=(width // 2, height // 2 - 80))
        window.blit(title_text, title_rect)

        play_text = font_button.render("Jugar", True, PINK)
        play_rect = play_text.get_rect(center=(width // 2, height // 2 + 20))
        window.blit(play_text, play_rect)

        quit_text = font_button.render("Salir", True, WHITE)
        quit_rect = quit_text.get_rect(center=(width // 2, height // 2 + 80))
        window.blit(quit_text, quit_rect)

        if play_rect.collidepoint(mouse_pos):
            pygame.draw.rect(window, WHITE, play_rect, 2)
        elif quit_rect.collidepoint(mouse_pos):
            pygame.draw.rect(window, WHITE, quit_rect, 2)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if play_rect.collidepoint(event.pos):
                    run_game() 
                    return
                elif quit_rect.collidepoint(event.pos):
                    pygame.quit()
                    quit()

def draw_instructions():
    overlay = pygame.Surface((width, height))
    overlay.set_alpha(200)
    window.blit(background_image, (0, 0))

    font_instr = pygame.font.SysFont("Comic Sans MS", 25)
    lines = [
        "¡Bienvenido a Kitty World!",
        "Usa la tecla a y d para mover el cohete",
        "Evita los obstáculos",
        "Usa la tecla w para disparar",
        "Haz clic en OK para comenzar"
    ]

    for i, line in enumerate(lines):
        text = font_instr.render(line, True, WHITE)
        rect = text.get_rect(center=(width // 2, height // 2 - 110 + i * 40))
        window.blit(text, rect)

    ok_font = pygame.font.SysFont("Comic Sans MS", 35)
    ok_text = ok_font.render("OK", True, PINK)
    ok_rect = ok_text.get_rect(center=(width // 2, height // 2 + 135))
    pygame.draw.rect(window, WHITE, ok_rect.inflate(20, 10), 2)
    window.blit(ok_text, ok_rect)

    return ok_rect

def run_game():
    global player_pos_x, player_health, score, bat_speed, bat_spawn_delay, bat_spawn_timer

    state = "instrucciones"

    player_health = 40
    score = 0
    bat_speed = 2
    bat_spawn_delay = 30
    bat_spawn_timer = bat_spawn_delay

    player_rect = player_image.get_rect(center=(player_pos_x, player_pos_y))
    laser_rect = laser_image.get_rect()
    bats = []

    clock = pygame.time.Clock()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if state == "instrucciones" and ok_rect.collidepoint(event.pos):
                    state = "jugando"

        if state == "instrucciones":
            window.blit(background_image, (0, 0))
            ok_rect = draw_instructions()
            pygame.display.flip()
            clock.tick(60)
            continue  

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and player_pos_x > 0:
            player_pos_x -= player_speed
        if keys[pygame.K_d] and player_pos_x < width - player_rect.width:
            player_pos_x += player_speed
        if keys[pygame.K_w]:
            laser_rect.midbottom = (player_pos_x + player_rect.width // 2, player_pos_y)
            shoot_laser(laser_rect)

        window.blit(background_image, (0, 0))
        player_rect.center = (player_pos_x, player_pos_y)
        window.blit(player_image, player_rect)

        for bat in bats[:]:
            bat.move()
            bat.draw()

            if bat.rect.colliderect(player_rect):
                player_health -= 3
                bats.remove(bat)

        for laser in lasers[:]:
            laser.move()
            laser.draw()

            for bat in bats[:]:
                if laser.rect.colliderect(bat.rect):
                    score += 2
                    bats.remove(bat)
                    lasers.remove(laser)
                    break

        bat_spawn_timer -= 1
        if bat_spawn_timer == 0:
            bat_spawn_timer = bat_spawn_delay
            bats.append(Bat())

        score_text = font.render("Puntaje: " + str(score), True, PINK)
        score_text_rect = score_text.get_rect(topright=(width - 10, 10))
        window.blit(score_text, score_text_rect)

        health_text = font.render("Vida: " + str(player_health), True, PINK)
        health_text_rect = health_text.get_rect(topleft=(10, 10))
        window.blit(health_text, health_text_rect)

        # --- Verificar fin del juego ---
        if player_health <= 0:
            show_game_over()

        pygame.display.flip()
        clock.tick(60)

def shoot_laser(laser_rect):
    lasers.append(Laser(laser_rect))

class Bat:
    def __init__(self):
        self.image = bat_image
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, width - self.rect.width)
        self.rect.y = random.randint(-200, -40)

    def move(self):
        self.rect.y += bat_speed

        if self.rect.y > height:
            self.rect.x = random.randint(0, width - self.rect.width)
            self.rect.y = random.randint(-200, -40)

    def draw(self):
        window.blit(self.image, self.rect)

class Laser:
    def __init__(self, rect):
        self.image = laser_image
        self.rect = rect

    def move(self):
        self.rect.y -= 10

    def draw(self):
        window.blit(self.image, self.rect)

def show_game_over():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        window.blit(background_image, (0, 0))

        game_over_text = font.render("Perdiste!!", True, PINK)
        game_over_text_rect = game_over_text.get_rect(center=(width // 2, height // 2 - 100))
        window.blit(game_over_text, game_over_text_rect)

        continue_text = font.render("Sigue intentando. Lo hiciste Genial!!", True, PINK)
        continue_text_rect = continue_text.get_rect(center=(width // 2, height // 2 - 50))
        window.blit(continue_text, continue_text_rect)

        score_text = font.render("Puntaje: " + str(score), True, PINK)
        score_text_rect = score_text.get_rect(center=(width // 2, height // 2 ))
        window.blit(score_text, score_text_rect)

        restart_text = font.render("Reiniciar", True, WHITE)
        restart_text_rect = restart_text.get_rect(center=(width // 2, height // 2 + 50))
        window.blit(restart_text, restart_text_rect)

        quit_text = font.render("Salir", True, WHITE)
        quit_text_rect = quit_text.get_rect(center=(width // 2, height // 2 + 100))
        window.blit(quit_text, quit_text_rect)

        mouse_pos = pygame.mouse.get_pos()

        if restart_text_rect.collidepoint(mouse_pos):
            pygame.draw.rect(window, WHITE, restart_text_rect, 2)
            if pygame.mouse.get_pressed()[0]:
                run_game()
        elif quit_text_rect.collidepoint(mouse_pos):
            pygame.draw.rect(window, WHITE, quit_text_rect, 2)
            if pygame.mouse.get_pressed()[0]:
                pygame.quit()
                quit()

        pygame.display.flip()

lasers = []

show_menu()