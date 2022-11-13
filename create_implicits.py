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


def createGraph(characters, relationships):
    graph = Graph()
    sib_incrementer = 1  # Used to generate sibling numbers; always increases every time one is assigned
    for character in characters:
        graph.addCharacter(character['ID'])
    for relationship in relationships:
        char1 = graph.getChar(relationship['CHARACTER1'])
        char2 = graph.getChar(relationship['CHARACTER2'])
        # Adds parents and children to the graph
        if relationship['TYPE'] == 'Parent - Child':
            char1.addChild(char2)
            char2.addParent(char1)
        # Adds siblings to the graph, and adds implicit siblings transitively
        # Eg if a & b are siblings and b & c are siblings, makes them all siblings via sibling_nums
        if relationship['TYPE'] == 'Sibling - Sibling':
            # If neither has a sibling number, create one and give it to both.
            if char1.sibling_num == 0 and char2.sibling_num == 0:
                char1.sibling_num = sib_incrementer
                char2.sibling_num = sib_incrementer
                sib_incrementer += 1

            # If char1 has a sibling num and char2 doesn't, just give char2 char1's number
            if char1.sibling_num != 0 and char2.sibling_num == 0:
                char2.sibling_num = char1.sibling_num

            # If both have sibling numbers, then they need to be unified; look for all instances of char2's number and
            # replace them with char1's.
            if char1.sibling_num != 0 and char2.sibling_num != 0:
                old_sibling_num = char2.sibling_num  # storing char2's current sibling num so when char2 is reached and
                # changed, it doesn't start erasing char1's siblings
                for char in graph.charList:
                    if graph.charList[char].sibling_num == old_sibling_num:
                        graph.charList[char].sibling_num = char1.sibling_num
    return graph


def implicit_siblings(graph):
    """Given a parent - child and sibling - sibling graph, adds all implicit siblings based on shared
    parents and returns the new graph"""
    # Finds the highest existing sib_number and sets the incrementer above it, that way any new sibling numbers needed
    # will not conflict with existing ones.
    sib_incrementor = 1
    for char in graph.charList:
        if graph.getChar(char).sibling_num > sib_incrementor:
            sib_incrementor = graph.getChar(char).sibling_num + 1

    for char in graph.charList:
        if len(graph.getChar(char).children) > 1:  # if a character has multiple children
            # Find any existing sibling numbers among the children
            sibling_numbers = []
            for child in graph.getChar(char).children:
                if child.sibling_num != 0:
                    sibling_numbers.append(child.sibling_num)

            if len(sibling_numbers) == 0:  # If none had a sibling number, generate a new one and assign it to all
                for child in graph.getChar(char).children:
                    child.sibling_num = sib_incrementor
                    sib_incrementor += 1

            # If all have sibling numbers, and they are all the same, move on to the next character
            if len(sibling_numbers) == len(graph.getChar(char).children) and len(set(sibling_numbers)) == 1:
                continue

            if len(sibling_numbers) == 1:  # If only one had a sibling number, give it to the rest
                for child in graph.getChar(char).children:
                    child.sibling_num = sibling_numbers[0]

            # If there are multiple sibling numbers, all need to be unified, along with characters with those numbers
            for subChar in graph.charList:
                if graph.getChar(subChar).sibling_num in sibling_numbers:
                    graph.getChar(subChar).sibling_num = sibling_numbers[0]

    return graph


def add_implicits(graph):
    graph = implicit_siblings(graph)
    return graph


def testGraph():
    characters = [{'ID': 1}, {'ID': 2}, {'ID': 3}, {'ID': 4}, {'ID': 5}, {'ID': 6}, {'ID': 7}, {'ID': 8}, {'ID': 9}]
    relationships = [{'CHARACTER1': 1, 'CHARACTER2': 2, 'TYPE': 'Parent - Child'},
                     {'CHARACTER1': 1, 'CHARACTER2': 3, 'TYPE': 'Parent - Child'},
                     {'CHARACTER1': 3, 'CHARACTER2': 4, 'TYPE': 'Sibling - Sibling'},
                     {'CHARACTER1': 5, 'CHARACTER2': 6, 'TYPE': 'Sibling - Sibling'},
                     {'CHARACTER1': 6, 'CHARACTER2': 7, 'TYPE': 'Sibling - Sibling'},
                     {'CHARACTER1': 3, 'CHARACTER2': 7, 'TYPE': 'Sibling - Sibling'},
                     {'CHARACTER1': 8, 'CHARACTER2': 9, 'TYPE': 'Parent - Child'},
                     {'CHARACTER1': 9, 'CHARACTER2': 1, 'TYPE': 'Sibling - Sibling'}, ]

    base_graph = createGraph(characters, relationships)
    graph = add_implicits(base_graph)
    for child in graph.getChar(1).children:
        print(child.id)
    print(graph.getChar(8).children[0].id)
    for character in graph.charList:
        char = graph.getChar(character)
        print('character: ' + str(character) + ' sibnum: ' + str(char.sibling_num))
        for parent in char.parents:
            if parent:
                print('character: ' + str(character) + ' Parent: ' + str(parent.id))
