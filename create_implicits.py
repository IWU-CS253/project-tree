# This Character and Graph classes in this code aim to use a graph structure to simplify running through relationships
# between characters, represented as nodes and directional (parent or child) edges.

# The classes are built upon code written by Andrew Shallue, which itself was a modification of code
# found in chapter 6 of Problem Solving with Algorithms and Data Structures using Python, by Miller and Ranum

class Character:
    def __init__(self, num):
        self.id = num
        self.children = []  # list of children characters
        self.parents = []  # list of parent characters
        self.sibling_num = 0  # To store a sibling code if any are added. Sibling codes allow all siblings to be
        # indirectly connected; all characters that share the same sibling_num are siblings unless it is 0

    def addChild(self, child):
        self.children.append(child)

    def addParent(self, parent):
        self.parents.append(parent)


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
