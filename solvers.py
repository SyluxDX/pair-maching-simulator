""" Solvers """
import random

from board import Board

class Solver:
    """ Generic solver class """
    guesses: int
    wrong_guesses: int

    def __init__(self) -> None:
        self.guesses = 0
        self.wrong_guesses = 0

    def __str__(self) -> str:
        return f"{self.guesses};{self.wrong_guesses}"

    def reset(self) -> None:
        """ Reset guesses counters """
        self.guesses = 0
        self.wrong_guesses = 0

class SequentialSolver(Solver):
    """ Sequential Solver """
    name = "Sequential Solver"
    row: int
    column: int

    def _next_move(self, board: Board) -> bool:
        """ move "cursor" to next position.
        Return True if it reaches the board end, else returns False """
        self.column += 1
        if self.column == board.columns:
            self.column = 0
            self.row += 1

        return self.row == board.rows

    def solve(self, board: Board) -> None:
        """ solver board """
        self.row = 0
        self.column = 0
        known_pairs = {}
        next_pair = []

        while not board.complete:
            # known moves
            if next_pair:
                first, second = next_pair.pop(0)
                _ = board.flip_card(first[0], first[1])
                _ = board.flip_card(second[0], second[1])

            # unknown/discover moves
            else:
                # first flip
                first_flip = board.flip_card(self.row, self.column)
                first_pos = (self.row, self.column)

                self._next_move(board)

                # check if it is a already known pair
                if first_flip in known_pairs:
                    second_flip = board.flip_card(
                        known_pairs[first_flip][0],
                        known_pairs[first_flip][1],
                    )

                else:
                    second_flip = board.flip_card(self.row, self.column)

                    if first_flip == second_flip:
                        # lucky guess
                        pass
                    else:
                        # increase wrong guesses
                        self.wrong_guesses += 1

                        #check first move
                        if first_flip in known_pairs:
                            next_pair.append((first_pos, known_pairs[first_flip]))
                        else:
                            known_pairs[first_flip] = first_pos
                        #check seconds move
                        if second_flip in known_pairs:
                            next_pair.append(((self.row, self.column), known_pairs[second_flip]))
                        else:
                            known_pairs[second_flip] = (self.row, self.column)

                    # move cursor, if cursor reaches the end check if board is complete
                    if self._next_move(board) and not board.complete:
                        raise Exception("Board not completed. Something went wrong.")

            # Increase guesses
            self.guesses += 1

class RandomSolver(Solver):
    """ Random selection Solver """
    name = "Random Solver"
    row: int
    column: int
    reveled_board: list
    pairs_board: list

    ## DEBUG FUNCTION ###
    def debug_print(self) -> None:
        """ debug print """
        for i, reveled_row in enumerate(self.reveled_board):
            print(f"{''.join(reveled_row)}\t{''.join(self.pairs_board[i])}")
    #####################
    
    def _generate_random_moves(self, rows: int , columns: int) -> list:
        """ Generate list of random moves/picks """
        moves = [(x, y) for x in range(rows) for y in range(columns)]
        random.shuffle(moves)
        return moves

    def solve(self, board: Board) -> None:
        """ solver board """
        # self.row = 0
        # self.column = 0
        known_pairs = {}
        next_pair = []
        moves = self._generate_random_moves(board.rows, board.columns)
        #### DEBUG VARIABLES ####
        self.reveled_board = [["."]*board.columns for _ in range(board.rows)]
        self.pairs_board = [["."]*board.columns for _ in range(board.rows)]
        
        while not board.complete:
            # known moves
            if next_pair:
                first, second = next_pair.pop(0)
                flip = board.flip_card(first[0], first[1])
                self.pairs_board[first[0]][first[1]] = flip
                flip = board.flip_card(second[0], second[1])
                self.pairs_board[second[0]][second[1]] = flip

            # unknown/discover moves
            else:
                # first flip
                # Get next move
                row, column = moves.pop(0)
                first_flip = board.flip_card(row, column)
                # print("first_flip", first_flip)
                first_pos = (row, column)

                self.reveled_board[row][column] = first_flip

                # check if it is a already known pair
                if first_flip in known_pairs:
                    second_flip = board.flip_card(
                        known_pairs[first_flip][0],
                        known_pairs[first_flip][1],
                    )

                    self.reveled_board[known_pairs[first_flip][0]][known_pairs[first_flip][1]] = second_flip
                    self.pairs_board[first_pos[0]][first_pos[1]] = first_flip
                    self.pairs_board[known_pairs[first_flip][0]][known_pairs[first_flip][1]] = second_flip
                else:
                    # Get next move
                    row, column = moves.pop(0)
                    second_flip = board.flip_card(row, column)

                    self.reveled_board[row][column] = second_flip

                    if first_flip == second_flip:
                        # lucky guess
                        self.pairs_board[first_pos[0]][first_pos[1]] = first_flip
                        self.pairs_board[row][column] = second_flip
                    else:
                        # increase wrong guesses
                        self.wrong_guesses += 1

                        #check first move
                        if first_flip in known_pairs:
                            next_pair.append((first_pos, known_pairs[first_flip]))
                        else:
                            known_pairs[first_flip] = first_pos
                        #check seconds move
                        if second_flip in known_pairs:
                            next_pair.append(((row, column), known_pairs[second_flip]))
                        else:
                            known_pairs[second_flip] = (row, column)

                    # move cursor, if cursor reaches the end check if board is complete
                    if len(moves) == 0 and not board.complete:
                        raise Exception("Board not completed. Something went wrong.")

            # Increase guesses
            self.guesses += 1
