#includes
from __future__ import division  # So we are not using integer division
import re
import sys
from numpy import *


#Declare

Invalid_NewCoomand = "New command"
#Error messages
MSG_INV_COMM = "You must type a valid command"
Invalid_sCoomand_msg = ": Not found command "
Invalid_street_msg = "Valid street was not entered \"name\"."
Invalid_Addition_msg = "'a' specified for a street that already exists."
Invalid_Remove_msg = "'r' specified for a street that does not exist."
Invalid_Change_msg = "'c' specified for a street that does not exist."
Invalid_CoordM_msg = "Invalid coordinates: "


#Global
mode_debug = False 
streets_list = dict() 
streets_list_modified = dict() 
intersections_completelist = set() 
#Graph
Vertexes = dict()
Edges = set()
count_vertex = 0 



def init():
    #holds the program main loop
    CONTINUEEXEC = True
    while (CONTINUEEXEC):
        try:
            CONTINUEEXEC  = requestInput()
        except Exception, e:            
            printerrormsg(str(e))
    programendmessage()


def programendmessage():
    #show goodbye message
    try:
        sys.exit("Program terminated by user command. Bye.")
    except Exception, e:
        printerrormsg(str(e))


def debug(msg):
    if mode_debug == True :
        print("DEBUG: " + msg)


def printerrormsg(msg):
    sys.stderr.write("Error: " + msg + "\n")


#===========================================================================

# Request basic input and try to corect unperfect entries as possible
def requestInput(message = Invalid_NewCoomand):

    strinput = ""
    try:
        strinput = raw_input()
    except Exception, e:
        printerrormsg(" End of File")
        return False

    strinput = strinput.strip() #trim
    if len(strinput) < 1:
        printerrormsg(MSG_INV_COMM)
        return True

    command = ""
    args = ""

    fullcommand = strinput.split(' ', 1)
    command = fullcommand[0] #command is always the first set of character

    #check if there are args
    if len(fullcommand) > 1:
        args = fullcommand[1].strip()

    #debug command switch:
    if (mode_debug):
        #extra commands for debug:
        if(command=="0"):
            print_all_ds()
        elif(command=="9"):
            reset_streets()
        elif(command=="1"):
            test()
        elif(command=="2"):
            test_description()
        elif(command=="3"):
            test_parsa()

    #main command switch:
    if(command=="exit"):
        return False #exits program
    elif(command=="a"):
        add_street(args)
    elif(command=="c"):
        street_modify_cmd(args)
    elif(command=="r"):
        remove_street(args)
    elif(command=="g"):
        show_graph()
    else:
        printerrormsg('\'' + command + '\'' + Invalid_sCoomand_msg)

    return True

#===========================================================================

def reset_streets():
    debug("reseting all streets")
    global count_vertex
    global streets_list_modified
    global intersections_completelist
    global Vertexes
    global Edges
    global streets_list
    count_vertex = 0
    streets_list = dict()
    streets_list_modified = dict()
    intersections_completelist = set()
    Vertexes = dict()
    Edges = set()

def add_street(args):
    
    try:
        name = re.search('"(.*?)"', args).group(1)
    except Exception, e:
        printerrormsg(Invalid_street_msg)
        return

    if ( len(name) == 0 ): 
        printerrormsg(Invalid_street_msg)
        return

    
    if name in streets_list:
        printerrormsg(Invalid_Addition_msg)
        return

    #extract coordinates
    coordinates_strings = re.findall('\(.*?\)',args)
    if ( len(coordinates_strings) == 0 ): 
        printerrormsg( "Incomplete command in " + args + ", no coordinates found.")
        return

    if ( len(coordinates_strings) == 1 ): 
        printerrormsg("Incomplete coordinates in " + args +", no end point.")
        return

    coordinates = list()
    for c_string in coordinates_strings:
        try:
            x, y = map(float, c_string.strip().strip('()').split(','))
        except Exception, e:
            printerrormsg(Invalid_CoordM_msg + c_string) 
            return
        
        if (x == None) or (y == None):
            printerrormsg(Invalid_CoordM_msg + c_string)
            return
        #coordinates are good and added
        coordinates.append((x,y))

 

    
    streets_list[name] = coordinates

    return



#===========================================================================

def street_modify_cmd(args):
        #extract name
        try:
            name = re.search('"(.*?)"', args).group(1)
        except Exception, e:
            printerrormsg(Invalid_street_msg)
            return

        if name not in streets_list:
            printerrormsg(Invalid_Change_msg)
            return

        #extract coordinates
        coordinates_strings = re.findall('\(.*?\)',args)
        if ( len(coordinates_strings) == 0 ):
            printerrormsg( "Command not complete " + args + ", no coordinates found.")
            return

        if ( len(coordinates_strings) == 1 ): #no endpoint found
            printerrormsg("Cordinates not complete in " + args +", no end point.")
            return

        coordinates = list()
        for c_string in coordinates_strings:
            try:
                x, y = map(float, c_string.strip().strip('()').split(','))
            except Exception, e:
                printerrormsg(Invalid_CoordM_msg + c_string)
                return
            
            if (x == None) or (y == None):
                printerrormsg(Invalid_CoordM_msg + c_string)
                return
            
            coordinates.append((x,y))

        
        streets_list[name] = coordinates


#===========================================================================
def remove_street(args):
        #extract name
        try:
            name = re.search('"(.*?)"', args).group(1)
        except Exception, e:
            printerrormsg(Invalid_street_msg)
            return

        if name not in streets_list:
            printerrormsg(Invalid_Remove_msg)
            return

        #Entry seems OK. Lets delete it
        try:
            del streets_list[name]
        except Exception, e:
            pass






