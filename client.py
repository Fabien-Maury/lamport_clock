import socket             
import time
import random

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
		print('Local event happening in process '+str(self.pid))

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
		fmsg = str(msg)+'.'+str(self.clock.time)
		self.clock.setStatus('s')
		self.clock.update()

		try:
			self.socket.send(fmsg.encode('ascii'))
			print('Sent to server : '+str(msg))
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
			self.sendMsg()
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


p1 = Process('p1', False, 1, 'client')

while True :  # main loop

	try:
		s = socket.socket()        
		port = 12345        # ports below 1025 are taken      
		s.connect(('10.0.2.7', port))  # replace with your IP address
		p1.socketUpdate(s)
	except Exception as e:
		print('Error (main loop) : '+str(e))

	p1.pickAction((random.choice([0, 1, 2])))  # randomly choose : local event, send, or receive (send not available for our client)
	s.close()
	print('Local clock is now : '+str(p1.clock.pid)+'='+str(p1.clock.time))
	print('-'*55)
	time.sleep(random.randint(1,3))     
