

class Room(object): # from simple-text-adventure-game.py
    def __init__(self, name):     
        self.name = name
        self.exits = [None] * 4 # north, south, east, west
        self.items = [ ]
        if self.name=='The Prison':
            self.prisonLock=True
        elif self.name=='The Torture Chamber':
            self.goblinLock=True
        elif self.name=='The Goblin Room':
            self.exitLock=True
            self.goblinLife=True

        

    def getDirection(self, dirName):    
        dirName = dirName.lower()
        if (dirName in ['n', 'north']): return 0
        elif (dirName in ['s', 'south']): return 1
        elif (dirName in ['e', 'east']): return 2
        elif (dirName in ['w', 'west']): return 3
        else:
            print(f'Sorry, I do not recognize the direction {dirName}')
            return None

    def setExit(self, dirName, room):    
        direction = self.getDirection(dirName)
        self.exits[direction] = room

    def getExit(self, dirName):    
        direction = self.getDirection(dirName)
        if (direction == None):
            return None
        else:
            return self.exits[direction]

    def getAvailableDirNames(self):
        availableDirections = [ ]
        for dirName in ['North', 'South', 'East', 'West']:
            if (self.getExit(dirName) != None):
                availableDirections.append(dirName)
        if (availableDirections == [ ]):
            return 'None'
        else:
            return ', '.join(availableDirections)

class Item(object):     # from simple-text-adventure-game.py
    def __init__(self, name):
        self.name = name

