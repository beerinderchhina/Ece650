from __future__ import division  # So we are not using integer division
import re
import sys
import math
from numpy import *
import subprocess


# http://stackoverflow.com/questions/3838329/how-can-i-check-if-two-segments-intersect
# http://stackoverflow.com/questions/20677795/find-the-point-of-intersecting-lines
class Street(object):
    def __init__(self, name, coords):
        self.name = name
        self.coords = coords

		

class Graph(object):
    vs = []
    es = []	
	

    def coord2index(self, coord):
        if coord in self.vs:
            return self.vs.index(coord)
        else:
            return False
            
    def index2coord(self, index):
        if index < len(self.vs):
            return self.vs[index]
        else:
            return False

    def add_vertex(self, coord):
        if coord not in self.vs:
            self.vs.append(coord)       

    def add_edge(self, v1, v2):
        edge = sorted([v1,v2])
        if edge not in self.vs:
            self.es.append(edge)       

    def node2str(self, coord):
        return '('+str(coord[0])+','+str(coord[1])+')'

    def edge2str(self, edge):
        return '<'+str(edge[0])+','+str(edge[1])+'>'
    
    def __str__(self):
        string = ''
        string += 'V = { \n'
        for i in range(len(self.vs)):
            string += '  ' + str(i) + ':  ' + self.node2str(self.vs[i]) + '\n'
        string += '} \n'
        string += 'E = { \n'
        for edge in self.es:
            string += '  ' + self.edge2str(edge) + ', \n'
        if len(self.es) > 0:
            string = string[:-3]
            string += '\n'
        string += '} \n'
        return string
        

		

#************************************************************
# Error Output
#************************************************************
def prnterror(message):
    """
    Displays an error message to stderr

    :param message: The error message to display
    :param line: The line where the error occurred
    :return: None
    """

    sys.stderr.write("%s\n" % (message))		
		
		
def parse(line):
    """
    Get the name and coordinates from an input line

    :param line: The command line
    :return: name, coordinates
    """

    parts = line.split('"')     # The name is inside " pair
    coords = []                 # No coordinates yet
    if len(parts) < 2:          # No name specified
        return None, coords     # No name, No coords
    if len(parts) == 3:         # We have coordinates to process
        for pair in parts[2].split(')'):   # Each coordinate pair
            try:
                if pair:
                    x, y = pair.split(',')  # Remove the ,
                    x = x.strip(" (")
                    point = int(x), int(y) # Get the x, y coordinates for the point
                    coords.append(point)    # Add the coordinate
            except:
                error("Error in coordinate", pair + ')')
                return parts[1], []     # 1 bad coordinate at least, so return no coordinates
    return parts[1], coords         # name, [coords]




def checkifparallel( a ) :
    b = empty_like(a)
    b[0] = -a[1]
    b[1] = a[0]
    return b
    
def checkintersections(a1,a2, b1,b2):
    da = a2-a1
    db = b2-b1
    dp = a1-b1
    dap = checkifparallel(da)
    denom = dot(dap, db)
    num = dot(dap, dp)
    result = (num / denom)*db + b1
    
    if result[0] < min(a1[0],a2[0],b1[0],b2[0]) or \
       result[0] > max(a1[0],a2[0],b1[0],b2[0]) or \
       result[1] < min(a1[1],a2[1],b1[1],b2[1]) or \
       result[1] > max(a1[1],a2[1],b1[1],b2[1]):
        return False
    
    return tuple([result[0], result[1]])

#cmds = {'a': add, 'r': remove} # the different commands

def add(line):
    name, coords = parse(line)
    if not name:
        return "No name specified in add"
    if not coords:
        return "No coordinates specified in add"
    if len(coords) < 2:
        return "No end point in add"
    if name in streets:
        return "Already an existing street called " + name
    streets[name] = Street(coords)



def change(line):
    name, coords = parse(line)
    if not name:
        return "No name specified in change"
    if not coords:
        return "No coordinates specified in change"
    if len(coords) < 2:
        return "No end point in add"
    if name not in streets:
        return "No existing street called " + name
    streets[name] = Street(coords)

streets = []
graph = Graph()

regx_name = '\".+\"'
regx_num = '-?\d+'
regx_coord = r'\(\s*'+regx_num+'\s*,\s*'+regx_num+'\s*\)'

rgx_add_st = '\s*a\s+'+regx_name+'\s*('+regx_coord+'\s*){2,}\s*$'
rgx_change_st = '\s*c\s+'+regx_name+'\s*('+regx_coord+'\s*){2,}\s*$'
rgx_remove_st = '\s*r\s+'+regx_name+'\s*$'
rgx_printg_st = '\s*g\s*'

rgx_chck_add = re.compile(rgx_add_st)
rgx_chck_change = re.compile(rgx_change_st)
rgx_chck_remove = re.compile(rgx_remove_st)
rgx_chck_printg = re.compile(rgx_printg_st)

while True:

   
    cmd = raw_input()
    
    #******************************    
    # Check commands
    #******************************
    if rgx_chck_add.match(cmd) or rgx_chck_change.match(cmd) or rgx_chck_remove.match(cmd):
        # recoord name and coordinates (if they exist)
        name = re.findall(regx_name,cmd)[0]
        coords = [ tuple([ float(num) for num in re.findall(regx_num,coord) ]) \
                  for coord in re.findall(regx_coord,cmd)]

        # Get current street list
        name_set = [ street.name for street in streets]

        #******************************   

        # Add a new street
        #******************************
        if rgx_chck_add.match(cmd):
            if name not in name_set:
                streets.append(Street(name, coords))
            else:
                prnterror('Error: street currently exists.')

        else:
            if name in name_set:
                #******************************        
                # street Change
                #******************************
                if rgx_chck_change.match(cmd):
                    index = name_set.index(name)
                    streets[index].coords = coords
                #******************************
                # street Remove
                #******************************
                else:
                    index = name_set.index(name)
                    streets.pop(index)
            else:
                prnterror('Error: \'c\' or \'r\' specified for a street that does not exist.')


    #******************************           
    # Output
    #******************************
    elif rgx_chck_printg.match(cmd):

        graph.vs = []
        graph.es = []
        
        for i in range(len(streets)-1):
            for m in range(len(streets[i].coords)-1):
                x1 = streets[i].coords[m]
                x2 = streets[i].coords[m+1]
                for j in range(i+1, len(streets)):
                    for n in range(len(streets[j].coords)-1):
                        x3 = streets[j].coords[n]
                        x4 = streets[j].coords[n+1]
                        x5 = checkintersections(array(x1), array(x2), array(x3), array(x4))

                        if x5 != False:
                            graph.add_vertex(x1)
                            graph.add_vertex(x2)
                            graph.add_vertex(x3)
                            graph.add_vertex(x4)
                            graph.add_vertex(x5)

                            graph.add_edge(graph.coord2index(x1),graph.coord2index(x5))
                            graph.add_edge(graph.coord2index(x2),graph.coord2index(x5))
                            graph.add_edge(graph.coord2index(x3),graph.coord2index(x5))
                            graph.add_edge(graph.coord2index(x4),graph.coord2index(x5))

        print(graph)         

    #******************************           
    # Input Error:
    #******************************
    else:
        prnterror('Error: Incorrect input format')
    

      

