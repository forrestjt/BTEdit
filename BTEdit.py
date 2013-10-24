import wx


class mRect:
  def __init__ (self, xx = 0, yy = 0):
      self.iR = wx.Rect(xx,yy,50,20)
      self.children = []
      self.name = "Node"
  def setName(self, n):
    self.name = n
  def addChild(self, c):
    self.children.append(c)
  def removeChild(self, c):
    if c in self.children:
      self.children.remove(c)
  def GetX(self):
    return self.iR.x
  def GetY(self):
    return self.iR.y
  def GetWidth(self):
    return self.iR.width
  def GetHeight(self):
    return self.iR.height
  def Set(self, xx, yy):
    self.iR.x = xx
    self.iR.y = yy
  def GetCenterX(self):
    return self.iR.x + (self.iR.width/2)
  def GetCenterY(self):
    return self.iR.y + (self.iR.height/2)
  def DrawTo(self, dc):
      dc.DrawRectangle(self.iR.x, self.iR.y, self.iR.width, self.iR.height)
      dc.DrawText(self.name, self.iR.x + 5, self.iR.y)
  def DrawLines(self, dc):
    for c in self.children:
      dc.DrawLine(self.GetCenterX(),self.GetCenterY(),c.GetCenterX(),c.GetCenterY())
  def Contains(self, xx, yy):
    return self.iR.Contains(wx.Point(xx,yy))


class BTEditFrame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, -1, "BT Edit",size=(500,350))
        #gridSizer = wx.GridSizer(1, 1, 0, 0)
        tSizer = wx.BoxSizer(wx.HORIZONTAL)
        editor = BTEditWindow(self, -1)
        editor.SetMinSize((300,300))
        tSizer.Add(editor, 5)
        
        self.sId=wx.NewId()
        self.list=wx.ListCtrl(self,self.sId,style=wx.LC_REPORT|wx.SUNKEN_BORDER)
        self.list.Show(True)

        self.list.InsertColumn(0,"Data 1")
        self.list.InsertColumn(1,"Data #2")

        # 0 will insert at the start of the list
        pos = self.list.InsertStringItem(0,"hello")
        # add values in the other columns on the same row
        self.list.SetStringItem(pos,1,"world")
        tSizer.Add(self.list, 3, wx.EXPAND)

        self.SetAutoLayout(True)
        self.SetSizer(tSizer)
        self.Layout()

class BTEditWindow(wx.Panel):
    def __init__ (self, parent,ID):

        wx.Window.__init__(self, parent, ID)
        self.contextPoint = wx.Point(0,0)

        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBack)
        self.Bind(wx.EVT_MOTION, self.OnMotion)
        self.Bind(wx.EVT_LEFT_UP, self.OnLeftUp)
        self.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)

        self.rects = []
        self.rects.append(mRect())
        self.rects.append(mRect())
        self.rects.append(mRect())
        self.rects[0].Set(50,70)
        self.rects[1].Set(120,10)
        self.rects[2].Set(220,70)

        self.rects[1].addChild(self.rects[0])
        self.rects[1].addChild(self.rects[2])

        self.sx = -1
        self.sy = -1
        self.focusRect = 0
        self.popupmenu = wx.Menu()
        item = self.popupmenu.Append(-1, "New Node")
        self.Bind(wx.EVT_MENU, self.OnNewNode, item)
        item = self.popupmenu.Append(-1, "Edit Name")
        self.Bind(wx.EVT_MENU, self.OnEditName, item)
        item = self.popupmenu.Append(-1, "Connect Node")
        self.Bind(wx.EVT_MENU, self.OnConnect, item)
        item = self.popupmenu.Append(-1, "Delete Node")
        self.Bind(wx.EVT_MENU, self.OnDeleteNode, item)
        self.popupmenu.AppendSeparator()
        item = self.popupmenu.Append(-1, "Exit")
        self.Bind(wx.EVT_MENU, self.OnPopupItemSelected, item)
        
        self.Bind(wx.EVT_CONTEXT_MENU, self.OnShowPopup)

    def OnConnect(self, event):
      if self.focusRect != 0:
        for r in self.rects[:]:
          if r.Contains(self.contextPoint.x,self.contextPoint.y):
            r.addChild(self.focusRect)
            self.Refresh()

    def OnEditName(self, event):
        for r in self.rects[:]:
          if r.Contains(self.contextPoint.x,self.contextPoint.y):
            dlg = wx.TextEntryDialog(self, "New Name")
            if dlg.ShowModal() == wx.ID_OK:
              r.setName(dlg.GetValue())
              self.Refresh()
    def OnShowPopup(self, event):
        pos = event.GetPosition()
        pos = self.ScreenToClient(pos)
        self.contextPoint = pos
        self.PopupMenu(self.popupmenu, pos)
    def OnDeleteNode(self, event):
      var = 0
      for r in self.rects:
        if r.Contains(self.contextPoint.x,self.contextPoint.y):
          var = r
      if var != 0:
        self.rects.remove(var)
        for q in self.rects:
          q.removeChild(var)
        self.Refresh()  

    def OnNewNode(self, event):
        for r in self.rects:
          if r.Contains(self.contextPoint.x,self.contextPoint.y):
            m = mRect()
            m.Set(r.GetX(),r.GetY() + 30)
            r.addChild(m)
            self.rects.append(m)
            self.Refresh()
            
    def OnPopupItemSelected(self, event):
        item = self.popupmenu.FindItemById(event.GetId())
        text = item.GetText()
        
        
    def OnLeftDown(self,event):
        for r in self.rects:
          if r.Contains(event.GetX(), event.GetY()):
            self.sx = event.GetX()
            self.sy = event.GetY()
            self.focusRect = r
            self.GetParent().list.InsertStringItem(0,"Focus")
            self.Refresh()
            
        return

    def OnLeftUp(self, event):
      self.sx = -1
      self.sy = -1
      return

    def OnMotion(self, event):
      if self.sx != -1 & self.sy != -1:
        x = (event.GetX() - self.sx) + self.focusRect.GetX()
        y = (event.GetY() - self.sy) + self.focusRect.GetY()
        self.focusRect.Set(x, y)
        self.sx = event.GetX()
        self.sy = event.GetY()
        self.Refresh()
        return

    def OnEraseBack(self, event):
        pass # do nothing to avoid flicker

    def OnPaint(self, event):
        dc = wx.PaintDC(self)
        size=self.GetClientSize()
        dc.SetBrush(wx.Brush('black'))
        dc.DrawRectangle(0,0,size.width,size.height)
        dc.SetPen(wx.Pen('red',2))
        dc.SetBrush(wx.Brush('white'))
        if self.focusRect != 0:
          dc.DrawRectangle(self.focusRect.GetX()-2,self.focusRect.GetY()-2,self.focusRect.GetWidth()+4,self.focusRect.GetHeight()+4)
        dc.SetPen(wx.Pen('blue',2))
        for r in self.rects:
            r.DrawLines(dc)
        for r in self.rects:
            r.DrawTo(dc)

if __name__=='__main__':
    app=wx.PySimpleApp()
    frame=BTEditFrame(None)
    frame.Show(True)
    app.MainLoop()
