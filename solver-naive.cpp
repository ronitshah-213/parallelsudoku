#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <iostream>
#include <string>
#include <fstream>
#include <sstream>
#include <string.h>
#include "timing.h"

using namespace std;


int get_board_size(int dim){
    /**
     * Returns the size of the array "board" given the board dimension
    */
    return dim * dim;
}


void print_size_board(int dim, string file){
    /**
     * Prints the board 
    */
    int num_of_dashes, dash_i;

    cout << "\nRunning a new board...\n" << endl;
    cout << "The board is: " << file << endl;
    cout << "The size is: " << dim << "-by-" << dim << endl;
    num_of_dashes = (3 * dim) + 8;
    for (dash_i = 0; dash_i < num_of_dashes; dash_i++) {
        cout << "-";
    }
    cout << "\n\n";
}


string board_str_from_file(string filename){
    /**
     * Fetches the data from the file as a string
    */
    string board_text;
    fstream board_file;
    
    // Opening the file
    board_file.open(filename, ios::in);

    if (board_file.is_open()) {
        string line_text;

        // Fetching each line in the text
        while (getline(board_file, line_text)) {
            board_text += line_text + " ";
        }

        // Closing the file
        board_file.close();
    }
    return board_text;
}


void get_board_from_str(string text, int *board){
    /**
     * Fetches the board from the text and stores it in "board" as an array of
     * integers
    */
    istringstream ss(text);
    string del;
    int i = 0;
    
    // Splitting the text by a whitespace and writing the integers to the board
    while (getline(ss, del, ' ')) {
        board[i] = stoi(del);
        i++;
    } 
}


int get_square_len(int size) {
    /**
     * Fetches the size of each sudoku square given the size of the board
    */
    int size_256, size_625;
    size_256 = 256;
    size_625 = 625;
    if (size == size_256)
        return 4;
    else return 5;
}


void print_board(int *board, int size, int dim) {
    /**
     * Prints the board in a better format given the board and the size of the
     * array
    */
    int square_len, brd_i, curr, num_of_dashes, dash_i, col_count;

    // Fetching the length of the sudoku square
    square_len = get_square_len(size);

    // Looping over the entire board and printing each number
    col_count = 0;
    for (brd_i = 0; brd_i < size; brd_i++) {
        curr = board[brd_i];
        // Printing a line of dashes once we print each square row
        if ((brd_i % (square_len * dim)) == 0 && brd_i != 0) {
            num_of_dashes = (3 * dim) + 8;
            for (dash_i = 0; dash_i < num_of_dashes; dash_i++) {
                cout << "-";
            }
            cout << "\n";
        }

        // Printing the current number to the console
        if (col_count == dim - 1) {
            if (curr >= 10) {
                cout << curr << " " << endl;
            }
            else {
                cout << curr << "  " << endl;
            }
            col_count = 0;
        }
        else {
            if (curr >= 10) {
                cout << curr << " ";
            }
            else {
                cout << curr << "  ";
            }
            // Printing dashes between each square
            if ((brd_i % dim) != 0 && ((brd_i + 1) % square_len) == 0) {
                cout << "| ";
            }
            col_count++;
        }
    }
    // Printing a newline and a line of dashes for formatting
    cout << "\n";
    for (dash_i = 0; dash_i < num_of_dashes; dash_i++) {
        cout << "-";
    }
    cout << "\n\n";
}


void print_input_board_message(int *board, int size, int dim, string filename) {
    /**
     * Prints the input
    */
    cout << "Here is the input board read from the file " << filename << " :\n\n" << endl; 
    print_board(board, size, dim);
}


void print_output_board_message(int *board, int size, int dim, string filename) {
    /**
     * Prints the input
    */
    cout << "Here is the solved board:\n\n" << endl; 
    print_board(board, size, dim);
}


int fetch_empty(int *board, int size) {
    /**
     * Fetches the index of the next empty cell in the board
    */
    int i = 0;
    while (i <= size) {
        if (board[i] == 0)
            return i;
        i++;
    }
    return i;
}


bool check_row(int *board, int num, int row, int dim) {
    /**
     * Checks if a number placement is valid in a row
    */
    int start, end, i;
    start = row * dim;
    end = (row + 1) * dim;

    for (i = start; i < end; i++){
        if (board[i] == num) {
            return false;
        }
    }
    return true;
}


