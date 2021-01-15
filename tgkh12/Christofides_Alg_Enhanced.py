############
############ ALTHOUGH I GIVE YOU THE 'BARE BONES' OF THIS PROGRAM WITH THE NAME
############ 'skeleton.py', YOU CAN RENAME IT TO ANYTHING YOU LIKE. HOWEVER, FOR
############ THE PURPOSES OF THE EXPLANATION IN THESE COMMENTS, I ASSUME THAT
############ THIS PROGRAM IS STILL CALLED 'skeleton.py'.
############
############ IF YOU WISH TO IMPORT STANDARD MODULES, YOU CAN ADD THEM AFTER THOSE BELOW.
############ NOTE THAT YOU ARE NOT ALLOWED TO IMPORT ANY NON-STANDARD MODULES!
############

import os
import sys
import time
import random
from collections import defaultdict, Counter
import copy

############
############ NOW PLEASE SCROLL DOWN UNTIL THE NEXT BLOCK OF CAPITALIZED COMMENTS.
############
############ DO NOT TOUCH OR ALTER THE CODE IN BETWEEN! YOU HAVE BEEN WARNED!
############

def read_file_into_string(input_file, ord_range):
    the_file = open(input_file, 'r') 
    current_char = the_file.read(1) 
    file_string = ""
    length = len(ord_range)
    while current_char != "":
        i = 0
        while i < length:
            if ord(current_char) >= ord_range[i][0] and ord(current_char) <= ord_range[i][1]:
                file_string = file_string + current_char
                i = length
            else:
                i = i + 1
        current_char = the_file.read(1)
    the_file.close()
    return file_string

def remove_all_spaces(the_string):
    length = len(the_string)
    new_string = ""
    for i in range(length):
        if the_string[i] != " ":
            new_string = new_string + the_string[i]
    return new_string

def integerize(the_string):
    length = len(the_string)
    stripped_string = "0"
    for i in range(0, length):
        if ord(the_string[i]) >= 48 and ord(the_string[i]) <= 57:
            stripped_string = stripped_string + the_string[i]
    resulting_int = int(stripped_string)
    return resulting_int

def convert_to_list_of_int(the_string):
    list_of_integers = []
    location = 0
    finished = False
    while finished == False:
        found_comma = the_string.find(',', location)
        if found_comma == -1:
            finished = True
        else:
            list_of_integers.append(integerize(the_string[location:found_comma]))
            location = found_comma + 1
            if the_string[location:location + 5] == "NOTE=":
                finished = True
    return list_of_integers

def build_distance_matrix(num_cities, distances, city_format):
    dist_matrix = []
    i = 0
    if city_format == "full":
        for j in range(num_cities):
            row = []
            for k in range(0, num_cities):
                row.append(distances[i])
                i = i + 1
            dist_matrix.append(row)
    elif city_format == "upper_tri":
        for j in range(0, num_cities):
            row = []
            for k in range(j):
                row.append(0)
            for k in range(num_cities - j):
                row.append(distances[i])
                i = i + 1
            dist_matrix.append(row)
    else:
        for j in range(0, num_cities):
            row = []
            for k in range(j + 1):
                row.append(0)
            for k in range(0, num_cities - (j + 1)):
                row.append(distances[i])
                i = i + 1
            dist_matrix.append(row)
    if city_format == "upper_tri" or city_format == "strict_upper_tri":
        for i in range(0, num_cities):
            for j in range(0, num_cities):
                if i > j:
                    dist_matrix[i][j] = dist_matrix[j][i]
    return dist_matrix

