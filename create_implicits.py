import app

class Character:
    def __init__(self, num):
        self.id = num
        self.children = []  # list of children Character
        self.parents = []  # list of parent Character
        self.sibling_num = None  # To store a sibling code if any are added

    # Adds a child Character
    def addChild(self, child):
        self.children.append(child)

    def addParent(self, parent):
        self.parents.append(parent)

    def __str__(self):
        return str(self.id)


class Graph:
    def __init__(self):
        self.charList = {}
        self.numCharacter = 0
        self.charKey = {}

    def addCharacter(self, key):  # adds a character to the graph
        self.numCharacter += 1
        newCharacter = Character(key)
        self.charList[key] = newCharacter
        return newCharacter

    def addParent_Child(self, p, c):
        self.charList[p].addChild(self.charList[c])
        self.charList[c].addParent(self.charList[c])
        
    def getChar(self, n):  # checks whether 'n' is in the graph
        if n in self.charList:
            return self.charList[n]
        else:
            return None
        

def createGraph(relationships, characters):
    graph = Graph()
    for character in characters:
        graph.addCharacter(character['ID'])
    for relationship in relationships:
        if relationship['TYPE'] == 'Parent - Child':
            if graph.getChar(relationship['CHARACTER1']):


            
            
            
        

