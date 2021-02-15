from z3 import *
import random

num_of_colors = 0
len_of_code = 0
guess_codes = []
turns = 0
#Solver
hard_const = []
s = Optimize()
A = []

def initialize(n,k):
    num_of_colors = n
    len_of_code = k
    A = [ [  Int("a_%s_%s" % (i, j)) for j in range(num_of_colors) ] 
      for i in range(len_of_code) ]
    for i in range(len_of_code):
        sum = 0
        for j in range(num_of_colors):
            hard_const.append(Or((A[i][j]==0),(A[i][j]==1)))
            sum = sum + A[i][j]
        hard_const.append((sum == 1))
    s.add(And(hard_const))

def put_first_player_response(red,white):
    #add soft constraints
    code = guess_codes[turns-1]
    if(red == len_of_code):
        return
    else:
        rsum = 0
        rwsum = 0
        for i in range(len_of_code):
            rsum = rsum + A[i,code[i]]
            for j in range(len_of_code):
                rwsum = rwsum + A[j,code[i]]
        s.add_soft(rsum == red)
        s.add_soft(rwsum == (red+white))


def get_second_player_move():
    #have to predict next move based on the constraints
    code = []
    if(turns == 0):
        for i in range(len_of_code):
            code.append(random.randint(0,num_of_colors-1))
        guess_codes.append(code)
        turns = turns + 1
    else:
        #use prev information to send out next best code?
        turns = turns + 1
    return code




