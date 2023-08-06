# -*- coding: utf-8 -*-
"""
Created on Mon Sep 26 22:33:02 2022

@author: lidon
"""

class list_node:
    def __init__(self,data=None,pred=None,succ=None):
        self.data=data
        self.pred=pred
        self.succ=succ
    def insert_as_pred(self,e):
        pass
    def insert_as_succ(self,e): 
        pass
    
class linked_list:
    #initialize the list with an array elements
    def __init__(self,elements=None):
        if elements==None:
            self.header=list_node()
            self.trailer=list_node()
            self.header.succ=self.trailer
            self.header.pred=None
            self.trailer.pred=self.header
            self.trailer.succ=None
            self.size=0
        else:
            # avoid using insert as last
            self.header=list_node()
            self.trailer=list_node()
            self.header.pred=None
            self.header.succ=self.trailer
            self.trailer.succ=None
            self.trailer.pred=self.header
            self.size=0
            for i in range(0,len(elements)):
                self.size=self.size+1
                self.trailer.insert_as_pred(elements[i])
            
        
    def __getitem__(self,key):
        p=self.first()
        while key>0:
            p=p.succ
            key=key-1
        return p.data
    
    def __setitem__(self,key,value):
        p=self.first()
        while key>0:
            p=p.succ
            key=key-1
        p.data=value
    
    def __len__(self):
        return self.size
    
    def __repr__(self):
        string=[]
        p=self.first()
        while p.succ!=None:
            string=[string]+[p.data]
            p=p.succ
        string=[string]
        #print(string)
        return str(string)
    
    # copy a linked list
    # from node to its n-1 th pred
    def copy(self,node=None,n=None):
        return self.copy_nodes(node=self.first(),n=self.size)
    
    # remove a node
    # return the removed value
    def remove(self,node):
        pass
        
    # remove all nodes
    # return number of nodes removed
    def clear(self):
        pass
    
    # copy n nodes starting from node to its n-1 succ
    # return a list consisting of these nodes
    def copy_nodes(self,node,n):
        pass
    
    # return size
    def size(self):
        pass
    
    # if it is empty (True if empty)
    def empty(self):
        return self.size<=0
    
    # return first node
    def first(self):
        return self.header.succ
    
    # return last node
    def last(self):
        return self.trailer.pred
    
    # return if node is valid (can be exposed to user)
    def valid(self,node):
        return node and (node!=self.header) and (node!=self.trailer)
    
    # return if ordered
    def disordered(self):
        pass
    
    # find data from linked list
    # from node to its n th pred
    # assume disordered
    def find(self,e,n=None,node=None):
        pass
    
    # search e and return the node <=e with largest rank
    # search e from n pred starting from node (from back to front)
    # assume ordered
    # if n and node are none, search from the whole list
    def search(self,e,n=None,node=None):
        pass
    
    # find the largest among node and its n-1 successors
    # if node and n None, search from whole list
    def select_max(self,node=None,n=None):
        if n==None and node==None:
            n=self.size
            node=self.header.succ
        p=node
        maximum=node
        for r in range(0,n):
            if maximum.data<p.data:
                maximum=p
            p=p.succ
        return maximum
    
    def insert_as_first(self,e):
        pass
    
    def insert_as_last(self,e):
        pass
    
    # insert e as the successor of node
    def insert_succ(self,node,e):
        pass
    
    # insert e as the pred of node
    def insert_pred(self,node,e):
        pass
    
    # remove a node
    def remove(self,node):
        pass
    
    # selection sort
    # sort n values starting from node
    def selection_sort(self,node=None,n=None):
        pass
    
    
    
    # insertion sort
    # sort n values starting from node
    def insertion_sort(self,node=None,n=None):
        pass
    
    # merge function
    # merge n nodes starting from p and m nodes starting from q
    # q may come from another linked list L
    def merge(self,p,n,L,q,m):
        pass
    
    # merge sort
    # sort n values starting from node
    def merge_sort(self,node=None,n=None):
        pass
    
    #sort
    def sort(self,func='selection',node=None,n=None):
        if func=='selection':
            self.selection_sort(node,n)
        elif func=='insertion':
            self.insertion_sort(node,n)
        elif func=='merge':
            self.merge_sort(node,n)
    
    #deduplicate
    # remove number of elements removed
    def deduplicate(self):
        pass
    
    # uniquify
    # return number of elements removed
    def uniquify(self):
        pass
    
    # reverse
    def reverse(self):
        pass
    
    # traverse
    def traverse(self,func):
        pass
    
    
    
    
    
    
    