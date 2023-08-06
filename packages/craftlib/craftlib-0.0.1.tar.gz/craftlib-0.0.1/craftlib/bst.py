# -*- coding: utf-8 -*-
"""
Created on Sun Oct 16 22:31:05 2022

@author: lidon
"""
# implementation of binary searching tree
from .bin_tree import*
from .bin_node import*
from .vector import*
from .linked_list import*


class entry:
    def __init__(self,key=None,value=None):
        self.key=key
        self.value=value
        
    def __lt__(self,other):
        return self.key<other.key
    def __gt__(self,other):
        return self.key>other.key
    def __le__(self,other):
        return self.key<=other.key
    def __ge__(self,other):
        return self.key>=other.key
    def __eq__(self,other):
        return self.key==other.key
    def __ne__(self,other):
        return self.key!=other.key
    
    def __repr__(self):
        return str([self.key,self.value])


class bst(bin_tree):
    # search in the bst starting from v for key e
    # hot is auxillary var
    def search_in(self,v,e,hot):
        if (not v) or (v.data==e):
            return v,hot
        hot=v
        if e<v.data:
            return self.search_in(v.lc,e,hot)
        else:
            return self.search_in(v.rc,e,hot)
    
    # search for e in bst
    def search(self,e):
        v,hot=self.search_in(self.root,e,hot=None)
        return v
    
    # insert e
    def insert(self,e):
        v,hot=self.search_in(self.root,e,hot=None)
        # the node already exists
        if v:
            return v
        x=bin_node(data=e,par=hot)
        if e<hot.data:
            hot.lc=x
        else:
            hot.rc=x
        self.size=self.size+1
        self.update_height_above(x)
        # return the inserted node
        return x
    
    # remove node v
    def remove_at(self,v,hot):
        w=v
        succ=None
        if not has_lc(v):
            v=v.rc
            succ=v
        elif not has_rc(v):
            v=v.lc
            succ=v
        else:
            w=w.succ()
            v.data,w.data=swap(v.data,w.data)
            u=w.par
            if u==v:
                succ=w.rc
                u.rc=succ
            else:
                succ=w.rc
                u.lc=succ
        hot=w.par
        if succ:
            succ.par=hot
            if hot:
                if succ.data<hot.data:
                    hot.lc=succ
                else:
                    hot.rc=succ
        # return the successor
        return succ
    
    # remove data e
    def remove(self,e):
        v,hot=self.search_in(self.root,e,hot=None)
        self.remove_at(v,hot)
        self.size=self.size-1
        self.update_height_above(hot)
        return True
    
    
    
    
    