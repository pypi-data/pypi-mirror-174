# -*- coding: utf-8 -*-
"""
Created on Sat Oct  1 21:10:02 2022

@author: lidon
"""

from .vector import*
from .linked_list import*
from .stack import*
from .hash_table import*
from .priority_queue import*
# implement some useful algorithms based on data structures we have implemented


# sort a vector
# input should be a list/vector object
# will return a new vector
# method specifies the way to sort
# supporting methods: merge, bubble, selection, quick, bucket
def sort(v,method='merge'):
    v=vector(v)
    u=v.copy()
    if method=='merge':
        u.merge_sort()
        return u
    elif method=='bubble':
        u.bubble_sort()
        return u
    elif method=='selection':
        u.selection_sort()
        return u
    elif method=='quick':
        u.quick_sort()
        return u
    elif method=='bucket':
        return bucket_sort(u)
    elif method=='heap':
        return heap_sort(u)




# some additional algorithms implemented by stack
# n the number in base 10, 0<base<16
# base: new base
# return a vector from high to low
# ex. convert(4,2)=[1,0,0]
def convert(n,base):
    # stk is some stack
    digit=[str(i) for i in range(0,9)]+['A','B','C','D','E','F']
    def inner_convert(stk,n,base,digit):
        if n>0:
            stk.push(digit[n%base])
            inner_convert(stk,int(n/base),base,digit)
        return stk
    stk=stack([])
    converted=inner_convert(stk,n,base,digit)
    
    # output the new_stack
    new_stk=stack([])
    while converted.length>0:
        new_stk.push(converted.top())
        converted.pop()
        
    return new_stk

#bracket checking
# check if there the brackets are legal
# brackets may include [],() and {}
def bra_check(string):
    stk=stack([])
    for i in range(0,len(string)):
        if string[i] in ['(','[','{']:
            stk.push(string[i])
        elif string[i]==')':
            if stk.empty():
                return False
            popped=stk.pop()
            if popped!='(':
                return False
        elif string[i]==']':
            if stk.empty():
                return False
            popped=stk.pop()
            if popped!=']':
                return False
        elif string[i]=='}':
            if stk.empty():
                return False
            popped=stk.pop()
            if popped!='}':
                return False
        else:
            a=1
    return stk.empty()

# solve n Queen problem
class queen:
    # x and y: respective coordinates
    def __init__(self,x,y):
        self.x=x
        self.y=y
        
    def __repr__(self):
        return f'({self.x},{self.y})'
        
    # verify if 2 queens are in conflict
    def __eq__(self,other):
        return self.x==other.x or self.y==other.y or (self.x+self.y)==(other.x+other.y) or (self.x-self.y)==(other.x-other.y)
    
    def copy(self):
        return queen(self.x,self.y)

# solve n queens problem
def place_queen(n):
    solution=stack([])
    q=queen(0,0)
    while solution.size()<n:
        # search w.r.t. line, prevent overflow
        if q.y>=n:
            # if overflow, track back and move the last queen to the next block
            q=solution.top()
            solution.pop()
            q.x=q.x+1
        # prevent overflow
        if q.x>=n:
            q.y=q.y+1
            q.x=0
        
        # current queen has contradictio with last queens, let it move again
        if solution.find(q)>=0:
            q.x=q.x+1
        # push the queen into the stack, move the new queen
        else:
            p=q.copy()
            solution.push(p)
            q.x=q.x+1
          
        # prevent overflow
        if q.x>=n:
            q.y=q.y+1
            q.x=0
    return solution

     
        
        
            