bool check_col(int *board, int col, int num, int size, int dim) {
    /**
     * Checks if a number placement is valid in a column
    */
    int i;
    for (i = col; i < size; i += dim) {
        if (board[i] == num) {
            return false;
        }
    }
    return true;
}


bool check_square(int *board, int num, int row, int col, int size, int dim) {
    /**
     * Checks if a number placement is valid in a square
    */
    int row_floor, row_ceil, col_floor, col_ceil, rowi, coli, square_len;

    // Fetching relevant values
    square_len = get_square_len(size);
    row_floor = (row / square_len) * square_len;
    row_ceil = ((row + square_len) / square_len) * square_len;
    col_floor = (col / square_len) * square_len;
    col_ceil = ((col + square_len) / square_len) * square_len;

    // Checking the square
    for (rowi = row_floor; rowi < row_ceil; rowi++) {
        for (coli = col_floor; coli < col_ceil; coli++) {
            if (board[(dim * rowi) + coli] == num) {
                return false;
            }
        }
    }
    return true;
}


bool is_valid(int *board, int num, int i, int size, int dim) {
    /**
     * Checks if a placement in an empty cell is valid or not
    */
    int row, col;
    //int square_len, row_floor, row_ceil, col_floor, col_ceil, ind; 

    // Fetching the row and column 
    row = i / dim;
    col = i % dim;

    // Checking the row
    if (!check_row(board, num, row, dim)) {
        return false;
    }

    // Checking the column
    if (!check_col(board, col, num, size, dim)) {
        return false;
    }

    // Checking the square
    if (!check_square(board, num, row, col, size, dim)) {
        return false;
    }
    return true;
}


bool solve_board(int *board, int size, int dim) {
    /**
     * Primary function that solves the sudoku board. 0s in the board represent
     * empty cells. This algorithm uses backtracking to solve the board. Returns
     * true if the we succeeded to solve the board; else, returns false
    */
    int brd_i, num;

    // Fetching the next empty index. If fetch empty returns size, we're done
    brd_i = fetch_empty(board, size);
    if (brd_i == size) return true;

    // Looping over all possible numbers
    for (num = 1; num <= dim; num++) {
        if (is_valid(board, num, brd_i, size, dim)) {
            board[brd_i] = num;
            if (solve_board(board, size, dim)) 
                return true;
            board[brd_i] = 0;
        }
    }
    return false;
}


void write_board(int *board, int size, int dim, string filename) {
    /**
     * Writes the board to the output file to check for correctness
    */
    string board_text;
    fstream board_file;
    int count, i;
    count = 0;

    // Modifying the filename
    filename = "solved-" + filename;
    
    // Opening the file
    board_file.open(filename, ios::out);

    if (board_file.is_open()) {

        for (i = 0; i < size; i++) {
            if (count == (dim-1)) {
                board_file << board[i] << "\n";
                count = 0;
            }
            else {
                board_file << board[i] << " ";
                count++;
            }
        }

        // Closing the file
        board_file.close();
    }
}


int main(int argc, char *argv[]){
    /**
     * Main function that runs all of the relevant functions
    */
    // Variable declarations
    string filename, board_text;
    int dim, board_size;
    int *board;
    bool solved;
    double runtime;

    // Fetching the board and size and printing them
    dim = stoi(argv[1]);
    filename = argv[2];
    board_size = get_board_size(dim);
    print_size_board(dim, filename);

    // Fetching the board from the file
    board_text = board_str_from_file(filename);
    board = (int*)malloc(sizeof(int) * board_size);
    get_board_from_str(board_text, board);

    // Printing the input board
    print_input_board_message(board, board_size, dim, filename);

    // Starting the timer
    Timer runtimeTimer;

    // Solving the board
    solved = solve_board(board, board_size, dim);
    
    // Stopping the timer
    runtime = runtimeTimer.elapsed();

    // Throwing an error if the board is unsolved
    if (!solved) {
        cout << "ERROR: Solver could not find solution...\n" << endl;
        throw std::exception();
    }

    // Printing the solved board
    print_output_board_message(board, board_size, dim, filename);

    // Writing the solved board to the output file
    write_board(board, board_size, dim, filename);

    printf("Total time taken: %.6fs\n", runtime);
    return 0;
}