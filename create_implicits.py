# This Character and Graph classes in this code aim to use a graph structure to simplify running through relationships
# between characters, represented as nodes and directional (parent or child) edges.

# The classes are built upon code written by Andrew Shallue, which itself was a modification of code
# found in chapter 6 of Problem Solving with Algorithms and Data Structures using Python, by Miller and Ranum

class Character:
    def __init__(self, num, name):
        self.id = num
        self.name = name
        self.children = []  # list of children characters
        self.parents = []  # list of parent characters
        self.niblings = []  # list of nibling characters
        self.piblings = []  # list of pibling characters
        self.cousins = []  # list of cousin characters
        self.generation = None
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
        self.charKey = {}

    def add_character(self, key, name):  # adds a character to the graph
        new_character = Character(key, name)
        self.charList[key] = new_character
        return new_character

    def add_Parent_Child(self, p, c):
        self.charList[p].add_child(self.charList[c])
        self.charList[c].add_parent(self.charList[c])

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
        graph.add_character(character['ID'], character['NAME'])
    for relationship in relationships:
        char1 = graph.get_char(relationship['CHARACTER1'])
        char2 = graph.get_char(relationship['CHARACTER2'])
        # Adds parents and children to the graph
        if relationship['TYPE'] == 'Parent - Child':
            char1.add_child(char2)
            char2.add_parent(char1)

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
        if graph.get_char(char).sibling_num >= sib_incrementor:
            sib_incrementor = graph.get_char(char).sibling_num + 1

    for char in graph.charList:
        if len(graph.get_char(char).children) > 1:  # if a character has multiple children
            # Find any existing sibling numbers among the children
            sibling_numbers = []
            for child in graph.get_char(char).children:
                if child.sibling_num != 0:
                    sibling_numbers.append(child.sibling_num)

            if len(sibling_numbers) == 0:  # If none had a sibling number, generate a new one and assign it to all
                for child in graph.get_char(char).children:
                    child.sibling_num = sib_incrementor

                sib_incrementor += 1

            # If all have sibling numbers, and they are all the same, move on to the next character
            if len(sibling_numbers) == len(graph.get_char(char).children) and len(set(sibling_numbers)) == 1:
                continue

            if len(sibling_numbers) == 1:  # If only one had a sibling number, give it to the rest
                for child in graph.get_char(char).children:
                    child.sibling_num = sibling_numbers[0]

            # If there are multiple sibling numbers, all need to be unified, along with characters with those numbers
            for subChar in graph.charList:
                if graph.get_char(subChar).sibling_num in sibling_numbers:
                    graph.get_char(subChar).sibling_num = sibling_numbers[0]

    return graph


def implicit_parents(graph):
    for character in graph.charList:
        char = graph.get_char(character)
        if len(char.parents) > 0 and char.sibling_num != 0:  # If a character has a parent and has siblings
            for subCharacter in graph.charList:
                subChar = graph.get_char(subCharacter)
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
        char = graph.get_char(character)
        if len(char.children) > 0 and char.sibling_num != 0:  # If a character has children and siblings:
            for child in char.children:
                for sibling in graph.charList:
                    sib = graph.get_char(sibling)
                    if sib.sibling_num == char.sibling_num and sib != char:
                        child.piblings.append(sib)
                        sib.niblings.append(child)
    return graph


def implicit_cousins(graph):
    for character in graph.charList:
        char = graph.get_char(character)
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
                base_char.grandparents[p.id] = 'Grandparent'
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
        char = graph.get_char(character)
        for parent in char.parents:
            graph = recur_grandparents(graph, char, parent)
    return graph


def add_implicits(graph):
    """Takes a graph and applies all implicit relationship functions to it, returning the new graph."""
    graph = implicit_siblings(graph)
    graph = implicit_parents(graph)
    graph = implicit_piblings(graph)
    graph = implicit_cousins(graph)
    graph = implicit_grandparents(graph)
    return graph


