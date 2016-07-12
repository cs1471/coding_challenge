from decimal import Decimal
import statistics as stat
import bisect
import datetime

class Edge:
    '''This class represents edges between nodes. It keeps track
    of transaction time stamps and actors and targets involved in
    each transaction'''
    def __init__(self, frmNode, toNode):
        #set timeStamp for each edge
        self.timeStamp = datetime.datetime
        #collect actor and target for each edge connection
        self.transaction = {'frm': frmNode, 'to': toNode}

    def set_timeStamp(self, ts):
        self.timeStamp = ts
        #mutator for setting timestamps

    def get_timeStamp(self):
        return self.timeStamp
        #accessor for getting timestamps

    def set_transaction(self, actor, target):
        self.transaction['frm'] = actor
        self.transaction['to'] = target
        #mutator for setting transaction actor and target

class Vertex:
    '''This class represents the nodes themselves. It keeps track
    of the name of either the actor or the target and also keeps
    track of the number of adjacent nodes, and the number of connections
    currently at the node given the 60 second window'''
    def __init__(self, node):
        #set the name of the node to either the actor or the target
        self.name = node
        #a dictionary to collect adjacent nodes
        self.connections = {}
        #a integer to keep track of number of connections
        self.num_connections = 0

    def add_neighbor(self, neighbor):
        self.connections[neighbor.name] = neighbor
        #mutator for adding adjacent nodes

    def get_connections(self):
        return self.connections.keys()
        #accessor for returning neighboring nodes

    def get_name(self):
        return self.name
        #accessor for setting name within a node

    def set_num_connections(self, value):
        self.num_connections += value
        #accessor for incrementing or decrementing
        #number of connections for a vertex

    def __str__(self):
        return str(self.name) + ' adjacent: ' + str([x.name for x in self.connections])

class Graph:
    '''This class represents the entire graph. It has two
    python dictionaries, one that keeps track of nodes and
    one that keeps tracks of edges'''
    def __init__(self):
        #a dictionary to store edge connections
        self.edge_dict = {}
        #a dictionary to store vertices
        self.vert_dict = {}
        #keeps track of the current time window
        self.current_window = None

    def __iter__(self):
        return iter(self.vert_dict.values())

    def add_vertex(self, node):
        # if the node is not a duplicate
        #create a vertex object
        if node not in self.vert_dict:
            new_vertex = Vertex(node)
            self.vert_dict[node] = new_vertex
        #otherwise return the node that has
        #already been created
        else:
            new_vertex = self.get_vertex(node)

        return new_vertex
        #if the vertex has not already been created
        #create a new vertex and add to the vertex
        #dictionary of the graph

    def get_vertex(self, n):
        if n in self.vert_dict:
            return self.vert_dict[n]
        else:
            return None
        #accessor function to access individual
        #vertices

    def get_edge(self, n):
        if n in self.edge_dict:
            return self.edge_dict[n]
        else:
            return None
        #accessor function to access individual
        #edges

    def remove_edge(self, edge):
        to_node_remove = self.get_vertex(edge.transaction['to'])
        frm_node_remove = self.get_vertex(edge.transaction['frm'])

        #remove expired edge
        del self.edge_dict[(frm_node_remove.name, to_node_remove.name)]

        #decrement number of connections
        to_node_remove.set_num_connections(-1)
        #if the node is now empty remove node entirely
        if to_node_remove.num_connections == 0:
            del self.vert_dict[to_node_remove.name]
        #otherwise remove the corresponding name in the transaction
        #from the adjacency list
        else:
            del to_node_remove.connections[frm_node_remove.name]

        # decrement number of connections
        frm_node_remove.set_num_connections(-1)
        #if the node is now empty remove node entirely
        if frm_node_remove.num_connections == 0:
            del self.vert_dict[frm_node_remove.name]
        #otherwise remove the corresponding name in the transaction
        #from the adjacency list
        else:
            del frm_node_remove.connections[to_node_remove.name]

        #This function removes edges as timeStamps expire.
        #It also removes both actor and target from their
        #respective adjaceny lists once the edge has expired.
        #If the remaining node has no adjacent nodes then the
        #entire node is delted from the dictionary

    def get_median(self):
        medianList = []
        #return number of connections for each node and sort as inserted
        for node in self.vert_dict.values():
            bisect.insort(medianList, node.num_connections)

        #calculate the median
        temp = Decimal(stat.median(medianList))
        #set number of significant digits
        median = round(temp, 2)
        return median
        #This function returns the median number
        #of connections over the entire graph
        #the insort function was used to improve
        #time complexity

    def set_current_window(self, window):
        # Check if window is intialized, if it isn't set to first value
        if self.current_window == None:
            self.current_window = window
            return True
        #check if new transaction is before the current time stamp and
        #therefore already expired
        elif (window - self.current_window).total_seconds() < 0:
            return False
        #otherwise set to current time window
        else:
            self.current_window = window
            return True
        #this function verifies that new transaction
        #should be added to graph and returns false if it
        #is outside the current time window

    def add_edge(self, frm, to, timeStamp):
        newWindow = self.set_current_window(timeStamp)
        if newWindow:
            #create two new Vertex objects
            #one for the from node and one
            #for the two node
            frmNode = self.add_vertex(frm)
            toNode = self.add_vertex(to)

            #check if edge added was a duplicate
            #if it was not a duplicate increment
            #number of connections for both to and
            #from nodes
            if (frm, to) not in self.edge_dict\
                    and (to, frm) not in self.edge_dict:
                new_edge = Edge(frm, to)
                new_edge.set_timeStamp(timeStamp)
                self.edge_dict[(frm, to)] = new_edge
                toNode.set_num_connections(1)
                frmNode.set_num_connections(1)
            else:
                #if edge already exists then set timestamp
                #to the new transaction value
                new_edge = self.get_edge((frm, to))
                if new_edge is not None:
                    new_edge.set_timeStamp(timeStamp)
                else:
                    new_edge = self.get_edge((to, frm))
                    new_edge.set_timeStamp(timeStamp)

            #add edges and vertices to graph dictionaries
            self.vert_dict[frm].add_neighbor(toNode)
            self.vert_dict[to].add_neighbor(frmNode)
            self.update(timeStamp)
        else:
            return
        #This function adds one new edge and two
        #new nodes for each transaction.

    def get_vertices(self):
        return self.vert_dict.keys()
        #Accessor function for returning
        #vertices

    def update(aGraph, new_timestamp):
        #create a queue for all edges
        queue = [(e.get_timeStamp(), e) for e in aGraph.edge_dict.values()]
        time = True

        #sort the queue based on time stamp
        queue.sort(key=lambda queue: queue[0])

        while time == True:
            for edge in queue:
                #check if edge has expired - if it has remove edge
                if (new_timestamp - edge[1].timeStamp).total_seconds() > 60:
                    aGraph.remove_edge(edge[1])
                #if edge has not expired because the dictionary is sorted, all subsequent
                #timestamps are valid and therefore the function can be exited
                else:
                    time = False
                    break
        #This function updates the graph as transactions expire.