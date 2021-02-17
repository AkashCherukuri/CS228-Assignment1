from z3 import *

mp = []

def map_to_int(i):
	#Will cause ValueError if you're not careful!
	return mp.index(i)

def ind_in_gr(i,j,graph):
	i_new = mp[i]
	j_new = mp[j]
	if (i_new, j_new) in graph:
		return True
	return False 

def find_minimal(graph, start, t):
	#Constraints list
	constr = []

	#Solver
	s = Optimize()

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

	#To make efficient, use distinct property
	mp.sort()

	#Declare variables
	sz = len(mp)
	a = []
	c = []
	for i in range(sz):
		a.append([])
		c.append([])
		for j in range(sz):
			a[i].append([])
			c[i].append([])

	for i in range(sz):
		for j in range(sz):
			#Have only half of the square, assign only edge vars instead of all
			if i<j:
				c[i][j] = (Bool("c"+str(i)+str(j)))
				if ind_in_gr(i,j,graph):
					a[i][j] = (Bool("a"+str(i)+str(j)))
					#Add Soft_Constraint
					s.add_soft(a[i][j])


	#Assign Values for edge variables
	# for i in range(sz):
	# 	for j in range(sz):
	# 		if (mp[i],mp[j]) in graph or (mp[j],mp[i]) in graph:
	# 			#print("Found Edge: ",i, j)
	# 			#print("Corresponds to:",mp[i],mp[j],"\n")
	# 			#Add soft constraint over present edges
	# 			s.add_soft(a[i][j])

	# 		elif i != j:
	# 			#Add hard constraint over edges not present
	# 			constr.append(Not(a[i][j]))

	for i in range(sz):
		for j in range(sz):
			#Commutativity Constraint redundant as i<j
			# constr.append(And(Implies(a[i][j], a[j][i]), Implies(a[j][i], a[i][j])))
			# constr.append(And(Implies(c[i][j], c[j][i]), Implies(c[j][i], c[i][j])))

			# Generic redundant as i<j
			# constr.append(c[i][i])
			# constr.append(a[i][i])

			if i<j:
				#Connectivity
				for k in range(sz):
					# print(i,k,j)
					# print(c[i][j], c[i][k], c[k][j])
					if k<i:
						constr.append(Implies(And(c[k][i], c[k][j]),c[i][j]))
					elif i<k and k<j:
						constr.append(Implies(And(c[i][k], c[k][j]),c[i][j]))
					elif j<k:	
						constr.append(Implies(And(c[i][k], c[j][k]),c[i][j]))

				#Adjacent implies connectivity
				if ind_in_gr(i,j,graph):
					#print("adj: ",i,j,a[i][j],c[i][j])
					constr.append(Implies(a[i][j], c[i][j]))

	#Question's constraint
	s_map = map_to_int(start)
	t_map = map_to_int(t)
	constr.append(Not(c[s_map][t_map]))

	#Add all these constraints into the solver
	s.add(And( constr ))

	#Problem need not always be sat, if s,t are the same point
	s.check()
	mod = s.model()

	answer = []

	for edg in graph:
		i = map_to_int(edg[0])
		j = map_to_int(edg[1])

		if not mod[a[i][j]]:
			answer.append(edg)

	return len(answer)
