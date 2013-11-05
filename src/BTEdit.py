# BTEdit.py
# An Open Source Behavior Tree Editor and Designer supporting creation of and embeding AI scripts.
# Oct 28th 2013
# Copyright (c) 2013 Forrest Tait
# Released under the MIT License (see License file)

import wx
import datetime
from wx.lib.mixins.listctrl import TextEditMixin

ID_NEW_CHILD = wx.NewId()
ID_SET_PARENT = wx.NewId()
ID_DELETE_NODE = wx.NewId()

class mNode:
  def __init__ (self, xx = 0, yy = 0):
      self.shape = wx.Rect(xx,yy,50,20)
      self.children = []
      self.name = "Node"
      self.type = "Sequence"
      self.parent = 0
  def setParent(self, p):
    self.parent = p
  def getParent(self):
    return self.parent
  def getParentName(self):
    if self.parent == 0:
      return ""
    else:
      return self.parent.getName()
  def setType(self, t):
    self.type = t
  def getType(self):
    return self.type
  def setName(self, n):
    self.name = n
    
  def getName(self):
    return self.name
  def addChild(self, c):
    self.children.append(c)
    c.setParent(self)
  def removeChild(self, c):
    if c in self.children:
      self.children.remove(c)
  def Destroy(self):
    for c in self.children:
      c.setParent(0)
  def GetX(self):
    return self.shape.x
  def GetY(self):
    return self.shape.y
  def GetWidth(self):
    return self.shape.width
  def GetHeight(self):
    return self.shape.height
  def Set(self, xx, yy):
    self.shape.x = xx
    self.shape.y = yy
  def GetCenterX(self):
    return self.shape.x + (self.shape.width/2)
  def GetCenterY(self):
    return self.shape.y + (self.shape.height/2)
  def DrawTo(self, dc):
      (w, h) = dc.GetTextExtent(self.name)
      self.shape.width = w + 16
      self.shape.height = h + 4
      if self.type == "Selector":
        dc.DrawEllipse(self.shape.x-2, self.shape.y-1, self.shape.width+2, self.shape.height+2)
      else:
        dc.DrawRectangle(self.shape.x, self.shape.y, self.shape.width, self.shape.height)
      dc.DrawText(self.name, self.shape.x + 8, self.shape.y + 2)
  def DrawLines(self, dc):
    #for c in self.children:
    if self.parent != 0: 
      dc.DrawLine(self.GetCenterX(),self.GetCenterY(),self.parent.GetCenterX(),self.parent.GetCenterY())
  def Contains(self, xx, yy):
    return self.shape.Contains(wx.Point(xx,yy))
  
class NewListCtrl(wx.ListCtrl, TextEditMixin):
    def __init__(self, parent, ID, pos=wx.DefaultPosition,
                 size=wx.DefaultSize, style=0):
        wx.ListCtrl.__init__(self, parent, ID, pos, size, style)
        TextEditMixin.__init__(self)
    def OpenEditor(self, col, row):
      if col == 0 or row == 2:
        return
      else:
        super(NewListCtrl, self).OpenEditor(col,row)
        
