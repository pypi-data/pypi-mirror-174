# -*- coding: utf-8 -*-
"""
Created on Sun Sep 25 11:29:16 2022

@author: lidon
"""

# Abstract Data Type of Vector

class vector:
    # arr should be a python list 
    def __init__(self,arr=None):
        self.elements=arr
        self.length=0
        if arr:
            self.length=len(arr)
    
    # reload the [] operator
    def __getitem__(self,key):
        return self.elements[key]
    
    # reload setitem function
    def __setitem__(self,key,value):
        self.elements[key]=value
    
    # reload the representation to print
    def __repr__(self):
        return self.elements.__repr__()
    
    # reload len(x)
    def __len__(self):
        return self.elements.__len__()
    
    def __add__(self,other):
        new_elements=self.elements+other.elements
        return vector(new_elements)
    
    # return length of the vector
    def size(self):
        pass
    
    # return if the vector is empty
    def empty(self):
        return not self.length>0
    
    # return if the vector is in order
    # return total number of disordered pairs
    def disordered(self):
        pass
    
    # find element e from [low,high] vector, return its index
    def find(self, e,low=None,high=None):
        pass
    
    # search e using binary search
    def bin_search(self,e,low=None,high=None):
        pass
    
    # search e from the vector, assume vector is ordered (find doesn't assume so)
    def search(self,e,func="bin_search",low=None,high=None):
        if func=="bin_search":
            return self.bin_search(e,low,high)
    
    # exchange elements
    def bubble(self,low=None,high=None):
        pass
    
    # bubble sort
    def bubble_sort(self,low=None,high=None):
        pass
    
    # return the maximum number
    def maximum(self,low=None,high=None):
        pass
    
    # selection sort
    def selection_sort(self,low=None,high=None):
        pass
    
    # merge, used for merge sort
    def merge(self,low,mid,high):
        pass
    
    # merge sort
    def merge_sort(self,low=None,high=None):
        pass
    
    # line sweep
    def partition(self,low=None,high=None):
        pass
    
    # quick sort
    def quick_sort(self,low=None,high=None):
        pass
    
    # heap sort
    def heap_sort(self,low=None,high=None):
        pass
    
    # additionally define copy, to match the syntax of python
    # deep copy, instead of setting the pointer
    def copy(self):
        pass
    
    #remove element in index r
    def remove(self,r):
        pass
    
    # remove elements in [low,high)
    def remove_index(self,low,high):
        pass
    
    # insert element e into position r
    def insert(self,r,e):
        pass
    
    # insert element e at the tail of the vector
    def append(self,e):
        index=self.insert(self.length,e)
        return index
    
    # sort elements in [low,high)
    # if don't specify low and high, sort the whole vector
    def sort(self,func="quick",low=None,high=None):
        if func=="bubble":
            return self.bubble_sort(low,high)
        elif func=="selection":
            return self.selection_sort(low,high)
        elif func=="merge":
            return self.merge_sort(low,high)
        elif func=="heap":
            return self.heap_sort(low,high)
        elif func=="quick":
            return self.quick_sort(low,high)
    
    # unsort elements in [low,high) by permuting
    # if don't specify low and high, unsort the whole vector
    def unsort(self,low=None,high=None):
        pass
    
    # remove repeating elements
    # assume vector unsorted
    def deduplicate(self):
        pass
    
    # remove repeating elements
    # assume vector sorted
    def uniquify(self):
        pass
    
    # traverse the whole vector
    # apply func on every element in the vector
    def traverse(self,func):
        pass
    
    
    
    
    
    
    
    