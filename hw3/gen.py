import random

def generate_complete_sudoku():
    board = [[0 for _ in range(9)] for _ in range(9)]
    fill_board(board)
    return board

def fill_board(board):
    numbers = list(range(1, 10))
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                random.shuffle(numbers)
                for num in numbers:
                    if is_valid(board, num, i, j):
                        board[i][j] = num
                        if not find_empty_cell(board) or fill_board(board):
                            return True
                        board[i][j] = 0
                return False

def remove_cells(board, num_cells_to_remove):
    cells_removed = 0
    while cells_removed < num_cells_to_remove:
        row = random.randint(0, 8)
        col = random.randint(0, 8)

        if board[row][col] != 0:
            board[row][col] = 0
            cells_removed += 1

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
        print('[', end="")
        for j in range(9):
            print(board[i][j], end="")
            if j != 8:
                print(',', end=" ")
        print(']', end="")
        if i != 8:
            print(',')
        else:
            print('')

if __name__ == "__main__":
    complete_sudoku = generate_complete_sudoku()
    print_board(complete_sudoku)

    print("Enter the number of empty cells")
    num_cells_to_remove = int(input())
    remove_cells(complete_sudoku, num_cells_to_remove)

    print_board(complete_sudoku)
