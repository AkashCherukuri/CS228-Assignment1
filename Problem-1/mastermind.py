from z3 import *
import random

num_of_colors = 0
len_of_code = 0
guess_codes = []
hard_const = []
s = Optimize()
A = []

def initialize(n,k):
    global num_of_colors
    num_of_colors = n
    global len_of_code
    len_of_code = k
    # print("colors", n, "length of code", k)
    #A[i][j] is an INT which can take either 0/1. A[i][j] is 1 if the i'th position has the j'th color, 0 otherwise.
    for i in range(k):
        lst = []
        for j in range(n):
            lst.append(Bool("A[%s][%s]" %(i,j)))
        A.append(lst)

    for i in range(len_of_code):
        l = []
        for j in range(num_of_colors):
            l.append(A[i][j])
            for k in range(num_of_colors):
                #Add constraint that one position cannot have two colors
                if k != j:
                    hard_const.append(Implies((A[i][j]),(Not(A[i][k]))))        
        #Each position must have atleast one color
        s.add(Or(l))
    s.add(And(hard_const))

def put_first_player_response(red,white):
    #add soft constraints
    code = guess_codes[len(guess_codes)-1]
    #print("fun values: ", len_of_code)
    if(red == len_of_code):
        return
    else:
        colors=[]
        for i in range(len_of_code):
            if code[i] not in colors:
                colors.append(code[i])

        # print(colors)

        s.add_soft(Sum([If(Bool("A[%s][%s]" %(i,code[i])),1,0) for i in range(len_of_code)]) == red)
        s.add_soft(Sum([If(Bool("A[%s][%s]" %(i, j)),1,0) for i in range(len_of_code) for j in colors]) >= white + red)


def get_second_player_move():
    #have to predict next move based on the constraints
    gcode = [-1] * len_of_code
    if(len(guess_codes) == 0):
        for i in range(len_of_code):
            if(i<len_of_code/2):
                gcode[i] = 0
            else:
                gcode[i] = 1
        guess_codes.append(gcode)
        return gcode
    s.check()
    mod = s.model()
    # if s.check() == sat:
    #     print(mod)
    
    # print(mod)
    l = len(mod)
    # print("Length: ", l)
    #print(len(gcode))
    for i in range(l):
        if(mod[mod[i]]):
            st = str(mod[i])
            if(len(st) == 7):
                gcode[int(st[2])] = int(st[5])
            elif(len(st) == 8):
                gcode[int(st[2])] = int(st[5] + st[6])
            
    guess_codes.append(gcode)
    return gcode