#includes
import re
import sys
from numpy import *
#import ipdb for Debug

#===========================================================================
#Consts
MSG_NEWCOM = "New command"
#Error messages
MSG_INV_COMM = "You must type a valid command"
MSG_COMM_NOTFOUNF = ": command not found."
MSG_INV_STNAME = "You must specify a valid street name using doublequote marks \"name\"."
#Python 2.4.3 does not support format()
#MSG_COORD_INCOMPLETE = "Incomplete coordinates in %, no end point."
#MSG_COORD_NOTFOUND = "Incomplete command in %, no coordinates found."
MSG_ADD_EXISTS = "'a' specified for a street that already exists."
MSG_R_NOTEXIST = "'r' specified for a street that does not exist."
MSG_C_NOTEXIST = "'c' specified for a street that does not exist."
MSG_INV_COORD = "Invalid coordinates: "

#===========================================================================
#Global
debug_mode = False #Debug mode must be false as default
all_streets = dict() #dictionary, each street is a list of coordinates, which is a tuple of 2 floats
all_enhanced_streets = dict() #dictionary, copy of the street, but will have the intersections
all_intersections = set() #list of all intersections. This will help to build the graph.
#Graph
Vertexes = dict()
Edges = set()
vid_count = 0 #aux var to generate sequential ids


#=================================== MAIN PROGRAM ==========================

def init():
    #holds the program main loop
    CONTINUEEXEC = True
    while (CONTINUEEXEC):
        try:
            CONTINUEEXEC  = requestInput()
        except Exception, e:
            #report error, but continue accepting new entries
            reportError(str(e))
    exitProgram()


def exitProgram():
    #show goodbye message
    try:
        sys.exit("Program terminated by user command. Bye.")
    except Exception, e:
        reportError(str(e))


def debug(msg):
    if debug_mode == True :
        print("DEBUG: " + msg)


def reportError(msg):
    sys.stderr.write("Error: " + msg + "\n")


#===========================================================================

# Request basic input and try to corect unperfect entries as possible
def requestInput(message = MSG_NEWCOM):

    strinput = ""
    try:
        strinput = raw_input()
    except Exception, e:
        reportError(" End of File")
        return False

    strinput = strinput.strip() #trim
    if len(strinput) < 1:
        reportError(MSG_INV_COMM)
        return True

    command = ""
    args = ""

    fullcommand = strinput.split(' ', 1)
    command = fullcommand[0] #command is always the first set of character

    #check if there are args
    if len(fullcommand) > 1:
        args = fullcommand[1].strip()

    #debug command switch:
    if (debug_mode):
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
        change_street(args)
    elif(command=="r"):
        remove_street(args)
    elif(command=="g"):
        show_graph()
    else:
        reportError('\'' + command + '\'' + MSG_COMM_NOTFOUNF)

    return True

#===========================================================================

def reset_streets():
    debug("reseting all streets")
    global vid_count
    global all_enhanced_streets
    global all_intersections
    global Vertexes
    global Edges
    global all_streets
    vid_count = 0
    all_streets = dict()
    all_enhanced_streets = dict()
    all_intersections = set()
    Vertexes = dict()
    Edges = set()

def add_street(args):
    #extract name
    try:
        name = re.search('"(.*?)"', args).group(1)
    except Exception, e:
        reportError(MSG_INV_STNAME)
        return

    if ( len(name) == 0 ): #blank name found
        reportError(MSG_INV_STNAME)
        return

    #if street already exists, can not add
    if name in all_streets:
        reportError(MSG_ADD_EXISTS)
        return

    #extract coordinates
    coordinates_strings = re.findall('\(.*?\)',args)
    if ( len(coordinates_strings) == 0 ): #no coordinates found
        reportError( "Incomplete command in " + args + ", no coordinates found.")
        return

    if ( len(coordinates_strings) == 1 ): #no endpoint found
        reportError("Incomplete coordinates in " + args +", no end point.")
        return

    coordinates = list()
    for c_string in coordinates_strings:
        try:
            x, y = map(float, c_string.strip().strip('()').split(','))
        except Exception, e:
            reportError(MSG_INV_COORD + c_string) #invalid coordinates
            return
        #not sure if is possible to return wrong values without throwing previous exception
        if (x == None) or (y == None):
            reportError(MSG_INV_COORD + c_string)
            return
        #coordinates accepted
        coordinates.append((x,y))

    #Entry seems OK. Lets added it.

    #add new steet to streets dictionary
    all_streets[name] = coordinates

    return



