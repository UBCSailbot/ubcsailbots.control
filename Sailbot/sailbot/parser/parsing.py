'''
Created on 2013-01-20

@author: DG
'''
def parse(filename):
    index = 0
    numlist = list()
    fo = open(filename, "r")
    
    for line in fo:
        nums = [int(n)for n in line.split()]
        numlist.append(nums)
        index+=1
        
    return numlist