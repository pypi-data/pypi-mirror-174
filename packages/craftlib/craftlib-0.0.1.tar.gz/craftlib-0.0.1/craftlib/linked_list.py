# -*- coding: utf-8 -*-
"""
Created on Tue Sep 27 20:37:27 2022

@author: lidon
"""

from .listADT import*
import random
from .vector import*

# implement find()
def find(self,e,n=None,node=None):
    if n==None and node==None:
        n=self.size
        node=self.trailer
    while n>0:
        node=node.pred
        if e==node.data:
            return node
        n=n-1
    # find failed
    return None
# bind to linked list
linked_list.find=find

# implement insert_as_pred()
# insert e as the pred
def insert_as_pred(self,e):
    new_node=list_node(data=e,pred=self.pred,succ=self)
    self.pred.succ=new_node
    self.pred=new_node
    # return the pointer of the new node
    return self.pred
# bind to list_node
list_node.insert_as_pred=insert_as_pred

# implement insert as succ()
# insert e as the succ
def insert_as_succ(self,e):
    new_node=list_node(data=e,pred=self,succ=self.succ)
    self.succ.pred=new_node
    self.succ=new_node
    # return the pointer of the new node
    return self.succ
# bind to list_node
list_node.insert_as_succ=insert_as_succ

# implement insert_as_first
def insert_as_first(self,e):
    self.size=self.size+1
    return self.header.insert_as_succ(e)
# bind to linked_list
linked_list.insert_as_first=insert_as_first

# implement insert_as_last
def insert_as_last(self,e):
    self.size=self.size+1
    return self.trailer.insert_as_pred(e)
# bind to linked_list
linked_list.insert_as_last=insert_as_last

# implement insert_succ
def insert_succ(self,node,e):
    self.size=self.size+1
    return node.insert_as_succ(e)
# bind to linked list
linked_list.insert_succ=insert_succ

# implement insert_pred
def insert_pred(self,node,e):
    self.size=self.size+1
    return node.insert_as_pred(e)
# bind to linked list
linked_list.insert_pred=insert_pred

# implement copy_nodes()
def copy_nodes(self,node,n):
    new_list=linked_list()
    while n>0:
        new_list.insert_as_last(node.data)
        node=node.succ
        n=n-1
    return new_list
# bind to linked_list
linked_list.copy_nodes=copy_nodes


# implement remove()
def remove(self,node):
    backup=node.data
    node.pred.succ=node.succ
    node.succ.pred=node.pred
    del node
    self.size=self.size-1
    return backup
# bind to linked_list
linked_list.remove=remove

# implement clear()
# remove all nodes apart from header and trailer
# return number of nodes removed
def clear(self):
    old_size=self.size
    while self.size>0:
        self.remove(self.header.succ)
        #self.size=self.size-1
    return old_size
# bind to linked_list
linked_list.clear=clear

# implement deduplicate()
# return number of elements removed
def deduplicate(self):
    old_size=self.size
    # trivial linked list
    if self.size<2:
        return None
    # start from 1th element
    p=self.header.succ.succ
    index=1
    while p.succ!=None:
        if self.find(p.data,index,p):
            tmp=p.succ
            self.remove(p)
            p=tmp
        else:
            index=index+1
            p=p.succ
    return old_size-self.size
# bind to linked_list
linked_list.deduplicate=deduplicate 

# implement traverse
def traverse(self,func):
    p=self.header.succ
    while p.succ!=None:
        func(p.data)
        p=p.succ
# bind to linked_list
linked_list.traverse=traverse

# implement uniquify
# return number of elements removed
def uniquify(self):
    old_size=self.size
    p=self.header.succ
    q=p
    while p.succ!=self.trailer:
        q=p.succ
        if p.data!=q.data:
            p=q
        else:
            self.remove(q)
            q=p.succ
    return old_size-self.size
# bind to linked list
linked_list.uniquify=uniquify

# implement search
# note it returns node <=e with largest rank
def search(self,e,n=None,node=None):
    if n==None and node==None:
        n=self.size
        node=self.trailer
    p=node.pred
    while n>0:
        if p.data<=e:
            return p
        else:
            p=p.pred
            n=n-1
    return None
# bind to linked list
linked_list.search=search

#implement insertion sort
# complexity: O(n^2)
def insertion_sort(self,node=None,n=None):
    if node==None and n==None:
        node=self.header.succ
        n=self.size
    p=node.succ
    for r in range(1,n):
        if self.search(p.data,r,p)==None:
            self.insert_pred(node,p.data)
            p=p.succ
            self.remove(p.pred)
        else:
            self.insert_succ(self.search(p.data,r,p),p.data)
            p=p.succ
            self.remove(p.pred)
# bind to linked list
linked_list.insertion_sort=insertion_sort

# implement selection sort
# complexity: O(n^2)
def selection_sort(self,node=None,n=None):
    if node==None and n==None:
        node=self.header.succ
        n=self.size
        
    p=node
    tmp_head=p.pred
    tmp_tail=p
    for i in range(0,n):
        tmp_tail=tmp_tail.succ
    while n>1:
        maximum=self.select_max(tmp_head.succ,n)
        self.insert_pred(tmp_tail,self.remove(maximum))
        tmp_tail=tmp_tail.pred
        n=n-1
# bind to linked list
linked_list.selection_sort=selection_sort

# implement merge()
def merge(self,p,n,q,m):
    
    
    pp=p.pred
    qq=q.pred
    while m>0:
        if n>0 and p.data<=q.data:
            p=p.succ
            if q==p:
                break
            n=n-1
        else:
            m=m-1
            # can't change the relative position of p and q! (i.e. can't add new pred of p and q)
            # otherwise, the upper level p and q will also be changed
            p.data,q.data=swap(p.data,q.data)
            tmp=q.data
            q=q.succ
            self.remove(q.pred)
            self.insert_succ(p,tmp)
            p=p.succ
            
    p=pp.succ
# bind to linked list
linked_list.merge=merge


# implement merge sort
def merge_sort(self,node=None,n=None):
    if node==None and n==None:
        node=self.header.succ
        n=self.size
    if n<2:
        return 
    p=node
    m=int(n/2)
    q=p
    for i in range(0,m):
        q=q.succ
    
    self.merge_sort(p,m)
    self.merge_sort(q,n-m)
    self.merge(p,m,q,n-m)
# bind to linked list
linked_list.merge_sort=merge_sort



    