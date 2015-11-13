#!/usr/bin/env python
# http://docs.python.org/tutorial/
# http://docs.python.org/library/re.html

# a "Cases" (0,0) (10,10)
# a "ceses02" (10,0) (0,10)


#************************************************************
# imports
#************************************************************

import re
import sys
import math
from numpy import *
import subprocess


#************************************************************
# defines
#************************************************************

name_rx = '\".+\"'
num_rx = '-?\d+'
coord_rx = r'\(\s*'+num_rx+'\s*,\s*'+num_rx+'\s*\)'

cmd_a_rx = '\s*a\s+'+name_rx+'\s*('+coord_rx+'\s*){2,}\s*$'
cmd_c_rx = '\s*c\s+'+name_rx+'\s*('+coord_rx+'\s*){2,}\s*$'
cmd_r_rx = '\s*r\s+'+name_rx+'\s*$'
cmd_g_rx = '\s*g\s*'

cmd_a_chk = re.compile(cmd_a_rx)
cmd_c_chk = re.compile(cmd_c_rx)
cmd_r_chk = re.compile(cmd_r_rx)
cmd_g_chk = re.compile(cmd_g_rx)


    class Street():
        def __init__(self, name, coords):
            self.name = name
            self.coords = coords


    class Graph():
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
            
    
    


#******************************
# Line Intersect
# http://infohost.nmt.edu/tcc/help/lang/python/examples/homcoord/Line-intersect.html
# http://stackoverflow.com/questions/3252194/numpy-and-line-intersections
#******************************

def perp( a ) :
    b = empty_like(a)
    b[0] = -a[1]
    b[1] = a[0]
    return b
    
def seg_intersect(a1,a2, b1,b2):
    da = a2-a1
    db = b2-b1
    dp = a1-b1
    dap = perp(da)
    denom = dot(dap, db)
    num = dot(dap, dp)
    result = (num / denom)*db + b1
    
    if result[0] < min(a1[0],a2[0],b1[0],b2[0]) or \
       result[0] > max(a1[0],a2[0],b1[0],b2[0]) or \
       result[1] < min(a1[1],a2[1],b1[1],b2[1]) or \
       result[1] > max(a1[1],a2[1],b1[1],b2[1]):
        return False
    
    return tuple([result[0], result[1]])



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
    if cmd_a_chk.match(cmd) or cmd_c_chk.match(cmd) or cmd_r_chk.match(cmd):
        # recoord name and coordinates (if they exist)
        name = re.findall(name_rx,cmd)[0]
        coords = [ tuple([ float(num) for num in re.findall(num_rx,coord) ]) \
                  for coord in re.findall(coord_rx,cmd)]

        # Get current street list
        name_set = [ street.name for street in streets]

        #******************************    a "test01" (0,0) (10,10)

        # Add a new street
        #******************************
        if cmd_a_chk.match(cmd):
            if name not in name_set:
                streets.append(Street(name, coords))
            else:
                print('Error: street currently exists.')

        else:
            if name in name_set:
                #******************************        
                # Change an existing street
                #******************************
                if cmd_c_chk.match(cmd):
                    index = name_set.index(name)
                    streets[index].coords = coords
                #******************************
                # Remove an existing street
                #******************************
                else:
                    index = name_set.index(name)
                    streets.pop(index)
            else:
                print('Error: \'c\' or \'r\' specified for a street that does not exist.')


    #******************************           
    # Generate and print Graph
    #******************************
    elif cmd_g_chk.match(cmd):

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
                        x5 = seg_intersect(array(x1), array(x2), array(x3), array(x4))

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
        print('Error: Incorrect input format')
    

      

