""" 
Run this file to generate the 25x25 board with the following command:
    python3 board.py <size> <board_type>

The size parameter is either "16", or "25". These would generate 16x16 and 
25x25 boards respectively.

The board type parameter is either "random1", "random2", "edge", or "easy. These 
would make a board with these varying types of blanked out cells
"""

import sys
import math
import random


def get_board():
    """
    Fetches the board from the text file as a list
    """
    # Fetching the correct file name
    if (_SIZE == 16):
        filename = "template16.txt"
    else:
        filename = "template25.txt"

    # Fetching each line in the text file
    with open(filename, "r") as file:
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


def randomize_board(board):
    """
    Randomizes all of the numbers in the template board
    """
    # Getting a list of valid numbers for the given size
    valid_nums = []
    for num in range(_SIZE):
        valid_nums.append(num + 1)
    
    # Shuffling the list of valid numbers
    random.shuffle(valid_nums)

    # Replacing every number in the board with the appropriate number from the
    # shuffled list of nums
    board_len = len(board)
    for i in range(board_len):
        index = board[i] - 1
        board[i] = valid_nums[index]

    return board


def shuffle_board(board):
    """
    Shuffles the ordering of each square's rows and columns to get a unique 
    board
    """
    square_len = int(math.sqrt(_SIZE))
    # Getting the column and row ordering
    row_order = []
    col_order = []
    for num in range(square_len):
        row_order.append(num)
        col_order.append(num)
    random.shuffle(row_order)
    random.shuffle(col_order)

    # Shuffling the columns and rows based on the ordering
    do_col = random.randint(0, 1)
    board_shuff_row = []
    board_shuff_col = []
    row_chunksize = square_len * _SIZE
    if (do_col == 1):
        # Doing column shuffling first
        for row in range(_SIZE):
            lim = row * _SIZE
            for sqr_col in col_order:
                lim1 = lim + (sqr_col * square_len)
                lim2 = lim + ((sqr_col + 1) * square_len)
                board_shuff_col.extend(board[lim1:lim2])

        # Doing row shuffling 
        for sqr_row in row_order:
            lim1 = sqr_row * row_chunksize
            lim2 = (sqr_row + 1) * row_chunksize
            board_shuff_row.extend(board_shuff_col[lim1:lim2])
    else:
        # Doing row shuffling first
        for sqr_row in row_order:
            lim1 = sqr_row * row_chunksize
            lim2 = (sqr_row + 1) * row_chunksize
            board_shuff_row.extend(board[lim1:lim2])

        # Doing column shuffling
        for row in range(_SIZE):
            lim = row * _SIZE
            for sqr_col in col_order:
                lim1 = lim + (sqr_col * square_len)
                lim2 = lim + ((sqr_col + 1) * square_len)
                board_shuff_col.extend(board_shuff_row[lim1:lim2])

    if (do_col == 1):
        # Setting board to board_shuff_row
        board = board_shuff_row
    else:
        # Setting board to board_shuff_col
        board = board_shuff_col

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


def remove_cells(board, board_type):
    """
    Removes cells based on the board type to create a random sudoku puzzle for 
    the solver
    """
    if "random" in board_type:
        # Setting the number of cells to blank out
        num_of_blanks = math.ceil(0.42 * (_SIZE ** 2))

        # Randomly picking indices of the board to blank out
        count = 0
        indices = []
        while (count < num_of_blanks):
            index = random.randint(0, (len(board) - 1))
            if index not in indices:
                indices.append(index)
                count += 1
        
        # Blanking out the cells
        for index in indices:
            board[index] = 0

    elif board_type == "easy":
        # Setting the number of cells to blank out
        num_of_blanks = math.ceil(0.40 * (_SIZE ** 2))

        # Randomly picking indices of the board to blank out
        count = 0
        indices = []
        while (count < num_of_blanks):
            index = random.randint(0, (len(board) - 1))
            if index not in indices:
                indices.append(index)
                count += 1
        
        # Blanking out the cells
        for index in indices:
            board[index] = 0

    else:
        # Getting indices of the corner squares
        indices = []
        indices.extend(get_square_indices(0, 0, _SIZE))
        indices.extend(get_square_indices(0, _SIZE - 1, _SIZE))
        indices.extend(get_square_indices(_SIZE - 1, _SIZE - 1, _SIZE))
        indices.extend(get_square_indices(_SIZE - 1, 0, _SIZE))

        # Setting the number of cells to blank out
        num_of_blanks = math.ceil(0.05 * ((_SIZE ** 2) - (4 * _SIZE)))

        # Randomly picking indices of the board to blank out
        count = 0
        while (count < num_of_blanks):
            index = random.randint(0, (len(board) - 1))
            if index not in indices:
                indices.append(index)
                count += 1
        
        # Blanking out the cells
        for index in indices:
            board[index] = 0

    return board


def write_board(board, file):
    """
    Writes the board to the output file
    """
    count = 0
    with open(file, "w") as f:
        for num in board:
            if (count == _SIZE - 1):
                f.write(f"{num}\n")
                count = 0
            else:
                f.write(f"{num} ")
                count += 1


def __main__():
    """
    Runs all relevant functions to create randomized sudoku boards with blanked
    cells. All sudoku boards are written to relevant text files
    """
    # Fetching the raw board from the template
    board = get_board()
    
    # Randomizing and shuffling the board
    board = randomize_board(board)
    board = shuffle_board(board)

    # Randomly removing spaces based on the board type
    board = remove_cells(board, _BOARDTYPE)

    # Writing the board to the output file
    filename = f"{_BOARDTYPE}-{_SIZE}.txt"
    write_board(board, filename)
    

def fetch_params():
    """
    Fetches the difficult and size of the board from the command-line
    """
    # Checking if only 2 command-line arguments are passed in
    if (len(sys.argv) != 3):
        assert False, "Command-line Error: Incorrect number of command-line parameters passed in (2 needed)"

    # Checking if command-line arguments are valid
    size = sys.argv[1]
    board_type = sys.argv[2]
    if (size != "16" and size != "25"):
        assert False, "Command-line Error: 1st parameter (size) is invalid; must be 9, 16, or 25"
    if (board_type != "random1" and board_type != "easy" and board_type != "edge" and board_type != "random2"):
        assert False, "Command-line Error: 2nd parameter (board type) is invalid"
    return int(size), board_type


if __name__ == "__main__":
    _SIZE, _BOARDTYPE = fetch_params()
    __main__()