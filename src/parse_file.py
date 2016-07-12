import json
from graph import Graph
import datetime

class Parser:
    def __init__(self):
        #initialze graph
        self.graph = Graph()
        self.median = 0

    def setOptions(self, args, opts):
        #search through command line input
        #for input and output flags
        for arg in opts:
            if arg[0] == '-i':
                self.median = self.parser(arg[1])
            elif arg[0] == '-o':
                with open(arg[1], 'w') as f:
                    for value in self.median:
                        f.write(str(value) + "\n")


    def loadFile(self, fileName):
        #read in file by line
        file = open(fileName, 'r')
        file_python_format = file.readlines()
        return file_python_format

    def parser(self, fileName):
        json_info = self.loadFile(fileName)
        medianList = []
        for tuple in json_info:
            #parse json tuples
            temp = json.loads(tuple)
            #convert timestamp into a datetime object
            timePoint = datetime.datetime.strptime(temp['created_time'], "%Y-%m-%dT%H:%M:%SZ")
            #check to make sure that neither actor nor target are empty strings
            if temp['actor'] != '' and temp['target'] != '':
                #add edge and nodes to graph
                self.graph.add_edge(temp['actor'], temp['target'], timePoint)
                #get median of current graph
                medianList.append(self.graph.get_median())

        return medianList
