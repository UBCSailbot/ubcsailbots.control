'''
Created on 2013-01-20

@author: DG
'''
def parse(filepath):
    numlist = list()   #list of values in file
    try:
        with open(filepath,'r'): pass  # test if file can be opened, else pass error
    except IOError:
        return None
    
    fo = open(filepath,'r') 
    for line in fo:
        nums = [int(n)for n in line.split()]  #split by whitespace and append to numlist
        numlist.append(nums)
        
    return numlist