import socket             
import datetime
import random
import string

class LamportClock:
    def __init__(self, pid):
        self.pid = pid
        self.time = 0
        self.remoteClockMemory = False
        self.status = 0

    def set(self, t):
        self.time = t
        print('Clock '+str(self.pid)+' is now : '+str(self.time))
        return()

    def increment(self):
        self.time = self.time+1
        print('Clock '+str(self.pid)+' was incremented to : '+str(self.time))
        return()

    def reset(self):
        self.time = 0
        print('Clock '+str(self.pid)+' was reset to : '+str(self.time))
        return()

    def setMemory(self, n):
        self.remoteClockMemory = n
        print("Clock "+str(self.pid)+"'s memory was set to : "+str(self.remoteClockMemory))
        return()

    def setStatus(self, arg):
        self.status = arg
        print("Clock "+str(self.pid)+"'s status was set to : "+str(self.status))
        return()

    def update(self):
        print('Clock '+str(self.pid)+' update : ')
        if self.status == 'l':
            self.increment()
        elif self.status == 's':
            self.increment()
        elif self.status == 'r':
            self.time = max(self.time, self.remoteClockMemory)+1
            print('Clock '+str(self.pid)+' is now : '+str(self.time))
        return()


class Process:
    def __init__(self, pid, socket, priority, role):
        self.pid = pid
        self.socket = socket
        self. priority = priority
        self.role = role
        clock = LamportClock(self.pid)
        self.clock = clock

    def mockLocalEvent(self):
        print('Local event happening in '+str(self.pid))

        ########################################

        # add some code here for a real event

        ########################################

        self.clock.setStatus('l')
        self.clock.setMemory(False)
        self.clock.update()
        return()

    def receiveMsg(self):   
        try:  
            msg = self.socket.recv(4096)

            fmsg, receivedTime = msg.decode('ascii').split('.')
            print('Received from server : '+str(fmsg))

    
            self.clock.setStatus('r')
            self.clock.setMemory(int(receivedTime))
            self.clock.update()
        
        except Exception as e:
            print('Error (receiveMsg) : '+str(e))
            self.clock.setStatus('l')
            self.clock.update()
        return()

    def sendMsg(self, msg):
        i = 0
        for i in range(0,10):
            self.clock.setStatus('s')
            self.clock.update()

            fmsg = str(msg)+'.'+str(self.clock.time)
            
            try:
                self.socket.settimeout(4)  # do not keep waiting after 4sec

                c, addr = self.socket.accept()
                print ('Connection from client : ', addr )
                c.send(fmsg.encode('ascii'))
                print('Sent to client : '+str(msg))
                c.close()
                
            except Exception as e:
                print('Error (sendMsg) : '+str(e))
                self.clock.setStatus('l')
            return()

    def pickAction(self, n):
        if n == 0:
            self.mockLocalEvent()
        if n == 1 and self.role != 'server':
            self.receiveMsg()
        elif n ==1 and self.role == 'server':
            self.mockLocalEvent()
        if n == 2 and self.role != 'client':
            self.sendMsg(content)
        elif n ==2 and self.role == 'client':
            self.mockLocalEvent()
        return()

    def socketUpdate(self, s):
        try:
            self.socket = s
            print('Process '+str(self.pid)+"'s socket updated")
        except Exception as e:
            print('Error (socket update) : '+str(e))
        return()


def randomWord(n): # cryptographically secure random generator of string content
    return(''.join(random.SystemRandom().choice(string.ascii_letters + string.digits) for _ in range(n)))


p2 = Process('p2', False, 1, 'server')


try:  
    s = socket.socket()        
    port = 12345                
    s.bind(('', port))         
    s.listen(5)
    p2.socketUpdate(s)
    print('Socket listening on port : '+str(port))
except Exception as e:
    print('Error (socket initializing) : '+str(e))              
  
while True:
    try:
        content = randomWord(6)
        p2.pickAction((random.choice([0, 1, 2])))
        print('-'*55)
        p2.sendMsg(content)
    except Exception as e:
        print('Error (main loop) : '+str(e))  