def merge_implicits(characters, relationships):
    """Given a set of characters and relationships (sqlite objects including, at minimum, character ids and relationship
    types), creates a graph object to calculate additional implicit relationships. Adds those relationships to the
     relationship set, and returns it, along with the resulting graph."""

    graph = add_implicits(create_graph(characters, relationships))
    implicit_rels = []

    rel_list = []  # Simplifies avoiding duplicates, since relationship objects are fairly complex and difficult to
    # check exactly without tracking descriptions across the whole file. Also keeps implicits and explicits separate.
    for relationship in relationships:
        rel_list.append((relationship['CHARACTER1'], relationship['CHARACTER2'], relationship['TYPE']))

    for character in graph.charList:
        char = graph.get_char(character)
        if char.sibling_num != 0:  # Ensure that the character has any siblings before looping through and checking for them
            for sibling in graph.charList:
                sib = graph.get_char(sibling)
                if sib.sibling_num == char.sibling_num and char.id != sib.id:
                    # The one ready to put in the relationships list
                    full_rel = {'CHARACTER1': char.id, 'CHARACTER2': sib.id, 'TYPE': 'Sibling - Sibling',
                                'CHAR1_NAME': char.name, 'CHAR2_NAME': sib.name}
                    rel = (char.id, sib.id, 'Sibling - Sibling')
                    alt_rel = (sib.id, char.id, 'Sibling - Sibling')
                    if rel not in rel_list and alt_rel not in rel_list:
                        implicit_rels.append(full_rel)
                        rel_list.append(rel)
        for parent in char.parents:
            full_rel = {'CHARACTER1': parent.id, 'CHARACTER2': char.id, 'TYPE': 'Parent - Child',
                        'CHAR1_NAME': parent.name, 'CHAR2_NAME': char.name}
            rel = (parent.id, char.id, 'Parent - Child')
            if rel not in rel_list:
                implicit_rels.append(full_rel)
        for pibling in char.piblings:
            implicit_rels.append({'CHARACTER1': pibling.id, 'CHARACTER2': char.id, 'TYPE': 'Pibling - Nibling',
                                  'CHAR1_NAME': pibling.name, 'CHAR2_NAME': char.name})
        for cousin in char.cousins:
            full_rel = {'CHARACTER1': char.id, 'CHARACTER2': cousin.id, 'TYPE': 'Cousin - Cousin',
                        'CHAR1_NAME': char.name, 'CHAR2_NAME': cousin.name}
            rel = (char.id, cousin.id, 'Cousin - Cousin')
            alt_rel = (cousin.id, char.id, 'Cousin - Cousin')
            if rel not in rel_list and alt_rel not in rel_list:
                implicit_rels.append(full_rel)
                rel_list.append(rel)
        for grandparent in char.grandparents:
            gparent = graph.get_char(grandparent)  # Since iterating through gives us the keys, aka the ids
            implicit_rels.append({'CHARACTER1': gparent.id, 'CHARACTER2': char.id,
                                  'TYPE': char.grandparents[grandparent] + ' - ' + gparent.grandchildren[char.id],
                                  'CHAR1_NAME': gparent.name, 'CHAR2_NAME': char.name})

    return implicit_rels


