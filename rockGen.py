#!/usr/bin/env python

import pyglet

win = pyglet.window.Window()

def make_rock():

    print("Generating Rock")

@win.event
def on_draw():
    win.clear()

pyglet.app.run()