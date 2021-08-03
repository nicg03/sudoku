import random
import numpy as np
import pygame

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (192, 192, 192)
GREEN = (51, 165, 50)
RED = (255, 0, 0)

pygame.init()
screen = pygame.display.set_mode((450, 520))
pygame.display.set_caption('sudoku')

grid_pos = []
x = []
y = []
for i in range(0, 426):
    if (i + 25) % 50 == 0:
        x.append(i)
    if i % 50 == 0 or i == 0:
        if i > 400:
            pass
        else:
            y.append(i+1)
for i in y:
    for z in x:
        grid_pos.append((z, i))


def create_sudoku_pattern():
    f_line = list(range(1, 10))
    random.shuffle(f_line)
    count = 0
    for i in range(0, 3):
        for z in range(0, 3):
            if z == 1:
                for y in range(1, 10):
                    f_line.append(f_line[count:count + 9][y - 7])
                count += 9
            elif z == 2:
                for y in range(1, 10):
                    f_line.append(f_line[count:count + 9][y - 7])
                count += 9
            else:
                if i == 0:
                    pass
                else:
                    for y in range(1, 10):
                        f_line.append(f_line[count:count + 9][y - 2])
                    count += 9

    complete_sudoku_pattern = np.array(f_line).reshape((9, 9))
    not_complete_sudoku_pattern = complete_sudoku_pattern.copy()

    for i in range(0, 8):
        for a in range(2, random.randint(4, 5)):
            not_complete_sudoku_pattern[i, random.randint(0, 8)] = 0

    return [complete_sudoku_pattern, not_complete_sudoku_pattern]


sudoku_pattern = create_sudoku_pattern()
not_complete_sudoku_pattern = sudoku_pattern[1]
complete_sudoku_pattern = sudoku_pattern[0]


def draw_base():
    screen.fill(WHITE)

    pygame.draw.line(screen, BLACK, (0, 150), (500, 150), width=3)
    pygame.draw.line(screen, BLACK, (0, 300), (500, 300), width=3)
    pygame.draw.line(screen, BLACK, (0, 450), (500, 450), width=3)
    pygame.draw.line(screen, BLACK, (150, 0), (150, 450), width=3)
    pygame.draw.line(screen, BLACK, (300, 0), (300, 450), width=3)

    pygame.draw.line(screen, BLACK, (0, 50), (500, 50))
    pygame.draw.line(screen, BLACK, (0, 100), (500, 100))
    pygame.draw.line(screen, BLACK, (0, 200), (500, 200))
    pygame.draw.line(screen, BLACK, (0, 250), (500, 250))
    pygame.draw.line(screen, BLACK, (0, 350), (500, 350))
    pygame.draw.line(screen, BLACK, (0, 400), (500, 400))

    pygame.draw.line(screen, BLACK, (50, 0), (50, 450))
    pygame.draw.line(screen, BLACK, (100, 0), (100, 450))
    pygame.draw.line(screen, BLACK, (200, 0), (200, 450))
    pygame.draw.line(screen, BLACK, (250, 0), (250, 450))
    pygame.draw.line(screen, BLACK, (350, 0), (350, 450))
    pygame.draw.line(screen, BLACK, (400, 0), (400, 450))

    font = pygame.font.SysFont("Arial", 20)
    restart = font.render('RESTART', True, RED)
    screen.blit(restart, (50, 470))

    solve = font.render('SOLVE', True, RED)
    screen.blit(solve, (210, 470))

    new = font.render('NEW', True, RED)
    screen.blit(new, (360, 470))

grid_pos_dict = {}


def fill_with_incomplete_pattern():
    count = 0
    for i in range(0, 9):
        for z in range(0, 9):
            if not_complete_sudoku_pattern[i, z] == 0:
                pos = (grid_pos[count][0]-5, grid_pos[count][1]+10)
                grid_pos_dict[pos] = 0
                count += 1
                continue
            font = pygame.font.SysFont("Arial", 30)
            number = font.render('{}'.format(not_complete_sudoku_pattern[i, z]), True, BLACK)
            pos = (grid_pos[count][0]-5, grid_pos[count][1]+10)
            screen.blit(number, pos)
            grid_pos_dict[pos] = not_complete_sudoku_pattern[i, z]
            count += 1


def solve():
    count = 0
    for i in range(0, 9):
        for z in range(0, 9):
            if not_complete_sudoku_pattern[i, z] == 0:
                font = pygame.font.SysFont("Arial", 30)
                number = font.render('{}'.format(complete_sudoku_pattern[i, z]), True, GREEN)
                pos = (grid_pos[count][0] - 5, grid_pos[count][1] + 10)
                screen.blit(number, pos)
                count += 1
            else:
                count += 1


def fill_with_number(numbers_pos):
    if numbers_pos:
        for pos in numbers_pos.keys():
            font = pygame.font.SysFont("Arial", 30)
            number = font.render(numbers_pos[pos], True, BLACK)
            screen.blit(number, pos)

    else:
        pass


screen.fill(WHITE)

restart_button = pygame.draw.rect(screen, WHITE, (35, 470, 80, 30), 0)

font = pygame.font.SysFont("Arial", 20)
restart = font.render('RESTART', True, RED)
screen.blit(restart, (50, 470))

solve_button = pygame.draw.rect(screen, WHITE, (210, 470, 80, 30), 0)

font = pygame.font.SysFont("Arial", 20)
restart = font.render('SOLVE', True, RED)
screen.blit(restart, (210, 470))

new_button = pygame.draw.rect(screen, WHITE, (360, 470, 80, 30), 0)