def read_in_algorithm_codes_and_tariffs(alg_codes_file):
    flag = "good"
    code_dictionary = {}   
    tariff_dictionary = {}  
    if not os.path.exists(alg_codes_file):
        flag = "not_exist"  
        return code_dictionary, tariff_dictionary, flag
    ord_range = [[32, 126]]
    file_string = read_file_into_string(alg_codes_file, ord_range)  
    location = 0
    EOF = False
    list_of_items = []  
    while EOF == False: 
        found_comma = file_string.find(",", location)
        if found_comma == -1:
            EOF = True
            sandwich = file_string[location:]
        else:
            sandwich = file_string[location:found_comma]
            location = found_comma + 1
        list_of_items.append(sandwich)
    third_length = int(len(list_of_items)/3)
    for i in range(third_length):
        code_dictionary[list_of_items[3 * i]] = list_of_items[3 * i + 1]
        tariff_dictionary[list_of_items[3 * i]] = int(list_of_items[3 * i + 2])
    return code_dictionary, tariff_dictionary, flag

############
############ THE RESERVED VARIABLE 'input_file' IS THE CITY FILE UNDER CONSIDERATION.
############
############ IT CAN BE SUPPLIED BY SETTING THE VARIABLE BELOW OR VIA A COMMAND-LINE
############ EXECUTION OF THE FORM 'python skeleton.py city_file.txt'. WHEN SUPPLYING
############ THE CITY FILE VIA A COMMAND-LINE EXECUTION, ANY ASSIGNMENT OF THE VARIABLE
############ 'input_file' IN THE LINE BELOW iS SUPPRESSED.
############
############ IT IS ASSUMED THAT THIS PROGRAM 'skeleton.py' SITS IN A FOLDER THE NAME OF
############ WHICH IS YOUR USER-NAME, E.G., 'abcd12', WHICH IN TURN SITS IN ANOTHER
############ FOLDER. IN THIS OTHER FOLDER IS THE FOLDER 'city-files' AND NO MATTER HOW
############ THE NAME OF THE CITY FILE IS SUPPLIED TO THIS PROGRAM, IT IS ASSUMED THAT 
############ THE CITY FILE IS IN THE FOLDER 'city-files'.
############

input_file = "AISearchfile048.txt"

############
############ PLEASE SCROLL DOWN UNTIL THE NEXT BLOCK OF CAPITALIZED COMMENTS.
############
############ DO NOT TOUCH OR ALTER THE CODE IN BETWEEN! YOU HAVE BEEN WARNED!
############

if len(sys.argv) > 1:
    input_file = sys.argv[1]

the_particular_city_file_folder = "city-files"
    
if os.path.isfile("../" + the_particular_city_file_folder + "/" + input_file):
    ord_range = [[32, 126]]
    file_string = read_file_into_string("../" + the_particular_city_file_folder + "/" + input_file, ord_range)
    file_string = remove_all_spaces(file_string)
    print("I have found and read the input file " + input_file + ":")
else:
    print("*** error: The city file " + input_file + " does not exist in the folder '" + the_particular_city_file_folder + "'.")
    sys.exit()

location = file_string.find("SIZE=")
if location == -1:
    print("*** error: The city file " + input_file + " is incorrectly formatted.")
    sys.exit()
    
comma = file_string.find(",", location)
if comma == -1:
    print("*** error: The city file " + input_file + " is incorrectly formatted.")
    sys.exit()
    
num_cities_as_string = file_string[location + 5:comma]
num_cities = integerize(num_cities_as_string)
print("   the number of cities is stored in 'num_cities' and is " + str(num_cities))

comma = comma + 1
stripped_file_string = file_string[comma:]
distances = convert_to_list_of_int(stripped_file_string)

counted_distances = len(distances)
if counted_distances == num_cities * num_cities:
    city_format = "full"
elif counted_distances == (num_cities * (num_cities + 1))/2:
    city_format = "upper_tri"
elif counted_distances == (num_cities * (num_cities - 1))/2:
    city_format = "strict_upper_tri"
else:
    print("*** error: The city file " + input_file + " is incorrectly formatted.")
    sys.exit()

dist_matrix = build_distance_matrix(num_cities, distances, city_format)
print("   the distance matrix 'dist_matrix' has been built.")

