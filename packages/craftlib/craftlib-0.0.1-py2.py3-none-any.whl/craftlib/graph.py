# -*- coding: utf-8 -*-
"""
Created on Thu Oct  6 21:49:38 2022

@author: lidon
"""

from enum import Enum
import math
from tinylib.vector import*
from tinylib.queues import*
from tinylib.stack import*
import random

class v_status(Enum):
    UNDISCOVERED=1
    DISCOVERED=2
    VISITED=3

class e_status(Enum):
    UNDETERMINED=0
    TREE=1
    CROSS=2
    FORWARD=3
    BACKWARD=4


class vertex:
    def __init__(self,data=None,in_deg=0,out_deg=0,status=None):
        self.data=data
        self.in_deg=in_deg
        self.out_deg=out_deg
        self.status=status
        if not self.status:
            self.status=v_status.UNDISCOVERED
        # time stamp
        self.d_time=-1
        self.f_time=-1
        # used in traverse tree
        self.parent=-1
        self.priority=math.inf
    def __repr__(self):
        return str(self.data)

class edge:
    def __init__(self,data=None,weight=1,status=None):
        self.data=data
        self.weight=weight
        self.status=status
        if not status:
            self.status=e_status.UNDETERMINED
    
    def copy(self):
        return edge(self.data,self.weight,self.status)