font = pygame.font.SysFont("Arial", 20)
new = font.render('NEW', True, RED)
screen.blit(new, (360, 470))

numbers_pos = {}

draw_base()
ptr = pygame.Rect(1, 1, 49, 49)
pygame.draw.rect(screen, GRAY, ptr)
fill_with_incomplete_pattern()

go = True
while go:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            go = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if new_button.collidepoint(pygame.mouse.get_pos()):
                complete_sudoku_pattern, not_complete_sudoku_pattern = create_sudoku_pattern()
                draw_base()
                ptr = pygame.Rect(1, 1, 49, 49)
                pygame.draw.rect(screen, GRAY, ptr)
                fill_with_incomplete_pattern()
                numbers_pos = {}
            elif solve_button.collidepoint(pygame.mouse.get_pos()):
                solve()
            elif restart_button.collidepoint(pygame.mouse.get_pos()):
                draw_base()
                ptr = pygame.Rect(1, 1, 49, 49)
                pygame.draw.rect(screen, GRAY, ptr)
                fill_with_incomplete_pattern()
                numbers_pos = {}
        elif event.type == pygame.KEYDOWN:
            if event.key == 1073741903:  # freccia destra
                if ptr.topleft[0] >= 399:
                    pass
                else:
                    ptr.topleft = (ptr.topleft[0]+50, ptr.topleft[1])
                    draw_base()
                    pygame.draw.rect(screen, GRAY, ptr)
                    fill_with_incomplete_pattern()
                    fill_with_number(numbers_pos)
            elif event.key == 1073741904:  # freccia sinistra
                if ptr.topleft[0] <= 1:
                    pass
                else:
                    ptr.topleft = (ptr.topleft[0]-50, ptr.topleft[1])
                    draw_base()
                    pygame.draw.rect(screen, GRAY, ptr)
                    fill_with_incomplete_pattern()
                    fill_with_number(numbers_pos)
            elif event.key == 1073741906:  # freccia alta
                if ptr.topleft[1] <= 1:
                    pass
                else:
                    ptr.topleft = (ptr.topleft[0], ptr.topleft[1]-50)
                    draw_base()
                    pygame.draw.rect(screen, GRAY, ptr)
                    fill_with_incomplete_pattern()
                    fill_with_number(numbers_pos)
            elif event.key == 1073741905:  # freccia bassa
                if ptr.topleft[1] >= 399:
                    pass
                else:
                    ptr.topleft = (ptr.topleft[0], ptr.topleft[1]+50)
                    draw_base()
                    pygame.draw.rect(screen, GRAY, ptr)
                    fill_with_incomplete_pattern()
                    fill_with_number(numbers_pos)
            elif event.key == 8:  # tasto cancella
                try:
                    n_pos = (ptr.midtop[0] - 5, ptr.midtop[1] + 10)
                    numbers_pos[n_pos] = ''
                    draw_base()
                    pygame.draw.rect(screen, GRAY, ptr)
                    fill_with_incomplete_pattern()
                    fill_with_number(numbers_pos)
                except:
                    pass
            else:
                if event.unicode == '1':
                    n_pos = (ptr.midtop[0]-5, ptr.midtop[1]+10)
                    if grid_pos_dict[n_pos] == 0:
                        numbers_pos[n_pos] = '1'
                        fill_with_number(numbers_pos)
                elif event.unicode == '2':
                    n_pos = (ptr.midtop[0]-5, ptr.midtop[1]+10)
                    if grid_pos_dict[n_pos] == 0:
                        numbers_pos[n_pos] = '2'
                        fill_with_number(numbers_pos)
                elif event.unicode == '3':
                    n_pos = (ptr.midtop[0] - 5, ptr.midtop[1] + 10)
                    if grid_pos_dict[n_pos] == 0:
                        numbers_pos[n_pos] = '3'
                        fill_with_number(numbers_pos)
                elif event.unicode == '4':
                    n_pos = (ptr.midtop[0]-5, ptr.midtop[1]+10)
                    if grid_pos_dict[n_pos] == 0:
                        numbers_pos[n_pos] = '4'
                        fill_with_number(numbers_pos)
                elif event.unicode == '5':
                    n_pos = (ptr.midtop[0]-5, ptr.midtop[1]+10)
                    if grid_pos_dict[n_pos] == 0:
                        numbers_pos[n_pos] = '5'
                        fill_with_number(numbers_pos)
                elif event.unicode == '6':
                    n_pos = (ptr.midtop[0]-5, ptr.midtop[1]+10)
                    if grid_pos_dict[n_pos] == 0:
                        numbers_pos[n_pos] = '6'
                        fill_with_number(numbers_pos)
                elif event.unicode == '7':
                    n_pos = (ptr.midtop[0]-5, ptr.midtop[1]+10)
                    if grid_pos_dict[n_pos] == 0:
                        numbers_pos[n_pos] = '7'
                        fill_with_number(numbers_pos)
                elif event.unicode == '8':
                    n_pos = (ptr.midtop[0] - 5, ptr.midtop[1] + 10)
                    if grid_pos_dict[n_pos] == 0:
                        numbers_pos[n_pos] = '8'
                        fill_with_number(numbers_pos)
                elif event.unicode == '9':
                    n_pos = (ptr.midtop[0]-5, ptr.midtop[1]+10)
                    if grid_pos_dict[n_pos] == 0:
                        numbers_pos[n_pos] = '9'
                        fill_with_number(numbers_pos)
                else:
                    pass
        else:
            pass

    pygame.display.flip()

pygame.quit()

