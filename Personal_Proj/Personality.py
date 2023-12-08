import pygame
import sys

# Инициализируем Pygame
pygame.init()

# Устанавливаем размеры окна
window_size = (800, 600)

# Создаем окно
screen = pygame.display.set_mode(window_size)

# Задаем заголовок окна
pygame.display.set_caption("Игрулька")

# Основной игровой цикл
while True:
    # Обрабатываем события
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Заполняем экран черным цветом
    screen.fill((0, 0, 205))

    # Обновляем экран
    pygame.display.flip()
