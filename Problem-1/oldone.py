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
    print("init", len_of_code)
    #A[i][j] is an INT which can take either 0/1. A[i][j] is 1 if the i'th position has the j'th color, 0 otherwise.
    for i in range(k):
        lst = []
        for j in range(n):
            lst.append(Int("A[%s][%s]" %(i,j)))
        A.append(lst)

    for i in range(len_of_code):
        color_array = []
        for j in range(num_of_colors):
            color_array.append((A[i][j]==1))
            for k in range(num_of_colors):
                #Add constraint that one position cannot have two colors
                if k != j:
                    hard_const.append(Implies((A[i][j]==1),(A[i][k]==0)))
        
        #Each position must have atleast one color
        hard_const.append(Or(color_array))

    s.add(And(hard_const))

def put_first_player_response(red,white):
    #add soft constraints
    code = guess_codes[len(guess_codes)-1]
    len_of_code = len(code)
    print("fun values: ", len_of_code)
    if(red == len_of_code):
        return
    else:
        rsum = 0
        rwsum = 0
        for i in range(len_of_code):
            rsum = rsum + A[i][code[i]]
            for j in range(len_of_code):
                rwsum = rwsum + A[j][code[i]]
        s.add((rsum == Int(red)))
        s.add(rwsum == Int(red+white))


def get_second_player_move():
    #have to predict next move based on the constraints
    
    codelen = 0
    s.check()
    mod = s.model()
    print(mod)
    l = len(mod)
    print("Length: ", l)
    for i in range(l):
        if(mod[mod[i]] == 1):
            codelen = codelen + 1
    gcode = [-1] * codelen
    #print(len(gcode))
    #Problem here in string decomp.
    for i in range(l):
        if(mod[mod[i]] == 1):
            st = str(mod[i])
            gcode[int(st[2])] = int(st[5])
            
    print(gcode)
    guess_codes.append(gcode)
    return gcode