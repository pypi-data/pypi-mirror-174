# -*- coding: utf-8 -*-
"""
Created on Wed Oct 26 21:01:29 2022

@author: lidon
"""
from .vector import*
# implementation of priority queue

# some convenient functions
# heap implemented by complete binary tree

# return if i smaller than n and larger than -1
def legal(n,i):
    return (i>-1) and (i<n)
# parent node of pq[i]
def parent(i):
    return int((i-1)/2)
# return the last internal node
def last_internal(n):
    return parent(n-1)
# left child of i
def lchild(i):
    return 2*i+1
# right child of i
def rchild(i):
    return 2*i+2
# if i has parent
def parent_valid(i):
    return i>0
# if i has lchild
def lchild_valid(n,i):
    return legal(n,lchild(i))
# if i has rchild
def rchild_valid(n,i):
    return legal(n,rchild(i))
# return the bigger
# if equal, return the first one
def bigger(prior_queue,i,j):
    if prior_queue[i]<prior_queue[j]:
        return j
    else:
        return i
# find largest among i and its children
def boss(prior_queue,n,i):
    if rchild_valid(n,i):
        return bigger(prior_queue,bigger(prior_queue,i,lchild(i)),rchild(i))
    else:
        if lchild_valid(n,i):
            return bigger(prior_queue,i,lchild(i))
        else:
            return i
    
# priority queue
# implemented by binary heap
class priority_queue(vector):
    def __init__(self,arr=None):
        self.elements=arr
        self.length=0
        if arr:
            self.length=len(arr)
            self.heapify()
    
    # return max (i.e. the first element)
    def get_max(self):
        return self.elements[0]
    
    # percolate the element in rank r to the up
    def percolate_up(self,r):
        while parent_valid(r) and self.elements[r]>=self.elements[parent(r)]:
            self.elements[r],self.elements[parent(r)]=swap(self.elements[r],self.elements[parent(r)])
            r=parent(r)
        # return final position
        return r
    
    # private API, not exposed to users
    # if the user wants to insert value, must use insert()
    def append(self,e):
        self.elements.append(e)
        self.length+=1
    
    # insert value e
    def insert(self,e):
        self.append(e)
        self.percolate_up(self.length-1)
    
    # percolate the value to down
    def percolate_down(self,r):
        while r!=boss(self.elements,self.length,r):
            k=boss(self.elements,self.length,r)
            self.elements[r],self.elements[k]=swap(self.elements[r],self.elements[k])
            r=k
        return r
    
    # delete maximum
    def del_max(self):
        maximum=self.elements[0]
        self.elements[0]=self.elements[self.length-1]
        self.remove(self.length-1)
        self.percolate_down(0)
        return maximum
    
    # change the vector into a heap
    # heapify using Floyd algorithm
    def heapify(self):
        # all leaf nodes are themselves a hep
        i=last_internal(self.length) 
        while legal(self.length,i):
            self.percolate_down(i)
            i=i-1

# implement heap sort
def heap_sort(v):
    h=priority_queue(v)
    last=v.length-1
    while not h.empty():
        v[last]=h.del_max()
        last=last-1
    return v
        
    
    