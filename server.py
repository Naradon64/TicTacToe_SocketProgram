from socket import *
import random
PORT = 3478

STATUS_IDLE = 200  # Idle status: The client is not allowed to perform any actions. It should wait or read data.
STATUS_OK = 201  # OK status: The server is ready to receive input from the client.
STATUS_INPUT_ERROR = 401  # Input Error status: The client's input was invalid. The client should try again.
STATUS_FINISH = 800  # Finish status: The program has terminated.


class TicTacToe:
    def __init__(self, firstClientSocket, secondClientSocket):
        self.firstClient = firstClientSocket
        self.secondClient = secondClientSocket

        self.playableClient = ""  # Determines which client is currently allowed to make a move: either the first client or the second client.

        self.firstClientSymbol =  "_"  # Symbol representing the first client's moves on the game board. Initially set to an underscore ('_').
        self.secondClientSymbol =  "_"  # Symbol representing the second client's moves on the game board. Initially set to an underscore ('_').


        self.table = [['_'] * 3 for _ in range(3)]
        
    def start(self):
        print("Game started!")
        self.announcement()
        self.decideWhoFirst()  # Determines which client goes first and assigns the corresponding symbols.

        while True:
            
            
            self.clientInputTurn()
            winner, loser = self.check_win()
            if winner != None:
                self.sendMessageToClient("Congratulations! You win!", STATUS_FINISH, winner)
                self.sendMessageToClient("Sorry, you lose. Better luck next time.", STATUS_FINISH, loser)
                break
            

    def clientInputTurn(self):
        tableString = self.print_table()
        self.sendMessageToClient(tableString, STATUS_OK, self.playableClient)
        print("In a turn")

        while True:
            try: 
                inputFromClient = self.playableClient.recv(1024).decode() # Receive an input from the client


                # Check whether the input is valid or not.
                if len(inputFromClient) > 2 or len(inputFromClient) < 2:
                    raise ValueError("The length of the input is invalid, please enter the row position first than the column position (eg. A1 or C3).")
                if inputFromClient[0].lower() not in {'a', 'b', 'c'}:
                    raise ValueError("The column character must be between a-c.")
                if not inputFromClient[1].isdigit() or int(inputFromClient[1]) not in {1, 2, 3}:
                    raise ValueError("The column number must be between 1 and 3.")


                if inputFromClient[0].lower() == 'a':
                    columnPos = 0
                elif inputFromClient[0].lower() == 'b':
                    columnPos = 1
                elif inputFromClient[0].lower() == 'c':
                    columnPos = 2
                
                # If-else condition to check whether the value in 2D array has already been taken or not.
                if self.table[columnPos][int(inputFromClient[1]) - 1] == "_" :
                    if self.playableClient == self.firstClient:
                        self.table[columnPos][int(inputFromClient[1]) - 1] = self.firstClientSymbol
                        self.playableClient = self.firstClient
                    elif self.playableClient == self.secondClient:
                        self.table[columnPos][int(inputFromClient[1]) - 1] = self.secondClientSymbol
                        self.playableClient = self.secondClient

                    self.sendMessageToClient("Your move has been accepted. Please wait for the other player to take their turn.", STATUS_IDLE, self.playableClient)
                    # Print a table after the move has been accepted.
                    tableString = self.print_table()
                    self.sendMessageToClient(tableString, STATUS_IDLE, self.playableClient)
                    if self.playableClient == self.firstClient:
                        self.playableClient = self.secondClient
                    else:
                        self.playableClient = self.firstClient

                    
                    
                    return 
                else:
                    raise ValueError("The position has already been taken.")

            except ValueError as e: 
                self.sendMessageToClient(e, STATUS_INPUT_ERROR, self.playableClient)

        
        

    def print_table(self):
        # column headers
        table_string = "  1 2 3\n"
        for i, row in enumerate(self.table):
            # row header
            table_string += chr(ord('a') + i) + ' '
            for cell in row:
                table_string += cell + ' '
            table_string += '\n'
        return table_string
        
    def check_win(self):
        # Check rows
        for row in self.table:
            if all(cell == self.firstClientSymbol for cell in row):
                return self.firstClient, self.secondClient  # First client wins, second client loses
            elif all(cell == self.secondClientSymbol for cell in row):
                return self.secondClient, self.firstClient  # Second client wins, first client loses

        # Check columns
        for col in range(3):  # Iterate over 3 columns
            if all(self.table[row][col] == self.firstClientSymbol for row in range(3)):  # Check each cell in the column
                return self.firstClient, self.secondClient  # First client wins, second client loses
            elif all(self.table[row][col] == self.secondClientSymbol for row in range(3)):
                return self.secondClient, self.firstClient  # Second client wins, first client loses

        # Check diagonals
        if all(self.table[i][i] == self.firstClientSymbol for i in range(3)) or \
                all(self.table[i][2 - i] == self.firstClientSymbol for i in range(3)):
            return self.firstClient, self.secondClient  # First client wins, second client loses
        elif all(self.table[i][i] == self.secondClientSymbol for i in range(3)) or \
                all(self.table[i][2 - i] == self.secondClientSymbol for i in range(3)):
            return self.secondClient, self.firstClient  # Second client wins, first client loses

        return None, None  # No winner yet




    def decideWhoFirst(self):
        coin_flip = random.randint(1,2)
        if coin_flip == 1:
            self.firstClientSymbol = "X"
            self.secondClientSymbol = "O"
            self.playableClient = self.firstClient
            self.sendMessageToClient("You goes first.", STATUS_IDLE, self.firstClient)
        else:
            self.secondClientSymbol = "X"
            self.firstClientSymbol = "O"
            self.playableClient = self.secondClient
            self.sendMessageToClient("You goes first.", STATUS_IDLE, self.secondClient)

            


    def announcement(self):
        print("Announcing...")

        self.sendMessageToClient("Welcome to Tic Tac Toe!\n", STATUS_IDLE, self.firstClient)
        self.sendMessageToClient("Tic Tac Toe is a classic game played on a 3x3 grid. The goal of the game is to be the first player to get three of your symbols (either 'X' or 'O') in a row, column, or diagonal.\n", STATUS_IDLE, self.firstClient)

        self.sendMessageToClient("Welcome to Tic Tac Toe!\n", STATUS_IDLE, self.secondClient)
        self.sendMessageToClient("Tic Tac Toe is a classic game played on a 3x3 grid. The goal of the game is to be the first player to get three of your symbols (either 'X' or 'O') in a row, column, or diagonal.\n", STATUS_IDLE, self.secondClient)



    def sendMessageToClient(self, message, statusCode, client):
        client.send(f"{message}|||{statusCode}".encode())
        print(f"Sent a message to a client where the status code is [{statusCode}]")


serverSocket = socket(AF_INET, SOCK_STREAM)

try:
    serverSocket.bind(("", PORT))
    serverSocket.listen(2)

    firstClientSocket, firstClientAddress = serverSocket.accept()
    print("First client connected.")

    secondClientSocket, secondClientAddress = serverSocket.accept()
    print("Second client connected.")
    TicTacToeObject = TicTacToe(firstClientSocket, secondClientSocket)
    TicTacToeObject.sendMessageToClient("You're the first client that joined the server", STATUS_IDLE, firstClientSocket)
    TicTacToeObject.sendMessageToClient("You're the second client that joined the server", STATUS_IDLE, secondClientSocket)

    print("initialize...")
    TicTacToeObject.start()
        
    
finally:
    try:
        if 'firstClientSocket' in locals():
            TicTacToeObject.sendMessageToClient("Server is shutting down. Thank you for playing!", STATUS_FINISH, firstClientSocket)
            firstClientSocket.close()
        if 'secondClientSocket' in locals():
            TicTacToeObject.sendMessageToClient("Server is shutting down. Thank you for playing!", STATUS_FINISH, secondClientSocket)
            secondClientSocket.close()
    except NameError:
        print("One or both of the client sockets were not defined.")
    serverSocket.close()