############
############ YOU NOW HAVE THE NUMBER OF CITIES STORED IN THE INTEGER VARIABLE 'num_cities'
############ AND THE TWO_DIMENSIONAL MATRIX 'dist_matrix' HOLDS THE INTEGER CITY-TO-CITY 
############ DISTANCES SO THAT 'dist_matrix[i][j]' IS THE DISTANCE FROM CITY 'i' TO CITY 'j'.
############ BOTH 'num_cities' AND 'dist_matrix' ARE RESERVED VARIABLES AND SHOULD FEED
############ INTO YOUR IMPLEMENTATIONS.
############

############
############ THERE NOW FOLLOWS CODE THAT READS THE ALGORITHM CODES AND TARIFFS FROM
############ THE TEXT-FILE 'alg_codes_and_tariffs.txt' INTO THE RESERVED DICTIONARIES
############ 'code_dictionary' AND 'tariff_dictionary'. DO NOT AMEND THIS CODE!
############ THE TEXT FILE 'alg_codes_and_tariffs.txt' SHOULD BE IN THE SAME FOLDER AS
############ THE FOLDER 'city-files' AND THE FOLDER WHOSE NAME IS YOUR USER-NAME, E.G., 'abcd12'.
############

code_dictionary, tariff_dictionary, flag = read_in_algorithm_codes_and_tariffs("../alg_codes_and_tariffs.txt")

if flag != "good":
    print("*** error: The text file 'alg_codes_and_tariffs.txt' does not exist.")
    sys.exit()

print("The codes and tariffs have been read from 'alg_codes_and_tariffs.txt':")

############
############ YOU NOW NEED TO SUPPLY SOME PARAMETERS.
############
############ THE RESERVED STRING VARIABLE 'my_user_name' SHOULD BE SET AT YOUR USER-NAME, E.G., "abcd12"
############

my_user_name = "tgkh12"

############
############ YOU CAN SUPPLY, IF YOU WANT, YOUR FULL NAME. THIS IS NOT USED AT ALL BUT SERVES AS
############ AN EXTRA CHECK THAT THIS FILE BELONGS TO YOU. IF YOU DO NOT WANT TO SUPPLY YOUR
############ NAME THEN EITHER SET THE STRING VARIABLES 'my_first_name' AND 'my_last_name' AT 
############ SOMETHING LIKE "Mickey" AND "Mouse" OR AS THE EMPTY STRING (AS THEY ARE NOW;
############ BUT PLEASE ENSURE THAT THE RESERVED VARIABLES 'my_first_name' AND 'my_last_name'
############ ARE SET AT SOMETHING).
############

my_first_name = "Kah Gene"
my_last_name = "Leong"

############
############ YOU NEED TO SUPPLY THE ALGORITHM CODE IN THE RESERVED STRING VARIABLE 'algorithm_code'
############ FOR THE ALGORITHM YOU ARE IMPLEMENTING. IT NEEDS TO BE A LEGAL CODE FROM THE TEXT-FILE
############ 'alg_codes_and_tariffs.txt' (READ THIS FILE TO SEE THE CODES).
############

algorithm_code = "CA"

############
############ DO NOT TOUCH OR ALTER THE CODE BELOW! YOU HAVE BEEN WARNED!
############

if not algorithm_code in code_dictionary:
    print("*** error: the agorithm code " + algorithm_code + " is illegal")
    sys.exit()
print("   your algorithm code is legal and is " + algorithm_code + " -" + code_dictionary[algorithm_code] + ".")

############
############ YOU CAN ADD A NOTE THAT WILL BE ADDED AT THE END OF THE RESULTING TOUR FILE IF YOU LIKE,
############ E.G., "in my basic greedy search, I broke ties by always visiting the first 
############ city found" BY USING THE RESERVED STRING VARIABLE 'added_note' OR LEAVE IT EMPTY
############ IF YOU WISH. THIS HAS NO EFFECT ON MARKS BUT HELPS YOU TO REMEMBER THINGS ABOUT
############ YOUR TOUR THAT YOU MIGHT BE INTERESTED IN LATER.
############

