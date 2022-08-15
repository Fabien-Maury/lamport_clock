class VectorClock:
	def __init__(self, pid, size):
		self.pid = pid
		self.size = size
		self.vector = [0]*self.size
		self.remoteVectorMemory = False
		self.status = [0]*self.size

		def set(self, v):
        self.vector = v
        print('Clock '+str(self.pid)+' is now : '+str(self.vector))
        return()

    def increment(self, process):
    	newVector=[]
        for i in range(0,len(self.vector)):
        	if process == 'all':
        		newVector.append(newVector[i]+1)

        	else:
        		if i == process:
        			newVector.append(self.vector[i]+1)
        		else:
        			newVector.append(self.vector[i])
        self.vector = newVector


        print('Process '+str(process)+'on clock '+str(self.pid)+' was incremented to : '+str(self.vector))
        return()

    def reset(self, process):
        for i in range(0,len(self.vector)):
        	if process == 'all':
        		newVector.append(0)

        	else:
        		if i == process:
        			newVector.append(0)
        		else:
        			newVector.append(self.vector[i])
        self.vector = newVector
        print('Process'+str(process)+'on clock '+str(self.pid)+' was reset to 0')
        return()

    def setMemory(self, v):
        self.remoteVectorMemory = v
        print("Vector "+str(self.pid)+"'s memory was set to : "+str(self.remoteVectorMemory))
        return()

    def setStatus(self, process, arg):
        self.status[process] = arg
        print('Process '+str(process)+" on clock "+str(self.pid)+"'s status was set to : "+str(self.status[process]))
        return()

    def update(self, process)
        print('Vector '+str(self.pid)+' update : ')


        if self.status[process] == 'l':
            self.increment(process)
        elif self.status[process] == 's':
            self.increment(process)
        elif self.status[process] == 'r':
        	newVector = self.vector
        	newVector[process] = self.vector[process]+1
        	for i in range(0, len(self.vector)):
        		newVector[i] = max(newVector[i], self.remoteVectorMemory[i])

        	self.vector = newVector
        	print('Vector '+str(self.pid)+' is now : '+str(self.vector))
        return()
