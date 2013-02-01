'''
Created on 2013-01-20

@author: DG
'''
def parse(filepath):
    index = 0
    numlist = list()
    try:
        with open(filepath,'r') as fo: pass
    except IOError as e:
        return None
    
    fo = open(filepath,'r')
    for line in fo:
        nums = [int(n)for n in line.split()]
        numlist.append(nums)
        index+=1
        
    return numlist