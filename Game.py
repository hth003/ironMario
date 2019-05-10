""" Game to play 'Lost Rovers'. This is the file you edit.
To make more ppm files, open a gif or jpg in xv and save as ppm raw.
Put the three ADTs in their own files.
"""
from gameboard import *
from random import *

'''------------------------------LINKED LIST ADT------------------------------'''
class Node:
    # Purpose: Store the part in the inventory
    def __init__(self, data = None, count = 0, next = None):
        """Initialize class Node. Input: name of part, its count and the pointer"""
        self.data = data
        self.count = count
        self.next = next

    def getData(self):
        """Access the data of the node"""
        return self.data

    def getCount(self):
        """Access the count of the node"""
        return self.count
    
class List:
    # Purpose: List ADT that store the inventory
    def __init__(self, initList = None):
        """Initialize datatype List"""
        self.head = None

    def __str__(self):
        """Return string representation of the list"""
        reprStr = ''
        currNode = self.head
        while currNode:
            reprStr = reprStr + str(currNode.count) + ' ' + str(currNode.data) + '\n'
            currNode = currNode.next
        return reprStr

    def isEmpty(self):
        """Check if the list is empty"""
        return self.head == None
    
    def isPartinList(self,partName, count):
        """Check if item in the list or not"""
        currNode = self.head
        while currNode:
            if currNode.data == partName and currNode.count >= count:
                return True
            currNode = currNode.next
        return False
        
    def addPart(self,name):
        """Add picked part to the inventory. Input: name (string) of part"""
        currNode = self.head
        while currNode is not None:
            if currNode.data == name: # if part in inventory already, just add count
                currNode.count += 1
                return
            currNode = currNode.next
        self.head = Node(name,1,self.head) # if part is not in inventory, make new node

    def removePart(self,name,count):
        """Remove item from the list"""
        currNode = self.head
        while currNode is not None:
            if currNode.data == name:
                if currNode.count > count:
                    currNode.count = currNode.count - count
                elif currNode.count == count:
                    if currNode == self.head:
                        self.head = currNode.next
                    else:
                        prevNode.next = currNode.next
            prevNode = currNode
            currNode = currNode.next
    
'''-----------------------------STACK ADT------------------------------------'''
class Stack(List):
    # Purpose: Stack ADT to store the entered portal
    def __init__(self):
        """Initialize Stack using linked list by inherit List class"""
        List.__init__(self)

    def push(self,obj):
        """Push an object at the beginning of the stack"""
        self.head = Node(obj,0,self.head)

    def pop(self):
        """Pop an object out of the stack"""
        if self.head is not None:
            currNode = self.head
            self.head = currNode.next
            return currNode.data
        return None
    
    def setTypeItem(self,data):
        """Set all same item to the same type"""
        currNode = self.head
        while currNode is not None:
            currNode.data.setType(data)
            currNode = currNode.next

    def peek(self):
        """Return the top of the stack"""
        return self.head.data
    
'''-----------------------------QUEUE ADT------------------------------------'''
class Queue:
    def __init__(self): # 1+1+1+1+1 => O(1)
        """Initialize circular array for queue ADT"""
        self._capacity = 7 #O(1)
        self._queue = [None] * self._capacity  #O(1)
        self._size = 0  #O(1)
        self._start = 0 #O(1)
        self._end = 0   #O(1)
        
    def __repr__(self): #O(1)
        return str(self._queue) # O(1)
    
    def isEmpty(self): # total O(1)
        """Is the queue empty?"""
        return self._size == 0 #O(1)
    
    def doubleCapacity(self): # total: O(n)
        """Double the capacity and expand the queue base on new capacity"""
        self._capacity = self._capacity * 2 #O(1)
        tempLs = [None] * self._capacity    #O(1)
        if self._start < self._end:         # if state ment: O(n)
            for i in range(self._size):     #O(n) - n is self._size
                tempLs[i] = self._queue[i]
        else: # else branch: O(x+y) = O(n) - n is self._size
            for i in range(self._end+1):    #O(x) 
                tempLs[i] = self._queue[i]
            for k in range(self._start,self._size): #O(y)
                tempLs[k+self._size] = self._queue[k]
            self._start = self._start + self._size #O(1)
        self._queue = tempLs #O(1)
        
    def enqueue(self,data): # total: O(n)
        """Enqueue an item at the end of the queue"""
        # if pass capacity, double capacity and the array
        while self._size >= self._capacity: #O(n)
            self.doubleCapacity() #O(n)
        if self._size != 0: # O(1)
            self._end = (self._end+1)% self._capacity # O(1)
        self._queue[self._end] = data # O(1)
        self._size += 1 # O(1)        

    def peek(self): # total: O(1)
        """Return the item at the top of the queue with thout making any change"""
        return self._queue[self._start] #O(1)
    
    def dequeue(self): # total O(1)
        """Dequeue the item at the top of the queue, return
        then delete it from the queue"""
        topItem = self._queue[self._start] #O(1)
        self._queue[self._start] = None    #O(1)
        self._start = (self._start+1)% self._capacity #O(1)
        self._size -= 1 #O(1)
        return topItem  #O(1)
    