class BTEditFrame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, -1, "BTEdit",size=(600,350))
        #gridSizer = wx.GridSizer(1, 1, 0, 0)
        
        tSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.editor = BTEditWindow(self, -1)
        self.editor.SetMinSize((210,210))
        tSizer.Add(self.editor, 5, wx.EXPAND)
        
        self.sId=wx.NewId()
        self.list=NewListCtrl(self,self.sId,style=wx.LC_REPORT|wx.SUNKEN_BORDER)
        self.list.SetSizeHints(170,-1,-1,-1)
        self.list.Show(True)

        self.list.InsertColumn(0,"Property")
        self.list.InsertColumn(1,"Value")

        self.indicies = []
        # 0 will insert at the start of the list
        self.list.InsertStringItem(0,"Name:")
        self.list.InsertStringItem(1,"Type:")
        self.list.InsertStringItem(2,"Parent:")
        
        tSizer.Add(self.list, 0, wx.EXPAND)

        menubar = wx.MenuBar()
        fileMenu = wx.Menu()
        item = fileMenu.Append(-1, 'New', 'Make a new tree')
        self.Bind(wx.EVT_MENU, self.editor.OnNew, item)
        item = fileMenu.Append(-1, 'Open', 'Open data from a file')
        self.Bind(wx.EVT_MENU, self.editor.OnOpen, item)
        item = fileMenu.Append(-1, 'Save', 'Save to file')
        self.Bind(wx.EVT_MENU, self.editor.OnSave, item)
        item = fileMenu.Append(-1, 'Save As ...', 'Save as a new file')
        self.Bind(wx.EVT_MENU, self.editor.OnSaveAs, item)
        item = fileMenu.Append(-1, 'Export to cpp', 'Exports current tree')
        self.Bind(wx.EVT_MENU, self.editor.OnExportCode, item)
        fileMenu.AppendSeparator()
        item = fileMenu.Append(wx.ID_EXIT, 'Quit', 'Quit application')
        self.Bind(wx.EVT_MENU, self.OnClose, item)

        helpMenu = wx.Menu()
        item = helpMenu.Append(-1, 'About', 'About BTEdit')
        self.Bind(wx.EVT_MENU, self.OnAbout, item)

        optionMenu = wx.Menu()
        item = optionMenu.AppendRadioItem(-1, 'Color Scheme 1', 'Set as Color Scheme')
        self.Bind(wx.EVT_MENU, self.editor.OnColor1, item)
        item = optionMenu.AppendRadioItem(-1, 'Color Scheme 2', 'Set as Color Scheme')
        self.Bind(wx.EVT_MENU, self.editor.OnColor2, item)
        item = optionMenu.AppendRadioItem(-1, 'Color Scheme 3', 'Set as Color Scheme')
        self.Bind(wx.EVT_MENU, self.editor.OnColor3, item)
        
        
        menubar.Append(fileMenu, '&File')
        menubar.Append(optionMenu,'&Options')
        menubar.Append(helpMenu, '&Help')
        self.SetMenuBar(menubar)
        self.SetSizer(tSizer)
        self.Layout()

        self.Bind(wx.EVT_LIST_END_LABEL_EDIT, self.editor.OnEndLabelEdit)
        self.Bind(wx.EVT_CLOSE,self.OnClose)
        icon = wx.Icon("tree.ico", wx.BITMAP_TYPE_ICO)
        self.SetIcon(icon)
        
    def OnClose(self, event):
        self.Destroy()
    def OnAbout(self, event):
      wx.MessageBox("BTEdit is an Open Source Behavior Tree Editor.\nSee License and Readme for additional information.", "About BTEdit")

