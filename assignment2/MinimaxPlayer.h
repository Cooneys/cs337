/*
 * MinimaxPlayer.h
 *
 *  Created on: Apr 17, 2015
 *      Author: wong
 */

#ifndef MINIMAXPLAYER_H
#define MINIMAXPLAYER_H

#include "OthelloBoard.h"
#include "Player.h"
#include <vector>

/**
 * This class represents an AI player that uses the Minimax algorithm to play the game
 * intelligently.
 */
class MinimaxPlayer : public Player {
public:

	/**
	 * @param symb This is the symbol for the minimax player's pieces
	 */
	MinimaxPlayer(char symb);

	/**
	 * Destructor
	 */
	virtual ~MinimaxPlayer();

    /*######################################
    ## The following function returns the board score
    ## input: OthelloBoard* board
    ## output: int differential
    ######################################*/

	int utilityFunction(OthelloBoard *board);

    /*######################################
    ## The following function returns the list of successors given a player and the current board
    ## input: char p_symbol OthelloBoard* board
    ## output: vector<OthelloBoard*> return_board
    ######################################*/
    
	std::vector<OthelloBoard*> successorFunction(char playerSymbol, OthelloBoard *board);

    /*######################################
    ## The following function returns the best minimum value for a given player and board, recursive
    ## input: int row int column char p_symbol OthelloBoard* board
    ## output: int check_min
    ######################################*/
    
    int miniFunction(int &row, int &column, char playerSymbol, OthelloBoard *board);

    /*######################################
    ## The following function returns the best maximum value for a given player and board, recursive
    ## input: int row int column char p_symbol OthelloBoard* board
    ## output: int check_max
    ######################################*/

	int maxFunction(int &row, int &column, char playerSymbol, OthelloBoard *board);
	

	/**
	 * @param b The board object for the current state of the board
	 * @param col Holds the return value for the column of the move
	 * @param row Holds the return value for the row of the move
	 */
    void get_move(OthelloBoard* b, int& col, int& row);

    /**
     * @return A copy of the MinimaxPlayer object
     * This is a virtual copy constructor
     */
    MinimaxPlayer* clone();

private:

};


#endif
