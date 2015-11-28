import math

nodes 		= 0			# number of nodes
CapMatrix 	= None		# capacity matrix
FlowMatrix 	= None		# flow matrix
MaxFlow		= 0			# flow to T
nodeArray   = [ ]
pathList 	= [ ]
usedList	= [ ]

def initialize():
	global nodes
	global CapMatrix
	global FlowMatrix
	global MaxFlow
	
	print "Please enter the number of nodes, not including S and T"
	nodes = int(raw_input("Number of nodes: "))
	nodes += 2
	print "So, including S and T, there are " + str(nodes) + " nodes."
	print "\nNow will ask for connectivity of each node, forward flow only"
	print "Remember that 0 = S and " + str(nodes-1) + " = T."
	print "Enter a -1 if you want to pass on to the next node"
	
	CapMatrix  = [[0 for i in range(nodes)] for j in range(nodes)]
	FlowMatrix = [[0 for i in range(nodes)] for j in range(nodes)]
	#CapMatrix[1][2] = 4
	
	tempCap = 0
	for x in range(nodes):
		while True:
			tempConn = int(raw_input("Node " + str(x) + " flows to node: "))
			if (tempConn == -1):
				print "going to next node..."
				break	# if NaN
			if (tempConn >= nodes):
				print "out of range! continuing..."
				continue
			tempCap  = int(raw_input("With capacity: "))
			print "Alright, updating matrix...\n"
			CapMatrix[x][tempConn] = tempCap	
	
	
def FindNMPHandler():
	global nodes
	global CapMatrix
	global FlowMatrix
	global MaxFlow
	global nodeArray
	global startNode
	global pathList
	global usedList
	
	count = 1000000
	while count > 0:
		FindNMP(0, [ ])
		for path in pathList:
			print path
			usedList.append(path)
			AugmentPath(path)
			pathList = [ ]
			break
		count -= 1
		#print count
	return True
	

def FindNMP(x, array):
	global nodes
	global CapMatrix
	global FlowMatrix
	global pathList
	global usedList
	
	#find a non-max path
	if abs(x) == nodes-1:
		if usedList.count(array) == 0:
			pathList.append(array)
			print array
		return
	
	for k in range(1,nodes):
		#print "\n\ncalled again - x,k = " + str(x) + "," + str(k)
		if k == x or array.count(k) != 0:
			continue
		
		if CapMatrix[x][k] != 0 and IsNonMax(x,k):
			array.append(k)
			FindNMP(k, array)
			#return -1
		elif CapMatrix[k][x] != 0 and FlowMatrix[k][x] > 0:
			array.append(k*-1)
			FindNMP(k, array)
			#return -1
	
	#print "returned none\n"
	return None		# nothing found :(


def IsNonMax(x,y):
	global nodes
	global CapMatrix
	global FlowMatrix
	global MaxFlow
	
	
	if CapMatrix[x][y] > FlowMatrix[x][y]:
		return True	
	return False


def AugmentPath(path):
	global nodes
	global CapMatrix
	global FlowMatrix
	global MaxFlow
	
	# first, find max flow increase
	prevNode = 0
	minVal = 99999
	for node in path:
		absNode = abs(node)
		if node > 0:
			val = CapMatrix[prevNode][absNode]
		if node < 0:
			val = CapMatrix[absNode][prevNode]
		if val <= minVal:
			minVal = val
		prevNode = node
	
	prevNode = 0
	for node in path:
		absNode = abs(node)
		if node > 0:
			val = FlowMatrix[prevNode][absNode]
			val += minVal
			FlowMatrix[prevNode][absNode] = val
		if node < 0:
			val = FlowMatrix[absNode][prevNode]
			val -= minVal
			FlowMatrix[absNode][prevNode] = val
		prevNode = node
	MaxFlow += minVal
	
initialize()
FindNMPHandler()
print "done?"
print "MaxFlow = " + str(MaxFlow)
print "Flow matrix: "
print FlowMatrix