def print_all_ds():
    
    print "====================="
    print "Original streets"
    print streets_list
    print "Enhanced streets"
    print streets_list_modified
    print "Intersections"
    print intersections_completelist
    print "====================="


def show_graph():
    reset_graph()
    draw_intersections()
    generate_graph()
    print_graph()


def  reset_graph():
    global count_vertex
    global streets_list_modified
    global intersections_completelist
    global Vertexes
    global Edges
    count_vertex = 0
    streets_list_modified = dict()
    intersections_completelist = set()
    Vertexes = dict()
    Edges = set()

def draw_intersections():

    for akey in streets_list:
        debug("PROCESS STREET " + str(akey))
        streetA = streets_list[akey]
        enhanced_streetA = list(streetA)
        #for j,point in enumerate(streetA):
        for j in range(len(streetA)-1):
            #segment A
            Ap = streetA[j]
            Aq = streetA[j+1]
            debug("Segment " + str(Ap) + str(Aq))
            segA_intersections = set() #store in a set to avoid repetition

            for bkey in streets_list:
                streetB = streets_list[bkey]
                #for i,point in enumerate(streetB):
                for i in range(len(streetB)-1):
                    Bp = streetB[i]
                    Bq = streetB[i+1]
                    
                    if (akey == bkey):
                        continue
                        
                    try:
                        intersection = findLineIntersect(Ap,Aq,Bp,Bq)
                    except Exception, e:
                        intersection = None

                    if intersection == None:
                        continue
                    else:
                        intersection = tuple(intersection)
                        segA_intersections.add(intersection)
                        intersections_completelist.add(intersection)
           
            
            if (segA_intersections): #if there is at least one intersection
                insert_new_points(enhanced_streetA,segA_intersections,Ap,Aq)
            #end of segment j
        #
        streets_list_modified[akey] = enhanced_streetA
        

def insert_new_points(street, newPoints, pointA, pointB):

    segA_intersections_list = list(newPoints)
    if (pointA<pointB): 
        segA_intersections_list.sort(reverse=True)
    else:
        segA_intersections_list.sort()

   

    pointB_index = street.index(pointB)

    for inter in segA_intersections_list:
        debug("inserting " + str(inter) + " in index " + str(pointB_index))
        
        if inter not in street:
            street.insert(pointB_index,inter) 


def generate_graph():

    for point in intersections_completelist:
        vertexid = test_and_add_vertex(point)
        #find neighbors
        for key in streets_list_modified:
            street = streets_list_modified[key]
            if point in street:
                index = street.index(point)
                try:
                    point_n1 = street[index-1] 
                    vertexid_n1 = test_and_add_vertex(point_n1)
                    #add Edge
                    test_and_add_edge((vertexid,vertexid_n1))
                except Exception, e:
                    debug("left neighbor not found")
                try:
                    point_n2 = street[index+1] #if tthere is a point after
                    vertexid_n2 = test_and_add_vertex(point_n2)
                    #add Edge, with found or new vertex
                    test_and_add_edge((vertexid,vertexid_n2))
                except Exception, e:
                    debug("right neighbor not found")

def test_and_add_edge(edge):
    for e in Edges:
        if (e[0] == edge[1] and e[1] == edge[0]) or (e[0] == edge[0] and e[1] == edge[1]) :
            #edge exists, just ignore
            return
    #not in graph
    Edges.add(edge)

def test_and_add_vertex(vertex):
    global count_vertex
    #test if vertex already exists
    for key in Vertexes:
        if Vertexes[key] == vertex:
            return key

    #not in graph
    count_vertex = count_vertex + 1
    vid = "v" + str(count_vertex)
    Vertexes[vid] = vertex

    return vid


def print_graph():
    if (mode_debug):
        print "=====GRAPH====="
        print "V = {"
        for key in Vertexes:
            print "    " + str(key) + ":    " + str(Vertexes[key])
        print "}"
        print "E = {"
        for e in Edges:
            print "    <" + str(e[0]) + "," + str(e[1]) + ">;  dbg;" + str(Vertexes[e[0]]) + ";" + str(Vertexes[e[1]])

        print "}"
    else:
        print "V = {"
        for key in Vertexes:
            print "    " + str(key) + ":    " + str(Vertexes[key])
        print "}"
        print "E = {"
        for e in Edges:
            print "    <" + str(e[0]) + "," + str(e[1]) + ">,"

        print "}"


#========================================= AUX ==============================

def findLineIntersect(lineAp, lineAq,lineBp, lineBq):
# http://stackoverflow.com/questions/3838329/how-can-i-check-if-two-segments-intersect
# http://stackoverflow.com/questions/20677795/find-the-point-of-intersecting-lines
    (x1,y1) = lineAp
    (x2,y2) = lineAq
    (u1,v1) = lineBp
    (u2,v2) = lineBq
    (a,b), (c,d) = (x2-x1, u1-u2), (y2-y1, v1-v2)
    e, f = u1-x1, v1-y1
    # Solve ((a,b), (c,d)) * (t,s) = (e,f)
    den = float(a*d - b*c)
    if (den==0): #todo: checar pq isso acontece e o near n detecta
        return None
    if near(den, 0):
        # parallel
        
        if near(float(e)/b, float(f)/d):
            # collinear
            px = x1
            py = y1
            return px,py
        else:
            return None
    else:
        t = (e*d - b*f)/den
        s = (a*f - e*c)/den
        
        if (0<=t<=1) and (0<=s<=1):
            px = x1 + t*(x2-x1)
            py = y1 + t*(y2-y1)
            return px, py
        else:
            return None


def near(a, b, rtol=1e-5, atol=1e-8):
    return abs(a - b) < (atol + rtol * abs(b))


#Start the program
init()
