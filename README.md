# Python-Chat-Room
Local chatroom server/client

Local chatroom via socket port 9999
Chat room only works on linux

Required Setup
-----------
1 terminal running server + many client can join.

Chatroom commands
--------------
All commands start with '/' followed by the command
If command require an argument have a space between command and arugment
/u username         - change username
/j roomname         - joing chatroom
/l roomname         - leave chatroom 
/c roomname         - create chatroom 
/d roomname         - set chatroom as default room 
/all                - displays all chatrooms on server
/mem                - displays all memeber in your default chatroom
/where              - displays chatrooms that user is a memeber of
/quit               - disconnects from chat server
/(chatroom) message - sends a message to a chatroom
/[username] message - sends a private message to a user\n
