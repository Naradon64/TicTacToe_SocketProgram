# TicTacToe with Socket Programming

## Assignment Overview
This project is part of the "Computer Communications and Cloud Computing Principles" class (01418351) and involves implementing a TicTacToe game using socket programming. The goal is to create a client-server application where two clients can connect to the server and play TicTacToe against each other.

### Game Rules
- Tic Tac Toe is a classic game played on a 3x3 grid.
- The goal of the game is to be the first player to get three of your symbols (either 'X' or 'O') in a row, column, or diagonal.
- Players take turns placing their symbols on the grid until one player achieves the winning condition or the grid is full.

## How to Run
To run the TicTacToe game, you need to start the server and connect clients to it.

### Running the Server
1. Run the `server.py` file to start the server.
2. The server will listen for incoming connections from clients.

### Running the Client
1. Run the `client.py` file twice to start two separate instances of the client.
2. Each client will connect to the server and display the game interface.
3. Follow the prompts in each client to input your moves and play the game against the opponent.
4. When the game has a winner or ends in a draw, the server will terminate itself and disconnect the clients.

### Terminating the Game
- To terminate the game, simply close the server window. This will shut down the server and disconnect all clients.