added_note = ""

############
############ NOW YOUR CODE SHOULD BEGIN.
############

## Kruskal's Alg ##
def getKey(tup):
    return tup[2]

def find_root(parent, vertex):
    if parent[vertex] == vertex:
        return vertex
    return find_root(parent, parent[vertex])

def node_union(parent, rank, x, y):
    root_of_x = find_root(parent, x)
    root_of_y = find_root(parent, y)
    if rank[root_of_x] < rank[root_of_y]:
        parent[root_of_x] = root_of_y
    elif rank[root_of_x] > rank[root_of_y]:
        parent[root_of_y] = root_of_x
    else:
        parent[root_of_y] = root_of_x
        rank[root_of_x] += 1

def kruskalMST(dist_matrix, num_cities):
    mst_connections = defaultdict(list)
    index = 0
    edge_count = 0
    edges = []
    parent = [city for city in range(num_cities)]
    rank = [0]*num_cities

    for i in range(len(dist_matrix)): 
            for j in range(len(dist_matrix[i])):
                if i != j:
                    edges.append((i, j, dist_matrix[i][j]))

    edges = sorted(edges, key=getKey)
    while edge_count < num_cities - 1:
        from_city, to_city, dist = edges[index]
        index += 1
        x = find_root(parent, from_city)
        y = find_root(parent, to_city)
        if x != y:
            edge_count += 1
            mst_connections[from_city].append(to_city)
            mst_connections[to_city].append(from_city)
            node_union(parent, rank, x, y)

    return mst_connections
###################

## Prim's Alg ##
def isValidEdge(city1, city2, vertexInMST): 
    if city1 == city2: 
        return 0
    if (vertexInMST[city1] == 0 and vertexInMST[city2] == 0) or (vertexInMST[city1] == 1 and vertexInMST[city2] == 1): 
        return 0
    return 1

def primMST(dist_matrix, num_cities, starting_city): 
    mst_connections = defaultdict(list)
    vertexInMST = [0] * num_cities 
    num_of_edges_added = 0
    vertexInMST[starting_city] = 1
    
    while num_of_edges_added < num_cities-1:
        min_dist = sys.maxsize
        from_city = -1
        to_city = -1
        for i in range(len(dist_matrix)): 
            for j in range(len(dist_matrix[i])): 
                if dist_matrix[i][j] < min_dist:
                    if isValidEdge(i, j, vertexInMST): 
                        min_dist = dist_matrix[i][j] 
                        from_city = i 
                        to_city = j 
  
        if from_city != -1 and to_city != -1: 
            mst_connections[from_city].append(to_city)
            mst_connections[to_city].append(from_city) 
            num_of_edges_added += 1
            vertexInMST[to_city] = vertexInMST[from_city] = 1

    return mst_connections
################

def get_odd_vertices(mstStruc):
    return [v for v in mstStruc if len(mstStruc[v])%2 != 0]

# class City(object):
#     count = 0 

#     def __init__(self):
#         self.name = City.count
#         City.count += 1
#         self.neighbors = []
#         self.match = None
#         self.mark = False
#         self.parent = None
#         self.root = None

#     def path_to_root(self):
#         path = [self]
#         city_node = self
#         while city_node != city_node.root:
#             city_node = city_node.parent
#             path.append(city_node)
#         return path

#     def get_aug_path_on_cycle(self, match_node, cycle):
#         i = cycle.index(self)
#         j = cycle.index(match_node)
#         path = []

#         if (i > 0 and j == i - 1) or (i == 0 and j == len(cycle) - 1):
#             cycle_rev = cycle[i::-1] + cycle[:i:-1]
#             for node in cycle_rev:
#                 path.append(node)
#                 if node.match not in cycle_rev:
#                     return path

#         else:
#             cycle_forward = cycle[i::] + cycle[:i]
#             for node in cycle_forward:
#                 path.append(node)
#                 if node.match not in cycle_forward:
#                     # return path

