import pygame
import numpy as np
import math

# Инициализация Pygame
pygame.init()

# Константы
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
# Угол поворота в радианах
rotation_angle = 0.01
# Текущее смещение объектов
translation_x = 0
translation_y = 0
# Коэффициент масштабирования
i = 2
sx, sy = 1, 1

# Создание окна
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Отрисовка дома")

house_vertices = [
    (-HOUSE_WIDTH / i, -HOUSE_HEIGHT / i),
    (HOUSE_WIDTH / i, -HOUSE_HEIGHT / i),
    (HOUSE_WIDTH / i, 0),
    (0, ROOF_HEIGHT),
    (-HOUSE_WIDTH / i, 0)
]

door_vertices = [
    (-DOOR_WIDTH / i, -HOUSE_HEIGHT / i),
    (DOOR_WIDTH / i, -HOUSE_HEIGHT / i),
    (DOOR_WIDTH / i, 0),
    (-DOOR_WIDTH / i, 0)
]

left_window_vertices = [
    (-WINDOW_WIDTH / i - WINDOW_OFFSET, -HOUSE_HEIGHT / i + WINDOW_HEIGHT / i + WINDOW_OFFSET),
    (WINDOW_WIDTH / i - WINDOW_OFFSET, -HOUSE_HEIGHT / i + WINDOW_HEIGHT / i + WINDOW_OFFSET),
    (WINDOW_WIDTH / i - WINDOW_OFFSET, -HOUSE_HEIGHT / i + WINDOW_HEIGHT + WINDOW_OFFSET),
    (-WINDOW_WIDTH / i - WINDOW_OFFSET, -HOUSE_HEIGHT / i + WINDOW_HEIGHT + WINDOW_OFFSET)
]

right_window_vertices = [
    (-WINDOW_WIDTH / i + WINDOW_OFFSET, -HOUSE_HEIGHT / i + WINDOW_HEIGHT / i + WINDOW_OFFSET),
    (WINDOW_WIDTH / i + WINDOW_OFFSET, -HOUSE_HEIGHT / i + WINDOW_HEIGHT / i + WINDOW_OFFSET),
    (WINDOW_WIDTH / i + WINDOW_OFFSET, -HOUSE_HEIGHT / i + WINDOW_HEIGHT + WINDOW_OFFSET),
    (-WINDOW_WIDTH / i + WINDOW_OFFSET, -HOUSE_HEIGHT / i + WINDOW_HEIGHT + WINDOW_OFFSET)
]

world_matrix = np.array([
    [1, 0, WIDTH / 2],
    [0, -1, HEIGHT / 2]
])

translation_matrix = np.array([
    [1, 0, 0],
    [0, 1, 0]
])

scale_matrix = np.array([
        [sx, 0],
        [0, sy]
])

rotation_matrix = np.array([
    [math.cos(rotation_angle), -math.sin(rotation_angle)],
    [math.sin(rotation_angle), math.cos(rotation_angle)]
])

clock = pygame.time.Clock()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        translation_x -= 2  # Смещение влево
    if keys[pygame.K_RIGHT]:
        translation_x += 2  # Смещение вправо
    if keys[pygame.K_UP]:
        translation_y -= 2  # Смещение вверх
    if keys[pygame.K_DOWN]:
        translation_y += 2  # Смещение вниз
    if keys[pygame.K_1]:
        rotation_angle -= 0.01
    if keys[pygame.K_z]:
        rotation_angle = 0
    if keys[pygame.K_d]:
        rotation_angle += 0.01
    if keys[pygame.K_w]:
        sx *= 1.001
        sy *= 1.001
        scale_matrix = np.array([
            [sx, 0],
            [0, sy]
        ])
    if keys[pygame.K_s]:
        sx /= 1.001
        sy /= 1.001
        scale_matrix = np.array([
            [sx, 0],
            [0, sy]
        ])
    if keys[pygame.K_ESCAPE]:
        running = False

    # Очистка экрана
    if running:
        screen.fill(BACKGROUND_COLOR)

        world_matrix_with_translation = world_matrix.copy()
        world_matrix_with_translation[0, 2] += translation_x
        world_matrix_with_translation[1, 2] += translation_y

        house_vertices = [tuple(np.dot([x, y], rotation_matrix)) for x, y in house_vertices]
        door_vertices = [tuple(np.dot([x, y], rotation_matrix)) for x, y in door_vertices]
        left_window_vertices = [tuple(np.dot([x, y], rotation_matrix)) for x, y in left_window_vertices]
        right_window_vertices = [tuple(np.dot([x, y], rotation_matrix)) for x, y in right_window_vertices]

        house_vertices = [tuple(np.dot([x, y], scale_matrix)) for x, y in house_vertices]
        door_vertices = [tuple(np.dot([x, y], scale_matrix)) for x, y in door_vertices]
        left_window_vertices = [tuple(np.dot([x, y], scale_matrix)) for x, y in left_window_vertices]
        right_window_vertices = [tuple(np.dot([x, y], scale_matrix)) for x, y in right_window_vertices]

        # Преобразование координат с учетом смещения
        world_house = [tuple(np.dot([x, y, 1], world_matrix_with_translation.T)) for x, y in house_vertices]
        world_door = [tuple(np.dot([x, y, 1], world_matrix_with_translation.T)) for x, y in door_vertices]
        world_left_window = [tuple(np.dot([x, y, 1], world_matrix_with_translation.T)) for x, y in left_window_vertices]
        world_right_window = [tuple(np.dot([x, y, 1], world_matrix_with_translation.T)) for x, y in
                              right_window_vertices]

        pygame.draw.polygon(screen, LINE_COLOR, world_house[:5], 2) #house
        pygame.draw.polygon(screen, LINE_COLOR, [world_house[2], world_house[4]], 2) #roof
        pygame.draw.polygon(screen, DOOR_COLOR, world_door, 0)
        pygame.draw.polygon(screen, LINE_COLOR, world_door, 2)
        pygame.draw.polygon(screen, WINDOW_COLOR, world_left_window, 0)
        pygame.draw.polygon(screen, LINE_COLOR, world_left_window, 2)
        pygame.draw.polygon(screen, WINDOW_COLOR, world_right_window, 0)
        pygame.draw.polygon(screen, LINE_COLOR, world_right_window, 2)

        for window in (world_left_window, world_right_window):
            pygame.draw.lines(screen, LINE_COLOR, True, [window[0], window[2]], 2)
            pygame.draw.lines(screen, LINE_COLOR, True, [window[1], window[3]], 2)

        # Обновление экрана
        pygame.display.flip()

        # Ограничение частоты кадров
        clock.tick(60)  # 60 FPS

# Завершение Pygame
pygame.quit()
