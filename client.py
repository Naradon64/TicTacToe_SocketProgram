from socket import *

SERVERNAME = "localhost"
PORT = 3478



def receiver():

    response = clientSocket.recv(1024).decode().split("|||", 2)
    return response

   
    

    
clientSocket = socket(AF_INET, SOCK_STREAM)

try:
    clientSocket.connect((SERVERNAME, PORT))

    while True:
        message = receiver()
        if message != None:
            print(f"{message[0]} \nYour STATUS CODE is: [{message[1]}]\n")

        if message[1] in [ "201", "401"]:
            inputMessage = input("Enter a position: ")
            clientSocket.send(inputMessage.encode())
        if message[1] == "800":
            break

finally:

    clientSocket.close()