# class Supercity(City):
#     def __init__(self, cycle=None):
#         super(Supercity, self).__init__()
#         self.cycle = cycle

#     def shrink_cycle_to_vertex(self, nodes):
#         nodes = [node for node in nodes if node not in self.cycle]
#         nodes.append(self)

#         for node in self.cycle:
#             if node.match and node.match not in self.cycle:
#                 self.match = node.match
#             for neighbor in node.neighbors:
#                 if neighbor not in self.cycle:
#                     self.neighbors.append(neighbor)
#         self.neighbors = list(set(self.neighbors))

#         for node in nodes:
#             if node.match in self.cycle:
#                 node.match = self
#             node.neighbors = [neighbor for neighbor in node.neighbors if neighbor not in self.cycle]
#             if node in self.neighbors:
#                 node.neighbors.append(self)

#         return nodes

#     def expand_nodes_into_cycle(self, nodes):
#         nodes = [node for node in nodes if node is not self]
#         for node in nodes:
#             node.neighbors = [neighbor for neighbor in node.neighbors if neighbor is not self]

#         for node in self.cycle:
#             nodes.append(node)
#             if node.match and node.match not in self.cycle:
#                 node.match.match = node
#             for neighbor in node.neighbors:
#                 if neighbor not in self.cycle:
#                     neighbor.neighbors.append(node)

#         return nodes

#     def expand_path(self, path, cycle):
#         if self not in path:
#             return path

#         elif self == path[0]:
#             for node in cycle:
#                 if path[1] in node.neighbors:
#                     if node.match:
#                         cpath = node.get_aug_path_on_cycle(node.match, cycle)
#                     else:
#                         cpath = [node]
#                     return cpath[::-1] + path[1:]

#         elif self == path[-1]:
#             for node in cycle:
#                 if path[-2] in node.neighbors:
#                     if node.match:
#                         cpath = node.get_aug_path_on_cycle(node.match, cycle)
#                     else:
#                         cpath = [node]
#                     return path[:-1] + cpath

#         else:
#             idx = path.index(self)
#             if path.index(self.match) == idx - 1:
#                 for node in cycle:
#                     if path[idx + 1] in node.neighbors:
#                         cpath = node.get_aug_path_on_cycle(node.match, cycle)
#                         return path[:idx] + cpath[::-1] + path[idx + 1 :]

#             elif path.index(self.match) == idx + 1:
#                 for node in cycle:
#                     if path[idx - 1] in node.neighbors:
#                         cpath = node.get_aug_path_on_cycle(node.match, cycle)
#                         return path[:idx] + cpath + path[idx + 1 :]

# class EdmondsBlossomGraph:

#     def __init__(self):
#         self.nodes = None

#     def reset(self):
#         for index in self.nodes:
#             self.nodes[index].mark = False
#             self.nodes[index].parent = None
#             self.nodes[index].root = None

#     def get_connected_city_pairs(self):
#         matchings = []
#         available_nodes = [i for i in range(len(self.nodes))]
#         for index in self.nodes:
#             if self.nodes[index].match and self.nodes[index].name in available_nodes:
#                 matchings.append((self.nodes[index].name, self.nodes[index].match.name))
#                 available_nodes.remove(self.nodes[index].name)
#                 available_nodes.remove(self.nodes[index].match.name)
#         return matchings

#     def get_max_matching(self):
#         path = self.augment_path()
#         if not path:
#             return self
#         else:
#             self.augment_matching(path)
#             return self.get_max_matching()

#     def augment_path(self):
#         self.reset()

#         exposed_nodes = [node for node in self.nodes.values() if node.match is None]
#         for node in exposed_nodes:
#             node.parent = node
#             node.root = node