'''-------------------------GAME OBJECTS------------------------------'''
class Item:
    #Purpose: a parent class that represent and manage all items in the room
    def __init__(self, itemType):
        """Input: a string represent item type. Purpose: initialize object Item"""
        self._itemType = itemType

    def getItemImage(self):
        """Input: self. Output: return a string of image file"""
        return str(self._itemType)+ ".ppm"

    def __str__(self):
        """Represent item by its type"""
        return self._itemType

    def setType(self, newType):
        """Set new item type"""
        self._itemType = newType
        
class ShipComponent(Item):
    #Purpose: represent ship component object of the game
    pass

class Portal(Item):
    #Purpose: represent portal object of the game
    def __init__(self, itemType, myRoom = None, myLocation = None):
        """Input: a string represent item type and portal location.
        Purpose: initialize lass Portal """
        Item.__init__(self,itemType)
        self._myRoom = myRoom
        self._myLocation = myLocation
        self._connectPortal = None

    def getRoom(self):
        """Return portal's room"""
        return self._myRoom

    def getLocation(self):
        """Return portal's location"""
        return self._myLocation

    def getConnectPortal(self):
        """Return connected portal"""
        return self._connectPortal

    def setConnectPortal(self,otherPortal):
        """Set portal pointing to its linked portal"""
        self._connectPortal = otherPortal
    
class Part(Item):
    #Purpose: represent part object of the game
    pass
        
class Room:
    #Purpose: Represent the room's map. Include a 2D array which
    #is the copy of the grid
    def __init__(self, size):
        """Input: the size of the room (an interger).
           Purpose: Initialize the room and create empty 2D array to store the room"""
        self._size = size
        self.map = [[None for i in range(self._size)] for j in range(self._size)]
  
    def __getitem__( self, ndxTuple ):
        """Input: position of item([r,c]. 
           Purpose: Get the content of the element at position [i,j] """
        row = ndxTuple[0]
        col = ndxTuple[1]
        return self.map[row][col]

    def __setitem__( self, ndxTuple, value ):
        """Input: position of item([r,c] and the replaced value. 
           Purpose: Set the content of the element at position [i,j] """
        row = ndxTuple[ 0 ]
        col = ndxTuple[ 1 ]
        self.map[row][col] = value

    def placeShipComponent(self):
        """Purpose: By hardcode, put ship component object into the map (the 2D array)"""
        self.map[6][7], self.map[7][6], self.map[7][7], self.map[7][8],\
                        self.map[8][6], self.map[8][8]\
                        = ShipComponent('headbroken'),ShipComponent('handbroken'),\
                        ShipComponent('bodybroken'),ShipComponent('handbroken'),\
                        ShipComponent('legbroken'),ShipComponent('legbroken')
   
    def placeItems(self, item):
        """Input: a string that indicate the item need to place.
           Purpose: Random the number and position of the input item and put
           those item on the map"""
        if item == 'Portal':
            numItem = randint(3,8)
        else:
            numItem = randint(5,15)
        typePart = ['wrench','resistor','bulb','mushroom','coin']
        for i in range(numItem):
            while True:
                r = randint(0,14)
                c = randint(0,14)
                if self.map[r][c] == None:
                    break
            if item == 'Portal':
                self.map[r][c] = Portal('pipe', myRoom = self, myLocation = (r,c))
            else:
                self.map[r][c] = Part(typePart[i%5])

    def searchPortal(self):
        """Search for empty portal in the room. Return its location."""
        for r in range(self._size):
            for c in range(self._size):
                if type(self.map[r][c]) == Portal:
                    if self.map[r][c].getConnectPortal() == None:
                        return self.map[r][c].getLocation()
        
