import pygame
import numpy as np
import math

# Initialize Pygame
pygame.init()

# Define constants
WIDTH, HEIGHT = 800, 600
BACKGROUND_COLOR = (0, 0, 0)  # Black background color
LINE_COLOR = (255, 255, 255)  # White line color
PROJ_COLOR = (255, 0 , 0)
HOUSE_COLOR = (0, 0, 0)  # Red house color
DOOR_COLOR = (100, 50, 0)  # Door color
WINDOW_COLOR = (100, 100, 255)  # Window color
HOUSE_WIDTH = 200
HOUSE_HEIGHT = 200
ROOF_HEIGHT = 100
DOOR_WIDTH = 40
DOOR_HEIGHT = 100
WINDOW_WIDTH = 40
WINDOW_HEIGHT = 40
WINDOW_OFFSET = 45
rotation_angle = 0.01
projection_x, projection_y, projection_z = False, False, False
sx, sy, sz = 1, 1, 1

# Create Pygame screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Lab3")

# Define vertices
house_vertices = [
    (-HOUSE_WIDTH / 2, -HOUSE_HEIGHT / 2, 0, 1),
    (HOUSE_WIDTH / 2, -HOUSE_HEIGHT / 2, 0, 1),
    (HOUSE_WIDTH / 2, 0, 0, 1),
    (-HOUSE_WIDTH / 2, 0, 0, 1)
]
roof_vertices = [
    (HOUSE_WIDTH / 2, 0, 0, 1),
    (0, ROOF_HEIGHT, 0, 1),
    (-HOUSE_WIDTH / 2, 0, 0, 1),
    (0, 0, 0, 1)
]
house_vertices_2 = [
    (-HOUSE_WIDTH / 2, -HOUSE_HEIGHT / 2, 200, 1),
    (HOUSE_WIDTH / 2, -HOUSE_HEIGHT / 2, 200, 1),
    (HOUSE_WIDTH / 2, 0, 200, 1),
    (-HOUSE_WIDTH / 2, 0, 200, 1)
]
roof_vertices_2 = [
    (HOUSE_WIDTH / 2, 0, 200, 1),
    (0, ROOF_HEIGHT, 200, 1),
    (-HOUSE_WIDTH / 2, 0, 200, 1),
    (0, 0, 0, 1)
]
door_vertices = [
    (-DOOR_WIDTH / 2, -HOUSE_HEIGHT / 2, 0, 1),
    (DOOR_WIDTH / 2, -HOUSE_HEIGHT / 2, 0, 1),
    (DOOR_WIDTH / 2, 0, 0, 1),
    (-DOOR_WIDTH / 2, 0, 0, 1)
]
left_window_vertices = [
    (-WINDOW_WIDTH / 2 - WINDOW_OFFSET, -HOUSE_HEIGHT / 2 + WINDOW_HEIGHT / 2 + WINDOW_OFFSET, 0, 1),
    (WINDOW_WIDTH / 2 - WINDOW_OFFSET, -HOUSE_HEIGHT / 2 + WINDOW_HEIGHT / 2 + WINDOW_OFFSET, 0, 1),
    (WINDOW_WIDTH / 2 - WINDOW_OFFSET, -HOUSE_HEIGHT / 2 + WINDOW_HEIGHT + WINDOW_OFFSET, 0, 1),
    (-WINDOW_WIDTH / 2 - WINDOW_OFFSET, -HOUSE_HEIGHT / 2 + WINDOW_HEIGHT + WINDOW_OFFSET, 0, 1)
]
right_window_vertices = [
    (-WINDOW_WIDTH / 2 + WINDOW_OFFSET, -HOUSE_HEIGHT / 2 + WINDOW_HEIGHT / 2 + WINDOW_OFFSET, 0, 1),
    (WINDOW_WIDTH / 2 + WINDOW_OFFSET, -HOUSE_HEIGHT / 2 + WINDOW_HEIGHT / 2 + WINDOW_OFFSET, 0, 1),
    (WINDOW_WIDTH / 2 + WINDOW_OFFSET, -HOUSE_HEIGHT / 2 + WINDOW_HEIGHT + WINDOW_OFFSET, 0, 1),
    (-WINDOW_WIDTH / 2 + WINDOW_OFFSET, -HOUSE_HEIGHT / 2 + WINDOW_HEIGHT + WINDOW_OFFSET, 0, 1)
]

