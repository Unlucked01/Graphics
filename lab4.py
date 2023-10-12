import pygame
import numpy as np
import math

# Initialize Pygame
pygame.init()

# Define constants
WIDTH, HEIGHT = 800, 600
BACKGROUND_COLOR = (0, 0, 0)
LINE_COLOR = (255, 255, 255)
PROJ_COLOR = (255, 0, 0)
SEC_COLOR = (0, 255, 0)
THD_COLOR = (0, 0, 255)
HOUSE_COLOR = (0, 0, 0)
DOOR_COLOR = (100, 50, 0)
WINDOW_COLOR = (100, 100, 255)
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
pygame.display.set_caption("Lab4")

# Define vertices
house_vertices = [
    (-HOUSE_WIDTH / 2, -HOUSE_HEIGHT / 4, 100, 1),
    (HOUSE_WIDTH / 2, -HOUSE_HEIGHT / 4, 100, 1),
    (HOUSE_WIDTH / 2, -HOUSE_HEIGHT / 4, -100, 1),
    (-HOUSE_WIDTH / 2, -HOUSE_HEIGHT / 4, -100, 1),
    (-HOUSE_WIDTH / 2, HOUSE_HEIGHT / 4, 100, 1),
    (HOUSE_WIDTH / 2, HOUSE_HEIGHT / 4, 100, 1),
    (HOUSE_WIDTH / 2, HOUSE_HEIGHT / 4, -100, 1),
    (-HOUSE_WIDTH / 2, HOUSE_HEIGHT / 4, -100, 1),
    (0, HOUSE_HEIGHT / 2, 100, 1),  # 8
    (0, HOUSE_HEIGHT / 2, -100, 1),  # 9
    (-DOOR_WIDTH / 2, -HOUSE_HEIGHT / 4, -100, 1),
    (DOOR_WIDTH / 2, -HOUSE_HEIGHT / 4, -100, 1),
    (DOOR_WIDTH / 2, HOUSE_HEIGHT / 4, -100, 1),
    (-DOOR_WIDTH / 2, HOUSE_HEIGHT / 4, -100, 1),  # 13
    (-WINDOW_WIDTH / 2 - WINDOW_OFFSET, -HOUSE_HEIGHT / 4 + WINDOW_HEIGHT / 2 + WINDOW_OFFSET, -100, 1),  # left
    (WINDOW_WIDTH / 2 - WINDOW_OFFSET, -HOUSE_HEIGHT / 4 + WINDOW_HEIGHT / 2 + WINDOW_OFFSET, -100, 1),
    (WINDOW_WIDTH / 2 - WINDOW_OFFSET, -HOUSE_HEIGHT / 4 + WINDOW_HEIGHT + WINDOW_OFFSET, -100, 1),
    (-WINDOW_WIDTH / 2 - WINDOW_OFFSET, -HOUSE_HEIGHT / 4 + WINDOW_HEIGHT + WINDOW_OFFSET, -100, 1),
    (-WINDOW_WIDTH / 2 + WINDOW_OFFSET, -HOUSE_HEIGHT / 4 + WINDOW_HEIGHT / 2 + WINDOW_OFFSET, -100, 1),  # right
    (WINDOW_WIDTH / 2 + WINDOW_OFFSET, -HOUSE_HEIGHT / 4 + WINDOW_HEIGHT / 2 + WINDOW_OFFSET, -100, 1),
    (WINDOW_WIDTH / 2 + WINDOW_OFFSET, -HOUSE_HEIGHT / 4 + WINDOW_HEIGHT + WINDOW_OFFSET, -100, 1),
    (-WINDOW_WIDTH / 2 + WINDOW_OFFSET, -HOUSE_HEIGHT / 4 + WINDOW_HEIGHT + WINDOW_OFFSET, -100, 1)
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
    global house_vertices

    house_vertices = [np.dot([x, y, z, 1], rotation_matrix_x) for x, y, z, a in house_vertices]
    house_vertices = [np.dot([x, y, z, 1], rotation_matrix_y) for x, y, z, a in house_vertices]
    house_vertices = [np.dot([x, y, z, 1], scale_matrix) for x, y, z, a in house_vertices]


def define_position(world_house):
    v01x = world_house[1][0] - world_house[2][0]
    v01y = world_house[1][1] - world_house[2][1]
    v03x = world_house[5][0] - world_house[6][0]
    v03y = world_house[5][1] - world_house[6][1]

    nz = v03x*v01y-v03y*v01x

    if nz <= 0:
        pygame.draw.line(screen, LINE_COLOR, (world_house[0][0], world_house[0][1]),
                         [world_house[1][0], world_house[1][1]], 2)
        pygame.draw.line(screen, LINE_COLOR, (world_house[1][0], world_house[1][1]),
                         [world_house[2][0], world_house[2][1]], 2)
        pygame.draw.line(screen, LINE_COLOR, (world_house[2][0], world_house[2][1]),
                         [world_house[3][0], world_house[3][1]], 2)
        pygame.draw.line(screen, LINE_COLOR, (world_house[3][0], world_house[3][1]),
                         [world_house[0][0], world_house[0][1]], 2)

    else:
        pygame.draw.line(screen, LINE_COLOR, (world_house[4][0], world_house[4][1]),
                         [world_house[5][0], world_house[5][1]], 2)
        pygame.draw.line(screen, LINE_COLOR, (world_house[5][0], world_house[5][1]),
                         [world_house[6][0], world_house[6][1]], 2)
        pygame.draw.line(screen, LINE_COLOR, (world_house[6][0], world_house[6][1]),
                         [world_house[7][0], world_house[7][1]], 2)
        pygame.draw.line(screen, LINE_COLOR, (world_house[7][0], world_house[7][1]),
                         [world_house[4][0], world_house[4][1]], 2)

        pygame.draw.line(screen, LINE_COLOR, (world_house[8][0], world_house[8][1]),
                         [world_house[9][0], world_house[9][1]], 2)

        pygame.draw.line(screen, LINE_COLOR, (world_house[7][0], world_house[7][1]),
                         [world_house[9][0], world_house[9][1]], 2)
        pygame.draw.line(screen, LINE_COLOR, (world_house[6][0], world_house[6][1]),
                         [world_house[9][0], world_house[9][1]], 2)

        pygame.draw.line(screen, LINE_COLOR, (world_house[4][0], world_house[4][1]),
                         [world_house[8][0], world_house[8][1]], 2)
        pygame.draw.line(screen, LINE_COLOR, (world_house[5][0], world_house[5][1]),
                         [world_house[8][0], world_house[8][1]], 2)

    v04x = world_house[4][0] - world_house[0][0]
    v04y = world_house[4][1] - world_house[0][1]

    v03x = world_house[3][0] - world_house[0][0]
    v03y = world_house[3][1] - world_house[0][1]

    nz2 = v04x*v03y-v04y*v03x
    if nz2 <= 0:
        pygame.draw.line(screen, LINE_COLOR, (world_house[0][0], world_house[0][1]),
                         [world_house[3][0], world_house[3][1]], 2)
        pygame.draw.line(screen, LINE_COLOR, (world_house[3][0], world_house[3][1]),
                         [world_house[7][0], world_house[7][1]], 2)
        pygame.draw.line(screen, LINE_COLOR, (world_house[7][0], world_house[7][1]),
                         [world_house[4][0], world_house[4][1]], 2)
        pygame.draw.line(screen, LINE_COLOR, (world_house[4][0], world_house[4][1]),
                         [world_house[0][0], world_house[0][1]], 2)

        pygame.draw.line(screen, LINE_COLOR, (world_house[7][0], world_house[7][1]),
                         [world_house[9][0], world_house[9][1]], 2)
        pygame.draw.line(screen, LINE_COLOR, (world_house[6][0], world_house[6][1]),
                         [world_house[9][0], world_house[9][1]], 2)

    else:
        pygame.draw.line(screen, LINE_COLOR, (world_house[1][0], world_house[1][1]),
                         [world_house[2][0], world_house[2][1]], 2)
        pygame.draw.line(screen, LINE_COLOR, (world_house[2][0], world_house[2][1]),
                         [world_house[6][0], world_house[6][1]], 2)
        pygame.draw.line(screen, LINE_COLOR, (world_house[6][0], world_house[6][1]),
                         [world_house[5][0], world_house[5][1]], 2)
        pygame.draw.line(screen, LINE_COLOR, (world_house[5][0], world_house[5][1]),
                         [world_house[1][0], world_house[1][1]], 2)

    v011x = world_house[1][0] - world_house[0][0]
    v011y = world_house[1][1] - world_house[0][0]
    v044x = world_house[4][0] - world_house[0][0]
    v044y = world_house[4][1] - world_house[0][1]

    nz3 = v011x*v044y-v011y*v044x

    if nz3 <= 0:
        pygame.draw.line(screen, LINE_COLOR, (world_house[0][0], world_house[0][1]),
                         [world_house[1][0], world_house[1][1]], 2)
        pygame.draw.line(screen, LINE_COLOR, (world_house[1][0], world_house[1][1]),
                         [world_house[5][0], world_house[5][1]], 2)
        pygame.draw.line(screen, LINE_COLOR, (world_house[5][0], world_house[5][1]),
                         [world_house[4][0], world_house[4][1]], 2)
        pygame.draw.line(screen, LINE_COLOR, (world_house[4][0], world_house[4][1]),
                         [world_house[0][0], world_house[0][1]], 2)

        pygame.draw.line(screen, LINE_COLOR, (world_house[4][0], world_house[4][1]),
                         [world_house[8][0], world_house[8][1]], 2)
        pygame.draw.line(screen, LINE_COLOR, (world_house[5][0], world_house[5][1]),
                         [world_house[8][0], world_house[8][1]], 2)

    else:
        pygame.draw.line(screen, LINE_COLOR, (world_house[3][0], world_house[3][1]),
                         [world_house[2][0], world_house[2][1]], 2)
        pygame.draw.line(screen, LINE_COLOR, (world_house[2][0], world_house[2][1]),
                         [world_house[6][0], world_house[6][1]], 2)
        pygame.draw.line(screen, LINE_COLOR, (world_house[6][0], world_house[6][1]),
                         [world_house[7][0], world_house[7][1]], 2)
        pygame.draw.line(screen, LINE_COLOR, (world_house[7][0], world_house[7][1]),
                         [world_house[3][0], world_house[3][1]], 2)

        pygame.draw.line(screen, LINE_COLOR, (world_house[7][0], world_house[7][1]),
                         [world_house[9][0], world_house[9][1]], 2)
        pygame.draw.line(screen, LINE_COLOR, (world_house[6][0], world_house[6][1]),
                         [world_house[9][0], world_house[9][1]], 2)

        pygame.draw.polygon(screen, LINE_COLOR, [tuple(k[:2]) for k in world_house[10:14]], 2)
        pygame.draw.polygon(screen, DOOR_COLOR, [tuple(k[:2]) for k in world_house[10:14]], 0)

        pygame.draw.polygon(screen, LINE_COLOR, [tuple(k[:2]) for k in world_house[14:18]], 2)
        pygame.draw.polygon(screen, WINDOW_COLOR, [tuple(k[:2]) for k in world_house[14:18]], 0)
        pygame.draw.polygon(screen, LINE_COLOR, [tuple(k[:2]) for k in world_house[18:22]], 2)
        pygame.draw.polygon(screen, WINDOW_COLOR, [tuple(k[:2]) for k in world_house[18:22]], 0)

        for window in (world_house[14:18], world_house[18:22]):
            pygame.draw.lines(screen, LINE_COLOR, True, [window[0][:2], window[2][:2]], 2)
            pygame.draw.lines(screen, LINE_COLOR, True, [window[1][:2], window[3][:2]], 2)


def draw_scene():
    calculate_transformations()
    global world_matrix
    if running:
        screen.fill(BACKGROUND_COLOR)

        world_house = [np.dot([x, y, z, 1], world_matrix) for x, y, a, z in house_vertices]
        define_position(world_house)

        pygame.display.flip()
        clock.tick(60)


while running:
    handle_events()
    draw_scene()

pygame.quit()
