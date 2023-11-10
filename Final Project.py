import pygame
import random

# Initialize Pygame
pygame.init()

# Define screen dimensions
screen_width = 800
screen_height = 600

# Create a Pygame window
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Coordinate Plane")

# Load background image
background_image = pygame.image.load('background2.bmp').convert_alpha()

# Define font and colors for text
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

# Create a single asteroid
asteroid = None
spawn_new_asteroid = True  # Flag to indicate if a new asteroid should be spawned

class Missile(pygame.sprite.Sprite):
    def __init__(self, start_x, start_y, target_x, target_y):
        super().__init__()
        self.image = pygame.image.load('missile1.png').convert_alpha()
        self.mask = pygame.mask.from_surface(self.image)  # Create the mask based on the image
        self.rect = self.image.get_rect()
        self.rect.center = (start_x, start_y)
        self.target_x = target_x
        self.target_y = target_y
        self.speed = 10
        self.finished = False  # Flag to check if the missile is finished

    def update(self):
        if not self.finished:
            direction_x = self.target_x - self.rect.centerx
            direction_y = self.target_y - self.rect.centery
            distance = ((direction_x) ** 2 + (direction_y) ** 2) ** 0.5

            if distance != 0:
                self.rect.x += (direction_x / distance) * self.speed
                self.rect.y += (direction_y / distance) * self.speed

            if self.rect.collidepoint(self.target_x, self.target_y):
                self.finished = True  # Set the flag when the missile reaches its target

class Asteroid(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('asteroid1.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.speed = 0
        self.spawn_random_position()

    def spawn_random_position(self):
        # Generate a random x and y position within the coordinate plane
        x = random.randint(160, screen_width - 160 - self.rect.width)
        y = random.randint(100, screen_height - 100 - self.rect.height)
        self.rect.topleft = (x, y)

    def update(self):
        # Update the asteroid's position
        self.rect.x += self.speed

        # Check if the asteroid moves off the screen, and spawn a new one
        if self.rect.right < 0:
            spawn_new_asteroid = True

        # Check for collision with the rocket (missile)
        if pygame.sprite.spritecollide(self, missile_group, True):
            # Remove the asteroid if it collides with the rocket
            asteroid_group.remove(self)
            spawn_new_asteroid = True

asteroid_group = pygame.sprite.Group()
missile_group = pygame.sprite.Group()

running = True
missile = None

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                if missile and missile.finished:
                    missile_group.remove(missile)
                    missile = None
                try:
                    user_text = user_text.replace(" ", "")
                    x, y = map(int, user_text.split(","))
                    target_x = origin_x + x * scale
                    target_y = origin_y - y * scale
                    if missile is None:
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

    # Draw the x and y axes
    pygame.draw.line(screen, (255, 255, 255), (160, origin_y), (screen_width - 160, origin_y), 2)
    pygame.draw.line(screen, (255, 255, 255), (origin_x, 100), (origin_x, screen_height - 100), 2)

    # Draw gridlines
    for x in range(160, screen_width - 160, scale):
        pygame.draw.line(screen, gridline_color, (x, 100), (x, screen_height - 100), 1)
    for y in range(100, screen_height - 100, scale):
        pygame.draw.line(screen, gridline_color, (160, y), (screen_width - 160, y), 1)

    # Render and draw the axis labels
    x_label_surface = font.render(x_label, True, (255, 255, 255))
    screen.blit(x_label_surface, (screen_width - x_label_surface.get_width() - 80, origin_y + 10))

    y_label_surface = font.render(y_label, True, (255, 255, 255))
    screen.blit(y_label_surface, (origin_x + 10, 70))

    # Check if a new asteroid should be spawned
    if spawn_new_asteroid:
        if asteroid:
            asteroid_group.remove(asteroid)
        asteroid = Asteroid()
        asteroid_group.add(asteroid)
        spawn_new_asteroid = False

    missile_group.update()
    missile_group.draw(screen)

    asteroid_group.update()
    asteroid_group.draw(screen)

    # Render and display the user's text input
    text_surface = font.render(f"({user_text})", True, text_color)
    box_width = text_surface.get_width() + 10
    box_height = text_surface.get_height() + 10
    pygame.draw.rect(screen, box_color, (text_x - 5, text_y - 5, box_width, box_height))
    screen.blit(text_surface, (text_x, text_y))

    pygame.display.flip()

pygame.quit()
