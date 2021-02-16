from z3 import *
import random

num_of_colors = 0
len_of_code = 0
turns = 0
#Solver
guess_codes = []
hard_const = []
s = Optimize()
A = []

def initialize(n,k):
    turns = 0
    num_of_colors = n
    len_of_code = k
    A = [ [  Int("A[%s][%s]" % (i, j)) for j in range(num_of_colors) ] 
      for i in range(len_of_code) ]
    for i in range(len_of_code):
        sum = 0
        for j in range(num_of_colors):
            hard_const.append(Or((A[i][j]==0),(A[i][j]==1)))
            sum = sum + A[i][j]
        hard_const.append((sum == 1))
    s.add(And(hard_const))
    #s.check()
    #print (s.model())

def put_first_player_response(red,white):
    #add soft constraints
    code = guess_codes[len(guess_codes)-1]
    if(red == len_of_code):
        return
    else:
        rsum = 0
        rwsum = 0
        for i in range(len_of_code):
            rsum = rsum + A[i,code[i]]
            for j in range(len_of_code):
                rwsum = rwsum + A[j,code[i]]
        s.add_soft((rsum == Int(red)))
        s.add_soft(rwsum == Int(red+white))


def get_second_player_move():
    #have to predict next move based on the constraints
    
    codelen = 0
    s.check()
    mod = s.model()
    l = len(mod)
    for i in range(l):
        if(mod[mod[i]] == 1):
            codelen = codelen + 1
    gcode = [-1] * codelen
    #print(len(gcode))
    for i in range(l):
        if(mod[mod[i]] == 1):
            st = str(mod[i])
            gcode[int(st[2])] = int(st[5])
            
    print(gcode)
    guess_codes.append(gcode)
    return gcode




