'''Модуль, описывающий логику игры "Змейка".'''
from random import choice

import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 20

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


class GameObject:
    '''Базовый класс, от которого наследуются другие игровые объекты.'''

    def __init__(self) -> None:
        '''Метод, инициализирующий объект класса GameObject.'''
        self.position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.body_color = None

    def draw(self) -> None:
        '''
        Это абстрактный метод,
        который предназначен для переопределения в дочерних классах.
        Этот метод должен определять,
        как объект будет отрисовываться на экране.
        '''
        pass


class Apple(GameObject):
    '''Класс, описывающий игровой объект- яблоко.'''

    def __init__(self) -> None:
        '''Метод, инициализирующий объект класса Apple.'''
        super().__init__()
        self.body_color = APPLE_COLOR
        self.randomize_position(self.position)

    def randomize_position(self, snake_positions) -> None:
        '''
        Метод, устанавливающий случайное
        положение яблока на игровом поле.
        '''
        available_positions = [
            (x * GRID_SIZE, y * GRID_SIZE)
            for x in range(GRID_WIDTH)
            for y in range(GRID_HEIGHT)
            if (x * GRID_SIZE, y * GRID_SIZE) not in snake_positions
        ]
        if available_positions:
            self.position = choice(available_positions)

    def draw(self):
        '''Метод, отрисовывающий яблоко на игровом поле.'''
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    '''Класс, описывающий игровой объект- змейку.'''

    def __init__(self) -> None:
        '''Метод, инициализирующий объект класса Snake.'''
        super().__init__()
        self.length = 1
        self.positions = [self.position]
        self.direction = RIGHT
        self.next_direction = None
        self.body_color = SNAKE_COLOR

    def update_direction(self) -> None:
        '''Метод, обновляющий направление движения змейки.'''
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self, apple=None) -> None:
        '''Метод, обновляющий позицию змейки.'''
        cur_head = self.get_head_position()
        new_position = (
            (cur_head[0] + self.direction[0] * GRID_SIZE) % SCREEN_WIDTH,
            (cur_head[1] + self.direction[1] * GRID_SIZE) % SCREEN_HEIGHT
        )

        if new_position not in self.positions[2:]:
            self.positions.insert(0, new_position)
            if apple:
                self.length += 1
            if len(self.positions) > self.length:
                self.positions.pop()
        else:
            self.reset()

    def draw(self) -> None:
        '''Метод, отрисовывающий змейку на экране.'''
        for position in self.positions:
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

    def get_head_position(self) -> tuple:
        '''Метод, возвращающий позицию головы змейки.'''
        return self.positions[0]

    def get_snake_positions(self) -> list[tuple]:
        '''Метод, возвращающий позиции змейки в массиве.'''
        return self.positions

    def reset(self) -> None:
        '''
        Метод, сбрасывающий змейку
        в начальное состояние после столкновения с собой.
        '''
        self.length = 1
        self.positions = [self.position]
        self.direction = choice([UP, DOWN, LEFT, RIGHT])
        screen.fill(BOARD_BACKGROUND_COLOR)


def handle_keys(game_object) -> None:
    '''
    Функция, обрабатывающая нажатия клавиш,
    чтобы изменить направление движения змейки.
    '''
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    '''Функция, запускающая игровой процесс.'''
    pygame.init()
    snake = Snake()
    apple = Apple()

    while True:
        clock.tick(SPEED)
        screen.fill(BOARD_BACKGROUND_COLOR)

        apple.draw()
        snake.draw()

        handle_keys(snake)
        snake.update_direction()

        if snake.get_head_position() == apple.position:
            snake.move(apple)
            apple.randomize_position(snake.get_snake_positions())
        else:
            snake.move()

        pygame.display.update()


if __name__ == '__main__':
    main()
