# Forest walk example using pi3d module
# =====================================
# Copyright (c) 2012 - Tim Skillman
# Version 0.04 - 20Jul12
#
# grass added, new environment cube using FACES
#
# This example does not reflect the finished pi3d module in any way whatsoever!
# It merely aims to demonstrate a working concept in simplfying 3D programming on the Pi
#
# PLEASE INSTALL PIL imaging with:
#
#    $ sudo apt-get install python-imaging
#
# before running this example
#
from __future__ import absolute_import

import math,random

from pi3d import Display
from pi3d.Keyboard import Keyboard
from pi3d.Mouse import Mouse
from pi3d.Texture import Texture

from pi3d.context.Light import Light
from pi3d.Camera import Camera
from pi3d.Shader import Shader

from pi3d.shape.ElevationMap import ElevationMap
from pi3d.shape.EnvironmentCube import EnvironmentCube
from pi3d.shape.EnvironmentCube import loadECfiles
from pi3d.shape.MergeShape import MergeShape
from pi3d.shape.Plane import Plane
from pi3d.shape.Sphere import Sphere

from pi3d.util.Screenshot import screenshot

# Setup display and initialise pi3d
DISPLAY = Display.create(x=100, y=100)
DISPLAY.setBackColour(0.4,0.8,0.8,1)      # r,g,b,alpha

camera = Camera((0, 0, 0), (0, 0, -1), (1, 1000, DISPLAY.win_width/1000.0, DISPLAY.win_height/1000.0))
light = Light((1, 1, 4))
#========================================

# load shader
shader = Shader("shaders/bumpShade")

tree2img = Texture("textures/tree2.png")
tree1img = Texture("textures/tree1.png")
grassimg = Texture("textures/grass.png")
hb2img = Texture("textures/hornbeam2.png")
bumpimg = Texture("textures/grasstile_n.jpg")
reflimg = Texture("textures/stars.jpg")
rockimg = Texture("textures/rock1.jpg")

#myecube = EnvironmentCube(900.0,"HALFCROSS")
ectex=loadECfiles("textures/ecubes","sbox")
myecube = EnvironmentCube(camera, light, 900.0,"FACES")
for i in range(6):
  myecube.buf[i].set_draw_details(shader, [ectex[i]], 0.0, -1.0)

# Create elevation map
mapwidth = 1000.0
mapdepth = 1000.0
mapheight = 60.0
mountimg1 = Texture("textures/mountains3_512.jpg")
mymap = ElevationMap("textures/mountainsHgt.jpg", camera=camera, light=light,
                     width=mapwidth, depth=mapdepth, height=mapheight,
                     divx=32, divy=32) #testislands.jpg
mymap.buf[0].set_draw_details(shader, [mountimg1, bumpimg], 128.0, 0.0)
mymap.set_fog((0.3, 0.3, 0.4, 1.0), 650.0)

#Create tree models
treeplane = Plane(camera, light, 4.0,5.0)

treemodel1 = MergeShape(camera, light, "baretree")
treemodel1.add(treeplane.buf[0], 0,0,0)
treemodel1.add(treeplane.buf[0], 0,0,0, 0,90,0)

treemodel2 = MergeShape(camera, light, "bushytree")
treemodel2.add(treeplane.buf[0], 0,0,0)
treemodel2.add(treeplane.buf[0], 0,0,0, 0,60,0)
treemodel2.add(treeplane.buf[0], 0,0,0, 0,120,0)

#Scatter them on map using Merge shape's cluster function
mytrees1 = MergeShape(camera, light, "trees1")
mytrees1.cluster(treemodel1.buf[0], mymap,0.0,0.0,200.0,200.0,30,"",8.0,3.0)
mytrees1.buf[0].set_draw_details(shader, [tree2img], 0.0, 0.0)
#         (shape,elevmap,xpos,zpos,w,d,count,options,minscl,maxscl)

mytrees2 = MergeShape(camera, light, "trees2")
mytrees2.cluster(treemodel2.buf[0], mymap,0.0,0.0,200.0,200.0,30,"",6.0,3.0)
mytrees2.buf[0].set_draw_details(shader, [tree1img], 0.0, 0.0)
#         (shape,elevmap,xpos,zpos,w,d,count,options,minscl,maxscl)

mytrees3 = MergeShape(camera, light, "trees3")
mytrees3.cluster(treemodel2, mymap,0.0,0.0,300.0,300.0,30,"",4.0,2.0)
mytrees3.buf[0].set_draw_details(shader, [hb2img], 0.0, 0.0)
#         (shape,elevmap,xpos,zpos,w,d,count,options,minscl,maxscl)

#Create monolith
monolith = Sphere(camera, light, 8.0, 12, 48, sy = 10.0)
monolith.translate(100.0, -mymap.calcHeight(100.0, 350) + 10.0, 350.0)
#monolith.buf[0].set_draw_details(shader, [rockimg, bumpimg, reflimg], 32.0, 0.3)
monolith.buf[0].set_draw_details(shader, [rockimg], 2.0, 0.4)
monolith.set_fog((0.3, 0.3, 0.4, 1.0), 650.0)

#screenshot number
scshots = 1

#avatar camera
rot = 0.0
tilt = 0.0
avhgt = 3.5
xm = 0.0
zm = 0.0
ym = mymap.calcHeight(xm, zm) + avhgt

# Fetch key presses
mykeys = Keyboard()
mymouse = Mouse()
mymouse.start()

omx=mymouse.x
omy=mymouse.y

# Display scene and rotate cuboid
while 1:
  DISPLAY.clear()

  camera.reset()
  camera.rotate(tilt, 0, 0)
  camera.rotate(0, rot, 0)
  camera.translate((xm, ym, zm))

  myecube.draw()
  mymap.draw()
  monolith.draw()
  mytrees1.draw()
  mytrees2.draw()
  mytrees3.draw()

  mx=mymouse.x
  my=mymouse.y

  #if mx>display.left and mx<display.right and my>display.top and my<display.bottom:
  rot -= (mx-omx)*0.1
  tilt += (my-omy)*0.1
  omx=mx
  omy=my

  #Press ESCAPE to terminate
  k = mykeys.read()
  if k >-1:
    if k==119:  #key W
      xm -= math.sin(math.radians(rot))
      zm += math.cos(math.radians(rot))
      ym = mymap.calcHeight(xm, zm) + avhgt
    elif k==115:  #kry S
      xm += math.sin(math.radians(rot))
      zm -= math.cos(math.radians(rot))
      ym = mymap.calcHeight(xm, zm) + avhgt
    elif k==39:   #key '
      tilt -= 2.0
      print tilt
    elif k==47:   #key /
      tilt += 2.0
    elif k==97:   #key A
      rot -= 2
    elif k==100:  #key D
      rot += 2
    elif k==112:  #key P
      screenshot("forestWalk"+str(scshots)+".jpg")
      scshots += 1
    elif k==10:   #key RETURN
      mc = 0
    elif k==27:  #Escape key
      mykeys.close()
      mymouse.stop()
      DISPLAY.destroy()
      break
    else:
      print k

  DISPLAY.swapBuffers()
quit()
