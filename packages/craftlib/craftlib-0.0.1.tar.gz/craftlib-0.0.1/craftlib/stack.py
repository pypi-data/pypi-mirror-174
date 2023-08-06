# -*- coding: utf-8 -*-
"""
Created on Sat Oct  1 19:18:30 2022

@author: lidon
"""

from .vector import*
from .vectorADT import*

class stack(vector):
    def __init__(self,elements):
        super(stack,self).__init__(elements)
    
    # push e to the end of the stack
    def push(self,e):
        self.insert(self.size(),e)
    
    # pop e from the end of the stack
    # return the poped value
    def pop(self):
        return self.remove(self.size()-1)
    
    # return the top element
    def top(self):
        return self.elements[self.size()-1]