class Rover:
    #Purpose: Represent the object Rover and store the position of rover
    def __init__(self, position):
        """Input: rover position. Purpose: Initialize rover object"""
        self._position = position

    def setPosition(self,newPos):
        """Set new position for rover"""
        self._position = newPos

    def getPosition(self):
        """Get rover's position"""
        return self._position

    def moveUp(self):
        """Move rover up one step.Return False if the move is illegal"""
        if self._position.y != 0:
            self._position.y -=1
            return True
        return False

    def moveDown(self):
        """Move rover down one step.Return False if the move is illegal"""
        if self._position.y != 14:
            self._position.y +=1
            return True
        return False

    def moveLeft(self):
        """Move rover left one step.Return False if the move is illegal"""
        if self._position.x != 0:
            self._position.x -=1
            return True
        return False

    def moveRight(self):
        """Move rover right one step.Return False if the move is illegal"""
        if self._position.x != 14:
            self._position.x +=1
            return True
        return False
            
'''--------------------------------TASK--------------------------------------'''
class Task:
    # Purpose: Represent the task in the game
    def __init__(self,name):
        """Initialize the task with its name and supplies"""
        self._name = name
        self._supplies = []
        self.generateSupplies()

    def __str__(self):
        """Return the string representation of the task"""
        reprStr = 'Help Mario build Iron Man suit!'+'\n' +'To make the ' + self._name + ',you need:'+'\n'
        for part in self._supplies:
            reprStr = reprStr + str(part.getCount()) + ' ' + part.getData() + '\n'
        return reprStr

    def getName(self):
        """Return the name of the task"""
        return self._name

    def getSupplies(self):
        """Return the supplies that task need"""
        return self._supplies

    def generateSupplies(self):
        """Generate random supplies for the task"""
        typePart = ['wrench','resistor','bulb','mushroom','coin']
        chosenPart = []
        for i in range(3):
            randomPart = choice(typePart)
            chosenPart.append(randomPart)
            typePart.remove(randomPart)
        for part in chosenPart:
            amount = randint(1,3)
            self._supplies.append(Node(part,amount))

class Tasks(Queue):
    # Purpose: Represent the queue of task in the game
    def __init__(self):
        """Initialize Tasks by inheriting Queue ADT"""
        Queue.__init__(self)

    def generateTaskName(self):
        """Generate all the tasks that the rover need to do."""
        brokenComponent = ['head','hand','leg','body','hand','leg']
        for component in brokenComponent:
            self.enqueue(Task(component))

