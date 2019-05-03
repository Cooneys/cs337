/*
 * MinimaxPlayer.cpp
 *
 *  Created on: Apr 17, 2015
 *      Author: wong
 */
#include <iostream>
#include <assert.h>
#include "MinimaxPlayer.h"

using std::vector;

// A couple references for planning out various implementation methods:
// http://stackoverflow.com/questions/6887838/improving-minimax-algorithm
// http://mnemstudio.org/game-reversi-example-2.htm
// https://github.com/bekoeppel/Lynx-Reversi-Player/blob/master/miniMaxPlayer/MiniMaxPlayer.java

MinimaxPlayer::MinimaxPlayer(char symb) :
		Player(symb) {

}

MinimaxPlayer::~MinimaxPlayer() {

}

/*######################################
## The following function returns the board score
## input: OthelloBoard* board
## output: int differential
######################################*/

int MinimaxPlayer::utilityFunction(OthelloBoard *board) {
    int differential = board->count_score(board->get_p1_symbol()) - board->count_score(board->get_p2_symbol());
	return differential;
}

/*######################################
## The following function returns the list of successors given a player and the current board
## input: char p_symbol OthelloBoard* board
## output: vector<OthelloBoard*> return_board
######################################*/

vector<OthelloBoard*> MinimaxPlayer::successorFunction(char p_symbol, OthelloBoard *board) {
	vector<OthelloBoard*> return_board;
	for (int col = 0; col < board->get_num_cols(); col++) {
		for (int row = 0; row < board->get_num_rows(); row++) {
			if (board->is_legal_move(col, row, p_symbol)) {
				return_board.push_back(new OthelloBoard(*board));
				return_board.back()->play_move(col, row, symbol);
				return_board.back()->row = row;
				return_board.back()->column = col;
			}
		}
	}
	return return_board;
}

/*######################################
## The following function returns the best minimum value for a given player and board, recursive
## input: int row int column char p_symbol OthelloBoard* board
## output: int check_min
######################################*/

int MinimaxPlayer::miniFunction(int &row, int &column, char p_symbol, OthelloBoard *board) {
	vector<OthelloBoard*> return_board;
	int min_row = 0;
	int min_col = 0;
	int check_min = 500;

	return_board = successorFunction(p_symbol, board);

	if (return_board.size() == 0) {
		return utilityFunction(board);
	}

	for (int i = 0; i < return_board.size(); i++) {
		if (miniFunction(row, column, p_symbol, return_board[i]) > check_min) {
			min_row = return_board[i]->row;
			min_col = return_board[i]->column;
			check_min = miniFunction(row, column, p_symbol, return_board[i]);
		}
	}

	row = min_row;
	column = min_col;
	return check_min;
}

/*######################################
## The following function returns the best maximum value for a given player and board, recursive
## input: int row int column char p_symbol OthelloBoard* board
## output: int check_max
######################################*/

int MinimaxPlayer::maxFunction(int &row, int &column, char p_symbol, OthelloBoard *board) {
	vector<OthelloBoard*> return_board;
	int max_row    = 0;
	int max_col = 0;
	int check_max        = -500;

	return_board = successorFunction(p_symbol, board);

	if (return_board.size() == 0) {
		return utilityFunction(board);
	}

	for (int i = 0; i < return_board.size(); i++) {
		if (miniFunction(row, column, p_symbol, return_board[i]) > check_max) {
			max_row = return_board[i]->row;
			max_col = return_board[i]->column;
			check_max = miniFunction(row, column, p_symbol, return_board[i]);
		}
	}

	row = max_row;
	column = max_col;
	return check_max;
}

/*######################################
## The following function runs the minimaxFunction based off player
## input: OthelloBoard* b int &col int &row
## output: N/A
######################################*/

void MinimaxPlayer::get_move(OthelloBoard *b, int &col, int &row) {
	if (symbol == b->get_p1_symbol()) {
		maxFunction(row, col, symbol, b);
	} else if (symbol == b->get_p2_symbol()) {
		maxFunction(row, col, symbol, b);
	}
}

MinimaxPlayer* MinimaxPlayer::clone() {
	MinimaxPlayer* result = new MinimaxPlayer(symbol);
	return result;
}
