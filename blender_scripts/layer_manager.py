#!BPY

""" Registration info for Blender menus:
Name: 'Layer Manager'
Blender: 240
Group: 'System'
Tooltip: 'Manages layers and layers sets'
"""

# --------------------------------------------------------------------------
# ***** BEGIN GPL LICENSE BLOCK *****
#
# Copyright (C) 2005-2006 Mariano Hidalgo
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
#
# ***** END GPL LICENCE BLOCK *****
# --------------------------------------------------------------------------


__author__ = "Mariano Hidalgo AKA uselessdreamer"
__url__ = ("blender", "elysiun")
__version__ = "1.0"

__bpydoc__ = """\
Blender Layer Manager Script 1.0

The buttons on each row are:
Solo Layer - Click to make this layer the only one visible (this
   is the same as regular click in the layer buttons in header).
Turn Layer ON and OFF - Click to turn layer on and off (same as
   Ctrl Click in the layer buttons in the 3D View header).
Layer Name - Shows the layer name. Click to change it.
Layer Objects - Displays a menu with all the object in this layer.   

By using Layer Sets you can easily prepare sets of layers with the
requiered ones to do a full render, make a set with only important
layers, objects but no enviroment, etc.
You can add a empty set or add a copy of the current one with the
options in the menu left to the set name. To rename a set just click
in the set name string input. The little X on the right will remove
the set from the list.

Layer names and layer set are saved in the .blend as texts.
"""

import Blender
from Blender import Draw, BGL, Text, Scene, Window, Object

toggles = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]  
offset = 0

#~ try:
  #~ print 'normal stuff...'
  #~ txt = Text.Get("layernames")
#~ except:
  #~ print 'Blender, we have an exception!'
  #~ txt = Text.New("layernames")
  #~ txt.write("Camera afdsfsnd Martelly\n")
  #~ layersets = ["Working Set,1"]
  #~ for i in range(19):
    #~ txt.write("huhu " + i + " hihih\n")
  #~ for i in layersets:
    #~ txt.write(i +"\n")

# initialisation
DefaultLayers = ['box','mesh','time_snapshots','eps_snapshots','frequency_snapshots','excitations','probes','spheres','blocks','cylinders']

txt = Text.New("layernames")
for i in range(20):
  if i<len(DefaultLayers):
    txt.write(DefaultLayers[i]+'\n')
  else:
    txt.write('\n')

layersets = ["Working Set,1"]
for i in layersets:
  txt.write(i +"\n")
  
names = txt.asLines()
names.pop()
layersets = names[20:]  



curset = layersets[0][0:layersets[0].find(",")]

scn = Scene.getCurrent()
for i in range(20):
  if scn.layers.count(i):
    toggles[i-1] = 1


def event(evt, val):
  global offset
  if evt == Draw.ESCKEY or evt == Draw.QKEY or evt == Draw.RIGHTMOUSE:
    Draw.Exit()             
    return
  if evt == Draw. WHEELUPMOUSE:
    offset = offset +20
    Draw.Redraw(1)    
  if evt == Draw. WHEELDOWNMOUSE:
    offset = offset -20
    Draw.Redraw(1)    