#         for node in exposed_nodes:
#             if not node.mark:
#                 for neighbor in node.neighbors:
#                     # if self.edges[tuple(sorted([node.name, neighbor.name]))]:
#                     if neighbor not in exposed_nodes:
#                         neighbor.parent = node
#                         neighbor.root = node.root
#                         neighbor.mark = True  # odd distance from root
#                         # self.mark_edges(node, neighbor)
#                         exposed_nodes.append(neighbor)

#                         match = neighbor.match
#                         match.parent = neighbor
#                         match.root = neighbor.root
#                         # self.mark_edges(neighbor, adj_match)
#                         exposed_nodes.append(match)
#                     else:
#                         if not (len(neighbor.path_to_root()) % 2):
#                             # self.mark_edges(node, neighbor)
#                             pass
#                         else:
#                             if node.root != neighbor.root:
#                                 path1 = node.path_to_root()
#                                 path2 = neighbor.path_to_root()
#                                 return path1[::-1] + path2
#                             else:
#                                 return self.blossom(node, neighbor)
#                 node.mark = True

#         return []

#     def blossom(self, node1, node2):
#         path1 = node1.path_to_root()
#         path2 = node2.path_to_root()
#         cycle = path1[::-1] + path2[:-1]

#         # Contract cycle nodes to supernode
#         supercity = Supercity(cycle)
#         node_list = supercity.shrink_cycle_to_vertex(self.nodes.values())
#         self.nodes = {node.name: node for node in node_list}
#         # self.compute_edges()
#         aug_path = self.augment_path()

#         # Expand supernode back to original cycle nodes
#         aug_path = supercity.expand_path(aug_path, cycle)
#         node_list = supercity.expand_nodes_into_cycle(self.nodes.values())
#         self.nodes = {node.name: node for node in node_list}
#         # self.compute_edges()

#         return aug_path

#     def augment_matching(self, path):
#         for count, city in enumerate(path):
#             if (count + 1) % 2:
#                 city.match = path[count + 1]
#             else:
#                 city.match = path[count - 1]

# def edmondBlossomAlg(oddVertices):
#     matchings = {}
#     list_of_cities = [City() for _ in oddVertices]
#     for count, city in enumerate(oddVertices):
#         list_of_cities[count].neighbors = [city for city in list_of_cities if city != list_of_cities[count]]
#     EB_Graph = EdmondsBlossomGraph() 
#     EB_Graph.nodes = {city.name: city for city in list_of_cities}
#     EB_Graph.get_max_matching()
#     matchings = EB_Graph.get_connected_city_pairs()
    
#     return matchings

def minWeightPerfectMatch(oddVertices, dist_matrix):
    matchings = []
    available_nodes = copy.deepcopy(oddVertices)

    while available_nodes:

        current_pairings = []

        for v in available_nodes:
            smallest_dist = sys.maxsize
            chosen_neighbour = -1
            for neighbor in available_nodes:
                if v == neighbor:
                    continue

                distance = dist_matrix[v][neighbor]
                if distance < smallest_dist:
                    smallest_dist = distance
                    chosen_neighbour = neighbor

            current_pairings.append((v, chosen_neighbour, smallest_dist))

        min_pair = [pairing for pairing in current_pairings if pairing[2] == min([weight[2] for weight in current_pairings])][0]
        matchings.append((min_pair[0], min_pair[1]))
        available_nodes.remove(min_pair[0])
        available_nodes.remove(min_pair[1])

    return matchings

def graph_union(mst, matchings):
    for matching in matchings:
        nodeA = matching[0]
        nodeB = matching[1]
        mst[nodeA].append(nodeB)
        mst[nodeB].append(nodeA)

def getTourLength(tour, dist_matrix, num_cities):
    edge_count = 1
    city1 = 0
    city2 = 1
    tour_length = 0
    while edge_count <= num_cities-1:
        tour_length += dist_matrix[tour[city1]][tour[city2]]
        edge_count += 1
        city1 += 1
        city2 += 1

    return tour_length + dist_matrix[tour[city2-1]][tour[0]]

