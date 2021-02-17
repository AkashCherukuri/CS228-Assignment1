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
	if t < start:
		tmp = start
		start = t
		t = tmp

	#Declare variables
	sz = len(mp)
	c = []
	for i in range(sz):
		c.append([])
		for j in range(sz):
			c[i].append([])


	s_map = map_to_int(start)
	t_map = map_to_int(t)
			
	for i in range(sz):
		for j in range(i+1,sz):
			#Have only half of the square, assign only edge vars instead of all
			c[i][j] = (Bool("c"+str(i)+str(j)))
			if ind_in_gr(i,j,graph):
				#Add Soft_Constraint
				s.add_soft(c[i][j])


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
		#Connectivity
		for k in range(sz):
			# print(i,k,j)
			# print(c[i][j], c[i][k], c[k][j])
			if s_map<i:
				if k<s_map:
					constr.append(Implies(And(c[k][s_map], c[k][i]),c[s_map][i]))
				elif s_map<k and k<i:
					constr.append(Implies(And(c[s_map][k], c[k][i]),c[s_map][i]))
				elif i<k:	
					constr.append(Implies(And(c[s_map][k], c[i][k]),c[s_map][i]))
			elif s_map>i:
				if k<i:
					constr.append(Implies(And(c[k][i], c[k][s_map]),c[i][s_map]))
				elif i<k and k<s_map:
					constr.append(Implies(And(c[i][k], c[k][s_map]),c[i][s_map]))
				elif s_map<k:	
					constr.append(Implies(And(c[i][k], c[s_map][k]),c[i][s_map]))
				

	#Question's constraint
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

		if not mod[c[i][j]]:
			answer.append(edg)

	return len(answer)