def test_graph():
    characters = [{'ID': 1, 'NAME': 'A'}, {'ID': 2, 'NAME': 'B'}, {'ID': 3, 'NAME': 'C'}, {'ID': 4, 'NAME': 'D'},
                  {'ID': 5, 'NAME': 'E'},
                  {'ID': 6, 'NAME': 'F'}, {'ID': 7, 'NAME': 'G'}, {'ID': 8, 'NAME': 'H'}, {'ID': 9, 'NAME': 'I'},
                  {'ID': 10, 'NAME': 'J'}, {'ID': 11, 'NAME': 'K'}, {'ID': 12, 'NAME': 'L'}, {'ID': 13, 'NAME': 'M'},
                  {'ID': 14, 'NAME': 'M'}]
    # This format mirrors the way sqlite objects are structured, and how we will access the relevant attributes
    relationships = [{'CHARACTER1': 1, 'CHARACTER2': 2, 'TYPE': 'Parent - Child'},
                     {'CHARACTER1': 1, 'CHARACTER2': 3, 'TYPE': 'Parent - Child'},
                     {'CHARACTER1': 3, 'CHARACTER2': 4, 'TYPE': 'Sibling - Sibling'},
                     {'CHARACTER1': 5, 'CHARACTER2': 6, 'TYPE': 'Sibling - Sibling'},
                     {'CHARACTER1': 6, 'CHARACTER2': 7, 'TYPE': 'Sibling - Sibling'},
                     {'CHARACTER1': 3, 'CHARACTER2': 7, 'TYPE': 'Sibling - Sibling'},
                     {'CHARACTER1': 8, 'CHARACTER2': 9, 'TYPE': 'Parent - Child'},
                     {'CHARACTER1': 9, 'CHARACTER2': 1, 'TYPE': 'Sibling - Sibling'},
                     {'CHARACTER1': 9, 'CHARACTER2': 10, 'TYPE': 'Sibling - Sibling'},
                     {'CHARACTER1': 10, 'CHARACTER2': 11, 'TYPE': 'Parent - Child'},
                     {'CHARACTER1': 11, 'CHARACTER2': 12, 'TYPE': 'Parent - Child'},
                     {'CHARACTER1': 12, 'CHARACTER2': 13, 'TYPE': 'Parent - Child'},
                     {'CHARACTER1': 10, 'CHARACTER2': 14, 'TYPE': 'Sibling - Sibling'}]

    base_graph = create_graph(characters, relationships)
    graph = add_implicits(base_graph)
    generations = create_generations(characters, relationships)
    for child in graph.get_char(1).children:
        print(child.id)
    print(graph.get_char(8).children[0].id)
    for character in graph.charList:
        char = graph.get_char(character)
        print('character: ', str(character), ' sibnum: ', str(char.sibling_num), ' generation: ', str(generations[char.id]))

    '''
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
                print('character: ', str(character), ' Grandparent: ', str(grandparent),
                      str(char.grandparents[grandparent]))'''


def recur_generations(graph, char, visited=[]):
    visited.append(char)
    distance = char.generation

    for child in char.children:
        if child not in visited:
            distance += 1
            child.generation = distance
            recur_generations(graph, child, visited)

    distance = char.generation  # Resetting distance to the proper recursion depth

    for parent in char.parents:
        if parent not in visited:
            distance -= 1
            parent.generation = distance
            recur_generations(graph, parent, visited)

    distance = char.generation  # Resetting distance to the proper recursion depth

    for sibling in graph.charList:
        sib = graph.get_char(sibling)
        if sib.sibling_num == char.sibling_num and sib.sibling_num != 0:
            if sib not in visited:
                sib.generation = distance
                recur_generations(graph, sib, visited)

    return graph


def create_generations(characters, relationships):
    graph = add_implicits(create_graph(characters, relationships))
    pivot_chars = find_top(graph)
    for char in pivot_chars:
        char.generation = 0
        graph = recur_generations(graph, char)

    # Applying generations to siblings who may have been missed
    for character in graph.charList:
        char = graph.get_char(character)
        if char.sibling_num != 0 and char.generation:
            for sibling in graph.charList:
                sib = graph.get_char(sibling)
                if sib.sibling_num == char.sibling_num:
                    sib.generation = char.generation

    # Creating a dictionary to be passed to the html for generations
    generations = {}
    for character in graph.charList:
        char = graph.get_char(character)
        generations[char.id] = char.generation

    return generations


# Note that this does not necessarily find the true top; just an acceptable point of reference (a character with no
# parents)
def find_top(graph):
    checked = []  # A list of checked sibling numbers to avoid ridiculous amounts of excessive looping
    top_char = []  # A list of all top characters
    for character in graph.charList:
        char = graph.get_char(character)
        if char.sibling_num == 0:
            if len(char.parents) == 0:
                top_char.append(char)
        elif char.sibling_num not in checked:
            if len(char.parents) == 0:
                for sibling in graph.charList:
                    sib = graph.get_char(sibling)
                    if sib.sibling_num == char.sibling_num:
                        if len(sib.parents) != 0:
                            checked.append(char.sibling_num)

                if char.sibling_num not in checked:
                    top_char.append(char)

            else:
                checked.append(char.sibling_num)

    return top_char
