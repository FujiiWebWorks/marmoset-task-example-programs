'''
Created on 2014/12/01

@author: admin
'''
from pyglet.gl import *
from VectC import VectC
from VectOneChar import VectOneChar
#from __builtin__ import True

class TextOpenGLObj(object):
    def __init__(self, pos=[0,0]):
        '''
        Constructor
        '''
        self.isAutoDraw = True
        self.pos = pos
        self.posA = [0.0,0.0]
        self.sizeOfChar = 0.04
        self.sizeOfCharX = 0.7
        self.sizeOfCharY = 0.9
        self.scaleCX = self.sizeOfChar * self.sizeOfCharX
        self.scaleCY = self.sizeOfChar * self.sizeOfCharY
        self.text = '012'
        
        self.vcspace = VectOneChar(' ',[VectC(0.0,0.0,'n')])
        self.vcperiod = VectOneChar('.',[
                    VectC(0.0,  0.0,'l'),
                    VectC(0.02 ,0.0,'c'),
                    VectC(0.02 ,0.02,'c'),
                    VectC(0.0 , 0.02,'c'),
                    VectC(0.0,0.0,'e'),
                    ]);
        self.vc0_9 = [ VectOneChar('0',[
                            VectC( 0.0,-1.0,'l'),
                            VectC( 0.0, 0.0,'c'),
                            VectC( 1.0, 0.0,'c'),
                            VectC( 1.0,-1.0,'c'),
                            VectC( 0.0,-1.0,'e') ]),
                       VectOneChar('1',[
                            VectC( 0.8,-0.8,'l'),
                            VectC( 1.0,-1.0,'c'),
                            VectC( 1.0, 0.0,'e') ]),
                       VectOneChar('2',[
                            VectC( 0.0,-1.0,'l'),
                            VectC( 1.0,-1.0,'c'),
                            VectC( 1.0,-0.5,'c'),
                            VectC( 0.0,-0.5,'c'),
                            VectC( 0.0, 0.0,'c'),
                            VectC( 1.0, 0.0,'e') ]),
                       VectOneChar('3',[
                            VectC( 0.0,-1.0,'l'),
                            VectC( 1.0,-1.0,'c'),
                            VectC( 1.0,-0.5,'c'),
                            VectC( 0.0,-0.5,'c'),
                            VectC( 1.0,-0.5,'c'),
                            VectC( 1.0, 0.0,'c'),
                            VectC( 0.0, 0.0,'e')]),
                       VectOneChar('4',[
                            VectC( 0.8,-1.0,'l'),
                            VectC( 0.0,-0.5,'c'),
                            VectC( 1.0,-0.5,'e'),
                            VectC( 0.8,-1.0,'l'),
                            VectC( 0.8, 0.0,'e')]),
                       VectOneChar('5',[
                            VectC( 1.0,-1.0,'l'),
                            VectC( 0.0,-1.0,'c'),
                            VectC( 0.0,-0.5,'c'),
                            VectC( 1.0,-0.5,'c'),
                            VectC( 1.0, 0.0,'c'),
                            VectC( 0.0, 0.0,'e')]),
                       VectOneChar('6',[
                            VectC( 1.0,-1.0,'l'),
                            VectC( 0.0,-1.0,'c'),
                            VectC( 0.0, 0.0,'c'),
                            VectC( 1.0, 0.0,'c'),
                            VectC( 1.0,-0.5,'c'),
                            VectC( 0.0,-0.5,'e')]),
                       VectOneChar('7',[
                            VectC( 0.0,-1.0,'l'),
                            VectC( 1.0,-1.0,'c'),
                            VectC( 1.0, 0.0,'e')]),
                       VectOneChar('8',[
                            VectC( 0.0,-1.0,'l'),
                            VectC( 0.0, 0.0,'c'),
                            VectC( 1.0, 0.0,'c'),
                            VectC( 1.0,-1.0,'c'),
                            VectC( 0.0,-1.0,'e'),
                            VectC( 0.0,-0.5,'l'),
                            VectC( 1.0,-0.5,'e')]),
                      VectOneChar('9',[
                            VectC( 1.0,-1.0,'l'),
                            VectC( 0.0,-1.0,'c'),
                            VectC( 0.0,-0.5,'c'),
                            VectC( 1.0,-0.5,'e'),
                            VectC( 1.0,-1.0,'l'),
                            VectC( 1.0, 0.0,'c'),
                            VectC( 0.0, 0.0,'e'),]),
                      
                      ]
        

    def setAutoDraw(self,value):
        '''
        Constructor
        '''
        self.isAutoDraw = value

    def setText(self,text,log=False):
        self.text = text

    def drawTest(self):
        ofsx = self.pos[0]
        ofsy = self.pos[1]
        glBegin(GL_TRIANGLES)
        glColor3f(1.0, 0.0, 1)
        glVertex3f(ofsx+(0.0), ofsy+(0.5), 1)
        glVertex3f(ofsx+(-0.5), ofsy+(-0.5), 1)
        glVertex3f(ofsx+(0.5), ofsy+(-0.5), -1)
        glEnd()


    def drawVectOneChar(self,ofsxy, vc):
        ofsx = ( ofsxy[0])
        ofsy = ( ofsxy[1]) # OpenGL xy 
        # print ' ofsxy ' + str(ofsx) + ' ' + str(ofsy)
        v = vc.v

        for one in v:
            ''' for Begin '''
            if one.m == ord('l'):
                glBegin(GL_LINE_STRIP)
            
            ''' For Code '''
            if one.m == ord('n') :
                ''' dont draw '''
            elif one.m == ord('l') or one.m == ord('e') or one.m == ord('c'):
                glVertex2f(ofsx+(self.scaleCX*one.getXOpenGL()), ofsy+(self.scaleCY*one.getYOpenGL()))
            
            ''' for end '''
            if one.m == ord('e'):
                glEnd()
                
        
    def drawOneC(self,ofsxy02, c):
        itOne = self.vc0_9[0]
        if ord(' ') == c:
            itOne = self.vcspace
        elif ord('.') == c:
            # ascii hex 2e Period (fullstop)
            itOne = self.vcperiod;
        elif ord('0') <= c and c <= ord('9'):
            cb = c - ord('0')
            itOne = self.vc0_9[cb]
        
        self.drawVectOneChar(ofsxy02,itOne)

    def draw(self):
        if self.isAutoDraw :
            ofsxy01 = list(self.pos)
            ofsxy02 = [ofsxy01[0]+self.posA[0],ofsxy01[1]+self.posA[1] ]
            for c in self.text:
                self.drawOneC(ofsxy02,ord(c))
                ofsxy02[0] = ofsxy02[0] + (1.0 *self.sizeOfChar)

            
    def setPosA(self,posxy):
        self.posA=posxy        