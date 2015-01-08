__author__ = 'James'
import socket

HOST = 'localhost'    # The remote host
PORT = 50000              # The same port as used by the server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
s.send('firstfile')
data = s.recv(1024)
print 'Received', repr(data)
s.send('nextfile')
data = s.recv(1024)
print 'Received', repr(data)
s.close()