world_matrix = np.array([
    [1, 0, 0, 0],
    [0, -1, 0, 0],
    [0, 0, 1, 0],
    [WIDTH / 2, HEIGHT / 2, 0, 1]
])
scale_matrix = np.array([
    [sx, 0, 0, 0],
    [0, sy, 0, 0],
    [0, 0, sz, 0],
    [0, 0, 0, 1]
])
rotation_matrix_x = np.array([
    [math.cos(rotation_angle), 0, -math.sin(rotation_angle), 0],
    [0, 1, 0, 0],
    [math.sin(rotation_angle), 0, math.cos(rotation_angle), 0],
    [0, 0, 0, 1]
])

rotation_matrix_y = np.array([
    [1, 0, 0, 0],
    [0, math.cos(rotation_angle), math.sin(rotation_angle), 0],
    [0, -math.sin(rotation_angle), math.cos(rotation_angle), 0],
    [0, 0, 0, 1]
])

rotation_matrix_z = np.array([
    [math.cos(rotation_angle), -math.sin(rotation_angle), 0, 0],
    [math.sin(rotation_angle), math.cos(rotation_angle), 0, 0],
    [0, 0, 1, 0],
    [0, 0, 0, 1]
])

orthographic_projection_matrix_z = np.array([
    [1, 0, 0, 0],
    [0, 1, 0, 0],
    [0, 0, 0, 0],
    [1, 1, 0, 1]
])
orthographic_projection_matrix_y = np.array([
    [1, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 1, 0],
    [1, 1, 0, 1]
])
orthographic_projection_matrix_x = np.array([
    [0, 0, 0, 0],
    [0, 1, 0, 0],
    [0, 0, 1, 0],
    [1, 1, 0, 1]
])

# Define clock
clock = pygame.time.Clock()

# Define running flag
running = True


def apply_scaling(sx, sy, sz):
    global scale_matrix
    scale_matrix = np.array([
        [sx, 0, 0, 0],
        [0, sy, 0, 0],
        [0, 0, sz, 0],
        [0, 0, 0, 1]
    ])


def handle_events():
    global running, rotation_angle, sx, sy, sz, scale_matrix, world_matrix, projection_z, projection_x, projection_y
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        world_matrix[3][0] -= 2  # Move left
    if keys[pygame.K_RIGHT]:
        world_matrix[3][0] += 2  # Move right
    if keys[pygame.K_UP]:
        world_matrix[3][1] -= 2  # Move up
    if keys[pygame.K_DOWN]:
        world_matrix[3][1] += 2  # Move down
    if keys[pygame.K_z]:
        projection_z = True
    if keys[pygame.K_x]:
        projection_x = True
    if keys[pygame.K_c]:
        projection_y = True
    if keys[pygame.K_w]:
        sx *= 1.001
        sy *= 1.001
        sz *= 1.001
        apply_scaling(sx, sy, sz)
    if keys[pygame.K_s]:
        sx /= 1.001
        sy /= 1.001
        sz /= 1.001
        apply_scaling(sx, sy, sz)
    if keys[pygame.K_ESCAPE]:
        running = False