#===========================================================================

def change_street(args):
        #extract name
        try:
            name = re.search('"(.*?)"', args).group(1)
        except Exception, e:
            reportError(MSG_INV_STNAME)
            return

        if name not in all_streets:
            reportError(MSG_C_NOTEXIST)
            return

        #extract coordinates
        coordinates_strings = re.findall('\(.*?\)',args)
        if ( len(coordinates_strings) == 0 ):
            reportError( "Incomplete command in " + args + ", no coordinates found.")
            return

        if ( len(coordinates_strings) == 1 ): #no endpoint found
            reportError("Incomplete coordinates in " + args +", no end point.")
            return

        coordinates = list()
        for c_string in coordinates_strings:
            try:
                x, y = map(float, c_string.strip().strip('()').split(','))
            except Exception, e:
                reportError(MSG_INV_COORD + c_string)
                return
            #not sure if is possible to return wrong values without throwing previous exception
            if (x == None) or (y == None):
                reportError(MSG_INV_COORD + c_string)
                return
            #coordinates accepted
            coordinates.append((x,y))

        #Entry seems OK. Lets achange it.

        #update street definition in dictionary
        all_streets[name] = coordinates


#===========================================================================
def remove_street(args):
        #extract name
        try:
            name = re.search('"(.*?)"', args).group(1)
        except Exception, e:
            reportError(MSG_INV_STNAME)
            return

        if name not in all_streets:
            reportError(MSG_R_NOTEXIST)
            return

        #Entry seems OK. Lets delete it
        try:
            del all_streets[name]
        except Exception, e:
            pass


#============================== Graph ==========================================



def print_all_ds():
    #debug function
    print "====================="
    print "Original streets"
    print all_streets
    print "Enhanced streets"
    print all_enhanced_streets
    print "Intersections"
    print all_intersections
    print "====================="


def show_graph():
    reset_graph()
    process_intersections()
    generate_graph()
    print_graph()


def  reset_graph():
    global vid_count
    global all_enhanced_streets
    global all_intersections
    global Vertexes
    global Edges
    vid_count = 0
    all_enhanced_streets = dict()
    all_intersections = set()
    Vertexes = dict()
    Edges = set()

def process_intersections():

    for akey in all_streets:
        debug("PROCESS STREET " + str(akey))
        streetA = all_streets[akey]
        enhanced_streetA = list(streetA)
        #for j,point in enumerate(streetA):
        for j in range(len(streetA)-1):
            #segment A
            Ap = streetA[j]
            Aq = streetA[j+1]
            debug("Segment " + str(Ap) + str(Aq))
            segA_intersections = set() #store in a set to avoid repetition

            for bkey in all_streets:
                streetB = all_streets[bkey]
                #for i,point in enumerate(streetB):
                for i in range(len(streetB)-1):
                    Bp = streetB[i]
                    Bq = streetB[i+1]

                    #if same street are in hand, be careful
                    #Based on a discussion on learn, its not possible to have intersections from the same street
                    if (akey == bkey):
                        continue
                        '''if (Ap == Bp):# or (Aq == Bq): #sub segment or the same
                        #    continue
                        #if they are before or after each other
                        if (Aq == Bp) or (Bq == Ap) or (Ap == Bp):
                            continue
                        '''
                    #todo: optimization to avoid too many comparisons can be done here
                    #The truth: do they intersect?
                    try:
                        intersection = findLineIntersect(Ap,Aq,Bp,Bq)
                    except Exception, e:
                        intersection = None

                    if intersection == None:
                        continue
                    else:
                        intersection = tuple(intersection)
                        segA_intersections.add(intersection)
                        all_intersections.add(intersection)

            #end of comparisons
            #build enhanced segment:
            debug("Intersections found: " + str(segA_intersections))
            if (segA_intersections): #if there is at least one intersection
                insert_new_points(enhanced_streetA,segA_intersections,Ap,Aq)
            #end of segment j
        #
        all_enhanced_streets[akey] = enhanced_streetA
        debug("FINISHED STREET. NEW STATUS: " + akey + str(enhanced_streetA))
        #end of street akey
    #end of all streets as A

