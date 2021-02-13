from z3 import *

mp = []

def map_to_int(i):
	#Will cause ValueError if you're not careful!
	return mp.index(i)

def find_minimal(graph, s, t):
	#Constraints list
	constr = []

	#Create mapping
	for edg in graph:
		i = edg[0]
		j = edg[1]
		try:
			mp.index(i)
		except ValueError:
			mp.append(i)
		try:
			mp.index(j)
		except ValueError:
			mp.append(j)

	#Declare variables
	sz = len(mp)
	a = []
	c = []
	for i in range(sz):
		a.append([])
		for j in range(sz):
			a[i].append(Bool("a"+str(i)+str(j)))
			c[i].append(Bool("c"+str(i)+str(j)))

	#Assign Values for edge variables
	for edg in graph:
		i = map_to_int(edg[0])
		j = map_to_int(edg[1])

		#TODO: Add present edges as soft constr and non-present edges as hard constr
		#constr.append(a[i][j])

	for i in range(sz):
		for j in range(sz):
			#Commutativity Constraint
			constr.append(And(Implies(a[i][j], a[j][i]), Implies(a[j][i], a[i][j])))
			constr.append(And(Implies(c[i][j], c[j][i]), Implies(c[j][i], c[i][j])))

			#Generic
			constr.append(c[i][i])

			#Connectivity
			for k in range(sz):
				constr.append(Implies(And(c[i][k], c[k][j]),c[i][j]))

			#Adjacent implies connectivity
			constr.append(Implies(a[i][j], c[i][j]))

	#Question's constraint
	s_map = map_to_int(s)
	t_map = map_to_int(t)
	constr.append(Not(c[s_map][t_map]))