def calculate_transformations():
    global house_vertices, roof_vertices, door_vertices, left_window_vertices, right_window_vertices, house_vertices_2, roof_vertices_2

    # house_vertices = [np.dot([x, y, z, 1], rotation_matrix_x) for x, y, z, a in house_vertices]
    # roof_vertices = [np.dot([x, y, z, 1], rotation_matrix_x) for x, y, z, a in roof_vertices]
    # door_vertices = [np.dot([x, y, z, 1], rotation_matrix_x) for x, y, z, a in door_vertices]
    # left_window_vertices = [np.dot([x, y, z, 1], rotation_matrix_x) for x, y, z, a in left_window_vertices]
    # right_window_vertices = [np.dot([x, y, z, 1], rotation_matrix_x) for x, y, z, a in right_window_vertices]
    #
    # house_vertices_2 = [np.dot([x, y, z, 1], rotation_matrix_x) for x, y, z, a in house_vertices_2]
    # roof_vertices_2 = [np.dot([x, y, z, 1], rotation_matrix_x) for x, y, z, a in roof_vertices_2]
    #
    # house_vertices = [np.dot([x, y, z, 1], rotation_matrix_y) for x, y, z, a in house_vertices]
    # roof_vertices = [np.dot([x, y, z, 1], rotation_matrix_y) for x, y, z, a in roof_vertices]
    # door_vertices = [np.dot([x, y, z, 1], rotation_matrix_y) for x, y, z, a in door_vertices]
    # left_window_vertices = [np.dot([x, y, z, 1], rotation_matrix_y) for x, y, z, a in left_window_vertices]
    # right_window_vertices = [np.dot([x, y, z, 1], rotation_matrix_y) for x, y, z, a in right_window_vertices]
    #
    # house_vertices_2 = [np.dot([x, y, z, 1], rotation_matrix_y) for x, y, z, a in house_vertices_2]
    # roof_vertices_2 = [np.dot([x, y, z, 1], rotation_matrix_y) for x, y, z, a in roof_vertices_2]

    house_vertices = [np.dot([x, y, z, 1], scale_matrix) for x, y, z, a in house_vertices]
    roof_vertices = [np.dot([x, y, z, 1], scale_matrix) for x, y, z, a in roof_vertices]
    door_vertices = [np.dot([x, y, z, 1], scale_matrix) for x, y, z, a in door_vertices]
    left_window_vertices = [np.dot([x, y, z, 1], scale_matrix) for x, y, z, a in left_window_vertices]
    right_window_vertices = [np.dot([x, y, z, 1], scale_matrix) for x, y, z, a in right_window_vertices]

    house_vertices_2 = [np.dot([x, y, z, 1], scale_matrix) for x, y, z, a in house_vertices_2]
    roof_vertices_2 = [np.dot([x, y, z, 1], scale_matrix) for x, y, z, a in roof_vertices_2]


def draw_figure(world_house, world_roof, world_door, world_left_window, world_right_window, world_house_2, world_roof_2):
    pygame.draw.polygon(screen, LINE_COLOR, [tuple(k[:2]) for k in world_house], 2)
    # pygame.draw.polygon(screen, LINE_COLOR, [tuple(k[:2]) for k in world_roof[:3]], 2)
    # pygame.draw.polygon(screen, DOOR_COLOR, [tuple(k[:2]) for k in world_door], 0)
    # pygame.draw.polygon(screen, LINE_COLOR, [tuple(k[:2]) for k in world_door], 2)
    # pygame.draw.polygon(screen, WINDOW_COLOR, [tuple(k[:2]) for k in world_left_window], 0)
    # pygame.draw.polygon(screen, LINE_COLOR, [tuple(k[:2]) for k in world_left_window], 2)
    # pygame.draw.polygon(screen, WINDOW_COLOR, [tuple(k[:2]) for k in world_right_window], 0)
    # pygame.draw.polygon(screen, LINE_COLOR, [tuple(k[:2]) for k in world_right_window], 2)

    # for window in (world_left_window, world_right_window):
    #     pygame.draw.lines(screen, LINE_COLOR, True, [window[0][:2], window[2][:2]], 2)
    #     pygame.draw.lines(screen, LINE_COLOR, True, [window[1][:2], window[3][:2]], 2)
    #
    pygame.draw.polygon(screen, LINE_COLOR, [tuple(k[:2]) for k in world_house_2[:5]], 2)
    # pygame.draw.polygon(screen, LINE_COLOR, [tuple(k[:2]) for k in world_roof_2[:3]], 2)

    for j in range(4):
        pygame.draw.line(screen, LINE_COLOR, tuple(world_house[j][:2]), tuple(world_house_2[j][:2]), 2)  # Connect the houses

    # pygame.draw.line(screen, LINE_COLOR, world_roof[1][:2], world_roof_2[1][:2], 2)