# e set and v set should be vector
# v set are vertex in graph
# e set is the adj matrix!
class graph:
    def __init__(self,v_set=vector([]),e_set=vector([])):
        self.v_set=v_set
        self.e_set=e_set
        # n and e are vertex num and edge num
        self.n=len(v_set)
        self.e=0
        if self.e_set and len(v_set)>1:
            for i in e_set:
                for j in i:
                    if j:
                        self.e=self.e+1
        
        # handle the case when have v set but no e set
        if v_set and not e_set:
            self.e_set=vector([vector([None for i in range(0,self.n)]) for j in range(0,self.n)])
    
    # return adj matrix
    def __repr__(self):
        mat=vector([])
        if self.n==1:
            mat.append(0)
            return str(mat)
        else:
            for i in range(0,len(self.e_set)):
                mat.append(vector([]))
                for j in range(0,len(self.e_set)):
                    if self.e_set[i][j]:
                        mat[i].append(self.e_set[i][j].weight)
                    else:
                        mat[i].append(0)
        return str(mat)
                        
                        
    
    
    # look up ith vertex
    def vertex(self,i):
        return self.v_set[i].data
    
    # in degree
    def in_degree(self,i):
        return self.v_set[i].in_deg
    
    # out degree
    def out_degree(self,i):
        return self.v_set[i].out_deg
    
    # if there exists an edge from i to j
    def exists(self,i,j):
        return i>=0 and i<self.n and j>=0 and self.e_set[i][j]
    
    # if there exists edge from i to j/from j to i
    def adjacent(self,i,j):
        return self.e_set[i][j] or self.e_set[j][i]
    
    # insert a vertex into the graph
    # return its index
    def insert_vertex(self,vertex):
        for j in range(0,self.n):
            self.e_set[j].append(None)
        self.n=self.n+1
        self.e_set.append(vector([None for k in range(0,self.n)]))
        return self.v_set.append(vertex)
    
    # remove ith vertex
    def remove_vertex(self,i):
        # delete out deg
        for j in range(0,self.n):
            if self.exists(i,j):
                self.v_set[j].in_deg=self.v_set[j].in_deg-1
        # remove the ith row of the matrix
        self.e_set.remove(i)
        # reduce the vertex number
        self.n=self.n-1
        # delete in deg
        for j in range(0,self.n):
            if self.e_set[j][i]:
                self.v_set[j].out_deg=self.v_set[j].out_deg-1
            self.e_set[j].remove(i)
        # return the deleted vertex
        return self.v_set.remove(i)
    
    # query the status of edge between i and j
    # otherwise return None (if no edge)
    def e_status(self,i,j):
        if e_set[i][j]:
            return e_set[i][j].status
        return None
    
    # query the data of edge between i and j
    # return None if no edge
    def e_data(self,i,j):
        if e_set[i][j]:
            return e_set[i][j].data
        return None
    
    # return weight of edge between i and j
    def weight(self,i,j):
        return e_set[i][j].weight
    
    # insert an edge
    # will automatically cover the old edge (if exists any)!
    def insert_edge(self,edge,i,j):
        self.e_set[i][j]=edge
        self.e=self.e+1
        self.v_set[i].out_deg=self.v_set[i].out_deg+1
        self.v_set[j].in_deg=self.v_set[j].in_deg+1
    
    # remove an edge
    # return the rmoved edge
    def remove_edge(self,i,j):
        removed=self.e_set[i][j].copy()
        self.e_set[i][j]=None
        self.e=self.e-1
        self.v_set[i].out_deg=self.v_set[i].out_deg-1
        self.v_set[j].in_deg=self.v_set[j].in_deg-1
        return removed
    
    # return the next neighbor of i wrt j
    # if does not exist, return -1
    def next_neighbor(self,i,j):
        j=j-1
        while j>-1 and not self.exists(i,j):
            j=j-1
        return j
    
    # return next adjacent of i wrt j (ignore direction)
    # if doesn't exists, return -1
    def next_adjacent(self,i,j):
        j=j-1
        while j>-1 and not (self.exists(i,j) or self.exists(j,i)):
            j=j-1
        return j
    
    # return first neighbor of i
    def first_neighbor(self,i):
        return self.next_neighbor(i,self.n)
    
    def first_adjacent(self,i):
        return self.next_adjacent(i,self.n)
    
    def d_time(self,i):
        return self.v_set[i].d_time
    
    def f_time(self,i):
        return self.v_set[i].f_time
    
    def parent(self,i):
        return self.v_set[i].parent
    
    def priority(self,i):
        return self.v_set[i].priority
    
    # reset all vertex/edge status after traversing
    def reset(self):
        for i in range(0,self.n):
            self.v_set[i].status=v_status.UNDISCOVERED
            self.v_set[i].d_time=-1
            self.v_set[i].f_time=-1
            self.v_set[i].parent=-1
            self.v_set[i].priority=-1
            for j in range(0,self.n):
                if self.exists(i,j):
                    self.e_set[i][j].status=e_status.UNDETERMINED
    
    # breadth first search algorithm
    # start from i-th vertex
    # func is the operation to the vertex
    
    # bfs in a sub-branch
    def bfs_branch(self,i,func=print):
        Q=queue()
        self.v_set[i].status=v_status.DISCOVERED
        Q.enqueue(i)
        while Q:
            v=Q.dequeue()
            func(self.v_set[v])
            self.v_set[v].status=v_status.VISITED
            u=self.first_neighbor(v)
            while u>-1:
                if self.v_set[u].status==v_status.UNDISCOVERED:
                    self.v_set[u].status=v_status.DISCOVERED
                    Q.enqueue(u)
                u=self.next_neighbor(v,u)
    
    # bfs through all sub-branches
    def bfs(self,i,func=print):
        self.reset()
        self.bfs_branch(i,func)
        for v in range(0,self.n):
            if self.v_set[v].status==v_status.UNDISCOVERED:
                self.bfs_branch(v,func)
    
    # depth first traverse algorithm
    # start from i-th vertex, apply func() to all visited vertex
    def dfs_branch(self,i,func=print):
        if self.v_set[i].status!=v_status.UNDISCOVERED:
            return
        else:
            func(self.v_set[i])
            self.v_set[i].status=v_status.DISCOVERED
            j=self.first_neighbor(i)
            while j>-1:
                if self.v_set[j].status==v_status.UNDISCOVERED:
                    self.dfs_branch(j,func)
                j=self.next_neighbor(i,j)
            self.v_set[i].status=v_status.VISITED
    
    # dfs through all sub branches
    def dfs(self,i,func=print):
        self.reset()
        self.dfs_branch(i,func)
        for v in range(0,self.n):
            if self.v_set[v].status==v_status.UNDISCOVERED:
                self.dfs_branch(v,func)
            
    
    # dfs for topological sorting
    # kept hidden from user
    def topo_dfs_branch(self,i,s=stack([])):
        if self.v_set[i].status!=v_status.UNDISCOVERED:
            return s
        else:
            self.v_set[i].status=v_status.DISCOVERED
            j=self.first_neighbor(i)
            while j>-1:
                if self.v_set[j].status==v_status.UNDISCOVERED:
                    s=self.topo_dfs_branch(j,s)
                j=self.next_neighbor(i,j)
            self.v_set[i].status=v_status.VISITED
            s.push(i)
            return s
    
    # topological sort
    def t_sort(self,i=0):
        self.reset()
        s=stack([])
        s=self.topo_dfs_branch(i,s)
        for v in range(0,self.n):
            if self.v_set[v].status==v_status.UNDISCOVERED:
                s=self.topo_dfs_branch(v,s)
        
        sort=vector([])
        while s:
            sort.append(s.pop())
        return sort
    
    # priority first search in a branch
    # priority_updater is a function to update the priority of each node
    def pfs_branch(self,i,priority_updater):
        if self.v_set[i].status==v_status.VISITED:
            return
        
        # add the starting point into the pfs tree
        self.v_set[i].priority=0
        self.v_set[i].parent=-1
        self.v_set[i].status=v_status.VISITED
        
        
        while 1:
            w=self.first_neighbor(i)
            while w>-1:
                # enumerate all neighbors, update their priority
                self.priority_updater(i,w)
                w=self.next_neighbor(i,w)
                
            # find point with tallest priority
            shortest=math.inf
            for w in range(0,self.n):
                if self.v_set[w].status==v_status.UNDISCOVERED:
                    if shortest>self.v_set[w].priority:
                        shortest=self.v_set[w].priority
                        i=w
            if self.v_set[i].status==v_status.VISITED:
                break
            self.v_set[i].status=v_status.VISITED
            self.e_set[self.v_set[i].parent][i].status=e_status.TREE
    
    # minimal spanning tree use prim
    # start from i
    # edges in MST will have the status TREE
    # assume undirected graph
    def mst(self,i):
        self.reset()
        new_v=vector([i])
        self.v_set[i].status=v_status.VISITED
        while len(new_v)<self.n:
            start=new_v[0]
            s=new_v[0]
            short=math.inf
            for u in new_v:
                w=self.first_adjacent(u)
                while w>-1:
                    if self.exists(u,w):
                        edg=self.e_set[u][w]
                    else:
                        edg=self.e_set[w][u]
                    if self.v_set[w].status!=v_status.VISITED and edg.weight<short:
                        start=u
                        s=w
                        short=edg.weight
                        #edg.status=e_status.TREE
                    w=self.next_adjacent(u,w)
            self.v_set[s].status=v_status.VISITED
            new_v.append(s)
            if self.exists(start,s):
                self.e_set[start][s].status=e_status.TREE
            else:
                self.e_set[s][start].status=e_status.TREE
    
    # find shortest path tree wrt i'
    # assume undirected graph
    # edges in SPT will have status TREE
    def spt(self,i): 
        self.reset()
        new_v=vector([i])
        self.v_set[i].status=v_status.VISITED
        self.v_set[i].priority=0
        while len(new_v)<self.n:
            start=new_v[0]
            s=new_v[0]
            short=math.inf
            for u in new_v:
                w=self.first_adjacent(u)
                while w>-1:
                    if self.exists(u,w):
                        edg=self.e_set[u][w]
                    else:
                        edg=self.e_set[w][u]
                    if self.v_set[w].status!=v_status.VISITED and self.v_set[u].priority+edg.weight<short:
                        start=u
                        s=w
                        short=self.v_set[start].priority+edg.weight
                        #edg.status=e_status.TREE
                    w=self.next_adjacent(u,w)
            self.v_set[s].status=v_status.VISITED
            
            new_v.append(s)
            if self.exists(start,s):
                self.e_set[start][s].status=e_status.TREE
                edge_weight=self.e_set[start][s].weight
            else:
                self.e_set[s][start].status=e_status.TREE
                edge_weight=self.e_set[s][start].weight
            self.v_set[s].priority=self.v_set[start].priority+edge_weight
    
    # construct a derived graph that only includes edges with TREE status
    # NOTE: this will automatically delete the original edges that 
    # are not members of the tree
    def derive_tree(self):
        #new_v=self.v_set.copy()
        #new_e=self.e_set.copy()
        #new_g=graph(new_v,new_e)
        for i in range(0,self.n):
            for j in range(0,self.n):
                if self.e_set[i][j]:
                    if self.e_set[i][j].status!=e_status.TREE:
                        self.remove_edge(i,j)
                if self.e_set[j][i]:
                    if self.e_set[j][i].status!=e_status.TREE:
                        self.remove_edge(j,i)
                        
    
        
    # priority first search starting from i
    def pfs(self,i,priority_updater):
        self.reset()
        self.pfs_branch(i,priority_updater)
        for i in range(0,self.n):
            self.pfs_branch(i,priority_updater)
    
    
    
    
    # priority updater of prim
    # update v wrt u
    def prim_pu(self,u,v):
        if self.v_set[v].status==v_status.UNDISCOVERED:
            self.v_set[v].priority=self.e_set[u][v].weight
            self.v_set[v].parent=u
    
                        
            
    
        
        
        
            


