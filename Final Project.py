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
plotted_points = []
user_input_x = ""  # Initialize user input for X coordinate
user_input_y = ""  # Initialize user input for Y coordinate
input_mode = "x"  # Initial input mode is for X coordinate

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
                # Check if Enter is pressed to plot the point
                try:
                    x_coordinate = int(
                        user_input_x) if user_input_x else 0  # Convert user input to an integer, default to 0 if input is empty
                    y_coordinate = int(
                        user_input_y) if user_input_y else 0  # Convert user input to an integer, default to 0 if input is empty
                    # Add the point to the list of plotted points
                    plotted_points.append((x_coordinate, y_coordinate))
                except ValueError:
                    print("Invalid input. Please enter valid integer coordinates.")
                user_input_x = ""  # Reset user input for X coordinate
                user_input_y = ""  # Reset user input for Y coordinate
                input_mode = "x"  # Reset input mode to X
            elif event.key == pygame.K_BACKSPACE:
                # Handle backspace to delete characters
                if input_mode == "x":
                    user_input_x = user_input_x[:-1]
                elif input_mode == "y":
                    user_input_y = user_input_y[:-1]
            elif event.key == pygame.K_SPACE:
                # Switch input mode to Y when spacebar is pressed
                input_mode = "y"
            elif event.key == pygame.K_MINUS:
                # Handle the negative sign (-) for both X and Y coordinates
                if input_mode == "x":
                    if not user_input_x:
                        user_input_x += "-"
                    elif user_input_x:
                        user_input_x = "-" + user_input_x
                elif input_mode == "y":
                    if not user_input_y:
                        user_input_y += "-"
                    elif user_input_y:
                        user_input_y = "-" + user_input_y
            else:
                # Handle other key presses to build the input strings
                if event.key >= 48 and event.key <= 57:
                    if input_mode == "x":
                        user_input_x += event.unicode
                    elif input_mode == "y":
                        user_input_y += event.unicode

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



    # Display the current user input
    font = pygame.font.Font(None, 36)
    text = font.render(f"( {user_input_x} , {user_input_y} )", True, (255, 255, 255))
    screen.blit(text, (680, 110))

    # Plot the user-defined points
    for x, y in plotted_points:
        pygame.draw.circle(screen, (255, 255, 0), (screen_width // 2 + x*20, screen_height // 2 - y*20), 5)



    pygame.display.flip()

pygame.quit()
