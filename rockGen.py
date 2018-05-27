#!/usr/bin/env python

import pyglet
import random
from pyglet.gl import *
from pyglet.window import *
from pyglet.window import mouse

win = pyglet.window.Window()

#Make 10 random numbers between 1 and 101
for x in range(10):
    print(random.randint(1, 101))

@win.event
def on_draw():
    #Clear Buffers
    glClear(GL_COLOR_BUFFER_BIT)

    #Draw outlines only
    glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

    #Drawing
    glBegin(GL_QUAD_STRIP)
    glVertex2i(50, 50)
    glVertex2i(75, 100)
    glVertex2i(200, 200)
    glVertex2i(50, 250)
    glEnd()

#Key presses!
@win.event
def on_key_press(symbol, modifiers):
    print("A key was pressed")

#Mouse clicks!
@win.event
def on_mouse_press(x, y, button, modifiers):
    if button == mouse.LEFT:
        print("The left mouse button was pressed.")

#Create a triangle set
pyglet.app.run()