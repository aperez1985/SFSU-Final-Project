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

class Missile(pygame.sprite.Sprite):
    def __init__(self, start_x, start_y, target_x, target_y):
        super().__init__()
        self.image = pygame.image.load('missile1.png').convert_alpha()
        self.mask = pygame.mask.from_surface(self.image)  # Create the mask based on the image
        self.rect = self.image.get_rect()
        self.rect.center = (start_x, start_y)
        self.target_x = target_x
        self.target_y = target_y +30
        self.speed = 2
        self.finished = False  # Flag to check if the missile is finished

    def update(self):
        if not self.finished:
            direction_x = self.target_x  - self.rect.centerx
            direction_y = self.target_y - self.rect.centery
            distance = ((direction_x) ** 2 + (direction_y) ** 2) ** 0.5
            print(target_x , target_y)
            new_missile_x = (target_x - origin_x) // scale
            new_missile_y = (origin_y - target_y) // scale
            print(new_missile_x , new_missile_y)

            if distance != 0:
                self.rect.x += (direction_x / distance) * self.speed
                self.rect.y += (direction_y / distance) * self.speed
                # Print the collision coordinates
                asteroid_x = (asteroid.rect.x - origin_x) // scale
                asteroid_y = (origin_y - asteroid.rect.y) // scale
                print(f"Collision Coordinates: ({asteroid_x}, {asteroid_y})")

                # Check for collision with the asteroid
                if self.rect.colliderect(asteroid.rect) and asteroid_y == new_missile_y:
                    

                    # Your code for handling the collision, such as creating an explosion
                    explosion = Explosion(self.target_x, self.target_y)
                    explosion_group.add(explosion)

                    # Remove the missile and asteroid from their respective groups
                    missile_group.remove(self)
                    asteroid.reset_position()
                #elif self.finished == True:
                    #missile_group.remove(self)




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

        # Change the PyCharm coordinate to Cartesian coordinate
        x_cartesian = (self.rect.x - origin_x) // scale
        y_cartesian = (origin_y - self.rect.y) // scale

        # Ensure the adjusted coordinates are within the coordinate plane boundaries
        x_cartesian = max(-int(coord_plane_width / (2 * scale)), min(int(coord_plane_width / (2 * scale)), x_cartesian))
        y_cartesian = max(-int(coord_plane_height / (2 * scale)), min(int(coord_plane_height / (2 * scale)), y_cartesian))

        # Set the asteroid's rect attributes to match the adjusted coordinates
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



# ... (your existing imports and code)

asteroid = Asteroid()  # Initialize the asteroid
asteroid_group.add(asteroid)

earth_destroyed = EarthDestroyed()
earth_destroyed_group.add(earth_destroyed)

running = True  # Initialize the running variable

missile = None  # Initialize missile here


while running:
    # Step 1: an asteroid1.png randomly appears on the cartesian coordinate.
    asteroid.reset_position()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if missile and missile.finished:
                        if user_text.strip() == f"{(asteroid.rect.x - origin_x) // scale}, {(origin_y - asteroid.rect.y) // scale}":
                            # Step 5: if the user entered coordinate match with the location of the asteroid1.png
                            #   this asteroid1.png disappear and another asteroid1.png randomly appears on the coordinate plane.
                            asteroid.reset_position()
                        else:
                            print("Missile coordinates do not match the asteroid. Try again.")
                            # Step 5: if the user entered a coordinate that does not match the location of the asteroid1.png
                            #   the asteroid1.png will blit to the left until it gets to x=10,
                            #   then an “EarthDestroyed.png” will appear on the screen.
                            while asteroid.rect.x > 10:
                                asteroid.rect.x -= 3
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

                                # Reset missile and create a new one
                                missile = Missile(origin_x, screen_height, target_x, target_y)
                                missile_group.add(missile)

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

                            show_earth_destroyed()
                            wait_for_restart()

                    try:
                        user_text = user_text.replace(" ", "")
                        x, y = map(int, user_text.split(","))
                        target_x = origin_x + x * scale
                        target_y = origin_y - y * scale
                        # Reset missile and create a new one
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
