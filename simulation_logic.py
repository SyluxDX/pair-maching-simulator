""" Simulate pair matching board game """
import argparse
from datetime import datetime

import board
import solvers

if __name__ == "__main__":
    _parser = argparse.ArgumentParser(description=
        ("Simulate pair matching games, for testing "
        "differents solver and find the best way to beat it"
        ))
    _parser.add_argument(
        "-s",
        "--board-size",
        type = int,
        nargs = "+",
        help = ("Board size, if singe size if profided a square board is created. "
        "Board must have an even number of cards"),
        )
    _parser.add_argument(
        "-n",
        "--number-boards",
        type = int,
        default = 100,
        help = "Number of boards to Simulate against",
        )

    ARGS = _parser.parse_args()

    if ARGS.board_size:
        if len(ARGS.board_size) == 1:
            ROWS = COLUMNS = ARGS.board_size
        elif len(ARGS.board_size) == 2:
            ROWS = ARGS.board_size[0]
            COLUMNS = ARGS.board_size[1]
        else:
            raise Exception("Board size argument can have 2 values maximum")
    else:
        ROWS = COLUMNS = 6

    # Create board with specified size
    board = board.Board(ROWS, COLUMNS)

    filename = f"{{}}-{ARGS.number_boards}-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}.csv"
    # create outputs files pointers
    with open(filename.format("sequential"), "w", encoding="utf8") as seqfp:

        solvers_list = [
            (solvers.SequentialSolver(), seqfp)
        ]
        # Add header to output files
        for _, fp in solvers_list:
            fp.write("Number_guesses;wrong_guesses\n")
        # Simulations
        for solver, fp in solvers_list:
            for n in range(ARGS.number_boards):
                print(f"Simulating {n+1}/{ARGS.number_boards} for {solver.name}", end="\r")
                solver.solve(board)
                fp.write(f"{solver}\n")
                board.generate_new_board()
                solver.guesses = 0
                solver.wrong_guesses = 0

            print()
