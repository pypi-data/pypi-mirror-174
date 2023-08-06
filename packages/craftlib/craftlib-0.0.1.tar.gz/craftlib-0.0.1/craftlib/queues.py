# -*- coding: utf-8 -*-
"""
Created on Sun Oct  2 21:28:02 2022

@author: lidon
"""

from .vector import*
from .linked_list import*


class queue(linked_list):
    # insert e to the last
    def enqueue(self,e):
        self.insert_as_last(e)
        
    # remove the first one
    def dequeue(self):
        return self.remove(self.first())
    def front(self):
        return self.first().data