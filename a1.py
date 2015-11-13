
#!/usr/bin/python

from __future__ import division  # So we are not using integer division
import sys  # for sys.argv
import fileinput  # to read from file or stdin
import copy
from copy import deepcopy


streets = {}
vertex = []
intersections = []
edge = []


	
def prnterror(message, line):
    """
    Displays an error message to stderr

    :param message: The error message to display
    :param line: The line where the error occurred
    :return: None
    """

    sys.stderr.write("%s:%s\n" % (message, line))		

def check_input(input):
	""" Analysis of the input to separate
	 the command, street name and the coordinates
	 if applicable."""

	input1=' '.join(input.split())
	input2=input1.split('"')
	cmd=input2[0].strip()
	result = []
	if cmd not in ['a', 'c', 'r', 'g', '']:
		prnterror("Error: <", cmd, "> is not a valid command.\n","invalid input")
	if cmd == 'a' or cmd == 'c' or cmd == 'r':
		if len(input2) != 3:
			prnterror("Error: Name of the street is not specified or specified without double quotation.\n","Invalid Input")
		name=input2[1]
		if name == '':
			prnterror("Error: Name of the street can not be empty.\n","Invalid Input")
			raise IndexError
		points= input2[2].strip()
		result.append(cmd)
		result.append(name)
		result.append(points)
	elif cmd == 'g':
		if len(input2) != 1:
			prnterror("Error: Street name or coordinates is/are specified for command 'g'.\n","Invalid Input")
			raise IndexError
		result.append(cmd)
	return result


def pointsError(points):
	""" Analysis of coordinates
	 to find the errors."""

	if points[0] != '(':
		 prnterror("Error: Bad input format","Invalid Input")
	n = len(points)
        if points[n-2] != ')':
		prnterror("Error: Bad input format","Invalid Input")
        i = 0
        flag = 0
        while points[i] != '\n':
		if points[i] == '(':
                	if flag == 1 or flag == 2:
				prnterror("Error: Bad input format","Invalid Input")
                        flag = 1
                        i=i+1
                elif points[i] == ',':
                       	if flag != 1:
				prnterror("Error: Bad input format","Invalid Input")
                        flag = 2
                        i=i+1
                elif points[i] == ')':
                        if flag != 2:
				prnterror("Error: Bad input format","Invalid Input")
                        flag = 3
                        i=i+1
                else:
			if points[i] != '-':
				if ord(points[i]) < ord('0') or ord(points[i])> ord('9'):
					raise ValueError
                        i=i+1

		
def extractNumbers(str):
	""" Receives (x,y), extracts x and y, 
	converts them to numbers and
	returns them as a list."""

	result=[]
	i=0
	number1=[]
    	number2=[]
    	while str[i]!=',':
		number1.append(str[i])
        	i=i+1
	if len(number1) == 0:
		raise ValueError
    	temp1=''.join(number1)
    	result.append(float(temp1))
    	i=i+1
    	while str[i]!=')':
        	number2.append(str[i])
        	i=i+1
	if len(number2) == 0:
		raise ValueError
    	temp2=''.join(number2)
    	result.append(float(temp2))
    	return result


# http://stackoverflow.com/questions/3838329/how-can-i-check-if-two-segments-intersect
# http://stackoverflow.com/questions/20677795/find-the-point-of-intersecting-lines
def check_intersection(x1, y1, x2, y2, w1, z1, w2, z2):
	""" Receives the coordinates
	 of two line segments, finds
	 the intrsection of them and
	 returns the result as a list
	 if there is any intersection."""

	a1 = y2 - y1
	b1 = x1 - x2
	c1 = a1*x1 + b1*y1
	a2 = z2 - z1
	b2 = w1 - w2
	c2 = a2*w1 + b2*z1
	slopesDif = a1*b2 - a2*b1
	if (slopesDif != 0):
		x = (b2*c1 - b1*c2)/slopesDif
		y = (a1*c2 - a2*c1)/slopesDif
		if x >= min([x1,x2]) and x <= max([x1,x2]) and x >= min([w1,w2]) and x <= max([w1,w2]) and y >= min([y1,y2]) and y <= max([y1,y2]) and y >= min([z1,z2]) and y <= max([z1,z2]):
			return [round(x,2),round(y,2)]
	else:
			if (x1 == w1 and y1 == z1) or (x1 == w2 and y1 == z2):
				return [x1, y1]
			elif (x2 == w1 and y2 == z1) or (x2 == w2 and y2 == z2):
				return [x2, y2]


def printGraph(vertices, edges):
	""" Print the graph by
	 printing the vertices
	 and edges."""
	vertexList = []
	vertexList.append('V')
	vertexList.append(str(len(vertices)))
	print>>sys.stdout, ' '.join(vertexList)

	edgeList = []
	edgeList.append("E ")
	edgeList.append('{')
	for i in range(0, len(edges)):
		edgeList.append('<')
		edgeList.append(str(edges[i][0]))
		edgeList.append(',') 
		edgeList.append(str(edges[i][1]))
		edgeList.append('>')
		if i != len(edges)-1:
			edgeList.append(',')
	edgeList.append('}')
	print>>sys.stdout, ''.join(edgeList)
	sys.stdout.flush()	