def draw_projection(world_house, world_roof, world_door, world_left_window, world_right_window, world_house_2, world_roof_2, projection, k1, k2):
    pygame.draw.polygon(screen, PROJ_COLOR, [tuple(k[:2] + k1) for k in np.dot(world_house, projection)], 2)
    pygame.draw.polygon(screen, PROJ_COLOR, [tuple(k[:2] + k2) for k in np.dot(world_house_2, projection)], 2)
    pygame.draw.polygon(screen, PROJ_COLOR, [tuple(k[:2] + k1) for k in np.dot(world_roof, projection)[:3]], 2)
    pygame.draw.polygon(screen, DOOR_COLOR, [tuple(k[:2] + k1) for k in np.dot(world_door, projection)], 0)
    pygame.draw.polygon(screen, PROJ_COLOR, [tuple(k[:2] + k1) for k in np.dot(world_door, projection)], 2)
    pygame.draw.polygon(screen, WINDOW_COLOR, [tuple(k[:2] + k1) for k in np.dot(world_left_window, projection)], 0)
    pygame.draw.polygon(screen, PROJ_COLOR, [tuple(k[:2] + k1) for k in np.dot(world_left_window, projection)], 2)
    pygame.draw.polygon(screen, WINDOW_COLOR, [tuple(k[:2] + k1) for k in np.dot(world_right_window, projection)], 0)
    pygame.draw.polygon(screen, PROJ_COLOR, [tuple(k[:2] + k1) for k in np.dot(world_right_window, projection)], 2)

    for window in (np.dot(world_left_window, projection), np.dot(world_right_window, projection)):
        pygame.draw.lines(screen, PROJ_COLOR, True, [window[0][:2] + k1, window[2][:2] + k1], 2)
        pygame.draw.lines(screen, PROJ_COLOR, True, [window[1][:2] + k1, window[3][:2] + k1], 2)

    pygame.draw.polygon(screen, PROJ_COLOR, [tuple(k[:2] + k2) for k in np.dot(world_roof_2, projection)[:3]], 2)

    for j in range(4):
        pygame.draw.line(screen, PROJ_COLOR, tuple(np.dot(world_house, projection)[j][:2] + k1),
                         tuple(np.dot(world_house_2, projection)[j][:2] + k2), 2)  # Connect the houses

    pygame.draw.line(screen, PROJ_COLOR, np.dot(world_roof, projection)[1][:2] + k1, np.dot(world_roof_2, projection)[1][:2] + k2, 2)


def draw_scene():
    calculate_transformations()
    global world_matrix
    if running:
        screen.fill(BACKGROUND_COLOR)

        world_house = [np.dot([x, y, z, 1], world_matrix) for x, y, a, z in house_vertices]
        world_roof = [np.dot([x, y, z, 1], world_matrix) for x, y, z, a in roof_vertices]
        world_door = [np.dot([x, y, z, 1], world_matrix) for x, y, z, a in door_vertices]
        world_left_window = [np.dot([x, y, z, 1], world_matrix) for x, y, z, a in
                             left_window_vertices]
        world_right_window = [np.dot([x, y, z, 1], world_matrix) for x, y, z, a in
                              right_window_vertices]

        world_house_2 = [np.dot([x, y, z, 1], world_matrix) for x, y, z, a in house_vertices_2]
        world_roof_2 = [np.dot([x, y, z, 1], world_matrix) for x, y, z, a in roof_vertices_2]

        # if projection_z:
        draw_projection(world_house, world_roof, world_door, world_left_window, world_right_window, world_house_2, world_roof_2, orthographic_projection_matrix_x, 200, 100)
        draw_projection(world_house, world_roof, world_door, world_left_window, world_right_window, world_house_2, world_roof_2, orthographic_projection_matrix_y, 200, 100)
        draw_projection(world_house, world_roof, world_door, world_left_window, world_right_window, world_house_2, world_roof_2, orthographic_projection_matrix_z, 150, 130)

        # draw_figure(world_house, world_roof, world_door, world_left_window, world_right_window, world_house_2, world_roof_2)


        pygame.display.flip()
        clock.tick(60)  # 60 FPS


while running:
    handle_events()
    draw_scene()


pygame.quit()
