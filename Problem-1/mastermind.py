from z3 import *
import random

num_of_colors = 0
len_of_code = 0
guess_codes = []
turns = 0
#Solver
s = Optimize()
A = []

def initialize(n,k):
    num_of_colors = n
    len_of_code = k
    A = [ [ Int("a_%s_%s" % (i, j)) for j in range(num_of_colors) ] 
      for i in range(len_of_code) ]

def put_first_player_response(red,white):
    #add soft constraints
    code = guess_codes[turns-1]
    if(red == 0 and white == 0):
        return
    elif(red == len_of_code):
        return
    else:
        #constraints here
        return

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
        return
    return code