class EulerianCircuit:
    def __init__(self, no_of_vertices, mst_connections):
        self.no_of_vertices = no_of_vertices
        self.graph = mst_connections
        self.tourMap = []

    def remove_edge(self, v1, v2):
        if v2 in self.graph[v1]:
            self.graph[v1].remove(v2)

        if v1 in self.graph[v2]:
            self.graph[v2].remove(v1)

    def DFS(self, vertex, visited):
        vertex_count = 1
        visited[vertex] = True
        for i in self.graph[vertex]:
            if not visited[i]: 
                vertex_count = 1 + self.DFS(i, visited)
        return vertex_count

    def isValidEdge(self, v1, v2):
        if len(self.graph[v1]) == 1:
            return True

        else:
            visited = [False]*self.no_of_vertices
            c1 = self.DFS(v1, visited)

            self.remove_edge(v1, v2)
            visited = [False]*self.no_of_vertices
            c2 = self.DFS(v1, visited)

            self.graph[v1].append(v2)
            self.graph[v2].append(v1)

            if c1 > c2:
                return False
            
            return True

    def traverseTour(self, start):
        for next_vertex in self.graph[start]:
            if self.isValidEdge(start, next_vertex):
                self.tourMap.append(start)
                self.remove_edge(start, next_vertex)
                self.traverseTour(next_vertex)

    def tourInit(self, dist_matrix):
        start = 0
        sdist = sys.maxsize
        for i in range(self.no_of_vertices):
            if len(self.graph[i]) %2 != 0:
                start = i
                break

        self.traverseTour(start)

def remove_repeated_vertices(tour, dist_matrix):
    final_tour = [-1]*len(tour)
    occurence = Counter(tour)
    count = 0
    city = 0

    while count < len(tour):
        comparisons = []
        if occurence[tour[city]] > 1:
            for i in range(len(tour)):
                if tour[i] == tour[city]:
                    if i == len(tour) - 1:
                        _tup = (i-1, i, 0)
                    else:
                        _tup = (i-1, i, i+1)
                    comparisons.append(_tup)
            smallest_dist = sys.maxsize
            smallest_tup = ()
            for tup in comparisons:
                dist = dist_matrix[tour[tup[0]]][tour[tup[1]]] + dist_matrix[tour[tup[1]]][tour[tup[2]]]
                if dist < smallest_dist:
                    smallest_dist = dist
                    smallest_tup = tup
            final_tour[smallest_tup[1]] = tour[city]

        else:
            final_tour[city] = (tour[city])

        city += 1
        count += 1

    return [city for city in final_tour if city != -1]

def christofides_algorithm(dist_matrix, num_cities):
    best_tour = []
    best_length = sys.maxsize
    for _ in range(num_cities+1):
        tour = []
        tour_length = 0

        if _ < num_cities:
            MST = primMST(dist_matrix, num_cities, _)
        else:
            MST = kruskalMST(dist_matrix, num_cities)
        # # print(f'\nMST connections: {MST}')
        oddVertices = get_odd_vertices(MST)
        # print(f'\nList of odd vertices: {oddVertices}')
        # matchings = edmondBlossomAlg(oddVertices)
        # matchings = [(oddVertices[matchings[i][0]], oddVertices[matchings[i][1]]) for i in range(len(matchings))]
        matchings = minWeightPerfectMatch(oddVertices, dist_matrix)
        # print(f'\nMinimum weight perfect matchings: {matchings}')
        graph_union(MST, matchings)
        # print(f'\nMatching union MST: {MST}')
        euler_tour = EulerianCircuit(num_cities, MST)
        euler_tour.tourInit(dist_matrix)
        tour = euler_tour.tourMap
        # print(f'\nTour: {tour}')
        tour = remove_repeated_vertices(tour, dist_matrix)
        # print(f'\nTour updated: {tour}')
        tour_length = getTourLength(tour, dist_matrix, num_cities)
        # print(f'Tour length: {tour_length}')

        if tour_length < best_length:
            best_length = tour_length
            best_tour = tour

    return best_tour, best_length

