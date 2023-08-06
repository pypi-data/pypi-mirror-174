# -*- coding: utf-8 -*-
"""
Created on Mon Oct 17 21:36:48 2022

@author: lidon
"""
# implementation of AVL tree
from .bst import*

# some useful APIs
def balanced(v):
    return stature(v.lc)==stature(v.rc)
def balance_factor(v):
    return stature(v.lc)-stature(v.rc)
def AVL_balanced(v):
    return (balance_factor(v)>-2) and (balance_factor(v)<2)
# return taller child of v
def taller_child(v):
    if stature(v.lc)>stature(v.rc):
        return v.lc
    if stature(v.lc)<stature(v.rc):
        return v.rc
    # if same height, return the child that is at the same side with its father
    if is_lc(v):
        return v.lc
    else:
        return v.rc


class AVL_tree(bst):
    # v are nodes and t are sub trees
    # order them in in order: t0 v0 t1 v1 t2 v2 t3
    def connect_34(self,v0,v1,v2,t0,t1,t2,t3):
        v0.lc=t0
        if t0:
            t0.par=v0
        v0.rc=t1
        if t1:
            t1.par=v1
        self.update_height(v0)
        v2.lc=t2
        v2.rc=t3
        if t2:
            t2.par=v2
        if t3:
            t3.par=v2
        self.update_height(v2)
        v1.lc=v0
        v1.rc=v2
        v0.par=v1
        v2.par=v1
        self.update_height(v1)
        return v1
    
    # rotate at node v use connect34    
    def rotate(self,v):
        p=v.par
        g=p.var
        # zig
        if is_lc(p):
            # zig zig
            if is_lc(v):
                p.par=g.par
                if g.par:
                    if p.data<g.par.data:
                        g.par.lc=p
                    else:
                        g.par.rc=p
                return self.connect_34(v,p,g,v.lc,v.rc,p.rc,g.rc)
            # zig zag
            if is_rc(v):
                v.par=g.par
                if g.par:
                    if v.data<g.par.data:
                        g.par.lc=v
                    else:
                        g.par.rc=v
                return self.connect_34(p,v,g,p.lc,v.lc,v.rc,g.rc)
        # zag
        if is_rc(p):
            # zag zag
            if is_rc(v):
                p.par=g.par
                if g.par:
                    if p.data<g.par.data:
                        g.par.lc=p
                    else:
                        g.par.rc=p
                return self.connect34(g,p,v,g.lc,p.lc,v.lc,v.rc)
            # zag zig
            if is_lc(v):
                v.par=g.par
                if g.par:
                    if v.data<g.par.data:
                        g.par.lc=v
                    else:
                        g.par.rc=v
                return self.connect34(g,v,p,g.lc,v.lc,v.rc,p.rc)
    
    # insert e into the tree, and automatically balance the tree
    def insert(self,e):
        v,hot=self.search_in(self.root,e,hot=None)
        # make sure the value doesn't exist
        if v:
            return v
        
        # insert the node
        new_v=bin_node(data=e)
        new_v.par=hot
        if hot:
            if e<hot.data:
                hot.lc=new_v
            else:
                hot.rc=new_v
        self.size=self.size+1
        #self.update_height_above(hot)
        # start from v's parent, check if each of its ancestor is unbalanced
        g=hot
        while g:
            # if g unbalanced, rebalance it by rotating
            if not AVL_balanced(g):
                if is_root(g):
                    g=self.rotate(taller_child(taller_child(g)))
                else:
                    if is_lc(g):
                        g.par.lc=self.rotate(taller_child(taller_child(g)))
                    else:
                        g.par.rc=self.rotate(taller_child(taller_child(g)))
                # if g balanced, all its ancestors will be balanced
                break
            else:
                self.update_height(g)
            g=g.par
        
        return new_v
    
    # return true if success, false otherwise
    def remove(self,e):
        v,hot=self.search_in(self.root,e,hot=None)
        # if v doesn't exist
        if not v:
            return False
        self.remove_at(v,hot)
        self.size=self.size-1
        g=hot
        # from hot, check one by one to above and rebalance by rotating
        while g:
            if not AVL_balanced(g):
                if is_root(g):
                    g=self.rotate(taller_child(taller_child(g)))
                else:
                    if is_lc(g):
                        g.par.lc=self.rotate(taller_child(taller_child(g)))
                    else:
                        g.par.rc=self.rotate(taller_child(taller_child(g)))
                # unbalance will propagate in deletion case, so continue searching
            self.update_height(g)
            g=g.par
        # removal successful
        return True
            
        
            