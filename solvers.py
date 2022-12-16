""" Solvers """
from board import Board

class Solver:
    """ Generic solver class """
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
    row = 0
    column = 0
    reveled_board = []
    pairs_board = []

    def _next_move(self, board: Board) -> bool:
        """ move "cursor" to next position.
        Return True if it reaches the board end, else returns False """
        self.column += 1
        if self.column == board.columns:
            self.column = 0
            self.row += 1

        return self.row == board.rows

    def print_boards(self):
        """ print revealed and pair debug boards """
        for i in range(len(self.reveled_board)):
            print(f"{''.join(self.reveled_board[i])}\t{''.join(self.pairs_board[i])}")

    def solve(self, board: Board):
        """ solver board """
        self.row = 0
        self.column = 0
        known_pairs = {}
        next_pair = []
        self.reveled_board = [["."]*board.columns for _ in range(board.rows)]
        self.pairs_board = [["."]*board.columns for _ in range(board.rows)]
        while not board.complete:
            # ### DEBUG
            # print("known pairs:", known_pairs)
            # print("guesses", self.guesses, "wrong", self.wrong_guesses)
            # print("cursor:", self.row, self.column)
            # print("next pairs:", next_pair)
            # input()
            # ###

            # known moves
            if next_pair:
                first, second = next_pair.pop(0)
                # _ = board.flip_card(first[0], first[1])
                # _ = board.flip_card(second[0], second[1])
                flip = board.flip_card(first[0], first[1])
                self.pairs_board[first[0]][first[1]] = flip
                flip = board.flip_card(second[0], second[1])
                self.pairs_board[second[0]][second[1]] = flip

            # unknown/discover moves
            else:
                # first flip
                first_flip = board.flip_card(self.row, self.column)
                # print("first_flip", first_flip)
                first_pos = (self.row, self.column)

                self.reveled_board[self.row][self.column] = first_flip

                self._next_move(board)

                # check if it is a already known pair
                if first_flip in known_pairs:
                    # print("known pair:", first_flip, known_pairs[first_flip][0], known_pairs[first_flip][1])
                    # _ = board.flip_card(known_pairs[first_flip][0], known_pairs[first_flip][1])

                    second_flip = board.flip_card(
                        known_pairs[first_flip][0],
                        known_pairs[first_flip][1],
                    )

                    self.reveled_board[known_pairs[first_flip][0]][known_pairs[first_flip][1]] = second_flip
                    self.pairs_board[first_pos[0]][first_pos[1]] = first_flip
                    self.pairs_board[known_pairs[first_flip][0]][known_pairs[first_flip][1]] = second_flip
                else:
                    second_flip = board.flip_card(self.row, self.column)

                    self.reveled_board[self.row][self.column] = second_flip

                    # print("second_flip", second_flip)
                    if first_flip == second_flip:
                        # lucky guess
                        self.pairs_board[first_pos[0]][first_pos[1]] = first_flip
                        self.pairs_board[self.row][self.column] = second_flip
                    else:
                        # increase wrong guesses
                        self.wrong_guesses += 1

                        #check first move
                        if first_flip in known_pairs:
                            next_pair.append((first_pos, known_pairs[first_flip]))
                        else:
                            known_pairs[first_flip] = first_pos
                        # self.reveled_board[first_pos[0]][first_pos[1]] = first_flip
                        #check seconds move
                        if second_flip in known_pairs:
                            next_pair.append(((self.row, self.column), known_pairs[second_flip]))
                        else:
                            known_pairs[second_flip] = (self.row, self.column)
                        # self.reveled_board[self.row][self.column] = second_flip

                    # move cursor, if cursor reaches the end check if board is complete
                    if self._next_move(board) and not board.complete:
                        raise Exception("Board not completed. Something went wrong.")

            # Increase guesses
            self.guesses += 1

            # debug print
            # print(board.complete)
            # print(board.pair_founds)
            # print(board)
            # print()
            # self.print_boards()
