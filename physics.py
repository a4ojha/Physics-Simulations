import pygame
import numpy as np

pygame.init()
pygame.font.init()

# setting up window
WIDTH = 600
HEIGHT = 600
toolbar_height = 200
background_color = (0,0,0)
screen = pygame.display.set_mode((WIDTH, HEIGHT + toolbar_height))
clock = pygame.time.Clock()
pygame.display.set_caption('Physics!!')

SCALE = 0.5


# Declaring motion variables 
x_mid = WIDTH / 2
y_mid = HEIGHT / 2

dt = 0
acc_grav = 500

jump_force = 150

curr_pos = pygame.Vector2(x_mid, HEIGHT)
x_speed = 0
y_speed = 0
radius = 10
on_ground = False

# Font
font = pygame.font.Font('font/Lato-Semibold.ttf', 16)
text = font.render("(" + str(curr_pos.x) + ", " + str(curr_pos.y) + ")", True, "white")
textRect = text.get_rect()
textRect.center = (WIDTH // 2, HEIGHT // 2)

# Arrow shape definition
def draw_horizontal_arrow(surface, color, start_pos, end_pos, shaft_width, right=True):
    x_start, y_start = start_pos
    x_end, y_end = end_pos

    # Define shaft height as half of the shaft width for centering the shaft
    shaft_height = shaft_width // 2

    # Define the length and width of the arrowhead
    arrowhead_length = shaft_width * 2  # or any other factor or fixed value you prefer
    arrowhead_width = shaft_width * 2  # should be greater than shaft_height

    # Calculate the points for the arrowhead
    if right:
        # Arrow pointing to the right
        arrowhead_base_x = x_end - arrowhead_length
        shaft_end_x = arrowhead_base_x
    else:
        # Arrow pointing to the left
        arrowhead_base_x = x_start + arrowhead_length
        x_start, x_end = x_end, x_start  # Swap start and end for the shaft
        shaft_end_x = arrowhead_base_x
        y_start, y_end = y_end, y_start  # Swap to keep the arrow on the same line

    # Define the points of the arrowhead polygon
    # ...
    if right:
        arrowhead_points = [
            end_pos,  # Tip of the arrowhead when pointing right
            (arrowhead_base_x, y_end - arrowhead_width),  # Top back corner
            (arrowhead_base_x, y_end + arrowhead_width),  # Bottom back corner
        ]
        shaft_end_x = arrowhead_base_x  # Shaft ends where the arrowhead base starts
    else:
        arrowhead_points = [
            start_pos,  # Tip of the arrowhead when pointing left
            (arrowhead_base_x, y_start + arrowhead_width),  # Top back corner
            (arrowhead_base_x, y_start - arrowhead_width),  # Bottom back corner
        ]
        x_end = arrowhead_base_x  # Shaft ends where the arrowhead base starts

    # Draw the shaft as lines
    if right:
        pygame.draw.line(surface, color, (x_start, y_start - shaft_height), (shaft_end_x, y_start - shaft_height), shaft_width)
        pygame.draw.line(surface, color, (x_start, y_start + shaft_height), (shaft_end_x, y_start + shaft_height), shaft_width)
    else:
        pygame.draw.line(surface, color, (arrowhead_base_x, y_start - shaft_height), (x_end, y_start - shaft_height), shaft_width)
        pygame.draw.line(surface, color, (arrowhead_base_x, y_start + shaft_height), (x_end, y_start + shaft_height), shaft_width)

    # Draw the arrowhead as a polygon
    pygame.draw.polygon(surface, color, arrowhead_points)


running = True
while running:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
    screen.fill(background_color)

    # Render pygame here
    pygame.draw.line(screen, "red", (x_mid, 0), (x_mid, HEIGHT))
    pygame.draw.line(screen, "red", (0, y_mid), (WIDTH, y_mid))
    pygame.draw.line(screen, "white", (0, HEIGHT), (WIDTH, HEIGHT))
    
    pygame.draw.circle(screen, "green", curr_pos, radius)
    
    
    # Movement keys
    keys = pygame.key.get_pressed()
    x_speed = 0
    
    # apply an upward force
    if (keys[pygame.K_UP] or keys[pygame.K_SPACE]) and on_ground:
        y_speed = -jump_force
        on_ground = False
                        
    if keys[pygame.K_RIGHT]:
        x_speed = 100
        arrowhead_offset = radius
        right = True
        if curr_pos.x + radius < WIDTH:
            curr_pos.x += x_speed * dt
    if keys[pygame.K_LEFT]:
        x_speed = -100
        arrowhead_offset = -1 * radius
        right = False
        if curr_pos.x - radius > 0:
            curr_pos.x -= (-1 * x_speed) * dt

    # Drawing direction arrow
    # if x_speed != 0:
    #     start_pos = (curr_pos.x + arrowhead_offset, curr_pos.y)
    #     end_pos = (curr_pos.x + x_speed * SCALE, curr_pos.y)
        
    #     if right == False:
    #         start_pos, end_pos = end_pos, start_pos

    #     draw_horizontal_arrow(screen, "white", (curr_pos.x + arrowhead_offset, curr_pos.y), (curr_pos.x + x_speed * SCALE, curr_pos.y), radius // 2, right)

    # Gravity and ground collision
    if curr_pos.y + radius <= HEIGHT:
        y_speed += acc_grav * dt
        curr_pos.y += y_speed * dt
        
    else:
        curr_pos.y = HEIGHT - radius  # Adjust position so it doesn't go below ground
        y_speed = 0
        on_ground = True
        
    # Current position text box
    bottom_rect = pygame.Rect(10, HEIGHT + 10, 20, 20)
    screen.blit(font.render("Current Position: (" + str(round(curr_pos.x-x_mid)) + ", " + str(round(-1*(curr_pos.y-y_mid))) + ")", True, "White"), bottom_rect)

    # updates the display
    pygame.display.flip()

    dt = clock.tick(60) / 1000  # limit FPS to 60
    
pygame.quit()