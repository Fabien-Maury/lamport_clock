# Lamport clock demonstrator

This project includes 3 files

client.py and server.py are the working Lamport clock implementation.
vectorClock.py is the unimplemented class for a vector clock.

--------------------------------------------------------------------------

# HOW TO USE IT ?

This project was developped and tested on Ubuntu 20, with Python 3.
You need to have network enabled, and possibly an Internet connection in case you need to download missing libraries.

You may need to edit the IP address and ports the sockets are using, in both files.

To make it work : run client.py and server.py as su, (client or server can be run first, it is not important)
ex : open a terminal in the directory where the files are stored and type :
sudo python3 client.py
sudo python3 server.py

If the address and ports are correctly configured, you should see the client and server communicating
in the terminal; and the clock should be keeping count of the events.

# TROUBLESHOOTING

-errors in the programs : the files are working with python3, probably not with python2
-the connection is refused : make sure you run the files with sudo
                             or restart the network on your machine, an unclosed connection may be using our ports
                             (for that type "sudo ifdown *", then "sudo ifup *", you may need to install a package for these commands)
                             
            
# HOW DOES IT WORK ?

Both the server and the client implement 2 classes : LamportClock and Process
LamportClock countains the counter and a few methods to interact with it, and update it in different situations.

Process defines our remote process, it includes some properties and description of the process itself
and 3 action methods: local event, message emission, and message reception.

Finally both files contain a main loop calling all these previous elements, defining client or server behavior.
The server only has access to the local event, and message emission actions.
First, it creates a socket and select a port to listen to. It will listen to any host emitting on that port.
Then it randomly does local events or message emission for a short while, and loops.

The client also uses a socket and select a port to connect to (the same port that the server is listening to).
It will randomly decides to do local events or to connect to the selected port.

Each clock counter can evolve independently when there is no communication between client and server.
When it happens that the server is listening at the same time that the client is trying to connect, the connection is established.
This enable the server to send a random message (like 2-factor authentificators do) to the client.
This count as an emission action for the server and a reception action for the client. The message also includes the server's time.
So the client can update its clock with this information.

If a connection attempt fails, it is considered a local event.
More clients could theoretically be added.

# VECTOR CLOCK

The vector clock class is built upon the Lamport clock class and is very similar. It was not used, but it should be possible 
to implement it.
