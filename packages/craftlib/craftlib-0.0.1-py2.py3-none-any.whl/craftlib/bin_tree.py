# -*- coding: utf-8 -*-
"""
Created on Sun Oct  2 22:22:25 2022

@author: lidon
"""
from .queues import*
from .bin_node import*



class bin_tree:
    # size: tree size
    # root: tree root
    def __init__(self,size=0,root=None):
        self.size=size
        self.root=root
    
    # print the subtree start from x
    # this function should be hidden from the user
    def print_tree(self,x):
        rep=vector([])
        rep.append(x.data)
        if x.lc:
            rep.append(self.print_tree(x.lc))
        if x.rc:
            rep.append(self.print_tree(x.rc))
        return rep
    
    # print the tree
    def __repr__(self):
        if not self.root:
            return str(vector([]))
        rep=self.print_tree(self.root)
        return str(rep)
    
    # update the height of node x
    # return the updated height
    def update_height(self,x):
        x.height=1+max(stature(x.lc),stature(x.rc))
        return x.height
    
    # update height of x and its ancestors
    def update_height_above(self,x):
        while x:
            self.update_height(x)
            x=x.par
    
    # return size of the tree
    def size(self):
        return self.size
    
    # empty or not
    def empty(self):
        return not self.root
    
    # return root
    def root(self):
        return self.root
    
    # insert as root with data e
    # return root
    # WARNING: this will remove the full tree if there exists any!
    def insert_as_root(self,e):
        self.size=1
        self.root=bin_node(data=e)
        return self.root
    
    # insert e as the lc of node x
    def insert_as_lc(self,x,e):
        self.size=self.size+1
        x.insert_as_lc(e)
        self.update_height_above(x)
        return x.lc
    
    def insert_as_rc(self,x,e):
        self.size=self.size+1
        x.insert_as_rc(e)
        self.update_height_above(x)
        return x.rc
    
    # attach tree as left subtree of x
    # return position of x
    # WARNING: the original left subtree of x will be removed (if any)!
    def attach_as_lc(self,x,tree):
        x.lc=tree.root
        tree.root.par=x
        self.size=self.size+tree.size
        self.update_height_above(x)
        tree.root=None
        tree.size=0
        return x
    
    def attach_as_rc(self,x,tree):
        x.rc=tree.root
        tree.root.par=x
        self.size=self.size+tree.size
        self.update_height_above(x)
        tree.root=None
        tree.size=0
        return x
    
    # remove subtree with x as its root
    def remove(self,x):
        # if x is the root of the tree
        if isroot(x):
            self.size=0
            self.root=None
        else:
            if is_lc(x):
                x.par.lc=None
            else:
                x.par.rc=None
            self.update_height_above(x.par)
            x.par=None
                    
            
    
    # remove subtree with x as its root and transform it into an independent subtree
    def secede(self,x):
        # if x is the root, just return the tree itself
        if isroot(x):
            return self
        else:
            # cutoff pointer from the parents
            if is_lc(x):
                x.par.lc=None
            else:
                x.par.rc=None
            # renew heights
            self.update_height_above(x.par)
            # construct a new tree starting from x
            new_tree=bin_tree(size=x.size(),root=x)
            x.par=None
            
            # renew size of the old tree
            self.size=self.size-new_tree.size
            return new_tree
    
    # traverse by level
    # x a node in tree
    def trav_level(self,x,func):
        Q=queue([])
        Q.enqueue(x)
        while len(Q)!=0:
            node_now=Q.dequeue()
            func(node_now.data)
            if has_lc(node_now):
                Q.enqueue(node_now.lc)
            if has_rc(node_now):
                Q.enqueue(node_now.rc)

    # preorder traverse
    # x is a node in the tree
    def trav_pre(self,x,func):
        if not x:
            return
        func(x.data)
        self.trav_pre(x.lc,func)
        self.trav_pre(x.rc,func)
    
    # in order traverse
    # x is a node in the tree
    def trav_in(self,x,func):
        if not x:
            return
        self.trav_in(x.lc,func)
        func(x.data)
        self.trav_in(x.rc,func)
    
    # traverse in post order
    # x a node in the tree
    def trav_post(self,x,func):
        if not x:
            return
        self.trav_post(x.lc,func)
        self.trav_post(x.rc,func)
        func(x.data)
    
    
    
    # reload <=
    def __le__(self,other):
        return self.root and  other.root and self.root<=other.root
    
    # reload ==
    def __eq__(self,other):
        return self.root and other.root and self.root==other.root
    