class Game(object):    # from simple-text-adventure-game.py
    def __init__(self, name, goal, startingRoom, startingInventory):
        self.name = name
        self.goal = goal
        self.room = startingRoom
        self.commandCounter = 0
        self.inventory = startingInventory
        self.goblinLife = True
        self.prisonLock= True
        self.goblinLock=True
        self.exitLock = True
        self.gameOver = False

    def getCommand(self):
        self.commandCounter += 1
        response = input(f'[{self.commandCounter}] Your command --> ')
        print()
        if (response == ''): response = 'help'
        responseParts = response.split(' ')
        command = responseParts[0]
        target = '' if (len(responseParts) == 1) else responseParts[1]
        return command, target

    def play(self):
        print(f'Welcome to {self.name}!')
        print(f'Your goal: {self.goal}!')
        print('Just press enter for help.')
        while (not self.gameOver):
            self.doLook()
            command, target = self.getCommand()
            if (command == 'help'): self.doHelp()
            elif (command == 'look'): self.doLook()
            elif (command == 'go'): self.doGo(target)
            elif (command == 'get'): self.doGet(target)
            elif (command == 'read'): self.doRead(target)
            elif (command == 'use'): self.doUse(target)
            elif (command == 'quit'): break
            else: print(f'Unknown command: {command}. Enter "help" for help.')
        print('Goodbye!')

    def doHelp(self):
        print('''
Welcome to this fine game!  Here are some commands you should know:
    help (print this message)
    look (see what's around you and check the items in the room)
    go north (or just 'go n'), go south, go east, go west
    get thing
    read thing
    use thing
    quit
Have fun!''')

    def superhelp(self):
        print('''
Welcome to this fine game!  Here are the steps to winning in this game
    Get the stone from the corpse’s body
    Use it to destroy the lock
    Get out and move to Torture chamber
    Move to Storage
    Pick up the key to goblin room
    Move back to torture chamber
    Unlock the lock and move to Goblin room
    Pick up the key to exit
    Leave

Have fun!''')
        

    def printItems(self, items):
        if (len(items) == 0):
            print('Nothing.')
        else:
            itemNames = [item.name for item in items]
            print(', '.join(itemNames))

    def findItem(self, targetItemName, itemList):
        for item in itemList:
            if (item.name == targetItemName):
                return item
        return None

    def doLook(self):
        print(f'\nI am in {self.room.name}')
        print(f'I can go these directions: {self.room.getAvailableDirNames()}')
        print('I can see these things: ', end='')
        self.printItems(self.room.items)
        print('I am carrying these things: ', end='')
        self.printItems(self.inventory)
        print()

    def doGo(self, dirName):
        newRoom = self.room.getExit(dirName)
        if (newRoom == None):
            print(f'Sorry, I cannot go in that direction.')
        elif newRoom.name == 'The Torture Chamber':
            if self.prisonLock==False:
                self.room = newRoom
            else:
                print("You cannot move as you are still in the prison.")
        elif newRoom.name == 'The Goblin Room':
            if self.goblinLock==False:
                self.room = newRoom
                if self.goblinLife:
                    print("A goblin is sleeping on his bed.")
                else:
                    print("There's a dead goblin on his bed.")
            else:
                print("The goblin's room is locked.")
        elif newRoom.name == 'The Exit':
            if self.exitLock==False:
                self.room=newRoom
                print("You managed to escape from the Goblin's hideout!")
                self.gameOver = True
            else:
                print("The exit door is locked.")
        else:
            self.room = newRoom
            

    def doGet(self, itemName):
        item = self.findItem(itemName, self.room.items)
        if (item == None):
            print('Sorry, but I do not see that here.')
        else:
            self.room.items.remove(item)
            self.inventory.append(item)

    def doRead(self,itemName):
        item = self.findItem(itemName, self.inventory)
        if (item.name == 'letter'):
            print("If you are reading this message, it probably means " + \
                  "I’m already dead. and a goblin is planning to" + \
                   "have you as his next meal. Before you get eaten" + \
                    "break the lock and get out.I was able to wear it down" +\
                    "enough over days with a sharp stone I found, but I no"+\
                    "longer have enough energy left to escape this place."+\
                    "Get out and take any of the weapons in that creature’s" +\
                    "torture chamber. You should be able to find the key to" +\
                    "its room in the storage; that goblin always leave it there" + \
                    "That thing is always carrying the key to the exit" + \
                    "with it 24/7…best of luck. Don't end up like me." + \
                    "Kill it if you want to. Prioritize your survival.")
        elif (item == None):
            print("Sorry, but I do not see anything.")
        else:
            print("sorry, but how do you even read that?")

    def doUse(self,itemName):
        stone = self.findItem('stone',self.inventory)
        Goblin_key=self.findItem('key_to_Goblin_Room',self.inventory)
        Exit_key=self.findItem('Exit_key',self.inventory)
        dagger=self.findItem('dagger',self.inventory)

        print("itemName",itemName)
        print("self.room",self.room.name)
        if (itemName != 'stone') and (itemName != "key_to_Goblin_Room")\
           and (itemName != 'Exit_key') and (itemName != 'dagger'):
            print ("I do not know how to use that!")
        elif (itemName == 'stone') and (self.room.name == 'The Prison'):
            if (stone==None):
                print ("I do not have a stone!")
            else:
                print("The stone broke, but you broke out of prison")
                self.inventory.remove(stone)
                self.prisonLock = False
        elif (itemName == 'key_to_Goblin_Room') and (self.room.name == 'The Torture Chamber'):
            if (Goblin_key==None):
                print ("I do not have a key to the Goblin's room!")
            else:
                print("You opened the door to the Goblin's room; the key broke")
                self.goblinLock = False
        elif (itemName == 'dagger') and (self.room.name == 'The Goblin Room'):
            if (dagger==None):
                print ("I do not have a dagger!")
            else:
                if self.goblinLife:
                    print("You stabbed the goblin's forehead. It died immediately.")
                    self.goblinLife=False
                else:
                    print("It's already dead, you sicko.")
                
        elif (itemName == 'Exit_key') and (self.room.name == 'The Goblin Room'):
            if (Exit_key==None):
                print ("I do not have a key to the exit!")
            else:
                print("You opened the door to the Exit.")
                self.exitLock = False
        else:
            print("There's right time and place for everything, but this isn't it.")

    

def playSimpleGame():
    # Make the Rooms
    Prison= Room('The Prison')
    Torture_Chamber = Room('The Torture Chamber')
    Storage = Room('The Storage')
    Goblin_Room = Room('The Goblin Room')
    Exit=Room('The Exit')

    # Make the map
    Prison.setExit('North', Torture_Chamber)
    Torture_Chamber.setExit('North', Goblin_Room)
    Torture_Chamber.setExit('West', Storage)
    Torture_Chamber.setExit('South', Prison)
    Storage.setExit('East', Torture_Chamber)
    Goblin_Room.setExit('East', Exit)

    # Make some items and add them to rooms
    stone=Item("stone")
    Prison.items.append(stone)
    
    letter=Item("letter")
    Prison.items.append(letter)
    
    dagger=Item("dagger")
    Torture_Chamber.items.append(dagger)
    
    key_to_Goblin_Room=Item("key_to_Goblin_Room")
    Storage.items.append(key_to_Goblin_Room)

    Exit_key=Item("Exit_key")
    Goblin_Room.items.append(Exit_key)


    # Make the game and play it. It starts from the prison room
    game = Game('Goblin Dungeon Game',
                'Escape from the Goblin Hideout',
                Prison,
                [ ])
    game.play()

playSimpleGame()
