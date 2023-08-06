# -*- coding: utf-8 -*-
"""
Created on Wed Oct 19 21:39:36 2022

@author: lidon
"""

from .bst import*
from .vector import*
from enum import Enum

def isprime(x):
    if x<=1:
        return False
    else:
        i=2
        for i in range(2,x):
            if x%i==0:
                return False
        return True

# generate n primes larger than c
def prime_gen(c,n):
    primes=vector([])
    # c even
    if c%2==0:
        i=3
        while len(primes)<n:
            if isprime(c+i):
                primes.append(c+i)
            i=i+2
        return primes
    # c odd
    if c%2==1:
        i=2
        while len(primes)<n:
            if isprime(c+i):
                primes.append(c+i)
            i=i+2
        return primes
        
# enumeration of lazy removal
class entry_status(Enum):
    UNUSED=1
    USED=2

class hash_table:
    # generate a hash table
    # length = c = 5 by default
    # don't use too large p, or it will take too long to 
    # select a prime number
    # p<1048576 is recommended
    def __init__(self,c=5,p=None):
        
        # if the user doesn't specify the prime we use
        if not p:
            primes=prime_gen(c+1000,1)
            p=primes[0]
        # M = length of hash table
        # N= number of queries
        self.M=p
        self.N=0
        # ht is the bucket
        # must consist of entries
        self.ht=vector([None for i in range(0,self.M)])
        self.lazy_removal=vector([entry_status.UNUSED for i in range(0,self.M)])
    
    # the default scheme to generate hash code
    def default_encoder(self,k):
        if type(k)==str:
            h=0
            for i in range(0,len(k)):
                # 37 is a magic number
                h=h+(37**i)*ord(k[i])
            return h%self.M
        else:
            return int(k)%self.M
    
    
    # define hash code
    def hash_code(self,k,encoder=None):
        # if don't specify an encoder, then use the default hash code generator
        if (not encoder):
            return self.default_encoder(k)
        else:
            return encoder(k)
    
    def size(self):
        return self.N
    
    # test if r is lazily removed
    def lazily_removed(self,r):
        if self.lazy_removal[r]==entry_status.USED:
            return True
        return False
    
    def mark_as_removed(self,r):
        self.lazy_removal[r]=entry_status.USED
        
        
    # probe linearly to prevent conflict
    def linear_probe(self,k):
        r=self.hash_code(k)
        while (self.ht[r] and self.ht[r].key!=k) or ((not self.ht[r]) and self.lazily_removed(r)):
            r=(r+1)%self.M
        # by ht[r] and lazy_removal[r] we know if searching is successful
        return r
    
    # get value by hashing
    def get(self,k):
        r=self.linear_probe(k)
        if self.ht[r]:
            return self.ht[r].value
        else:
            # if the key doesn't exist, deny the access
            return False
    
    # remove k
    def remove(self,k):
        r=self.linear_probe(k)
        if not self.ht[r]:
            # doesn't exist any value, removal denied
            return False
        self.ht[r]=None
        self.mark_as_removed(r)
        self.N=self.N-1
        # removal successful
        return True
    
    # find a free bucket
    def probe_for_free(self,k):
        r=self.hash_code(k)
        while self.ht[r]:
            r=(r+1)%self.M
        return r
    
    # insert
    # k: key
    # v: value
    def put(self,k,v):
        r=self.linear_probe(k)
        # can't insert same element
        if self.ht[r]:
            return False
        # find a free bucket
        r=self.probe_for_free(k)
        self.ht[r]=entry(k,v)
        self.N=self.N+1
        # if too many elements, rehash the table
        if 2*self.N>self.M:
            self.rehash()
        # insert successful
        return True
    
    # if too many elements, rehash the whole table
    def rehash(self):
        old_M=self.M
        old_N=self.N
        old_ht=self.ht
        primes=prime_gen(2*old_M,1)
        self.M=primes[0]
        self.N=0
        self.ht=[None for i in range(0,self.M)]
        self.lazy_removal=vector([entry_status.UNUSED for i in range(0,self.M)])
        for r in range(0,len(old_ht)):
            if old_ht[r]:
                self.put(old_ht[r].key,old_ht[r].value)


    # reload the [] operator
    # Allow user to visit directly by ht['Harry']
    def __getitem__(self,key):
        return self.get(key)
    
    # support directly setting an pair by the syntax
    # ht['Harry']='Potter'
    def __setitem__(self,key,value):
        self.put(key,value)
        
    # representation
    def __repr__(self):
        v=vector([])
        for i in range(0,self.M):
            if self.ht[i]:
                v.append(self.ht[i])
        return v.__repr__()
    
    
# implement bucket sort via hash table
# v is the input vector
def bucket_sort(v):
    c=len(v)
    p=prime_gen(c,1)[0]
    
    int_table=hash_table(c,p)
    for i in range(0,len(v)):
        int_table.put(v[i],v[i])
    
    v1=vector([])
    
    for j in range(0,int_table.M):
        if int_table.ht[j]:
            v1.append(int_table.ht[j].value)
    return v1

