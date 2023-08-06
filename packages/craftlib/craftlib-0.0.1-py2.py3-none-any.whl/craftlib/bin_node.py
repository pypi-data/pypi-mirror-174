# -*- coding: utf-8 -*-
"""
Created on Sun Oct  2 21:34:53 2022

@author: lidon
"""
from enum import Enum

class COLOR(Enum):
    RED=1
    BLUE=2

# return height of node p
# if null tree, return -1
def stature(p):
    if p:
        return p.height
    else:
        return -1

# some useful macros
def is_root(x):
    return not x.par
def is_lc(x):
    return (not is_root(x)) and (x==x.par.lc)
def is_rc(x):
    return (not is_root(x)) and (x==x.par.rc)
def has_par(x):
    return not is_root(x)
def has_lc(x):
    return x.lc
def has_rc(x):
    return x.rc
def has_child(x):
    return x.lc or x.rc
# if has both children
def has_children(x):
    return x.lc and x.rc
def is_leaf(x):
    return not x.has_child
# return the sibling of x
def sibling(x):
    if is_lc(x):
        return x.par.rc
    else:
        return x.par.lc
def uncle(x):
    if is_lc(x.par):
        return x.par.par.rc
    else:
        return x.par.par.lc
# return pointer from its parent
def from_par_to(x):
    if is_root(x):
        return x
    else:
        if is_lc(x):
            return x.par.lc
        else:
            return x.par.rc



class bin_node:
    # lc,rc: red children, left children
    # pt: parent
    # npl: null path length
    # color: red or black
    # definition of height: height starts from 0, any single node has height 0, null tree
    # has height 1
    # height of a node is the depth of the subtree starting from this node
    def __init__(self,data=None,par=None,lc=None,rc=None,height=0,npl=1,color=COLOR.RED):
        self.data=data
        self.par=par
        self.lc=lc
        self.rc=rc
        self.height=height
        self.color=color
    
    def __repr__(self):
        return str(self.data)
    
    # return number of all offsprings
    def size(self):
        x=self.lc
        y=self.rc
        # x and y are not null
        if x and y:
            return 1+x.size()+y.size()
        # x not null, y null
        if x and not y:
            return 1+x.size()
        # x null, y not null
        if not x and y:
            return 1+y.size()
        else:
            return 1
    
    # insert as left children, return the new children
    def insert_as_lc(self,e):
        child = bin_node(data=e,par=self)
        self.lc=child
        return child
    
    # insert as right children, return the new children
    def insert_as_rc(self,e):
        child=bin_node(data=e,par=self)
        self.rc=child
        return child
    
    # successor in trave in
    def succ(self):
        s=self
        if self.rc:
            s=self.rc
            while has_lc(s):
                s=s.lc
        else:
            while is_rc(s):
                s=s.par
            s=s.par
        return s
        
    
    # traverse wrt level
    def trav_level(self,func):
        pass
    
    # pre traverse
    def trav_pre(self,func):
        pass
    
    # In traverse
    def trav_in(self,func):
        pass
    
    # post traverse
    def trav_post(self,func):
        pass
    
    
    # reload <=
    def __le__(self,other):
        return self.data<=other.data
    
    # reload ==
    def __eq__(self,other):
        return self.data==other.data
    
  
    
    