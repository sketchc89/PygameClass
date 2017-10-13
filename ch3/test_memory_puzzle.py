import memory_puzzle as mp
import numpy as np

def test_board_even():
    '''Board needs to have an even number of boxes for pairs of matches.'''
    assert (mp.BOARD_WIDTH * mp.BOARD_HEIGHT) % 2 == 0

def test_board_size():
    '''Board is too big for the number of shapes/colors defined'''
    assert len(mp.ALL_COLORS) * len(mp.ALL_SHAPES) * 2 >= mp.BOARD_WIDTH * mp.BOARD_HEIGHT

def test_generate_revealed_false():
    '''Boxes initialized to unrevealed'''
    revealed_boxes = mp.generate_revealed_boxes_data(False)
    assert not np.array(revealed_boxes).all()

def test_randomized_board():
    '''Check that each shape and color combination is 2 times'''
    assert False
