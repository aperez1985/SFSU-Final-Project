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

                # Create an explosion animation at the target position
                explosion = Explosion(self.target_x, self.target_y)
                explosion_group.add(explosion)
                missile_group.remove(self)  # Remove the missile from the group

class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.images = [pygame.image.load(f'explosion1.png').convert_alpha() for i in range(1, 10)]
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.frame = 0
        self.animation_speed = 5  # Adjust the speed of the explosion animation

    def update(self):
        self.frame += 1
        if self.frame // self.animation_speed < len(self.images):
            self.image = self.images[self.frame // self.animation_speed]
        else:
            explosion_group.remove(self)  # Remove the explosion sprite when the animation is complete

class Asteroid(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('asteroid1.png').convert_alpha()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.reset_position()

    def reset_position(self):
        x_cartesian = random.randint(-coord_plane_width // 2, coord_plane_width // 2)
        y_cartesian = random.randint(-coord_plane_height // 2, coord_plane_height // 2)

        # Convert Cartesian coordinates to pygame coordinates
        self.rect.x = origin_x + x_cartesian * scale
        self.rect.y = origin_y - y_cartesian * scale

        # Check if the asteroid is within the coordinate plane
        if (
            origin_x - coord_plane_width // 2 <= self.rect.x <= origin_x + coord_plane_width // 2 and
            origin_y - coord_plane_height // 2 <= self.rect.y <= origin_y + coord_plane_height // 2
        ):
            # Print the Cartesian coordinates of the asteroid
            print(f"Asteroid Coordinates: ({x_cartesian}, {y_cartesian})")
        else:
            # If the asteroid is outside the coordinate plane, reset its position
            self.reset_position()

    def update(self):
        pass  # Add any asteroid-specific update logic if needed

missile_group = pygame.sprite.Group()
explosion_group = pygame.sprite.Group()
asteroid_group = pygame.sprite.Group()

running = True
missile = None  # Initialize the missile outside the loop
asteroid = Asteroid()  # Initialize the asteroid
asteroid_group.add(asteroid)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                if missile and missile.finished:
                    missile = None

                # Reset the asteroid's position
                asteroid.reset_position()

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

    asteroid_group.update()
    asteroid_group.draw(screen)

    missile_group.update()
    missile_group.draw(screen)

    explosion_group.update()
    explosion_group.draw(screen)

    # Render and display the user's text input
    text_surface = font.render(f"({user_text})", True, text_color)
    box_width = text_surface.get_width() + 10
    box_height = text_surface.get_height() + 10
    pygame.draw.rect(screen, box_color, (text_x - 5, text_y - 5, box_width, box_height))
    screen.blit(text_surface, (text_x, text_y))

    pygame.display.flip()

pygame.quit()
