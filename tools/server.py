"""
this will be the server (the chat room), it will recive messages from clients
then will store the messages somehow and will display them to alll the user's
date: 19/7/2020
author: Ron R
"""
import socket
import select
import sys
import threading

MESSAGE_SIZE_B = 1024

def clientthread(conn, addr, connected_clients):
    """
    # sends a message to the client whose user object is conn
    recives a message from the user
    than brodcast's it to the the rest
    """

    with conn:
        print('Connected by', addr)
        while True:
            try:
                message_to_brodcast = conn.recv(MESSAGE_SIZE_B).decode()
                if message_to_brodcast:
                    broadcast(message_to_brodcast, conn)
                    break
                else:
                    print("error the message is empty")
                    remove_client(conn)

            except Exception as e:
                print(f"[FALIURE] in reciving incoming message {e}")


def remove_client(connection, connected_clients):
    if connection in connected_clients:
        connected_clients.remove(connection)


def broadcast(message, curr_connection, connected_clients):
    """Using the below function, we broadcast the message to all
        clients who's object is not the same as the one sending
        the message """
    for client_connection in connected_clients:
        if client_connection != curr_connection:
            try:
                client_connection.send(bytes(message))
            except Exception as e:
                print(f"Could not send the broadcast to client: {client_connection}")
                client_connection.close()
                remove_client(client_connection, connected_clients)



if __name__ == "__main__":
    ip_client = sys.argv[1]
    port_client = sys.argv[2]
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((ip_client, port_client))
    list_of_clients = []
    server.listen(100)
    Running = True
    while Running:
        """Accepts a connection request and stores two parameters,  
        conn which is a socket object for that user, and addr  
        which contains the IP address of the client that just  
        connected"""
        conn, addr = server.accept()

        """Maintains a list of clients for ease of broadcasting 
        a message to all available people in the chatroom"""
        list_of_clients.append(conn)

        # prints the address of the user that just connected
        print( addr[0] + " connected")

        # creates and individual thread for every user
        # that connects
        curr_thread = threading.Thread(target=clientthread, args=(conn, addr,list_of_clients,))
        curr_thread.start()

    conn.close()
    server.close()


