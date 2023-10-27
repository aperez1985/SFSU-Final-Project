import pygame

# Initialize Pygame
pygame.init()

# Define screen dimensions
screen_width = 800
screen_height = 600

# Create a Pygame window
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Draw Line Example")

# Set line coordinates and color
start_pos = (100, 100)
end_pos = (400, 400)
line_color = (255, 0, 0)  # Red

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Clear the screen
    screen.fill((255, 255, 255))

    # Draw the line
    pygame.draw.line(screen, line_color, start_pos, end_pos, width=2)

    pygame.display.flip()

pygame.quit()