'''-----------------------------MAIN GAME------------------------------------'''
class Game:
    #Purpose: Represent the Game object which opperate the game
    SIZE = 15 # rooms are 15x15
    def __init__(self):
        """Purpose: Start the game. Initialize the map and the rover."""
        self.gui = GameBoard("Iron Mario", self, Game.SIZE)
        self.map = self._makeRoom(True)
        self.rover = Rover(Point(randint(0,14),randint(0,14)))
        self.inventory = List()
        self.enteredPortal = Stack()
        self.task = Tasks()
        self.task.generateTaskName()

    def _makeRoom(self,isFirst):
        """Input: a boolean value indicate if the room is the first room or not.
           Output: the map of the room ( a 2D array)
           Purpose: Create the map of the room"""
        room = Room(Game.SIZE)
        if isFirst == True:
            room.placeShipComponent()
        room.placeItems('Portal')
        room.placeItems('Part')
        return room
        
    def startGame(self):
        self.gui.run()

    def getRoverImage(self):
        """ Called by GUI when screen updates.
            Returns image name (as a string) of the rover. 
		(Likely 'rover.ppm') """
        # Your code goes here, this code is just an example
        return 'mario.ppm'

    def getRoverLocation(self):
        """ Called by GUI when screen updates.
            Returns location (as a Point). """
        return self.rover.getPosition()

    def _checkPortal(self,point):
        """Check if there is portal at input location.
           Go to a new room if there is a portal."""
        thisPortal = self.map[point.y,point.x]
        if type(thisPortal) == Portal: # check if there is portal
            connectPortal = thisPortal.getConnectPortal()
            if connectPortal == None: # if it have no linked portal
                connectPortal = self._makeLinkPortal(thisPortal)
            else:
                self.map = connectPortal.getRoom() # jump to connected room
                newPPos = connectPortal.getLocation()
                self.rover.setPosition(Point(newPPos[1],newPPos[0]))
            # check and make change on the portal stack if going back
            if not self.enteredPortal.isEmpty() and self.enteredPortal.peek() == thisPortal: 
                self.enteredPortal.pop()
            else:
                self.enteredPortal.push(connectPortal)
            self._revertNormal()
            
    def _revertNormal(self):
        """Revert all portal(include flashing portal) to normal"""
        if not self.enteredPortal.isEmpty():
            self.enteredPortal.setTypeItem('pipe')

    def _makeLinkPortal(self,thisPortal):
        """Make a connect portal to thisPortal"""
        newRoom = self._makeRoom(False)
        newPPos = newRoom.searchPortal() # search for new portal
        newPortal = newRoom[newPPos[0],newPPos[1]]
        thisPortal.setConnectPortal(newPortal) # set connect portal 
        newPortal.setConnectPortal(thisPortal)
        self.map = newRoom 
        self.rover.setPosition(Point(newPPos[1],newPPos[0]))
        return newPortal
    
    def getImage(self, point):
        """ Called by GUI when screen updates.
            Returns image name (as a string) or None for the 
		part, ship component, or portal at the given 
		coordinates. ('engine.ppm' or 'cake.ppm' or 
		'portal.ppm', etc) """
        if self.map[point.y,point.x] != None:
            return self.map[point.y,point.x].getItemImage()

    def goUp(self):
        """ Called by GUI when button clicked.
            If legal, moves rover. If the robot lands
            on a portal, it will teleport. """
        check = self.rover.moveUp()
        if check == True:
            self._checkPortal(self.getRoverLocation())
  
    def goDown(self):
        """ Called by GUI when button clicked. 
            If legal, moves rover. If the robot lands
            on a portal, it will teleport. """
        check = self.rover.moveDown()
        if check == True:
            self._checkPortal(self.getRoverLocation())

    def goLeft(self):
        """ Called by GUI when button clicked. 
            If legal, moves rover. If the robot lands
            on a portal, it will teleport. """
        check = self.rover.moveLeft()
        if check == True:
            self._checkPortal(self.getRoverLocation())

    def goRight(self):
        """ Called by GUI when button clicked. 
            If legal, moves rover. If the robot lands
            on a portal, it will teleport. """
        check = self.rover.moveRight()
        if check == True:
            self._checkPortal(self.getRoverLocation())

    def showWayBack(self):
        """ Called by GUI when button clicked.
            Flash the portal leading towards home. """
        if not self.enteredPortal.isEmpty():
            prevPortal = self.enteredPortal.peek()
            prevPortal.setType('pipe-flashing')

    def getInventory(self):
        """ Called by GUI when inventory updates.
            Returns entire inventory (as a string). 
		3 cake
		2 screws
		1 rug
	  """
        return str(self.inventory)

    def pickUp(self):
        """ Called by GUI when button clicked. 
		If rover is standing on a part (not a portal 
		or ship component), pick it up and add it
		to the inventory. """
        pos = self.getRoverLocation()
        item = self.map[pos.y,pos.x]
        if type(item) == Part:
            self.inventory.addPart(str(item))
            self.map[pos.y,pos.x] = None

    def getCurrentTask(self):
        """ Called by GUI when task updates.
            Returns top task (as a string). 
		'Fix the engine using 2 cake, 3 rugs' or
		'You win!' 
 	  """
        if not self.task.isEmpty():
            return str(self.task.peek())
        else:
            return 'You win! Fly around with your new Iron Man suit!'

    def performTask(self):
        """ Called by the GUI when button clicked.
            If necessary parts are in inventory, and rover
            is on the relevant broken ship piece, then fixes
            ship piece and removes parts from inventory. If
            we run out of tasks, we win. """
        task = self.task.peek()
        position = self.rover.getPosition()
        if str(self.map[position.y,position.x]) == task.getName() + 'broken':
            for part in task.getSupplies():
                if not self.inventory.isPartinList(part.getData(),part.getCount()):
                    return
            for part in task.getSupplies():
                self.inventory.removePart(part.getData(),part.getCount())
            self.task.dequeue()
            self.map[position.y,position.x].setType(task.getName())

    # Put other methods here as needed.

# Put other classes here or in other files as needed.
'''-----------------------------TEST QUEUE METHOD----------------------------'''
def testQueue():
    """Test the queue ADT"""
    myQueue = Queue()
    myQueue.enqueue(1)
    myQueue.enqueue(2)
    myQueue.enqueue(3)
    print('Enqueue 1,2,3: ',myQueue)
    myQueue.enqueue(4)
    print('Peek: ',myQueue.peek())
    myQueue.dequeue()
    print('Enqueue 4+ dequeue: ',myQueue)
    myQueue.enqueue(5)
    print('Enqueue 5: ',myQueue)
    myQueue.enqueue(6)
    print('Enqueue 6: ',myQueue)
    myQueue.enqueue(7)
    print('Enqueue 7: ',myQueue)
    print('Peek: ',myQueue.peek())
    myQueue.dequeue()
    print('Dequeue: ',myQueue)

'''-----------------------------LAUNCH GAME-------------------------------------'''

""" Launch the game. """
#testQueue()
g = Game()
g.startGame() # This does not return until the game is over
