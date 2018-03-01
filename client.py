# Thuan Pham
# May 22nd 2017
# Internet Relay Chat
# Python 2.7
# Client.py

import sys
import socket
import select


def chat(port_num):

    if len(sys.argv) < 2:
        print "USAGE: echo_client_sockets.py <HOST>";
    sys.exit(0)

    host = sys.argv[1]
    port = port_num

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.settimeout(2)
    try:
        server_socket.connect((host, port))
    except:
        print 'Unable to connect'
        sys.exit()

    print "Connected to chat server successfully\n"
    print "For a list of chat commands type ~help \n"



    sys.stdout.write('[Me] ')
    sys.stdout.flush()

    while 1:
        socket_list = [sys.stdin, server_socket]

        # Get the list sockets which are readable
        ready_to_read, ready_to_write, in_error = select.select(socket_list, [], [])
 
        for socket_port in ready_to_read:
            if socket_port == server_socket:
                data = socket_port.recv(4096)
                if data:
                    sys.stdout.write(data)
                    sys.stdout.write("[Me] ")
                    sys.stdout.flush()
                else:
                    print "\nYou have been disconnected from the chat server"
                    return
            else:
                # user entered a message
                msg = sys.stdin.readline()
                if msg == '/quit\n':
                    print "[SYSTEM] You have disconnected from the chat server."
                    return
                elif msg == '~help\n':
                    print_commands()
                    sys.stdout.write('[Me] ')
                    sys.stdout.flush()
                else:
                    server_socket.send(msg)
                    sys.stdout.write('[Me] ')
                    sys.stdout.flush()


def print_commands():

    print "All commands start with '/' followed by the command"
    print "If command require an argument have a space between command and arugment\n"
    print " /u username         - change username "
    print " /j roomname         - joing chatroom "
    print " /l roomname         - leave chatroom "
    print " /c roomname         - create chatroom "
    print " /d roomname         - set chatroom as default room "
    print " /all                - displays all chatrooms on server"
    print " /mem                - displays all memeber in your default chatroom"
    print " /where              - displays chatrooms that user is a memeber of"
    print " /quit               - disconnects from chat server"
    print " /(chatroom) message - sends a message to a chatroom"
    print " /[username] message - sends a private message to a user\n"


if __name__ == "__main__":

    try:
        chat(9999)

    except KeyboardInterrupt:
        print 'Quited'
