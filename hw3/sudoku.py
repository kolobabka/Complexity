def solve_sudoku(board):
    empty_cell = find_empty_cell(board)
    if not empty_cell:
        return True

    row, col = empty_cell

    for num in range(1, 10):
        if is_valid(board, num, row, col):
            board[row][col] = num

            if solve_sudoku(board):
                return True

            board[row][col] = 0

    return False

def find_empty_cell(board):
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                return (i, j)
    return None

def is_valid(board, num, row, col):
    if num in board[row]:
        return False

    if num in [board[i][col] for i in range(9)]:
        return False

    box_row = row // 3 * 3
    box_col = col // 3 * 3
    for i in range(box_row, box_row + 3):
        for j in range(box_col, box_col + 3):
            if board[i][j] == num:
                return False

    return True

def print_board(board):
    for i in range(9):
        if i % 3 == 0 and i != 0:
            print("-" * 21)
        for j in range(9):
            if j % 3 == 0 and j != 0:
                print(" | ", end="")
            print(f" {board[i][j]} ", end="")
        print()

if __name__ == "__main__":
    sudoku_board = [
        [0, 0, 1, 0, 0, 0, 0, 8, 0],
        [0, 0, 0, 0, 0, 5, 0, 0, 0],
        [0, 4, 0, 8, 0, 0, 0, 0, 0],
        [3, 0, 6, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 9, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 7],
        [0, 0, 0, 6, 0, 0, 0, 7, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0]

    ]

    print("Initial board :")
    print_board(sudoku_board)

    if solve_sudoku(sudoku_board):
        print("Solution :")
        print_board(sudoku_board)
    else:
        print("Impossible to solve")

