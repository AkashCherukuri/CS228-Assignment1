import disconnect



#print(set([(2,4),(3,4),(1,3),(2,4)]))

fin_eds=[]
fin_st=[]
for cc in range(10):
	edges = []
	with open("./test/edges_{}.txt".format(cc)) as f:
		for line in f:
			edges.append(tuple([int(v) for v in line.strip().split(',')]))
	s_t=[]
	with open('./test/s_t_{}.txt'.format(cc)) as f:
		for line in f:
			s_t.append(tuple([int(v) for v in line.strip().split(',')]))
	fin_st.append(s_t)
	fin_eds.append(edges)
counter=0
for cs in range(10):
	for s,t in fin_st[cs]:
		with open('./test/res1_{}.txt'.format(cs) , 'a') as the_file:
			the_file.write('{}\n'.format(disconnect.find_minimal(fin_eds[cs],s,t)))
		counter+=1
		print(counter)


