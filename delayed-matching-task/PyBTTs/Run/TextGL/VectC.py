'''
Created on 2014/12/01

@author: admin
'''

class VectC(object):
    '''
    classdocs
    '''
    def __init__(self, x,y,m):
        '''
        Constructor
        '''
        self.x = x
        self.y = y
        self.m = ord(m) # code
    
    def getXOpenGL(self):
        return self.x
    
    def getYOpenGL(self):
        return -self.y