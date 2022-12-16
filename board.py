""" Simulate pair matching board """

import string
import random

LETTERS = string.ascii_uppercase

class Board:
    """ Pair macthing board game """
    rows = 0
    columns = 0
    size = 0
    complete = False
    last_flip = None
    pair_founds = set()
    complete_board = None
    show_board = None

    def set_board_size(self, row_size: int, column_size: int) -> None:
        """ Set board size. Raise erros if size too big or odd number """
        size = row_size * column_size
        # check size
        if size > 52:
            raise Exception("Board too large. Please choose a board with at max 52 \"cards\"")
        if size%2:
            raise Exception("Board size not even.")
        # set size
        self.rows = row_size
        self.columns = column_size
        self.size = size

    def generate_new_board(self):
        """ Generate a new board with current configurations """
        # get random pool of cards
        card_pool = random.sample(LETTERS, self.size//2) * 2
        random.shuffle(card_pool)

        # create board
        self.complete_board = []
        for _ in range(self.rows):
            line = [card_pool.pop() for _ in range(self.columns)]
            self.complete_board.append(line)

        # set auxilary variables
        self.reset()

    def reset(self):
        """ Reset board without changing pairs """
        self.complete = False
        self.last_flip = None
        self.pair_founds = set()

    def flip_card(self, row: int, column: int) -> str:
        """ Flip a card """
        if row >= self.rows:
            raise Exception("Rows index out of range.")
        if column >= self.columns:
            raise Exception("Columns index out of range.")

        flip = self.complete_board[row][column]

        # check if it is second flip of pair
        if self.last_flip:
            if self.last_flip == flip:
                # add to pair found
                self.pair_founds.add(flip)
                # check if game if complete
                if not self.complete and (len(self.pair_founds) == self.size//2):
                    self.complete = True
            # set last to None
            self.last_flip = None
        else:
            self.last_flip = flip

        return flip

    def __init__(self, rows, columns):
        self.set_board_size(rows, columns)
        self.generate_new_board()

    def __str__(self):
        return "\n".join(
            ["".join(line) for line in self.complete_board]
        )