while True:
  try:
	input = raw_input()
	result_input = check_input(input)

	if result_input[0] == 'a':
		if streets.has_key(result_input[1]):
			prnterror("Error: 'a' specified for a street that already exists.\n",street)
		else:
			temp = result_input[2]
			points = ''. join(temp.split())
			pointsError(points+'\n')
			twoPoint = points.split('(')

			if len(twoPoint) < 3:
				prnterror("Error: Incomplete co-ordinates","Input Error")

			result_coords = []
			for i in range(1, len(twoPoint)):
				result_coords.append(extractNumbers(twoPoint[i]))

			for i in range(1, len(result_coords)):
				if result_coords[i] == result_coords[i-1]:
					prnterror("Error: Entered repetitive consecutive coordinates.\n","Invalid Input")
					raise IndexError

			streets[result_input[1]] = result_coords

	elif result_input[0] == 'c':
                if streets.has_key(result_input[1]):
                        temp = result_input[2]
                        points = ''. join(temp.split())
                        pointsError(points+'\n')
                        twoPoint = points.split('(')

			if len(twoPoint) <3:
				prnterror("Error: Incomplete co-ordinates","Input Error")

                        result_coords = []
                        for i in range(1, len(twoPoint)):
                                result_coords.append(extractNumbers(twoPoint[i]))

			for i in range(1, len(result_coords)):
                        	if result_coords[i] == result_coords[i-1]:
                                	prnterror("Error: Entered repetitive  coordinates","Invalid Input")
					raise IndexError

                        streets[result_input[1]] = result_coords

                else:
                        prnterror("Error: 'c' specified for a non existing street ","Invalid Input")
	
	elif result_input[0] == 'r':
		if result_input[2] != '':
			prnterror("Error: Coordinates specified for command ","")
		elif streets.has_key(result_input[1]) == True:
			del streets[result_input[1]]
		else:
			prnterror("Error: 'r' specified for a non existing street ","")

	
	elif result_input[0] == 'g':
		vertex = []
		edge = []
		intersections = []
		lines = []
		temp = streets.values()
		lines = copy.deepcopy(streets.values())
		for i in range(0, len(lines)):
			lines[i].append('\n')

		for i in range(0, len(temp)):
			for j in range(i+1, len(temp)):
				k = 0
				while k < (len(temp[i])-1):
					l = 0
					while l < (len(temp[j])-1):
						inters = check_intersection(temp[i][k][0], temp[i][k][1], temp[i][k+1][0], temp[i][k+1][1], temp[j][l][0], temp[j][l][1], temp[j][l+1][0], temp[j][l+1][1])
						if inters != None:
							if inters not in intersections:
								intersections.append(inters)
							q = lines[i].index(temp[i][k])
							z = lines[j].index(temp[j][l])
							while lines[i][q+1] != '\n':
								if min([lines[i][q][0], lines[i][q+1][0]]) <= inters[0] <= max([lines[i][q][0],lines[i][q+1][0]]) and min([lines[i][q+1][1],lines[i][q][1]]) <= inters[1] <= max([lines[i][q][1],lines[i][q+1][1]]):
									if lines[i][q] != inters and lines[i][q+1] != inters:
										lines[i].insert(q+1, inters)
									break
								q = q+1
							while lines[j][z+1]!='\n':
								if min([lines[j][z+1][0],lines[j][z][0]]) <= inters[0] <= max([lines[j][z][0],lines[j][z+1][0]]) and min([lines[j][z+1][1],lines[j][z][1]]) <= inters[1] <= max([lines[j][z][1],lines[j][z+1][1]]):
									if lines[j][z] != inters and lines[j][z+1] != inters:
										lines[j].insert(z+1, inters)
									break
								z = z+1
						l = l+1
					k= k+1
		# find edges and vertices
		vertex = copy.deepcopy(intersections)
		for x in intersections:
			for i in range(0, len(lines)):
				for j in range(0, len(lines[i])-1):
					if x == lines[i][j]:
						a = vertex.index(x)
						if j-1 >= 0: 
							if lines[i][j-1] != '\n':
								if lines[i][j-1] not in vertex:
									vertex.append(lines[i][j-1])
								b = vertex.index(lines[i][j-1])
								minab = min(a,b)
								maxab = max(a,b)
								if [minab,maxab] not in edge:
									edge.append([minab,maxab])
						if j+1 < len(lines[i]): 
							if lines[i][j+1] != '\n':
								if lines[i][j+1] not in vertex:
									vertex.append(lines[i][j+1])
								c = vertex.index(lines[i][j+1])
								minac = min(a,c)
								maxac = max(a,c)
								if [minac,maxac] not in edge:
									edge.append([minac,maxac])

		# print vertices and edges
		printGraph(vertex, edge)
		
  except EOFError:
     break
  except IndexError:
	 pass
  except (RuntimeError, TypeError, NameError):
     pass
  
