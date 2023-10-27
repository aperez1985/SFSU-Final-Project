import pygame

# Initialize Pygame
pygame.init()

# Define screen dimensions
screen_width = 800
screen_height = 600

# Create a Pygame window
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Coordinate Plane")
background_image = pygame.image.load('background1.bmp').convert_alpha()

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

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Clear the screen
    screen.fill((0, 0, 0))
    screen.blit(background_image, (0, 0))

    # Draw the x and y axes
    pygame.draw.line(screen, (255, 255, 255), (0, origin_y), (screen_width, origin_y), 2)
    pygame.draw.line(screen, (255, 255, 255), (origin_x, 0), (origin_x, screen_height), 2)

    # Draw gridlines
    for x in range(origin_x % scale, screen_width, scale):
        pygame.draw.line(screen, gridline_color, (x, 0), (x, screen_height), 1)
    for y in range(origin_y % scale, screen_height, scale):
        pygame.draw.line(screen, gridline_color, (0, y), (screen_width, y), 1)

    # Render and draw the axis labels
    x_label_surface = font.render(x_label, True, (255, 255, 255))
    screen.blit(x_label_surface, (screen_width - x_label_surface.get_width() - 10, origin_y + 10))

    y_label_surface = font.render(y_label, True, (255, 255, 255))
    screen.blit(y_label_surface, (origin_x + 10, 10))

    pygame.display.flip()

pygame.quit()