def button_event(evt): 
  global curset, templayers 
  
  #
  # Layer ON/OFF button events
  #
  if evt <20:
    toggles[evt] = 1 - toggles[evt]
    mylayers = []
    for i in range(20):
      if toggles[i]:
        mylayers.append(i+1)
        scn.layers = mylayers
    Draw.Redraw()
    scn.update(1)
    Blender.Redraw()
  
  #
  # Layer SOLO/UNSOLO button events
  #
  if evt >= 20 and evt < 40:
    if scn.layers != [evt -19]:
      templayers = scn.layers
      for i in range(20):
        toggles[i] = 0
      toggles[evt-20] = 1  
      scn.layers = [evt -19]
    else:
      scn.layers = templayers
      for item in scn.layers:
        toggles[item-1] = 1
    Draw.Redraw()
    scn.update(1)
    Blender.Redraw()
  
  #
  # Layer NAME Button events
  #
  if evt >= 40 and evt < 60 and Window.GetKeyQualifiers() != 48:
    newname = Draw.PupStrInput("Name:", names[evt-40], 25)
    if newname:
      names[evt-40] = newname
      updatetxt()
      Draw.Redraw()
  
  #
  # Layer OBJEctS button events
  #
  elif evt >= 60 and evt < 80:
    objs = []
    obs = Object.Get()
    for ob in obs:
      if ob.layers.count(evt-59):
        objs.append(ob.getName())
    menu = "Objects in this Layer%t|"
    for item in objs:  
      menu = menu + "|" + item  
    if menu != "Objects in this Layer%t|":
      menu = menu + "|%l|Select all%x100"
    else:
      menu = "Sorry%t|There are no Objects in this Layer"
    c = Draw.PupMenu(menu)  
    if c != -1 and c != 100 and menu != "Sorry%t|There are no Objects in this Layer":
      sel = Object.GetSelected()
      for item in sel:
        item.select(0)
      newob = Object.Get(objs[c-1])
      newob.select(1)
    elif c == 100:
      sel = Object.GetSelected()
      for item in sel:
        item.select(0)
      for item in objs:
        Object.Get(item).select(1)
  
  #
  # Remove Layer Set
  #
  if evt == 99:
    for item in layersets:
      if item.find(curset) != -1:
        toremove = item
        print "toremove:" + toremove
    layersets.remove(toremove)
    curset = layersets[0][0:layersets[0].find(",")]
    updatetxt()
    tomodify = layersets[0].split(",")
    tomodify.pop(0)    
    for item in range(21):
      toggles[item-1] = 0
    for item in tomodify:  
      toggles[int(item)-1] = 1
    Draw.Redraw(1)
  
  #
  # Update Layer Manager
  #
  if evt == 98:  
    for i in range(21):
      if scn.layers.count(i):
        toggles[i-1] = 1
      else:  
        toggles[i-1] = 0
    Draw.Redraw(1)
  
  #
  # Layer Sets Menu
  #
  if evt == 100:    
    if men.val <= len(layersets):
      # Set LayerSet current Set
      for item in layersets:
        if item.find(curset) != -1:
          tomodify = item
      if tomodify:
        tomodify = tomodify.split(",")
        tomodify.pop(0)
      count = 0
      c = -1
      for item in toggles:
        if item == 1: count = count +1
      if len(tomodify) != count:      
        c = Draw.PupMenu("Set has Changed. Save?%t|Yes|No")
      else:
        for item in tomodify:
          if toggles[int(item)-1] == 0:
            c = Draw.PupMenu("Set has Changed. Save?%t|Yes|No")
      if c != -1 and c != 2:
        for item in layersets:
          if item.find(curset) != -1:
            tomodify = item
        if tomodify:
          layersets.remove(tomodify)
          layersets.append(curset + "," + str(scn.layers)[1:-1])
          layersets.sort()
          layersets.reverse()
          updatetxt()
      toset = layersets[men.val-1].split(",")
      curset = toset[0]
      toset.pop(0)
      mylayers = []
      for item in toset:
        mylayers.append(int(item))
      scn.layers = mylayers  
      Draw.Redraw(1)
      for i in range(21):
        if scn.layers.count(i):
          toggles[i-1] = 1
        else:  
          toggles[i-1] = 0  
      #
      
    if men.val == 100 or men.val == 101:
      newset = Draw.PupStrInput("Set Name:", "", 25)
      if newset != None:
        newset = newset.replace(","," ")
        print newset
        if men.val == 100:
          layersets.append(newset + ",1")
        else:
          toap = newset
          for item in scn.layers:
            toap = toap + "," + str(item)
          layersets.append(toap)
        curset = layersets[-1][0:layersets[-1].find(",")]        
        if men.val == 100:
          scn.layers = [1]
          for i in range(20):
            toggles[i] = 0
          toggles[0] = 1
    elif men.val == 102:
      for item in layersets:
        if item.find(curset) != -1:
          tomodify = item
      if tomodify:
        layersets.remove(tomodify)
        layersets.append(curset + "," + str(scn.layers)[1:-1])
    layersets.sort()
    layersets.reverse()
    updatetxt()
    Draw.Redraw(1)
    scn.update(1)
    Blender.Redraw()
  
  if evt == 101:
    st.val = st.val.replace(","," ")
    count = 0
    for item in layersets:
      if item.find(curset) != -1:
          tomodify = item
          toindex = count
      count = count + 1    
    tomodify = tomodify.replace(curset,st.val)
    layersets[toindex] = tomodify
    layersets.sort()
    layersets.reverse()
    updatetxt()
    curset = st.val
    Draw.Redraw(1)
    