tour, tour_length = christofides_algorithm(dist_matrix, num_cities)
# kruskalMST(dist_matrix, num_cities)

############
############ YOUR CODE SHOULD NOW BE COMPLETE AND WHEN EXECUTION OF THIS PROGRAM 'skeleton.py'
############ REACHES THIS POINT, YOU SHOULD HAVE COMPUTED A TOUR IN THE RESERVED LIST VARIABLE 'tour', 
############ WHICH HOLDS A LIST OF THE INTEGERS FROM {0, 1, ..., 'num_cities' - 1}, AND YOU SHOULD ALSO
############ HOLD THE LENGTH OF THIS TOUR IN THE RESERVED INTEGER VARIABLE 'tour_length'.
############

############
############ YOUR TOUR WILL BE PACKAGED IN A TOUR FILE OF THE APPROPRIATE FORMAT AND THIS TOUR FILE,
############ WHOSE NAME WILL BE A MIX OF THE NAME OF THE CITY FILE, THE NAME OF THIS PROGRAM AND THE
############ CURRENT DATA AND TIME. SO, EVERY SUCCESSFUL EXECUTION GIVES A TOUR FILE WITH A UNIQUE
############ NAME AND YOU CAN RENAME THE ONES YOU WANT TO KEEP LATER.
############

############
############ DO NOT TOUCH OR ALTER THE CODE BELOW THIS POINT! YOU HAVE BEEN WARNED!
############

flag = "good"
length = len(tour)
for i in range(0, length):
    if isinstance(tour[i], int) == False:
        flag = "bad"
    else:
        tour[i] = int(tour[i])
if flag == "bad":
    print("*** error: Your tour contains non-integer values.")
    sys.exit()
if isinstance(tour_length, int) == False:
    print("*** error: The tour-length is a non-integer value.")
    sys.exit()
tour_length = int(tour_length)
if len(tour) != num_cities:
    print("*** error: The tour does not consist of " + str(num_cities) + " cities as there are, in fact, " + str(len(tour)) + ".")
    sys.exit()
flag = "good"
for i in range(0, num_cities):
    if not i in tour:
        flag = "bad"
if flag == "bad":
    print("*** error: Your tour has illegal or repeated city names.")
    sys.exit()
check_tour_length = 0
for i in range(0, num_cities - 1):
    check_tour_length = check_tour_length + dist_matrix[tour[i]][tour[i + 1]]
check_tour_length = check_tour_length + dist_matrix[tour[num_cities - 1]][tour[0]]
if tour_length != check_tour_length:
    flag = print("*** error: The length of your tour is not " + str(tour_length) + "; it is actually " + str(check_tour_length) + ".")
    sys.exit()
print("You, user " + my_user_name + ", have successfully built a tour of length " + str(tour_length) + "!")

local_time = time.asctime(time.localtime(time.time()))
output_file_time = local_time[4:7] + local_time[8:10] + local_time[11:13] + local_time[14:16] + local_time[17:19]
output_file_time = output_file_time.replace(" ", "0")
script_name = os.path.basename(sys.argv[0])
if len(sys.argv) > 2:
    output_file_time = sys.argv[2]
output_file_name = script_name[0:len(script_name) - 3] + "_" + input_file[0:len(input_file) - 4] + "_" + output_file_time + ".txt"

f = open(output_file_name,'w')
f.write("USER = " + my_user_name + " (" + my_first_name + " " + my_last_name + "),\n")
f.write("ALGORITHM CODE = " + algorithm_code + ", NAME OF CITY-FILE = " + input_file + ",\n")
f.write("SIZE = " + str(num_cities) + ", TOUR LENGTH = " + str(tour_length) + ",\n")
f.write(str(tour[0]))
for i in range(1,num_cities):
    f.write("," + str(tour[i]))
f.write(",\nNOTE = " + added_note)
f.close()
print("I have successfully written your tour to the tour file:\n   " + output_file_name + ".")