def insert_new_points(street, newPoints, pointA, pointB):

    segA_intersections_list = list(newPoints)
    if (pointA<pointB): #the direction will help to add all new intersections in the right order
        segA_intersections_list.sort(reverse=True)
    else:
        segA_intersections_list.sort()

    # The enhanced street  may have changed in other loop segment. So, the j index can not be used
    # We have to find the new index of pointB
    # Since there is no intersection with the same street,
    # its impossible to have more than one point with the same coordinates.

    pointB_index = street.index(pointB)

    for inter in segA_intersections_list:
        debug("inserting " + str(inter) + " in index " + str(pointB_index))
        #check if the intersections is not already a point
        if inter not in street:
            street.insert(pointB_index,inter) # #inserted in the position of the end of segment, in reverse order


def generate_graph():

    for point in all_intersections:
        vertexid = test_and_add_vertex(point)
        #find neighbors
        for key in all_enhanced_streets:
            street = all_enhanced_streets[key]
            if point in street:
                #Since the street can not intersect itself,
                #there is only one point that can be an intersection with the same coordinates
                index = street.index(point)
                #try to find neighbor points to add edges
                try:
                    point_n1 = street[index-1] #if there is a point before this intersection
                    vertexid_n1 = test_and_add_vertex(point_n1)
                    #add Edge, with found or new vertex
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
    #test if edge already exists
    #the graph if bidirectional, the inverse edge must be tested
    for e in Edges:
        if (e[0] == edge[1] and e[1] == edge[0]) or (e[0] == edge[0] and e[1] == edge[1]) :
            #edge exists, just ignore
            return
    #not in graph
    Edges.add(edge)

def test_and_add_vertex(vertex):
    global vid_count
    #test if vertex already exists
    for key in Vertexes:
        if Vertexes[key] == vertex:
            return key

    #not in graph
    vid_count = vid_count + 1
    vid = "v" + str(vid_count)
    Vertexes[vid] = vertex

    return vid


def print_graph():
    if (debug_mode):
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
    #Return the coordinates of a point of intersection given two lines or
    #None if the lines are parallel and non-collinear.
    #Return an arbitrary point of intersection if the lines are collinear.
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
        # If collinear, the equation is solvable with t = 0.
        # When t=0, s would have to equal e/b and f/d
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
        # When 0<=t<=1 and 0<=s<=1 the point of intersection occurs within the line segments
        if (0<=t<=1) and (0<=s<=1):
            px = x1 + t*(x2-x1)
            py = y1 + t*(y2-y1)
            return px, py
        else:
            return None


def near(a, b, rtol=1e-5, atol=1e-8):
    return abs(a - b) < (atol + rtol * abs(b))


#====================================Tests==================================
def test():
    add_street("\" RA\" (5,1)  (5,5) (5,10)")
    add_street("\"RB\" (1,4) (4,4) (10,4)")
    show_graph()

def test_description():
    #testing example from the assingment description
    add_street("a \"Weber Street\" (2,-1) (2,2) (5,5) (5,6) (3,8)")
    add_street("a \"King Street S\" (4,2) (4,8)")
    add_street("a \"Davenport Road\" (1,4) (5,8)")
    show_graph()

def test_parsa():
    #testing extra example posted by Parsa
    add_street("\"Columbia\" ( -3,-2) (-2, 0) (6 , 2 ) ")
    add_street("\"University\" (1,-2)(2,-1)(6,0)")
    add_street("\"Phillip\" (2,-2 ) ( 2 , 2 )")
    add_street("\"Lester\" (3,-4)")
    add_street("\"Albert\" (4,-2) (4,2)")
    add_street("\"Hazel\" (5,-1) (5,2)")
    add_street("\"University\" (6,-4) (8,12)")
    remove_street("\"King\")")
    change_street("\"King\")")
    change_street("\"Hazel\" (5,0) (5 , 2))")
    show_graph()
#===========================================================================
#Start the program
init()
