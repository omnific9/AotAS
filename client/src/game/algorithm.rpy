init python:
    
    import socket

    HOST = 'localhost'    # The remote host
    PORT = 8081              # The same port as used by the server
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    count = 0
    
    def senduserid(userid):
        s.send('userid##'+userid)
        data = s.recv(1024)
        return data
        
    def sendlog(logstring):
        s.send('log##'+logstring)
        data = s.recv(1024)
    
    def edittext(sentence):
        s.send('edittext##'+sentence)
        data = s.recv(1024)
        return data

    def firstfile():
        s.send('firstfile')
        data = s.recv(1024)
        return data
        
    def nextfile():
        s.send('nextfile')
        data = s.recv(1024)
        return data

    def updatevars(key, val):
        s.send('updatevars##'+key+'##'+val)
        data = s.recv(1024)

    def updatestory():
        s.send('updatestory')
        data = s.recv(1024)
        
    def perform(funcname):
        s.send('perform##'+funcname)
        data = s.recv(1024)
        
    def endgame():
        s.close()