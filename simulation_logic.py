""" Simulate pair matching board game """
import board
import solvers

if __name__ == "__main__":
    board = board.Board(6, 6)

    solver = solvers.SequentialSolver()
    # print(board)
    # print(board.rows, board.columns)
    for _ in range(1000):
        solver.solve(board)
        print(solver)
        board.generate_new_board()
        solver.guesses = 0
        solver.wrong_guesses = 0
