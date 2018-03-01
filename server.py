# Thuan Pham
# May 22nd 2017
# Internet Relay Chat
# Python 2.7
# Server.py

import socket
import select
from random import randint
from collections import Counter

# keeps track list of ports opened
list_of_clients = []

# keeps track of users linked via port object
# key to dict is port object in list_of_clients
book = {}

# keeps track of list of rooms, default room lobby
list_of_rooms = ["lobby"]


def server():

    # setting up server listening port
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('', 9999))
    server_socket.listen(10)

    # adds server port_id to list of clients
    list_of_clients.append(server_socket)
    print "Chat server started on port " + str(9999) + "\n"

    # server process
    while 1:
        # polls for ports that can be read
        ready_to_read, ready_to_write, in_error = select.select(list_of_clients, [], [], 0)

        # for all clients in list
        for client in ready_to_read:

            # if client connects to this socket
            # create connection
            # add new connection to list of client
            # this line checks for sockets that are readable
            # if it it readable and if that readable port is our
            # server port it means that a client wants to connect
            # accept clients request and add the client to the list
            if client == server_socket:

                # create connection accept incoming connection
                client_id, client_ip = server_socket.accept()

                # add connection to list_of_clients
                list_of_clients.append(client_id)

                # add new user to list of users
                book[client_id] = User("guest" + str(rand_num(4)))
                book[client_id].rooms.append("lobby")

                broadcast('\r[SYSTEM] ' + str(book[client_id].name) + " has joined the lobby\n",
                    client_id, server_socket, book[client_id].main_room)

                send_to_self("\r[SYSTEM] Welcome " + str(book[client_id].name) + " you have joined the lobby\n", 
                    client_id, server_socket)

            # if not a new connection do anything below
            else:
                try:
                    # read data from port
                    data = client.recv(4096)

                    # check if there is data inside port
                    if data:
                        # debug statements
                        print "Message received... sending to other clients"

                        # menu options initializer
                        if data[0] == '/' and len(data) > 4:

                            # change username command
                            if data[1] == 'u':
                                change_username(data[3:-1], client, server_socket)

                            # leave chatroom command
                            elif data[1] == 'l':
                                leave_chatroom(data[3:-1], client, server_socket)

                            # join chatroom command
                            elif data[1] == 'j':
                                join_chatroom(data[3:-1], client, server_socket)
      
                            # create chatroom command
                            elif data[1] == 'c':
                                create_chatroom(data[3:-1], client, server_socket)

                            # change chatroom to main room command
                            elif data[1] == 'd':
                                set_chatroom_as_default(data[3:-1], client, server_socket)

                            # list all chat rooms command
                            elif data[1:-1] == "all":
                                display_all_chatrooms(client, server_socket)

                            # list all members in a chatroom command
                            elif data[1:-1] == 'mem':
                                display_all_memebers(client, server_socket)

                            # send message to specified chatroom command
                            elif data[1] == '(':
                                dest, two, msg = data.partition(') ')
                                room = dest.partition('(')[2]
                                send_select_room(msg, room, client, server_socket)

                            # send private message to user
                            elif data[1] == '[':
                                dest, two, msg = data.partition('] ')
                                uname = dest.partition('[')[2]
                                send_private_msg(msg, uname, client, server_socket)

                            # list chat rooms user are part of command
                            elif data[1:-1] == 'where':
                                send_to_self("\r[SYSTEM] Chat rooms that you are in: " + str(book[client].rooms) + ".\n",
                                    client, server_socket)

                            # command invalid, sens notice
                            else:
                                send_to_self("\r[SYSTEM] Command not valid, please try again\n", client, socket)

                        else:
                            # no command option, then broadcast to all members of chatroom
                            if book[client].main_room in book[client].rooms:
                                broadcast('\r' + '[' + book[client].main_room + ':' + str(book[client].name) + '] ' + data,
                                          client, server_socket, book[client].main_room)
                            else:
                                send_to_self("\r[SYSTEM] Error, default room is not set, please set a default room\n",
                                    client, server_socket)

                    # no data in port i.e disconnected
                    else:
                        print "User has disconnected from server."

                        # remove user from list of users
                        if client in list_of_clients:
                            list_of_clients.remove(client)

                        # tell other users that user has left server
                        broadcast("\r[SYSTEM] " + str(book[client].name) + " has left the room.\n", client,
                                  server_socket, book[client].main_room)

                except:
                    broadcast("\r[SYSTEM] Client not responding, time out!", client, server_socket,
                              book[client].main_room)
                    print "ERROR IN PROGRAM \n"
                    continue


class User(object):
    #holds our user porfile
    def __init__(self, name):
        self.name = name
        self.rooms = []
        self.main_room = "lobby"


def is_user_taken(newname, server_socket):

    for user in list_of_clients:
        if user != server_socket:
            if book[user].name == newname:
                return False
    return True


def change_username(username, client, server_socket):
    if is_user_taken(username, server_socket):
        book[client].name = username
        send_to_self( "\r[SYSTEM] Username changed to " + 
        str(book[client].name) + '\n', client, server_socket)
    else:
        send_to_self("\r[SYSTEM] Username " + username + " already taken, choose different one"+ "\n", 
            client, server_socket)


