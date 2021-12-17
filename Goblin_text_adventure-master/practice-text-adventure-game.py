# simple-text-adventure-game.py

# This is a very simple text adventure game
# in the spirit of Zork or Scott Adams adventures
# (though much, much, much simpler).
# For fun, try some of these: http://zorkonline.net

# This is mostly just to demonstrate using OOP and 1d lists,
# and so the game infrastructure is minimal, just enough
# to make a reasonably fun game to play.

# Have fun and be creative with your own games, but
# also be sure to understand how every method in this file
# works!

class Room(object):
    def __init__(self, name):
        self.name = name
        self.exits = [None] * 4 # north, south, east, west

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

class Item(object):
    def __init__(self, name, shortName):
        self.name = name
        self.shortName = shortName

class Game(object):
    def __init__(self, name, goal, startingRoom, startingInventory):
        self.name = name
        self.goal = goal
        self.room = startingRoom
        self.commandCounter = 0
        self.inventory = startingInventory
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
            elif (command == 'put'): self.doPut(target)
            elif (command == 'pour'): self.doPour(target)
            elif (command == 'drink'): self.doDrink(target)
            elif (command == 'quit'): break
            else: print(f'Unknown command: {command}. Enter "help" for help.')
        print('Goodbye!')

    def doHelp(self):
        print('''
Welcome to this fine game!  Here are some commands I know:
    help (print this message)
    look (see what's around you)
    go north (or just 'go n'), go south, go east, go west
    get thing
    put thing
    pour thing
    drink thing
    quit
Have fun!''')

    def printItems(self, items):
        if (len(items) == 0):
            print('Nothing.')
        else:
            itemNames = [item.name for item in items]
            print(', '.join(itemNames))

    def findItem(self, targetItemName, itemList):
        for item in itemList:
            if (item.shortName == targetItemName):
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
        else:
            self.room = newRoom

    def doGet(self, itemName):
        item = self.findItem(itemName, self.room.items)
        if (item == None):
            print('Sorry, but I do not see that here.')
        elif (len(self.inventory) == 2):
            print('Sorry, I cannot carry more (maybe put something down)')
        else:
            self.room.items.remove(item)
            self.inventory.append(item)

    def doPut(self, itemName):
        item = self.findItem(itemName, self.inventory)
        if (item == None):
            print('Sorry, but I do not seem to be carrying that!')
        else:
            self.inventory.remove(item)
            self.room.items.append(item)

    def doPour(self, itemName):
        pitcher = self.findItem('pitcher', self.inventory)
        glass = self.findItem('glass', self.inventory)
        if (itemName != 'water'):
            print('I do not know how to pour that!')
        elif (pitcher == None):
            print('I am not holding a pitcher of water!')
        elif (glass == None):
            print('I am not holding a glass!')
        elif ('full' in glass.name):
            print('The glass is already full!')
        else:
            glass.name = 'A full glass of water'

    def doDrink(self, itemName):
        glass = self.findItem('glass', self.inventory)
        if (itemName != 'water'):
            print('Ewww, that sounds yucky.')
        elif (glass == None):
            print('I am not carrying a glass of water!')
        elif ('full' not in glass.name):
            print('The glass is not full!')
        elif ('Porch' not in self.room.name):
            print("It's not proper to drink water inside the house.")
        else:
            print('Delicious, cool, refreshing water.  Yummmmmm!!!!')
            print('You did it!!!!  You won!!!!!')
            self.gameOver = True

def playSimpleGame():
    # Make the Rooms
    kitchen = Room('The Kitchen')
    porch = Room('The Porch')
    familyRoom = Room('The Family Room')
    study = Room('The Study')

    # Make the map (note: it need not be physically possible)
    kitchen.setExit('West', porch)
    porch.setExit('East', kitchen)
    kitchen.setExit('East', familyRoom)
    kitchen.setExit('South', study)
    familyRoom.setExit('South', study)
    study.setExit('North', kitchen)

    # Make some items
    pitcher = Item('a water pitcher', 'pitcher')
    kitchen.items.append(pitcher)
    glass = Item('an empty glass', 'glass')
    study.items.append(glass)
    frog = Item('a happy bouncy green frog', 'frog')

    # Make the game and play it
    game = Game('This Simple Example Game',
                'Drink the water',
                kitchen,
                [])
    game.play()

playSimpleGame()
