import pygame
import os  # using operating system for folders

WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))  # creates the window and sets dimensions

# creating pygame event loop, having something display on the screen, in loop its refreshing the window,
# checking the score checking for collision

BLUE = (13, 35, 131)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

BORDER = pygame.Rect(WIDTH//2 - 5, 0, 5, HEIGHT)

FPS = 60
VEL = 5
BULLET_VEL = 7
MAX_BULLETS = 3
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40

SPACE = pygame.image.load(os.path.join('Assets', 'space.png'))

YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

YELLOW_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join('Assets', 'spaceship_yellow.png'))  # you can use slashes instead but this method is universal
YELLOW_SPACESHIP_IMAGE = pygame.transform.rotate(pygame.transform.scale(
    YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)  # rotates 90 degrees and changes size


RED_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join('Assets', 'spaceship_red.png'))
RED_SPACESHIP_IMAGE = pygame.transform.rotate(pygame.transform.scale(
    RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 270)


def draw_window(red, yellow, red_bullets, yellow_bullets):
    WIN.blit(SPACE, (0, 0))
    pygame.draw.rect(WIN, BLACK, BORDER)
    WIN.blit(YELLOW_SPACESHIP_IMAGE, (yellow.x, yellow.y))  # use blit when you want to draw a surface onto the screen
    WIN.blit(RED_SPACESHIP_IMAGE, (red.x, red.y))

    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)

    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)

    pygame.display.update()


def yellow_handle_movement(keys_pressed, yellow):
    if keys_pressed[pygame.K_a] and yellow.x - VEL > 0:  # LEFT
        yellow.x -= VEL
    elif keys_pressed[pygame.K_d] and yellow.x + VEL + yellow.width < BORDER.x:  # RIGHT
        yellow.x += VEL
    elif keys_pressed[pygame.K_w] and yellow.y - VEL > 0:  # UP
        yellow.y -= VEL
    elif keys_pressed[pygame.K_s] and yellow.y + VEL + yellow.height < HEIGHT - 10:  # DOWN
        yellow.y += VEL


def red_handle_movement(keys_pressed, red):
    if keys_pressed[pygame.K_LEFT] and red.x - VEL > BORDER.x:  # LEFT
        red.x -= VEL
    elif keys_pressed[pygame.K_RIGHT] and red.x + VEL + red.width < WIDTH:  # RIGHT
        red.x += VEL
    elif keys_pressed[pygame.K_UP] and red.y - VEL > 0:  # UP
        red.y -= VEL
    elif keys_pressed[pygame.K_DOWN] and red.y + VEL + red.height < HEIGHT - 10:  # DOWN
        red.y += VEL


def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    for bullet in yellow_bullets:
        bullet.x += BULLET_VEL
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)

    for bullet in red_bullets:
        bullet.x -= BULLET_VEL
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x < 0:
            red_bullets.remove(bullet)


def main():
    red = pygame.Rect(700, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    yellow = pygame.Rect(100, 200, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)

    red_bullets = []
    yellow_bullets = []

    clock = pygame.time.Clock()  # initiating the clock speed
    # game loop, game will not instantly open than close
    run = True
    while run:
        clock.tick(FPS)  # controls the speed of the while loop
        for event in pygame.event.get():  # always do, checking for events occurring in pygame
            if event.type == pygame.QUIT:  # if X button is pressed run is = to False so quits the while loop/program
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(yellow_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(
                        yellow.x + yellow.width, yellow.y + yellow.height // 2 - 2, 10, 5)
                    yellow_bullets.append(bullet)

                if event.key == pygame.K_RCTRL and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(
                        red.x, red.y + red.height // 2 - 2, 10, 5)
                    red_bullets.append(bullet)

        keys_pressed = pygame.key.get_pressed()
        yellow_handle_movement(keys_pressed, yellow)
        red_handle_movement(keys_pressed, red)

        handle_bullets(yellow_bullets, red_bullets, yellow, red)

        draw_window(red, yellow, red_bullets, yellow_bullets)

    pygame.quit()


# making sure only this function is run when we run this file directly
# so if this file is imported from somewhere else and is called the game will not run
if __name__ == "__main__":
    main()
