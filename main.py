import pygame
import random
import time

# Initialize Pygame
pygame.init()

# Define screen dimensions
screen_width = 800
screen_height = 600

# Create a Pygame window
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Coordinate Plane")
background_image = pygame.image.load('background2.bmp').convert_alpha()

font = pygame.font.Font(None, 36)
text_color = (0, 0, 0)
box_color = (255, 255, 255)

# Initialize text input and position
user_text = ""
text_x = 370
text_y = 560

# Define the dimensions of the coordinate plane
coord_plane_width = 600
coord_plane_height = 400

# Define the origin (center) of the coordinate plane
origin_x = screen_width // 2
origin_y = screen_height // 2

# Define the scale (pixels per unit) of the coordinate plane
scale = 20

# Define gridline colors
gridline_color = (50, 50, 50)

# Define labels for the axes
x_label = "X-axis"
y_label = "Y-axis"

# Create a font for the labels
font = pygame.font.Font(None, 36)

coordinates = []

score = 0
life = 3


class Missile(pygame.sprite.Sprite):
    def __init__(self, start_x, start_y, target_x, target_y):
        super().__init__()
        self.image = pygame.image.load('missile1.png').convert_alpha()
        self.mask = pygame.mask.from_surface(self.image)  # Create the mask based on the image
        self.rect = self.image.get_rect()
        self.rect.center = (start_x, start_y)
        self.target_x = target_x
        self.target_y = target_y + 30
        self.speed = 2
        self.finished = False  # Flag to check if the missile is finished

    def update(self):
        if not self.finished:
            direction_x = self.target_x - self.rect.centerx
            direction_y = self.target_y - self.rect.centery
            distance = ((direction_x) ** 2 + (direction_y) ** 2) ** 0.5
            new_missile_x = (target_x - origin_x) // scale
            new_missile_y = (origin_y - target_y) // scale

            if distance != 0:
                self.rect.x += (direction_x / distance) * self.speed
                self.rect.y += (direction_y / distance) * self.speed

                asteroid_x = (asteroid.rect.x - origin_x) // scale
                asteroid_y = (origin_y - asteroid.rect.y) // scale
                asteroid_x = asteroid_x + 1

                if self.rect.colliderect(asteroid.rect) and asteroid_y == new_missile_y and asteroid_x == new_missile_x:
                    explosion = Explosion(self.target_x, self.target_y - 20)
                    explosion_group.add(explosion)

                    missile_group.remove(self)
                    asteroid.reset_position()
                    global score
                    score = score + 10
                    print(f"score = {score}")
        if self.rect.x == target_x - 7 and self.rect.y == target_y:
            explosion = Explosion(self.target_x, self.target_y - 20)
            explosion_group.add(explosion)

            missile_group.remove(self)
            global life
            life = life - 1
            print(f"life = {life}")