def leave_chatroom(chatroom, client, server_socket):
    
    if chatroom in book[client].rooms:
        broadcast("\r[SYSTEM] " + str(book[client].name) + " has left the room\n", 
            client, server_socket, chatroom)
        send_to_self("\r[SYSTEM] You have left the chatroom " + chatroom + "\n",
            client, server_socket)
        book[client].rooms.remove(chatroom)
    else:
        send_to_self("\r[SYSTEM] You cannot leave a room you are not in\n",
            client, server_socket)


def join_chatroom(chatroom, client, server_socket):
    # checks if room is in list of rooms
    if chatroom in list_of_rooms:
        if chatroom in book[client].rooms:
            send_to_self("\r[SYSTEM] You are already in that chatroom\n", client, server_socket)
        else:
            book[client].rooms.append(chatroom)
            send_to_self("\r[SYSTEM] Joined chatroom, " + chatroom + '\n', 
                client, server_socket)
            broadcast("\r[SYSTEM] " + str(book[client].name) + " joined the room\n",
                client, server_socket, chatroom)
    else:
        send_to_self("\r[SYSTEM] Failed to join chatroom " + chatroom + ', room does not exist\n',
            client, server_socket)


def create_chatroom(chatroom, client, server_socket):
    if chatroom not in list_of_rooms:
        send_to_self("\r[SYSTEM] New chatroom created: " + chatroom + "\n",
            client, server_socket)
        list_of_rooms.append(chatroom)
    else:
        send_to_self(
            "\r[SYSTEM] Cannot create, chatroom " + chatroom + ", already exist\n",
            client, server_socket)


def set_chatroom_as_default(chatroom, client, server_socket):
    if chatroom in book[client].rooms:
        send_to_self("\r[SYSTEM] Default chatroom changed from " + book[client].main_room + " to ",
            client, server_socket)
        book[client].main_room = chatroom
        send_to_self(chatroom + ".\n", client, server_socket)
    else:
        send_to_self("\r[SYSTEM] Cannot change default room to " + chatroom + ", not a memeber or does not exist\n",
            client, server_socket)


def display_all_chatrooms(client, server_socket):
    roomlist = '\n'
    for rooms in list_of_rooms:
        roomlist = str(rooms) + ', ' + roomlist
    roomlist = "\r[SYSTEM] All chat rooms on server: " + roomlist
    send_to_self(roomlist, client, server_socket)


def display_all_memebers(client,server_socket):
    mem_list = ''
    # goes through list of keys
    for m in list_of_clients:
        # make sure key is not server socket and the rooms matches to user requesting
        if m != server_socket and book[client].main_room in book[m].rooms:
            mem_list = mem_list + str(book[m].name) + ', '
    send_to_self(
        "\r[SYSTEM] Users in " + str(book[client].main_room) + ": " + mem_list + "\n",
            client, server_socket)


def send_select_room(msg, room, client, server_socket):
    if room in book[client].rooms:
        broadcast( '\r' + '[' + room + ':' + str(book[client].name) + '] ' + msg,
            client, server_socket, room)
    else:
        send_to_self("\r[SYSTEM] Cannot send message to room " + room + ", you are not a memember of\n",
            client, server_socket)

def send_private_msg(msg, username, client_conn, server_socket):
    for client in list_of_clients:
        if client != server_socket and client != client_conn:
            if book[client].name == username:
                try:
                    client.send("\r[PM:" + book[client_conn].name + "] " + msg)
                except:
                    client.close()
                    if client in list_of_clients:
                        remove_from_list(client)
            elif book[client_conn].name == username:
                send_to_self("\r[SYSTEM] Cannot send private message to yourself\n",
                    client_conn, server_socket)
            else:
                send_to_self("\r[SYSTEM] Cannot send private message to user " + username + ", user does not exists\n",
                    client_conn, server_socket)


def send_to_self(message, client_conn, server_socket):
    # sends message to local client no broadcasting, for system messages
    for client in list_of_clients:
        if client != server_socket and client == client_conn:
            try:
                client.send(message)
            except:
                client.close()
                if client in list_of_clients:
                    remove_from_list(client)


def broadcast(message, client_conn, server_socket, room_dest):
    # goes through each user in list of users
    for client in list_of_clients:

        # if user is not itself and not the chat server's listening port
        # and also the same chatroom then you can send message
        if client != client_conn and client != server_socket and room_dest in book[client].rooms:

            print room_dest
            try:
                # send message to all other users in chat
                client.send(message)
            except:
                # user no longer there cannot send message
                # remove user from list of users
                print "User no longer exists, removing from list of users"
                client.close()
                if client in list_of_clients:
                    remove_from_list(client)


def remove_from_list(connection):
    if connection in list_of_clients:
        list_of_clients.remove(connection)


def rand_num(n):
    range_start = 10 ** (n - 1)
    range_end = (10 ** n) - 1
    return randint(range_start, range_end)


if __name__ == '__main__':
    server()