def  updatetxt():
  global txt
  Text.unlink(txt)
  txt = Text.New("layernames")
  for i in range(20):
    txt.write(names[i] +"\n")
  for i in layersets:
    txt.write(i +"\n")
  
def INTtoFLOAT(rgba):
  r = float(rgba[0] *10 /254) /10
  g = float(rgba[1] *10 /254) /10
  b = float(rgba[2] *10 /254) /10
  a = float(rgba[3] *10 /254) /10
  return [r,g,b,a]
  
def gui():
  global st,men,lsetmenu,curset, offset
  #lsetmenu = "Layer Sets%t"
  lsetmenu = ""
  for i in layersets:
    lsetmenu = lsetmenu + "|    " + i[0:i.find(",")]
  lsetmenu = lsetmenu + "|SAVE SET%x102|NEW SET FROM LAYERS%x101|NEW SET%x100"  
  
  theme = Blender.Window.Theme.Get()[0]
  buts = theme.get('buts')    
  r,g,b,a = INTtoFLOAT(buts.back)  
  BGL.glClearColor(r+0.05,g+0.05,b+0.05,a)
  BGL.glClear(BGL.GL_COLOR_BUFFER_BIT)
  
  
  BGL.glEnable(BGL.GL_BLEND)
  BGL.glBlendFunc(BGL.GL_SRC_ALPHA, BGL.GL_ONE_MINUS_SRC_ALPHA)
  
  r,g,b,a = INTtoFLOAT(buts.panel)
  
  BGL.glColor4f(r,g,b,a+0.1)
  BGL.glBegin(BGL.GL_POLYGON)
  BGL.glVertex2i(5, offset + 5)
  BGL.glVertex2i(5, offset + 415)
  BGL.glVertex2i(185, offset + 415)
  BGL.glVertex2i(185, offset + 5)
  BGL.glEnd()  
  
  r,g,b,a = INTtoFLOAT(buts.header)  
  BGL.glColor4f(r-0.1,g-0.1,b-0.1,a)
  BGL.glBegin(BGL.GL_POLYGON)
  BGL.glVertex2i(5, offset + 415)
  BGL.glVertex2i(5, offset + 431)
  BGL.glVertex2i(185, offset + 431)
  BGL.glVertex2i(185, offset + 415)
  BGL.glEnd()  
  
  BGL.glDisable(BGL.GL_BLEND)
  
  BGL.glColor3f(1,1,1)
  BGL.glRasterPos2i(10,offset + 419)
  Draw.Text("Layer Manager HUHU", "small")
  
  BGL.glColor3f(1,1,1)
  Draw.PushButton("Update", 98, 110, offset + 395, 60,16 , "Updates Layer Manager")
  men = Draw.Menu(lsetmenu, 100, 26, offset + 10, 18,16 ,1, "Display a menu with Layer Sets")
  Draw.PushButton("X", 99, 153, offset + 10, 18,16 , "Exit Layer Manager")
  st = Draw.String("SET:", 101, 44, offset + 10, 110,16 ,curset,25, "Current Layer Set")
  for i in range(20):
    Draw.Toggle(str(i+1), i, 25, offset + 375-(18*i), 25, 16, toggles[i],"Turn this Layer ON and OFF")
    Draw.PushButton("", i+20, 10, offset + 379-(18*i), 8, 8, "Solo this Layer")
    Draw.PushButton("", i+60, 173, offset + 376-(18*i), 6, 6, "Select Objects in this Layer")
    Draw.PushButton(names[i], i+40, 50, offset + 375 -(18*i), 120, 16, "Click to change Layer name")
  

def algosomething(filename):
  print 'Saluton mondo!'

def main():  
  Draw.Register(gui, event, button_event)
  
  print '=========================='
  print Blender.Window.GetScreens()
  print Blender.Window.GetAreaID()
  print Blender.Window.GetAreaSize()
  print Blender.Text.Get()
  print '=========================='
  #~ Blender.Window.FileSelector(algosomething, "Import Bristol FDTD file...");
  #~ Blender.Run('~/.blender/scripts/bfdtd_import.py')

if __name__ == "__main__":
  main()
