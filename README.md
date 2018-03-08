# Python-Chat-Room
Local chatroom server/client

Local chatroom via socket port 9999
Chat room only works on linux

Required Setup
-----------
1 terminal running server + many client can join.

Chatroom commands
--------------
All commands start with '/' followed by the command <br />
If command require an argument have a space between command and arugment <br />
/u username         - change username <br />
/j roomname         - joing chatroom <br />
/l roomname         - leave chatroom  <br />
/c roomname         - create chatroom  <br />
/d roomname         - set chatroom as default room  <br />
/all                - displays all chatrooms on server <br />
/mem                - displays all memeber in your default chatroom <br />
/where              - displays chatrooms that user is a memeber of <br />
/quit               - disconnects from chat server <br />
/(chatroom) message - sends a message to a chatroom <br />
/[username] message - sends a private message to a user <br />
