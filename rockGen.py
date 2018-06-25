#!/usr/bin/env python

import pyglet
import random
from pyglet.gl import *
from pyglet.window import *
import math

class Rock:
    def __init__(self):

        self.batch = pyglet.graphics.Batch()

        green = ("c3f", (0,255,0,)*4)
        yellow = ("c3f", (255, 255, 0,) * 4)
        blue = ("c3f", (0, 0, 255,) * 4)
        red = ("c3f", (255, 0, 0,) * 4)
        cyan = ("c3f", (0, 255, 255,) * 4)
        white = ("c3f", (255, 255, 255,) * 4)

        x, y, z = 0, 0, -1
        X, Y, Z = x+1, y+1, z+1

        self.batch.add(4, GL_QUADS, None, ("v3f", (X,y,z, x,y,z, x,Y,z, X,Y,z, )), green) #BACK
        self.batch.add(4, GL_QUADS, None, ("v3f", (x,y,Z, X,y,Z, X,Y,Z, x,Y,Z,)), yellow) #FRONT

        self.batch.add(4, GL_QUADS, None, ("v3f", (x,y,z, x,y,Z, x,Y,Z, x,Y,z,)), blue) #LEFT
        self.batch.add(4, GL_QUADS, None, ("v3f", (X,y,Z, X,y,z, X,Y,z, X,Y,Z,)), red) #RIGHT

        self.batch.add(4, GL_QUADS, None, ("v3f", (x,y,z, X,y,z, X,y,Z, x,y,Z,)), cyan) #BOTTOM
        self.batch.add(4, GL_QUADS, None, ("v3f", (x,Y,Z, X,Y,Z, X,Y,z, x,Y,z,)), white) #TOP

    def draw(self):
        self.batch.draw()

class Camera:
    def __init__(self, pos =(0,0,0), rot=(0,0)):
        self.pos = list(pos)
        self.rot = list(rot)

    def mouse_motion(self,dx,dy):
        dx /= 8; dy /= 8; self.rot[0] += dy; self.rot[1] -= dx
        if self.rot[0] > 90:self.rot[0] = 90
        elif self.rot[0] < -90:self.rot[0] = -90

    def update(self,dt,keys):
        s = dt * 10
        rotY = -self.rot[1]/180*math.pi
        dx,dz = s*math.sin(rotY),s*math.cos(rotY)
        if keys[key.W]: self.pos[0] += dx; self.pos[2] -= dz;
        if keys[key.S]: self.pos[0] -= dx; self.pos[2] += dz;
        if keys[key.A]: self.pos[0] -= dz; self.pos[2] -= dx;
        if keys[key.D]: self.pos[0] += dz; self.pos[2] += dx;

        if keys[key.SPACE]: self.pos[1] += s
        if keys[key.LSHIFT]: self.pos[1] -= s


class Window(pyglet.window.Window):
    def push(self,pos,rot):
        glPushMatrix()
        rot = self.camera.rot
        glRotatef(-rot[0],1,0,0)
        glRotatef(-rot[1],0,1,0)
        glTranslatef(-pos[0],-pos[1],-pos[2],)

    def Projection(self): glMatrixMode(GL_PROJECTION); glLoadIdentity()
    def Rock(self): glMatrixMode(GL_MODELVIEW); glLoadIdentity()

    'Sets the mouse to disappear and be locked on keypress of SPACE'
    def setLock(self,state): self.lock = state; self.set_exclusive_mouse(state)
    lock = False; mouse_lock = property(lambda self:self.lock, setLock)

    def set3d(self):
        self.Projection()
        gluPerspective(70, self.width/self.height, 0.05, 1000)
        self.Rock()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_minimum_size(400, 400)
        self.keys = key.KeyStateHandler()
        self.push_handlers(self.keys)
        pyglet.clock.schedule(self.update)

        self.rock = Rock()
        'player point of view in the scene'
        self.camera = Camera((0,1.5,4),(-30,0))

    'Handels mouse motions'
    def on_mouse_motion(self, x, y, dx, dy):
        if self.mouse_lock:
            self.camera.mouse_motion(dx,dy)

    'Handles key presses, two keybinds SPACE and ESC hard coded'
    def on_key_press(self,KEY,MOD):
        if KEY == key.ESCAPE: self.close()
        elif KEY == key.E: self.mouse_lock = not self.mouse_lock

    def update(self,dt):
        self.camera.update(dt,self.keys)

    def on_draw(self):
        self.clear()
        self.set3d()
        self.push(self.camera.pos, self.camera.rot)
        self.rock.draw()
        glPopMatrix()

if __name__ == '__main__':
    window = Window(width=700, height=700, caption="Magic Space Rocks", resizable=True)
    #glPolygonMode(GL_FRONT_AND_BACK, GL_LINE);
    glEnable(GL_DEPTH_TEST)
    #glEnable(GL_CULL_FACE)
    glClearColor(0,0,0,1)
    pyglet.app.run()