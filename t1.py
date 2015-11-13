


#************************************************************
# imports
#************************************************************
from __future__ import division  # So we are not using integer division
import re
import sys
import math
from numpy import *
import subprocess


#************************************************************
# Regex
#************************************************************

rgx_name = '\".+\"'
rgx_number = '-?\d+'
rgx_street_coordinates = r'\(\s*'+rgx_number+'\s*,\s*'+rgx_number+'\s*\)'

rgx_input_add = '\s*a\s+'+rgx_name+'\s*('+rgx_street_coordinates+'\s*){2,}\s*$'
cmd_c_rx = '\s*c\s+'+rgx_name+'\s*('+rgx_street_coordinates+'\s*){2,}\s*$'
rgx_input_remove = '\s*r\s+'+rgx_name+'\s*$'
rgx_input_graph = '\s*g\s*'

rgx_check_addstreet = re.compile(rgx_input_add)
rgx_check_changestreet = re.compile(cmd_c_rx)
rgx_check_removestreet = re.compile(rgx_input_remove)
rgx_check_graph = re.compile(rgx_input_graph)


class Street():
    def __init__(self, name, coords):
        self.name = name
        self.coords = coords


class Graph():
    vs = []
    es = []

    def getindexCoords(self, coord):
        if coord in self.vs:
            return self.vs.index(coord)
        else:
            return False
            
    def getcoordsfrmidx(self, index):
        if index < len(self.vs):
            return self.vs[index]
        else:
            return False

    def vertex_append(self, coord):
        if coord not in self.vs:
            self.vs.append(coord)       

    def edge_append(self, v1, v2):
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
        




#******************************
# # http://stackoverflow.com/questions/3838329/how-can-i-check-if-two-segments-intersect
# http://stackoverflow.com/questions/20677795/find-the-point-of-intersecting-lines
# http://infohost.nmt.edu/tcc/help/lang/python/examples/homcoord/Line-intersect.html
# http://stackoverflow.com/questions/3252194/numpy-and-line-intersections
#******************************

def prnterror(message,line):
    """
    Displays an error message to stderr

    :param message: The error message to display
    :param line: The line where the error occurred
    :return: None
    """

    sys.stderr.write("%s:%s\n" % (message, line))
	
	
def check_parallel( a ) :
    b = empty_like(a)
    b[0] = -a[1]
    b[1] = a[0]
    return b
    
def Check_intersections(a1,a2, b1,b2):
    da = a2-a1
    db = b2-b1
    dp = a1-b1
    dap = check_parallel(da)
    denom = dot(dap, db)
    num = dot(dap, dp)
    result = (num / denom)*db + b1
    
    if result[0] < min(a1[0],a2[0],b1[0],b2[0]) or \
       result[0] > max(a1[0],a2[0],b1[0],b2[0]) or \
       result[1] < min(a1[1],a2[1],b1[1],b2[1]) or \
       result[1] > max(a1[1],a2[1],b1[1],b2[1]):
        return False
    
    return tuple([round(result[0],2), round(result[1],2)])



#************************************************************
# main
#************************************************************

streets = []
graph = Graph()

while True:

    #******************************
    # get raw input and check cmd validity
    #******************************
    cmd = raw_input()
    
    #******************************    
    # Add a new street
    #******************************
    if rgx_check_addstreet.match(cmd) or rgx_check_changestreet.match(cmd) or rgx_check_removestreet.match(cmd):
        # recoord name and coordinates (if they exist)
        name = re.findall(rgx_name,cmd)[0]
        coords = [ tuple([ float(num) for num in re.findall(rgx_number,coord) ]) \
                  for coord in re.findall(rgx_street_coordinates,cmd)]

        # Get current street list
        name_set = [ street.name for street in streets]

        #******************************    a "test01" (0,0) (10,10)

        # Add a new street
        #******************************
        if rgx_check_addstreet.match(cmd):
            if name not in name_set:
                streets.append(Street(name, coords))
            else:
                prnterror('Error: street currently exists.',name)

        else:
            if name in name_set:
                #******************************        
                # Change an existing street
                #******************************
                if rgx_check_changestreet.match(cmd):
                    index = name_set.index(name)
                    streets[index].coords = coords
                #******************************
                # Remove an existing street
                #******************************
                else:
                    index = name_set.index(name)
                    streets.pop(index)
            else:
                prnterror('Error: \'c\' or \'r\' specified for a street that does not exist.',name)


    #******************************           
    # Generate and print Graph
    #******************************
    elif rgx_check_graph.match(cmd):

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
                        x5 = Check_intersections(array(x1), array(x2), array(x3), array(x4))

                        if x5 != False:
                            graph.vertex_append(x1)
                            graph.vertex_append(x2)
                            graph.vertex_append(x3)
                            graph.vertex_append(x4)
                            graph.vertex_append(x5)

                            graph.edge_append(graph.getindexCoords(x1),graph.getindexCoords(x5))
                            graph.edge_append(graph.getindexCoords(x2),graph.getindexCoords(x5))
                            graph.edge_append(graph.getindexCoords(x3),graph.getindexCoords(x5))
                            graph.edge_append(graph.getindexCoords(x4),graph.getindexCoords(x5))

        print(graph)         

    #******************************           
    # Input Error:
    #******************************
    else:
        prnterror('Error: Incorrect input format','Format Error')
    

      


