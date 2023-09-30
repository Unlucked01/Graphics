import pygame
import numpy as np
import math

pygame.init()

WIDTH, HEIGHT = 800, 600
BACKGROUND_COLOR = (0, 0, 0)  # Черный цвет фона
LINE_COLOR = (255, 255, 255)  # Белый цвет линий
HOUSE_COLOR = (0, 0, 0)  # Красный цвет дома
DOOR_COLOR = (100, 50, 0)  # Цвет двери
WINDOW_COLOR = (100, 100, 255)  # Цвет окон
HOUSE_WIDTH = 200
HOUSE_HEIGHT = 200
ROOF_HEIGHT = 100
DOOR_WIDTH = 40
DOOR_HEIGHT = 100
WINDOW_WIDTH = 40
WINDOW_HEIGHT = 40
WINDOW_OFFSET = 45
rotation_angle = 0.01
translation_x = 0
translation_y = 0
translation_z = 0
i = 2
sx, sy, sz = 1, 1, 1
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Lab2")

house_vertices = [
    (-HOUSE_WIDTH / i, -HOUSE_HEIGHT / i, 0, 1),
    (HOUSE_WIDTH / i, -HOUSE_HEIGHT / i, 0, 1),
    (HOUSE_WIDTH / i, 0, 0, 1),
    (-HOUSE_WIDTH / i, 0, 0, 1)
]
roof_vertices = [
    (HOUSE_WIDTH / i, 0, 0, 1),
    (0, ROOF_HEIGHT, 0, 1),
    (-HOUSE_WIDTH / i, 0, 0, 1),
    (0, 0, 0, 1)
]
house_vertices_2 = [
    (-HOUSE_WIDTH / i, -HOUSE_HEIGHT / i, 200, 1),
    (HOUSE_WIDTH / i, -HOUSE_HEIGHT / i, 200, 1),
    (HOUSE_WIDTH / i, 0, 200, 1),
    (-HOUSE_WIDTH / i, 0, 200, 1)
]
roof_vertices_2 = [
    (HOUSE_WIDTH / i, 0, 200, 1),
    (0, ROOF_HEIGHT, 200, 1),
    (-HOUSE_WIDTH / i, 0, 200, 1),
    (0, 0, 0, 1)
]
door_vertices = [
    (-DOOR_WIDTH / i, -HOUSE_HEIGHT / i, 0, 1),
    (DOOR_WIDTH / i, -HOUSE_HEIGHT / i, 0, 1),
    (DOOR_WIDTH / i, 0, 0, 1),
    (-DOOR_WIDTH / i, 0, 0, 1)
]
left_window_vertices = [
    (-WINDOW_WIDTH / i - WINDOW_OFFSET, -HOUSE_HEIGHT / i + WINDOW_HEIGHT / i + WINDOW_OFFSET, 0, 1),
    (WINDOW_WIDTH / i - WINDOW_OFFSET, -HOUSE_HEIGHT / i + WINDOW_HEIGHT / i + WINDOW_OFFSET, 0, 1),
    (WINDOW_WIDTH / i - WINDOW_OFFSET, -HOUSE_HEIGHT / i + WINDOW_HEIGHT + WINDOW_OFFSET, 0, 1),
    (-WINDOW_WIDTH / i - WINDOW_OFFSET, -HOUSE_HEIGHT / i + WINDOW_HEIGHT + WINDOW_OFFSET, 0, 1)
]
right_window_vertices = [
    (-WINDOW_WIDTH / i + WINDOW_OFFSET, -HOUSE_HEIGHT / i + WINDOW_HEIGHT / i + WINDOW_OFFSET, 0, 1),
    (WINDOW_WIDTH / i + WINDOW_OFFSET, -HOUSE_HEIGHT / i + WINDOW_HEIGHT / i + WINDOW_OFFSET, 0, 1),
    (WINDOW_WIDTH / i + WINDOW_OFFSET, -HOUSE_HEIGHT / i + WINDOW_HEIGHT + WINDOW_OFFSET, 0, 1),
    (-WINDOW_WIDTH / i + WINDOW_OFFSET, -HOUSE_HEIGHT / i + WINDOW_HEIGHT + WINDOW_OFFSET, 0, 1)
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
# z
rotation_matrix_x = np.array([
    [math.cos(rotation_angle), 0, -math.sin(rotation_angle), 0],
    [0, 1, 0, 0],
    [math.sin(rotation_angle), 0, math.cos(rotation_angle), 0],
    [0, 0, 1, 0]
])
# x
rotation_matrix_y = np.array([
    [1, 0, 0, 0],
    [0, math.cos(rotation_angle), math.sin(rotation_angle), 0],
    [0, -math.sin(rotation_angle), math.cos(rotation_angle), 0],
    [0, 0, 0, 1]
])
# z
rotation_matrix_z = np.array([
    [math.cos(rotation_angle), -math.sin(rotation_angle), 0, 0],
    [math.sin(rotation_angle), math.cos(rotation_angle), 0, 0],
    [0, 0, 1, 0],
    [0, 0, 0, 1]
])
clock = pygame.time.Clock()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        translation_x -= 0.02  # влево
    if keys[pygame.K_RIGHT]:
        translation_x += 0.02  # вправо
    if keys[pygame.K_UP]:
        translation_y -= 0.02  # вверх
    if keys[pygame.K_DOWN]:
        translation_y += 0.02  # вниз
    if keys[pygame.K_q]:
        translation_z += 0.02
    if keys[pygame.K_a]:
        translation_z -= 0.02
    if keys[pygame.K_z]:
        rotation_angle = 0
    if keys[pygame.K_d]:
        rotation_angle += 0.01
    if keys[pygame.K_w]:
        sx *= 1.001
        sy *= 1.001
        sz *= 1.001
        scale_matrix = np.array([
            [sx, 0, 0, 0],
            [0, sy, 0, 0],
            [0, 0, sz, 0],
            [0, 0, 0, 1]
        ])
    if keys[pygame.K_s]:
        sx /= 1.001
        sy /= 1.001
        sz /= 1.001
        scale_matrix = np.array([
            [sx, 0, 0, 0],
            [0, sy, 0, 0],
            [0, 0, sz, 0],
            [0, 0, 0, 1]
        ])
    if keys[pygame.K_ESCAPE]:
        running = False
    if running:
        screen.fill(BACKGROUND_COLOR)

        world_matrix_with_translation = world_matrix.copy()
        world_matrix_with_translation[0, 0] += translation_x
        world_matrix_with_translation[1, 1] += translation_y
        world_matrix_with_translation[2, 2] += translation_z

        house_vertices = [np.dot([x, y, z, 1], rotation_matrix_x) for x, y, z, a in house_vertices]
        roof_vertices = [np.dot([x, y, z, 1], rotation_matrix_x) for x, y, z, a in roof_vertices]
        door_vertices = [np.dot([x, y, z, 1], rotation_matrix_x) for x, y, z, a in door_vertices]
        left_window_vertices = [np.dot([x, y, z, 1], rotation_matrix_x) for x, y, z, a in left_window_vertices]
        right_window_vertices = [np.dot([x, y, z, 1], rotation_matrix_x) for x, y, z, a in right_window_vertices]

        house_vertices_2 = [np.dot([x, y, z, 1], rotation_matrix_x) for x, y, z, a in house_vertices_2]
        roof_vertices_2 = [np.dot([x, y, z, 1], rotation_matrix_x) for x, y, z, a in roof_vertices_2]

        house_vertices = [np.dot([x, y, z, 1], rotation_matrix_y) for x, y, z, a in house_vertices]
        roof_vertices = [np.dot([x, y, z, 1], rotation_matrix_y) for x, y, z, a in roof_vertices]
        door_vertices = [np.dot([x, y, z, 1], rotation_matrix_y) for x, y, z, a in door_vertices]
        left_window_vertices = [np.dot([x, y, z, 1], rotation_matrix_y) for x, y, z, a in left_window_vertices]
        right_window_vertices = [np.dot([x, y, z, 1], rotation_matrix_y) for x, y, z, a in right_window_vertices]

        house_vertices_2 = [np.dot([x, y, z, 1], rotation_matrix_y) for x, y, z, a in house_vertices_2]
        roof_vertices_2 = [np.dot([x, y, z, 1], rotation_matrix_y) for x, y, z, a in roof_vertices_2]

        # house_vertices = [np.dot([x, y, z, 1], rotation_matrix_z) for x, y, z, a in house_vertices]
        # door_vertices = [np.dot([x, y, z, 1], rotation_matrix_z) for x, y, z, a in door_vertices]
        # left_window_vertices = [np.dot([x, y, z, 1], rotation_matrix_z) for x, y, z, a in left_window_vertices]
        # right_window_vertices = [np.dot([x, y, z, 1], rotation_matrix_z) for x, y, z, a in right_window_vertices]
        #
        # house_vertices_2 = [np.dot([x, y, z, 1], rotation_matrix_z) for x, y, z, a in house_vertices_2]
        # roof_vertices_2 = [np.dot([x, y, z, 1], rotation_matrix_z) for x, y, z, a in roof_vertices_2]

        house_vertices = [np.dot([x, y, z, 1], scale_matrix) for x, y, z, a in house_vertices]
        roof_vertices = [np.dot([x, y, z, 1], scale_matrix) for x, y, z, a in roof_vertices]
        door_vertices = [np.dot([x, y, z, 1], scale_matrix) for x, y, z, a in door_vertices]
        left_window_vertices = [np.dot([x, y, z, 1], scale_matrix) for x, y, z, a in left_window_vertices]
        right_window_vertices = [np.dot([x, y, z, 1], scale_matrix) for x, y, z, a in right_window_vertices]

        world_house = [np.dot([x, y, z, 1], world_matrix_with_translation) for x, y, z, a in house_vertices]
        world_roof = [np.dot([x, y, z, 1], world_matrix_with_translation) for x, y, z, a in roof_vertices]
        world_door = [np.dot([x, y, z, 1], world_matrix_with_translation) for x, y, z, a in door_vertices]
        world_left_window = [np.dot([x, y, z, 1], world_matrix_with_translation) for x, y, z, a in left_window_vertices]
        world_right_window = [np.dot([x, y, z, 1], world_matrix_with_translation) for x, y, z, a in right_window_vertices]

        pygame.draw.polygon(screen, LINE_COLOR, [tuple(i[:2]) for i in world_house], 2)
        pygame.draw.polygon(screen, LINE_COLOR, [tuple(i[:2]) for i in world_roof[:3]], 2)
        pygame.draw.polygon(screen, DOOR_COLOR, [tuple(i[:2]) for i in world_door], 0)
        pygame.draw.polygon(screen, LINE_COLOR, [tuple(i[:2]) for i in world_door], 2)
        pygame.draw.polygon(screen, WINDOW_COLOR, [tuple(i[:2]) for i in world_left_window], 0)
        pygame.draw.polygon(screen, LINE_COLOR, [tuple(i[:2]) for i in world_left_window], 2)
        pygame.draw.polygon(screen, WINDOW_COLOR, [tuple(i[:2]) for i in world_right_window], 0)
        pygame.draw.polygon(screen, LINE_COLOR, [tuple(i[:2]) for i in world_right_window], 2)

        for window in (world_left_window, world_right_window):
            pygame.draw.lines(screen, LINE_COLOR, True, [window[0][:2], window[2][:2]], 2)
            pygame.draw.lines(screen, LINE_COLOR, True, [window[1][:2], window[3][:2]], 2)

        house_vertices_2 = [np.dot([x, y, z, 1], scale_matrix) for x, y, z, a in house_vertices_2]
        roof_vertices_2 = [np.dot([x, y, z, 1], scale_matrix) for x, y, z, a in roof_vertices_2]

        world_house_2 = [np.dot([x, y, z, 1], world_matrix_with_translation) for x, y, z, a in house_vertices_2]
        world_roof_2 = [np.dot([x, y, z, 1], world_matrix_with_translation) for x, y, z, a in roof_vertices_2]

        pygame.draw.polygon(screen, LINE_COLOR, [tuple(i[:2]) for i in world_house_2[:5]], 2)
        pygame.draw.polygon(screen, LINE_COLOR, [tuple(i[:2]) for i in world_roof_2[:3]], 2)

        for i in range(4):
            pygame.draw.line(screen, LINE_COLOR, tuple(world_house[i][:2]), tuple(world_house_2[i][:2]), 2)  # Connect the houses

        pygame.draw.line(screen,LINE_COLOR, world_roof[1][:2], world_roof_2[1][:2], 2)
        pygame.display.flip()
        clock.tick(60)  # 60 FPS

pygame.quit()