class BTEditWindow(wx.Panel):
    def __init__ (self, parent,ID):

        wx.Window.__init__(self, parent, ID)
        self.contextPoint = wx.Point(0,0)

        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBack)
        self.Bind(wx.EVT_MOTION, self.OnMotion)
        self.Bind(wx.EVT_LEFT_UP, self.OnLeftUp)
        self.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)

        self.nodes = []
        self.OnNew(0)
        self.OnColor1(0)

        self.sx = -1
        self.sy = -1
        self.focusNode = 0
        self.popupmenu = wx.Menu()
        item = self.popupmenu.Append(ID_NEW_CHILD, "New Child Node")
        self.Bind(wx.EVT_MENU, self.OnNewNode, item)
        item = self.popupmenu.Append(ID_SET_PARENT, "Set as Parent")
        self.Bind(wx.EVT_MENU, self.OnConnect, item)
        item = self.popupmenu.Append(ID_DELETE_NODE, "Delete Node")
        self.Bind(wx.EVT_MENU, self.OnDeleteNode, item)
        self.popupmenu.AppendSeparator()
        item = self.popupmenu.Append(-1, "Exit")
        self.Bind(wx.EVT_MENU, self.OnPopupItemSelected, item)
        self.Bind(wx.EVT_CONTEXT_MENU, self.OnShowPopup)
        

    def OnConnect(self, event):
      if self.focusNode != 0:
        for r in self.nodes[:]:
          if r.Contains(self.contextPoint.x,self.contextPoint.y) and r != self.focusNode:
            r.addChild(self.focusNode)
            self.Refresh()

    def OnShowPopup(self, event):
        pos = event.GetPosition()
        pos = self.ScreenToClient(pos)
        self.contextPoint = pos
        self.popupmenu.Enable(ID_NEW_CHILD, False )
        self.popupmenu.Enable(ID_SET_PARENT, False )
        self.popupmenu.Enable(ID_DELETE_NODE, False )
        for r in self.nodes:
          if r.Contains(pos.x,pos.y):
            self.popupmenu.Enable(ID_NEW_CHILD, True )
            if self.GetIndexOf(r) != 0:
              self.popupmenu.Enable(ID_DELETE_NODE, True )
            if self.focusNode != 0:
              if r != self.focusNode and r != self.focusNode.getParent():
                self.popupmenu.Enable(ID_SET_PARENT, True )        
        self.PopupMenu(self.popupmenu, pos)
    def OnDeleteNode(self, event):
      var = 0
      for r in self.nodes:
        if r.Contains(self.contextPoint.x,self.contextPoint.y):
          var = r
      if var != 0:
        var.Destroy()
        self.nodes.remove(var)
        for q in self.nodes:
          q.removeChild(var)
        self.focusNode = 0
        self.Refresh()  

    def OnNewNode(self, event):
        for r in self.nodes:
          if r.Contains(self.contextPoint.x,self.contextPoint.y):
            m = mNode()
            m.Set(r.GetX(),r.GetY() + 30)
            m.setParent(r)
            r.addChild(m)
            self.nodes.append(m)
            self.focusNode = m
            self.Refresh()
            
    def OnPopupItemSelected(self, event):
        item = self.popupmenu.FindItemById(event.GetId())
        text = item.GetText()
        
        
    def OnLeftDown(self,event):
        for r in self.nodes:
          if r.Contains(event.GetX(), event.GetY()):
            self.sx = event.GetX()
            self.sy = event.GetY()
            self.focusNode = r
            self.GetParent().list.SetStringItem(0,1,r.getName())
            self.GetParent().list.SetStringItem(1,1,r.getType())
            self.GetParent().list.SetStringItem(2,1,r.getParentName())
            self.Refresh()
            
        return

    def OnLeftUp(self, event):
      self.sx = -1
      self.sy = -1
      return

    def OnMotion(self, event):
      if self.sx != -1 & self.sy != -1:
        x = (event.GetX() - self.sx) + self.focusNode.GetX()
        y = (event.GetY() - self.sy) + self.focusNode.GetY()
        self.focusNode.Set(x, y)
        self.sx = event.GetX()
        self.sy = event.GetY()
        self.Refresh()
        return
    def OnEndLabelEdit(self, event):
        s = self.GetParent().list.GetItemText( event.GetIndex() )
        if self.focusNode != 0:
          if s == "Type:":
            self.focusNode.setType(event.GetText())
            self.Refresh()
          if s == "Name:":
            self.focusNode.setName(event.GetText())
            self.Refresh()

    def OnEraseBack(self, event):
        pass # do nothing to avoid flicker
    def OnColor1(self, event):
      cdb = wx.ColourDatabase()
      self.bgColor = cdb.Find('white')
      self.cellBgColor = cdb.Find('SKY BLUE')
      self.fgColor = cdb.Find('DARK GREEN')
      self.selColor = cdb.Find('LIME GREEN')
      self.Refresh()

    def OnColor2(self, event):
      cdb = wx.ColourDatabase()
      self.bgColor = cdb.Find('LIGHT GREY')
      self.cellBgColor = cdb.Find('SPRING GREEN')
      self.fgColor = cdb.Find('black')
      self.selColor = cdb.Find('NAVY')
      self.Refresh()

    def OnColor3(self, event):
      cdb = wx.ColourDatabase()
      self.bgColor = cdb.Find('LIGHT GREY')
      self.cellBgColor = cdb.Find('white')
      self.fgColor = cdb.Find('black')
      self.selColor = cdb.Find('yellow')
      self.Refresh()
    
    def GetIndexOf(self, o):
      if o in self.nodes:
        for i in range (len(self.nodes)):
          if self.nodes[i] == o:
            return i
      else:
        return -1

    def OnNew(self, event):
      del self.nodes[0:len(self.nodes)]
      self.nodes.append(mNode())
      self.nodes.append(mNode())
      self.nodes.append(mNode())
      self.nodes[0].Set(130,10)
      self.nodes[1].Set(50,70)
      self.nodes[2].Set(220,70)
      self.nodes[0].setName("Root")
      self.nodes[0].addChild(self.nodes[1])
      self.nodes[0].addChild(self.nodes[2])
      self.filename = 0
      self.focusNode = 0
      self.Refresh()

    def OnOpen(self, event):
      openFileDialog = wx.FileDialog(self, "Open File", "", "",
                                       "Text files (*.txt)|*.txt", wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
      if openFileDialog.ShowModal() == wx.ID_CANCEL:
        return     # the user changed idea...
      del self.nodes[0:len(self.nodes)]
      #self.nodes = []
      indicies = []
      parents  = []
      self.filename = openFileDialog.GetPath()
      with open(self.filename) as f:
        while True:
          line = f.readline()
          if not line:
            break
          n = mNode()
          n.setName(line.rstrip())
          line = f.readline()
          n.setType(line.rstrip())
          line = f.readline()
          templist = line.split()
          n.Set(int(templist[0]), (int(templist[1])))
          line = f.readline()
          parents.append(line)
          self.nodes.append(n)
        for i in range(len(self.nodes)):
          index = int(parents[i])
          if index != -1:
            self.nodes[index].addChild(self.nodes[i])

        f.close()
      self.Refresh()
      self.focusNode = 0
      return
    def OnSave(self, event):
      if self.filename == 0:
        self.OnSaveAs(event)
        return
      output = open(self.filename, "w")
      if output.closed:
          wx.MessageBox("Cannot save current contents in file '%s'."%saveFileDialog.GetPath())
          return
      for n in self.nodes:
        output.write(n.getName()+"\n")
        output.write(n.getType()+"\n")
        output.write("%d %d\n" %(n.GetX(),n.GetY()))
        if n.getParent() != 0:
          output.write("%d\n" % self.GetIndexOf(n.getParent()))
        else:
          output.write("-1\n")
      output.close()
      
      return
              
    def OnSaveAs(self, event):
        saveFileDialog = wx.FileDialog(self, "Save File As...", "", "",
                                   "txt files (*.txt)|*.txt", wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)  
        if saveFileDialog.ShowModal() == wx.ID_CANCEL:
            return     # the user changed idea...
        else:
          self.filename = saveFileDialog.GetPath()
          self.OnSave(event)
    def OnExportCode(self, event):
      saveFileDialog = wx.FileDialog(self, "Export Code As...", "", "",
                                   "cpp files (*.cpp)|*.cpp", wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)  
      if saveFileDialog.ShowModal() == wx.ID_CANCEL:
        return     # the user changed idea...
      else:
        with open(saveFileDialog.GetPath(),"w") as f:
          f.write("// Generated by BTEdit\n")
          f.write("// ")
          f.write("void buildTree()\n{\n")
          f.write("  int nSize = %d;\n"%len(self.nodes))
          f.write("  BTNode *nodes[nSize];\n")
          i = 0
          for n in self.nodes:
            f.write(("  nodes[%d] = new BT"%i)+n.getType()+"();\n")
            f.write("  nList.push_back(nodes[%d]);\n"%i)
            i += 1
          i = 0
          f.write("\n  //Add Children\n")
          for i in range(0, len(self.nodes)):
            for c in self.nodes[i].children:
              f.write("  nodes[%d]->addChild(nodes[%d]);\n"%(i,self.GetIndexOf(c)))
          f.write("}\n  //End Generated Code")
          f.close()
  
    def OnPaint(self, event):
        dc = wx.PaintDC(self)
        size=self.GetClientSize()
        
        dc.SetBrush(wx.Brush(self.bgColor))
        dc.SetPen(wx.Pen(self.bgColor,2))
        dc.DrawRectangle(0,0,size.width,size.height)
        
        
        dc.SetPen(wx.Pen(self.fgColor,2))
        dc.SetBrush(wx.Brush(self.cellBgColor))
        if self.focusNode != 0:
          self.focusNode.DrawTo(dc)
        for r in self.nodes:
            r.DrawLines(dc)
        dc.SetPen(wx.Pen(self.selColor,2))
        #dc.SetBrush(wx.Brush(self.bgColor))
        if self.focusNode != 0:
          if self.focusNode.getType() == "Selector":
            dc.DrawEllipse(self.focusNode.GetX()-4,self.focusNode.GetY()-3,self.focusNode.GetWidth()+6,self.focusNode.GetHeight()+6)
          else:
            dc.DrawRectangle(self.focusNode.GetX()-2,self.focusNode.GetY()-2,self.focusNode.GetWidth()+4,self.focusNode.GetHeight()+4)
        dc.SetPen(wx.Pen(self.fgColor,2))
        for r in self.nodes:
            r.DrawTo(dc)

if __name__=='__main__':
    app=wx.PySimpleApp()
    frame=BTEditFrame(None)
    frame.Show(True)
    app.MainLoop()
