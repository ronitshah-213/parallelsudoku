""" 
Run this file to check the sudoku board with the following command:
    python3 checker.py <filename> 

The filename parameter is a text file containing the board
"""

import sys
import os
import math


def get_board():
    """
    Fetches the board from the text file as a list
    """
    # Fetching each line in the text file
    with open(_FILENAME, "r") as file:
        file_lines = file.readlines()

    # Flattening and fetching the board
    board = []
    for line in file_lines:
        # Removing the last newline character and all of the whitespaces
        nums = line.strip().split(" ")

        # Fetching all of the numbers in each line
        for num in nums:
            board.append(int(num))
    
    return board


def get_index(row, col, dim):
    """
    Returns the index of a number in the board given the row, column and dim
    """
    index = (dim * row) + col
    return index


def get_square_indices(row, col, dim):
    """
    Helper function that returns the appropriate indices to check from for the 
    correctness check of a square given the row and col of a number
    """
    indices = []
    # Fetching the minimum and maximum rows and cols of the number's square
    square_len = int(math.sqrt(dim))
    row_floor = (row // square_len) * square_len
    row_ceil = ((row + square_len) // square_len) * square_len
    col_floor = (col // square_len) * square_len
    col_ceil = ((col + square_len) // square_len) * square_len

    # Looping over every row and col in the square and appending their index
    for row_i in range(row_floor, row_ceil):
        for col_i in range(col_floor, col_ceil):
            ind = get_index(row_i, col_i, dim)
            indices.append(ind)
    return indices


def check_board(board):
    """
    Checks the board for various criteria; Returns True if board is correct. If
    board is incorrect, an error message is returned to display to the user
    """
    # Checking if the board has correct dimensions
    dim = math.sqrt(len(board))
    if (dim != 9 and dim != 16 and dim != 25):
        assert False, f"Textfile {_FILENAME} contains a board with an invalid dimension of {dim}"
    dim = int(dim)

    # Loop that checks correctness of every number
    reason = ""
    valid = True
    for index, num in enumerate(board):
        # Fetching the row and column of the number
        row = int(index // dim)
        col = int(index % dim)

        # Checking if the number is >= 1 and <= dim
        if (num <= 0 or num > dim):
            reason = f"Number {num} at row {row} and column {col} is not within the number range"
            valid = False
            break

        # Checking if the number is the only number in row
        row_starti = row * dim
        row_endi = (row+1) * dim
        for i in range(row_starti, row_endi):
            if (index != i):
                if (board[i] == num):
                    reason = f"Number {num} in same col [({row}, {col}), ({row}, {int(i % dim)})]"
                    valid = False
                    break
        if (not valid):
            break

        # Checking if the number is the only number in col
        for i in range(col, len(board), dim):
            if (index != i):
                if (board[i] == num):
                    reason = f"Number {num} in same col [({row}, {col}), ({int(i // dim)}, {col})]"
                    valid = False
                    break 
        if (not valid):
            break

        # Checking if the number is the only number in square
        square_indices = get_square_indices(row, col, dim)
        for i in square_indices:
            if (index != i):
                if (board[i] == num):
                    reason = f"Number {num} in same square [({row}, {col}), ({int(i // dim)}, {int(i % dim)})]"
                    valid = False
                    break 
        if (not valid):
            break
    
    if (valid):
        reason = "No correctness error found!"

    return valid, reason


def print_message(board, status, error_reason):
    """
    Prints the error message and board in the terminal output
    """
    # Print error message from the status
    if (status):
        print(error_reason)
    else:
        print("ERROR:", error_reason)

    if (not status):
        # Printing the sudoku board in an appropriate format
        print(f"\nHere is the sudoku board read from the file {_FILENAME}:\n")
        dim = int(math.sqrt(len(board)))
        square_len = int(math.sqrt(dim))
        col_count = 0
        for i, num in enumerate(board):
            if (i % (dim * square_len) == 0 and i != 0):
                num_of_dashes = ((3 * dim) + 8)
                print(num_of_dashes * "-")
            if (col_count == dim - 1):
                if (num >= 10):
                    print(f"{num} ", end="")
                else:
                    print(f"{num}  ", end="")
                print('\n', end="")
                col_count = 0
            else:
                if (num >= 10):
                    print(f"{num} ", end="")
                else:
                    print(f"{num}  ", end="")
                
                if (i % dim != 0 and (i+1) % square_len == 0):
                    print("| ", end="")
                col_count += 1
        print("\n")
    print("\n___________________________________________________________\n")

def __main__():
    """
    Fetches the board and checks it, printing out correctness status and the 
    board to the user
    """
    print("\n___________________________________________________________\n")
    print("Running checker.py...\n")
    board = get_board()
    status, error_reason = check_board(board)
    print_message(board, status, error_reason)


if __name__ == "__main__":
    # Checking certain conditions for the command-line argument
    if (len(sys.argv) != 2):
        assert False, "Command-line Error: Incorrect number of command-line parameters passed in (1 needed)"
    _FILENAME = sys.argv[1]
    if (".txt" not in _FILENAME):
        assert False, "Command-line Error: File passed in must be a .txt file"
    if (_FILENAME not in os.listdir()):
        assert False, "Command-line Error: File passed in must be present in current directory"

    __main__()
