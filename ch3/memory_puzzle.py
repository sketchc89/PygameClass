#Memory Puzzle
#Al Sweigert
#Chris Sketch
#http://inventwithpython.com/pygame
#Released under "Simplified BSD" license
#Modified to use numpy arrays instead of 2d lists

import numpy as np
import random, pygame, sys
from pygame.locals import *

FPS = 30
WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480
REVEAL_SPEED = 8
BOX_SIZE = 40
GAP_SIZE = 10
BOARD_WIDTH = 10
BOARD_HEIGHT = 7
assert (BOARD_WIDTH * BOARD_HEIGHT) % 2 == 0, \
        'Board needs to have an even number of boxes for pairs of matches.'
X_MARGIN = int(WINDOW_WIDTH - (BOARD_WIDTH * (BOX_SIZE + GAP_SIZE)) / 2)
Y_MARGIN = int(WINDOW_HEIGHT - (BOARD_HEIGHT *  (BOX_SIZE + GAP_SIZE)) / 2)

GRAY =      (100, 100, 100)
NAVY_BLUE = ( 60,  60, 100)
WHITE =     (255, 255, 255)
RED =       (255,   0,   0)
GREEN =     (  0, 255,   0)
BLUE =      (  0,   0, 255)
YELLOW =    (255, 255, 255)
ORANGE =    (255, 128,   0)
PURPLE =    (255,   0, 255)
CYAN =      (  0, 255, 255)

BG_COLOR = NAVY_BLUE
LIGHT_BG_COLOR = GRAY
BOX_COLOR = WHITE
HIGHLIGHT_COLOR = BLUE

DONUT = 'donut'
SQUARE = 'square'
DIAMOND = 'diamond'
LINES = 'lines'
OVAL = 'oval'

ALL_COLORS = (RED, GREEN, BLUE, YELLOW, ORANGE, PURPLE, CYAN)
ALL_SHAPES = (DONUT, SQUARE, DIAMOND, LINES, OVAL)
assert len(ALL_COLORS) * len(ALL_SHAPES) * 2 >= BOARD_WIDTH * BOARD_HEIGHT, \
        'Board is too big for the number of shapes/colors defined.'

def main():
    global FPS_CLOCK, DISPLAY_SURF
    pygame.init()
    FPS_CLOCK = pygame.time.Clock()
    DISPLAY_SURF = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

    mouse_x = 0
    mouse_y = 0
    pygame.display.set_caption('Memory game')

    main_board = get_randomized_board()
    revealed_boxes = generate_revealed_boxes_data(False)
    first_selection = None

    DISPLAY_SURF.fill(BG_COLOR)
    start_game_animation(main_board)

    while True:
        mouse_clicked = False
        DISPLAY_SURF.fill(BG_COLOR)
        draw_board(main_board, revealed_boxes)

        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEMOTION:
                mouse_x, mouse_y = event.pos
            elif event.type == MOUSEBUTTONUP:
                mouse_x, mouse_y = event.pos
                mouse_clicked = True

            box_x = box_y = get_box_at_pixel(mouse_x, mouse_y)
            if box_x != None and box_y != None:
                if not revealed_boxes[box_x][box_y]:
                    draw_highlight_box(box_x, box_y)
                if not revealed_boxes[box_x][box_y] and mouse_clicked:
                    reveal_boxes_animation(main_board, [(box_x, box_y)])
                    revealed_boxes[box_x][box_y] = True
                    if first_selection == None:
                        first_selection = (box_x, box_y)
                    else:
                        icon1_shape, icon1_color = get_shape_color(main_board, 
                                                    first_selection[0], 
                                                    first_selection[1])
                        icon2_shape, icon2_color = get_shape_color(main_board,
                                                    second_selection[0],
                                                    second_selection[1])
                        if icon1_shape != icon2_shape or icon1_color != icon2_color:
                            pygame.time.wait(100)
                            cover_boxes_animation(main_board, 
                                    [(first_selection[0], first_selection[1]),
                                     (second_selection[0], second_selection[1])])
                            revealed_boxes[first_selection[0]][first_selection[1]] = False
                            revealed_boxes[box_x][box_y] = False
                        elif has_won(revealed_boxes):
                            game_won_animation(main_board)
                            pygame.time.wait(2000)

                            main_board = get_randomized_board()
                            revealed_boxes = generate_revealed_boxes_data(False)

                            draw_board(main_board, revealed_boxes)
                            pygame.display_update()
                            pygame.time.wait(1000)

                            start_game_animation(main_board)
                        first_selection = None
            pygame.display.update()
            FPS_CLOCK.tick(FPS)

def generate_revealed_boxes_data(val):
    '''Return a board with all boxes set to val

    Keyword arguments:
    val -- revealed or unrevealed, bool
    '''

    return np.ones((BOARD_WIDTH, BOARD_HEIGHT), dtype=bool)
