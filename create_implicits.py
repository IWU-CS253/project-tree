# This Character and Graph classes in this code aim to use a graph structure to simplify running through relationships
# between characters, represented as nodes and directional (parent or child) edges.

# The classes are built upon code written by Andrew Shallue, which itself was a modification of code
# found in chapter 6 of Problem Solving with Algorithms and Data Structures using Python, by Miller and Ranum

class Character:
    def __init__(self, num):
        self.id = num
        self.children = []  # list of children characters
        self.parents = []  # list of parent characters
        self.niblings = []  # list of nibling characters
        self.piblings = []  # list of pibling characters
        self.cousins = []  # list of cousin characters
        self.grandparents = {}  # Dictionary of grandparents; keys are character ids, values are levels
        # e.g. distinguishing great grandparent from great ... grandparent
        self.grandchildren = {}  # Same functionality as grandparents dictionary
        self.sibling_num = 0  # To store a sibling code if any are added. Sibling codes allow all siblings to be
        # indirectly connected; all characters that share the same sibling_num are siblings unless it is 0

    def add_child(self, child):
        self.children.append(child)

    def add_parent(self, parent):
        self.parents.append(parent)


class Graph:
    def __init__(self):
        self.charList = {}
        self.numCharacter = 0
        self.charKey = {}

    def add_character(self, key):  # adds a character to the graph
        self.numCharacter += 1
        newCharacter = Character(key)
        self.charList[key] = newCharacter
        return newCharacter

    def add_Parent_Child(self, p, c):
        self.charList[p].addChild(self.charList[c])
        self.charList[c].addParent(self.charList[c])

    def get_char(self, n):  # checks whether 'n' is in the graph
        if n in self.charList:
            return self.charList[n]
        else:
            return None


def create_graph(characters, relationships):
    """Given a set of characters and relationships (sqlite objects including, at minimum, character ids and relationship
    types), creates a graph object and stores the characters as vertices and parent-child relationships as directional
    edges. Siblings are given a number, and all characters that share the same sibling number are siblings."""
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


def implicit_parents(graph):
    for character in graph.charList:
        char = graph.getChar(character)
        if len(char.parents) > 0 and char.sibling_num != 0:  # If a character has a parent and has siblings
            for subCharacter in graph.charList:
                subChar = graph.getChar(subCharacter)
                # If a character is one of the siblings of the above character, give them all of their parents, and
                # the parents the sibling
                if subChar.sibling_num == char.sibling_num:
                    for parent in char.parents:
                        if parent not in subChar.parents:  # Prevents duplicates in the parents list
                            subChar.parents.append(parent)
                            parent.children.append(subChar)

    return graph


def implicit_piblings(graph):
    for character in graph.charList:
        char = graph.getChar(character)
        if len(char.children) > 0 and char.sibling_num != 0:  # If a character has children and siblings:
            for child in char.children:
                for sibling in graph.charList:
                    sib = graph.getChar(sibling)
                    if sib.sibling_num == char.sibling_num and sib != char:
                        child.piblings.append(sib)
                        sib.niblings.append(child)
    return graph


def implicit_cousins(graph):
    for character in graph.charList:
        char = graph.getChar(character)
        if len(char.piblings) != 0:
            for pibling in char.piblings:
                for child in pibling.children:
                    if child.sibling_num != char.sibling_num:
                        if child not in char.cousins:
                            char.cousins.append(child)
                        if char not in child.cousins:
                            child.cousins.append(char)

    return graph


def recur_grandparents(graph, base_char, cur_char, level=0):
    for p in cur_char.parents:  # Looping through all parents' parents
        if p not in base_char.grandparents:
            if level == 0:
                cur_char.grandparents[p.id] = 'Grandparent'
                p.grandchildren[base_char.id] = 'Grandchild'
            else:
                greats = ''
                for i in range(level):
                    greats = 'Great ' + greats
                base_char.grandparents[p.id] = greats + 'Grandparent'
                p.grandchildren[base_char.id] = greats + 'Grandchild'
            level += 1
            recur_grandparents(graph, base_char, p, level)
    return graph


def implicit_grandparents(graph):
    for character in graph.charList:
        char = graph.getChar(character)
        if len(char.parents) != 0:
            for v in char.parents:
                graph = recur_grandparents(graph, char, v)
    return graph


def add_implicits(graph):
    graph = implicit_siblings(graph)
    graph = implicit_parents(graph)
    graph = implicit_piblings(graph)
    graph = implicit_cousins(graph)
    graph = implicit_grandparents(graph)
    return graph


def test_graph():
    characters = [{'ID': 1}, {'ID': 2}, {'ID': 3}, {'ID': 4}, {'ID': 5}, {'ID': 6}, {'ID': 7}, {'ID': 8}, {'ID': 9},
                  {'ID': 10}, {'ID': 11}, {'ID': 12}]
    # This format mirrors the way sqlite objects are structured, and how we will access the relevant attributes
    relationships = [{'CHARACTER1': 1, 'CHARACTER2': 2, 'TYPE': 'Parent - Child'},
                     {'CHARACTER1': 1, 'CHARACTER2': 3, 'TYPE': 'Parent - Child'},
                     {'CHARACTER1': 3, 'CHARACTER2': 4, 'TYPE': 'Sibling - Sibling'},
                     {'CHARACTER1': 5, 'CHARACTER2': 6, 'TYPE': 'Sibling - Sibling'},
                     {'CHARACTER1': 6, 'CHARACTER2': 7, 'TYPE': 'Sibling - Sibling'},
                     {'CHARACTER1': 3, 'CHARACTER2': 7, 'TYPE': 'Sibling - Sibling'},
                     {'CHARACTER1': 8, 'CHARACTER2': 9, 'TYPE': 'Parent - Child'},
                     {'CHARACTER1': 9, 'CHARACTER2': 1, 'TYPE': 'Sibling - Sibling'},
                     {'CHARACTER1': 9, 'CHARACTER2': 10, 'TYPE': 'Parent - Child'},
                     {'CHARACTER1': 10, 'CHARACTER2': 11, 'TYPE': 'Parent - Child'},
                     {'CHARACTER1': 11, 'CHARACTER2': 12, 'TYPE': 'Parent - Child'}]

    base_graph = createGraph(characters, relationships)
    graph = add_implicits(base_graph)
    for child in graph.getChar(1).children:
        print(child.id)
    print(graph.getChar(8).children[0].id)
    for character in graph.charList:
        char = graph.getChar(character)
        print('character: ', str(character), ' sibnum: ', str(char.sibling_num))
        for parent in char.parents:
            if parent:
                print('character: ', str(character), ' Parent: ', str(parent.id))
        for nibling in char.niblings:
            if nibling:
                print('character: ', str(character), ' Nibling: ', str(nibling.id))
        for pibling in char.piblings:
            if pibling:
                print('character: ', str(character), ' Pibling: ', str(pibling.id))
        for cousin in char.cousins:
            if cousin:
                print('character: ', str(character), ' Cousin: ', str(cousin.id))
        for grandparent in char.grandparents:
            if grandparent:
                print('character: ', str(character), ' Grandparent: ', str(grandparent), str(char.grandparents[grandparent]))
