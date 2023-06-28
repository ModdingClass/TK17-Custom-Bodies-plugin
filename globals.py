from collections import OrderedDict

# we need to keep track of extra custom added bones
global animSkeletonValuesExtra     
animSkeletonValuesExtra = OrderedDict()  #"tail_joint"

#def initialize(): 

class sharedGlobals:
    animSkeletonValues = []   
    #animSkeletonValuesExtra = OrderedDict() 
    animSkeletonParenting = OrderedDict() 


