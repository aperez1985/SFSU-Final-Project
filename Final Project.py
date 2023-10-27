import pygame


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
text_x = 650
text_y = 50

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
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                # Handle the user's input (e.g., print it)
                print("User Input:", user_text)
                # Clear the input
                user_text = ""
            elif event.key == pygame.K_BACKSPACE:
                # Handle backspace
                user_text = user_text[:-1]
            else:
                # Add characters to the input
                user_text += event.unicode

    # Clear the screen
    screen.fill((0, 0, 0))
    screen.blit(background_image, (0, 0))

    # Draw the x and y axes
    pygame.draw.line(screen, (255, 255, 255), (160, origin_y), (screen_width-160, origin_y), 2)
    pygame.draw.line(screen, (255, 255, 255), (origin_x, 100), (origin_x, screen_height-100), 2)

    # Draw gridlines
    for x in range(160, screen_width-160, scale):
        pygame.draw.line(screen, gridline_color, (x, 100), (x, screen_height-100), 1)
    for y in range(100, screen_height-100, scale):
        pygame.draw.line(screen, gridline_color, (160, y), (screen_width-160, y), 1)

    # Render and draw the axis labels
    x_label_surface = font.render(x_label, True, (255, 255, 255))
    screen.blit(x_label_surface, (screen_width - x_label_surface.get_width() - 80, origin_y + 10))

    y_label_surface = font.render(y_label, True, (255, 255, 255))
    screen.blit(y_label_surface, (origin_x + 10, 70))

    # Render and display the user's text input
    text_surface = font.render(user_text, True, text_color)

    # Calculate the size of the box based on the text size
    box_width = text_surface.get_width() + 10  # Add some padding
    box_height = text_surface.get_height() + 10  # Add some padding

    # Draw the background box
    pygame.draw.rect(screen, box_color, (text_x - 5, text_y - 5, box_width, box_height))
    screen.blit(text_surface, (text_x, text_y))

    pygame.display.flip()

pygame.quit()