class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.images = [pygame.image.load(f'explosion1.png').convert_alpha() for i in range(1, 10)]
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.frame = 0
        self.animation_speed = 5  # Adjust the speed of the explosion animation
        self.duration = 1000  # Adjust the duration of the explosion in milliseconds
        self.start_time = pygame.time.get_ticks()  # Record the start time

    def update(self):
        self.frame += 1
        if self.frame // self.animation_speed < len(self.images):
            self.image = self.images[self.frame // self.animation_speed]
        else:
            current_time = pygame.time.get_ticks()
            if current_time - self.start_time > self.duration:
                explosion_group.remove(self)  # Remove the explosion sprite when the animation is complete


class Asteroid(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('asteroid1.png').convert_alpha()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.reset_position()

    def reset_position(self):
        self.rect.x = random.randint(160, screen_width - 160)
        self.rect.y = random.randint(100, screen_height - 100)

        x_cartesian = (self.rect.x - origin_x) // scale
        y_cartesian = (origin_y - self.rect.y) // scale

        x_cartesian = max(-int(coord_plane_width / (2 * scale)), min(int(coord_plane_width / (2 * scale)), x_cartesian))
        y_cartesian = max(-int(coord_plane_height / (2 * scale)),
                          min(int(coord_plane_height / (2 * scale)), y_cartesian))

        self.rect.x = origin_x - 15 + x_cartesian * scale
        self.rect.y = origin_y - 12 - y_cartesian * scale

        print(f"Asteroid Cartesian Coordinates: ({x_cartesian}, {y_cartesian})")

    def update(self):
        pass  # Add any asteroid-specific update logic if needed


class EarthDestroyed(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('EarthDestroyed.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (screen_width // 2, screen_height // 2)


earth_destroyed_group = pygame.sprite.Group()
missile_group = pygame.sprite.Group()
explosion_group = pygame.sprite.Group()
asteroid_group = pygame.sprite.Group()




def reset_game_state():
    global missile, asteroid
    missile = None
    asteroid.reset_position()

def reset_game():
    global life, score
    life = 3
    score = 0
    reset_game_state()


def show_game_over():
    game_over_font = pygame.font.SysFont('times new roman', 50)

    # Render "Game Over" text
    game_over_text = game_over_font.render('Game Over...', True, (0, 0, 255))
    game_over_text_rect = game_over_text.get_rect(
        center=(screen_width // 2, screen_height // 2 - game_over_text.get_height()))

    # Render "You failed to save the Earth" text
    fail_text = game_over_font.render('You Failed to Save the Earth!!', True, (0, 0, 255))
    fail_text_rect = fail_text.get_rect(center=(screen_width // 2, screen_height // 2 + fail_text.get_height()))

    # Display both lines
    screen.blit(game_over_text, game_over_text_rect)
    screen.blit(fail_text, fail_text_rect)

    pygame.display.flip()

def show_earth_destroyed():
    earth_destroyed_group.update()
    earth_destroyed_group.draw(screen)
    pygame.display.flip()


def wait_for_restart():
    waiting_for_restart = True
    while waiting_for_restart:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    waiting_for_restart = False
                    reset_game_state()
                    earth_destroyed_group.remove(earth_destroyed)
                    break


def display_score():
    score_font = pygame.font.SysFont('times new roman', 20)
    score_surface = score_font.render('Score: ' + str(score), True, box_color)
    life_surface = score_font.render('Life: ' + str(life), True, box_color)
    screen.blit(score_surface, (200, 0))
    screen.blit(life_surface, (300, 0))


asteroid = Asteroid()
asteroid_group.add(asteroid)

earth_destroyed = EarthDestroyed()
earth_destroyed_group.add(earth_destroyed)

running = True

missile = None

while running and life > 0:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    # Handle user input and create a new missile
                    if missile and missile.finished:
                        if user_text.strip() == f"{(asteroid.rect.x - origin_x) // scale}, {(origin_y - asteroid.rect.y) // scale}":
                            asteroid.reset_position()
                        else:
                            print("Missile coordinates do not match the asteroid. Try again.")
                            while asteroid.rect.x > 0:

                                # Show EarthDestroyed.png
                                show_earth_destroyed()
                                pygame.time.delay(2000)  # Wait for 2 seconds before restarting

                                # Show "Game Over"
                                show_game_over()
                                pygame.time.delay(2000)  # Wait for 2 seconds before quitting
                                quit()

                                # Break out of the inner loop
                                break

                                # Restart the game
                            reset_game()

                            # Break out of the inner loop
                            break

                    try:
                        user_text = user_text.replace(" ", "")
                        x, y = map(int, user_text.split(","))
                        target_x = origin_x + x * scale
                        target_y = origin_y - y * scale
                        missile = Missile(origin_x, screen_height, target_x, target_y)
                        missile_group.add(missile)
                    except (ValueError, IndexError):
                        print("Invalid input. Please enter coordinates in the format 'x, y'.")
                    user_text = ""
                elif event.key == pygame.K_BACKSPACE:
                    user_text = user_text[:-1]
                else:
                    user_text += event.unicode


        screen.fill((0, 0, 0))
        screen.blit(background_image, (0, 0))

        pygame.draw.line(screen, (255, 255, 255), (160, origin_y), (screen_width - 160, origin_y), 2)
        pygame.draw.line(screen, (255, 255, 255), (origin_x, 100), (origin_x, screen_height - 100), 2)

        for x in range(160, screen_width - 160, scale):
            pygame.draw.line(screen, gridline_color, (x, 100), (x, screen_height - 100), 1)
        for y in range(100, screen_height - 100, scale):
            pygame.draw.line(screen, gridline_color, (160, y), (screen_width - 160, y), 1)

        x_label_surface = font.render(x_label, True, (255, 255, 255))
        screen.blit(x_label_surface, (screen_width - x_label_surface.get_width() - 80, origin_y + 10))

        y_label_surface = font.render(y_label, True, (255, 255, 255))
        screen.blit(y_label_surface, (origin_x + 10, 70))

        display_score()
        asteroid_group.update()
        asteroid_group.draw(screen)

        missile_group.update()
        missile_group.draw(screen)

        explosion_group.update()
        explosion_group.draw(screen)

        text_surface = font.render(f"({user_text})", True, text_color)
        box_width = text_surface.get_width() + 10
        box_height = text_surface.get_height() + 10
        pygame.draw.rect(screen, box_color, (text_x - 5, text_y - 5, box_width, box_height))
        screen.blit(text_surface, (text_x, text_y))

        pygame.display.flip()

    # Display EarthDestroyed.png when life is 0
        if life == 0:
            show_earth_destroyed()
            show_game_over()
            pygame.time.delay(10000)  # Wait for 5 seconds before restarting
            reset_game()
            reset_game_state()
           # quit()

pygame.quit()
