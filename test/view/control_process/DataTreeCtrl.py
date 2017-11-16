import wx
from wx.lib.mixins import treemixin

class DemoTreeMixin(treemixin.VirtualTree, treemixin.DragAndDrop,
                    treemixin.ExpansionState):
    def __init__(self, *args, **kwargs):
        self.model = kwargs.pop('treemodel')
        self.log = kwargs.pop('log')
        super(DemoTreeMixin, self).__init__(*args, **kwargs)
        self.CreateImageList()

    def CreateImageList(self):
        print 'Creating Image List....'
        size = (16, 16)
        self.imageList = wx.ImageList(*size)
        for art in wx.ART_FOLDER, wx.ART_FILE_OPEN, wx.ART_NORMAL_FILE:
            self.imageList.Add(wx.ArtProvider.GetBitmap(art, wx.ART_OTHER,
                                                        size))
        self.AssignImageList(self.imageList)

    def OnGetItemText(self, indices):
        print 'OnGetItemText....'
        return self.model.GetText(indices)

    def OnGetChildrenCount(self, indices):
        print 'GetChildrenCount....'
        return self.model.GetChildrenCount(indices)

    def OnGetItemFont(self, indices):
        print 'OnGetItemFont.....'
        # Show how to change the item font. Here we use a small font for
        # items that have children and the default font otherwise.
        if self.model.GetChildrenCount(indices) > 0:
            return wx.SMALL_FONT
        else:
            return super(DemoTreeMixin, self).OnGetItemFont(indices)

    def OnGetItemTextColour(self, indices):
        print 'GetItemTextColour....'
        # Show how to change the item text colour. In this case second level
        # items are coloured red and third level items are blue. All other
        # items have the default text colour.
        if len(indices) % 2 == 0:
            return wx.RED
        elif len(indices) % 3 == 0:
            return wx.BLUE
        else:
            return super(DemoTreeMixin, self).OnGetItemTextColour(indices)

    def OnGetItemBackgroundColour(self, indices):
        # Show how to change the item background colour. In this case the
        # background colour of each third item is green.
        print 'OnGetItemBackGroundColour.....'
        print 'indices is ',indices
        if indices[-1] == 3:
            return wx.GREEN
        else:
            return super(DemoTreeMixin,
                         self).OnGetItemBackgroundColour(indices)

    def OnGetItemImage(self, indices, which):
        # Return the right icon depending on whether the item has children.
        print 'GetItemImage....'
        if which in [wx.TreeItemIcon_Normal, wx.TreeItemIcon_Selected]:
            if self.model.GetChildrenCount(indices):
                return 0
            else:
                return 2
        else:
            return 1

    def OnDrop(self, dropTarget, dragItem):
        print 'Droping.....'
        dropIndex = self.GetIndexOfItem(dropTarget)
        dropText = self.model.GetText(dropIndex)
        dragIndex = self.GetIndexOfItem(dragItem)
        dragText = self.model.GetText(dragIndex)
        self.log.write('drop %s %s on %s %s'%(dragText, dragIndex,
            dropText, dropIndex))
        self.model.MoveItem(dragIndex, dropIndex)
        self.GetParent().RefreshItems()