import pygame
import os
pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("My First Game!")

HEALTH_FONT = pygame.font.SysFont('comicsans', 40)
WINNER_FONT = pygame.font.SysFont('comicsans', 100)

WHITE = (255, 255, 255)
FPS = 60
VEL = 3
BLACK = (0, 0, 0)
BORDER = pygame.Rect(WIDTH//2 - 5, 0, 10, HEIGHT)
BULLET_VEL = 7
SPACESHIP_WIDTH = 55
SPACESHIP_HEIGHT = 40
MAX_AMMO = 5
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

TALL_HIT = pygame.USEREVENT + 1
WIDE_HIT = pygame.USEREVENT + 2

BACKGROUND = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'space.png')), (WIDTH, HEIGHT))

TALL_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'tall_ship.png'))
TALL_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(TALL_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 270)

WIDE_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'wide_ship.png'))
WIDE_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(WIDE_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)

def draw_window(tall, wide, tall_ammo, wide_ammo, tall_hp, wide_hp):
    WIN.blit(BACKGROUND, (0, 0))
    pygame.draw.rect(WIN, BLACK, BORDER)

    tall_hp_text = HEALTH_FONT.render("Health: " + str(wide_hp), 1, WHITE)
    wide_hp_text = HEALTH_FONT.render("Health: " + str(tall_hp), 1, WHITE)
    WIN.blit(tall_hp_text, (WIDTH - tall_hp_text.get_width() - 10, 10))
    WIN.blit(wide_hp_text, (10, 10))

    WIN.blit(TALL_SPACESHIP, (tall.x, tall.y))
    WIN.blit(WIDE_SPACESHIP, (wide.x, wide.y))

    for bullet in tall_ammo:
        pygame.draw.rect(WIN, RED, bullet)

    for bullet in wide_ammo:
        pygame.draw.rect(WIN, YELLOW, bullet)

    pygame.display.update()

def tall_spaceship_movement(keys_pressed, tall):
    if keys_pressed[pygame.K_a] and tall.x - VEL > 0:  # left
        tall.x -= VEL
    if keys_pressed[pygame.K_d] and tall.x + VEL + tall.width < BORDER.x:  # right
        tall.x += VEL
    if keys_pressed[pygame.K_w] and tall.y - VEL > 0:  # up
        tall.y -= VEL
    if keys_pressed[pygame.K_s] and tall.y + VEL + tall.height < HEIGHT - 15:  # down
        tall.y += VEL

def wide_spaceship_movement(keys_pressed, wide):
    if keys_pressed[pygame.K_LEFT] and wide.x - VEL > BORDER.x + BORDER.width:  # left
        wide.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and wide.x + VEL + wide.width < WIDTH:  # right
        wide.x += VEL
    if keys_pressed[pygame.K_UP] and wide.y - VEL > 0:  # up
        wide.y -= VEL
    if keys_pressed[pygame.K_DOWN] and wide.y + VEL + wide.height < HEIGHT - 15:  # down
        wide.y += VEL

def handle_bullets(tall_ammo, wide_ammo, tall, wide):
    for bullet in tall_ammo:
        bullet.x += BULLET_VEL
        if wide.colliderect(bullet):
            pygame.event.post(pygame.event.Event(WIDE_HIT))
            tall_ammo.remove(bullet)
        elif bullet.x > WIDTH:
           tall_ammo.remove(bullet)

    for bullet in wide_ammo:
        bullet.x -= BULLET_VEL
        if tall.colliderect(bullet):
            pygame.event.post(pygame.event.Event(TALL_HIT))
            wide_ammo.remove(bullet)
        elif bullet.x < 0:
            wide_ammo.remove(bullet)

def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(draw_text, (WIDTH//2 - draw_text.get_width()/2, HEIGHT/2 - draw_text.get_height()/1))
    pygame.display.update()
    pygame.time.delay(5000)

def main():
    tall = pygame.Rect(100, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    wide = pygame.Rect(700, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)

    tall_ammo = []
    tall_hp = 10
    wide_ammo = []
    wide_hp = 10

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(tall_ammo) < MAX_AMMO:
                    bullet = pygame.Rect(tall.x + tall.width, tall.y + tall.height//2, 10, 5)
                    tall_ammo.append(bullet)
                if event.key == pygame.K_RCTRL and len(wide_ammo) < MAX_AMMO:
                    bullet = pygame.Rect(wide.x, wide.y + wide.height//2, 10, 5)
                    wide_ammo.append(bullet)

            if event.type == TALL_HIT:
                tall_hp -= 1

            if event.type == WIDE_HIT:
                wide_hp -= 1

        winner_text = ""
        if tall_hp <= 0:
            winner_text = "Wide Wins!"

        if wide_hp <= 0:
            winner_text = "Tall Wins!"

        if winner_text != "":
            draw_winner(winner_text)
            break

        keys_pressed = pygame.key.get_pressed()
        tall_spaceship_movement(keys_pressed, tall)
        wide_spaceship_movement(keys_pressed, wide)
        draw_window(tall, wide, tall_ammo, wide_ammo, tall_hp, wide_hp)

        handle_bullets(tall_ammo, wide_ammo, tall, wide)

    main()

if __name__ == "__main__":
    main()