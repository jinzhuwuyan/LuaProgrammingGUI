#! encoding: utf-8
import wx, wx.lib.customtreectrl, wx.gizmos
try:
    import treemixin 
except ImportError:
    from wx.lib.mixins import treemixin

overview = treemixin.__doc__

class TreeModel(object):
    ''' TreeModel holds the domain objects that are shown in the different
    tree controls. Each domain object is simply a two-tuple consisting of
    a label and a list of child tuples, i.e. (label, [list of child tuples]). 
    '''
    def __init__(self, *args, **kwargs):
        self.items = []
        self.itemCounter = 0
        super(TreeModel, self).__init__(*args, **kwargs)

    def GetItem(self, indices):
        text, children, childrendata = 'root', self.items, {}
        print 'Getting item is %s, indices is %s  ' % (str(self.items), str(indices))
        for index in indices:
            print 'children[index] is %s' % str(children[index])
            text, children, childrendata = children[index]
        return text, children, childrendata

    def GetText(self, indices):
        return self.GetItem(indices)[0]

    def GetChildren(self, indices):
        return self.GetItem(indices)[1]

    def GetChildrenCount(self, indices):
        return len(self.GetChildren(indices))

    def SetChildrenCount(self, indices, count, model = None):
        children = self.GetChildren(indices)
        if not model:

            # children = self.GetChildren(indices)

            while len(children) > count:
                children.pop()
            while len(children) < count:
                children.append(('item %d'%self.itemCounter, [], {}))
                self.itemCounter += 1
        else:
            print model
            # while len(children) < count:
            for value in model:

                children.append(value)
                self.itemCounter += 1

    def MoveItem(self, itemToMoveIndex, newParentIndex):
        itemToMove = self.GetItem(itemToMoveIndex)
        newParentChildren = self.GetChildren(newParentIndex)
        newParentChildren.append(itemToMove)
        oldParentChildren = self.GetChildren(itemToMoveIndex[:-1])
        oldParentChildren.remove(itemToMove)


class DemoTreeMixin(treemixin.VirtualTree, treemixin.DragAndDrop, 
                    treemixin.ExpansionState):
    def __init__(self, *args, **kwargs):
        self.model = kwargs.pop('treemodel')
        self.log = kwargs.pop('log')
        print 'Init DemoTreeMixin ...', str(self.model.items)
        super(DemoTreeMixin, self).__init__(*args, **kwargs)
        self.CreateImageList()

    def SetTreeModel(self, model):
        self.model = model

    def CreateImageList(self):
        print 'Creating Image List....'
        size = (16, 16)
        self.imageList = wx.ImageList(*size)
        for art in wx.ART_FOLDER, wx.ART_FILE_OPEN, wx.ART_NORMAL_FILE:
            self.imageList.Add(wx.ArtProvider.GetBitmap(art, wx.ART_OTHER, 
                                                        size))
        # self.AssignImageList(self.imageList)

    def OnGetItemText(self, indices):
        print 'OnGetItemText.... %s ' % self.model.GetText(indices)
        return self.model.GetText(indices)

    def OnGetChildrenCount(self, indices):
        print 'GetChildrenCount....'
        print self.model.items
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
        # if indices[-1] == 2:
        #     return wx.GREEN
        # else:
        return super(DemoTreeMixin,
                         self).OnGetItemBackgroundColour(indices)

    # def OnGetItemImage(self, indices, which):
    #     # Return the right icon depending on whether the item has children.
    #     print 'GetItemImage....'
    #     if which in [wx.TreeItemIcon_Normal, wx.TreeItemIcon_Selected]:
    #         if self.model.GetChildrenCount(indices):
    #             return 0
    #         else:
    #             return 2
    #     else:
    #         return 1

    def OnDrop(self, dropTarget, dragItem):
        print 'Droping.....'
        # dropIndex = self.GetIndexOfItem(dropTarget)
        # dropText = self.model.GetText(dropIndex)
        # dragIndex = self.GetIndexOfItem(dragItem)
        # dragText = self.model.GetText(dragIndex)
        # self.log.write('drop %s %s on %s %s'%(dragText, dragIndex,
        #     dropText, dropIndex))
        # self.model.MoveItem(dragIndex, dropIndex)
        self.RefreshItems()
        self.UnselectAll()



class VirtualTreeCtrl(DemoTreeMixin, wx.TreeCtrl):
    pass



class VirtualTreeListCtrl(DemoTreeMixin, wx.gizmos.TreeListCtrl):
    def __init__(self, *args, **kwargs):
        kwargs['style'] = wx.TR_DEFAULT_STYLE | wx.TR_FULL_ROW_HIGHLIGHT
        super(VirtualTreeListCtrl, self).__init__(*args, **kwargs)
        self.checked = None
        self.AddColumn('命令')
        self.AddColumn('值')
        a = self.GetColumn(0)
        print 'SelectedImage is ', a.GetSelectedImage()
        for art in wx.ART_TIP, wx.ART_WARNING:
            self.imageList.Add(wx.ArtProvider.GetBitmap(art, wx.ART_OTHER,
                                                        (16, 16)))

    def OnGetItemText(self, indices, column=0):
        # Return a different label depending on column.

        _pos = list(indices)[::-1]
        print "indices's type is %s, _pos is %s" % (str(type(indices)), str(_pos))
        _item = self.get_itembypos(self.model.items, _pos)
        print 'Get Item in TreeListCtrl, no pos item is %s, items is %s, column is %d' \
              % (str(self.model.items), str(_item), column)
        func_str = _item[0]
        child = _item[1]
        paras = _item[2]
        print 'Get Item in TreeListCtrl, func_str is %s, child is %s, paras is %s' % (str(func_str), str(child), str(paras))
        if 'condition' in paras.keys():
            condition_paras = paras['condition']
            # condition_paras ==> ([condition1, condition2, ...], 'list')
            first_condition = condition_paras[0][0]
            first_conditionName = first_condition[0]
            first_conditionValue = first_condition[2]['condition_value']
            first_conditionOperation = first_condition[2]['operation_value']
            paras_str = ''.join([first_conditionName, first_conditionValue, first_conditionOperation, ',...'])
        else:
            paras_str = ','.join([str(para[0] if isinstance(para, tuple) or isinstance(para, list) else para) for para in paras.values()])
        return func_str if column == 0 else paras_str


    def OnItemChecked(self, event):
        print 'ItemChecked.....'
        item = event.GetItem()
        itemIndex = self.GetIndexOfItem(item)
        if self.GetItemType(item) == 2:
            # It's a radio item; reset other items on the same level
            for nr in range(self.GetChildrenCount(self.GetItemParent(item))):
                self.checked[itemIndex[:-1]+(nr,)] = False
        self.checked[itemIndex] = True

    def get_itembypos(self, item, pos):

        index = pos.pop()
        print 'item[index] is %s' % str(item[index])
        func_str, child, paras = item[index]
        if not pos:
            return func_str, child, paras
        else:
            return self.get_itembypos(child, pos)


class VirtualTreeListCtrl_ControlIF(DemoTreeMixin, wx.gizmos.TreeListCtrl):
    def __init__(self, *args, **kwargs):
        kwargs['style'] = wx.TR_DEFAULT_STYLE | wx.TR_FULL_ROW_HIGHLIGHT
        super(VirtualTreeListCtrl_ControlIF, self).__init__(*args, **kwargs)
        self.checked = None
        self.AddColumn('条件')
        self.AddColumn('条件值')
        self.AddColumn('操作值')

        for art in wx.ART_TIP, wx.ART_WARNING:
            self.imageList.Add(wx.ArtProvider.GetBitmap(art, wx.ART_OTHER,
                                                        (16, 16)))

    def OnGetItemText(self, indices, column=0):
        # Return a different label depending on column.
        _pos = list(indices)[::-1]
        print "indices's type is %s, _pos is %s" % (str(type(indices)), str(_pos))
        _item = self.get_itembypos(self.model.items, _pos)
        print 'Get Item in TreeListCtrl, no pos item is %s, items is %s, column is %d' \
              % (str(self.model.items), str(_item), column)
        func_str = _item[0]
        child = _item[1]
        paras = _item[2]
        print 'Get Item in TreeListCtrl, func_str is %s, child is %s, paras is %s' % (str(func_str), str(child), str(paras))
        paras_str = ','.join([str(para[0]) for para in paras.values()])
        para_list = {0: func_str, 1: paras['condition_value'], 2: paras['operation_value']}
        return para_list[column]


    def OnItemChecked(self, event):
        print 'ItemChecked.....'
        item = event.GetItem()
        itemIndex = self.GetIndexOfItem(item)
        if self.GetItemType(item) == 2:
            # It's a radio item; reset other items on the same level
            for nr in range(self.GetChildrenCount(self.GetItemParent(item))):
                self.checked[itemIndex[:-1]+(nr,)] = False
        self.checked[itemIndex] = True

    def get_itembypos(self, item, pos):

        index = pos.pop()
        print 'item[index] is %s' % str(item[index])
        func_str, child, paras = item[index]
        if not pos:
            return func_str, child, paras
        else:
            return self.get_itembypos(child, pos)


class VirtualCustomTreeCtrl(DemoTreeMixin, 
                            wx.lib.customtreectrl.CustomTreeCtrl):
    def __init__(self, *args, **kwargs):
        self.checked = {}
        kwargs['style'] = wx.TR_HIDE_ROOT | \
            wx.TR_HAS_BUTTONS | wx.TR_FULL_ROW_HIGHLIGHT
        super(VirtualCustomTreeCtrl, self).__init__(*args, **kwargs)
        self.Bind(wx.lib.customtreectrl.EVT_TREE_ITEM_CHECKED,
                  self.OnItemChecked)

    def OnGetItemType(self, indices):
        print 'getItemType.....'
        if len(indices) == 1:
            return 1
        elif len(indices) == 2:
            return 2
        else:
            return 0

    def OnGetItemChecked(self, indices):
        print 'GetItemChecked....'
        return self.checked.get(indices, False)

    def OnItemChecked(self, event):
        print 'ItemChecked.....'
        item = event.GetItem()
        itemIndex = self.GetIndexOfItem(item)
        if self.GetItemType(item) == 2: 
            # It's a radio item; reset other items on the same level
            for nr in range(self.GetChildrenCount(self.GetItemParent(item))):
                self.checked[itemIndex[:-1]+(nr,)] = False
        self.checked[itemIndex] = True



class TreeNotebook(wx.Notebook):
    def __init__(self, *args, **kwargs):
        treemodel = kwargs.pop('treemodel')
        log = kwargs.pop('log')
        super(TreeNotebook, self).__init__(*args, **kwargs)
        self.trees = []
        for class_, title in [(VirtualTreeCtrl, 'TreeCtrl'),
                              (VirtualTreeListCtrl, 'TreeListCtrl'),
                              (VirtualCustomTreeCtrl, 'CustomTreeCtrl')]:
            tree = class_(self, treemodel=treemodel, log=log)
            self.trees.append(tree)
            self.AddPage(tree, title)
        self.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, self.OnPageChanged)

    def OnPageChanged(self, event):
        print 'Changing page.....'
        oldTree = self.GetPage(event.OldSelection)
        newTree = self.GetPage(event.Selection)
        newTree.RefreshItems()
        newTree.SetExpansionState(oldTree.GetExpansionState())
        event.Skip()

    def GetIndicesOfSelectedItems(self):
        print 'GetIndicesOfSelectedItems.....'
        tree = self.trees[self.GetSelection()]
        if tree.GetSelections():
            return [tree.GetIndexOfItem(item) for item in tree.GetSelections()]
        else:
            return [()]

    def RefreshItems(self):
        print 'Refreshing items is %s' % str(self.trees[self.GetSelection()])
        tree = self.trees[self.GetSelection()]
        tree.RefreshItems()
        tree.UnselectAll()


class TesPanel(wx.Panel):
    def __init__(self, parent, log):
        self.log = log
        super(TesPanel, self).__init__(parent)
        self.treemodel = TreeModel()
        self.CreateControls()
        self.LayoutControls()

    def CreateControls(self):
        self.notebook = TreeNotebook(self, treemodel=self.treemodel, 
                                     log=self.log)
        self.label = wx.StaticText(self, label='Number of children: ')
        self.childrenCountCtrl = wx.SpinCtrl(self, value='0', max=10000)
        self.button = wx.Button(self, label='Update children')
        self.button.Bind(wx.EVT_BUTTON, self.OnEnter)

    def LayoutControls(self):
        hSizer = wx.BoxSizer(wx.HORIZONTAL)
        options = dict(flag=wx.ALIGN_CENTER_VERTICAL|wx.ALL, border=2)
        hSizer.Add(self.label, **options)
        hSizer.Add(self.childrenCountCtrl, 2, **options)
        hSizer.Add(self.button, **options)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.notebook, 1, wx.EXPAND)
        sizer.Add(hSizer, 0, wx.EXPAND)
        self.SetSizer(sizer)

    def OnEnter(self, event):
        indicesList = self.notebook.GetIndicesOfSelectedItems()
        newChildrenCount = self.childrenCountCtrl.GetValue()
        for indices in indicesList:
            text = self.treemodel.GetText(indices)
            print 'text is %s ' % str(text)
            oldChildrenCount = self.treemodel.GetChildrenCount(indices)
            print 'oldChildrenCount is %d' % oldChildrenCount
            self.log.write('%s %s now has %d children (was %d)' % (text, indices,
                                                                   newChildrenCount, oldChildrenCount))
            self.treemodel.SetChildrenCount(indices, newChildrenCount)
        self.notebook.RefreshItems()


# def runTest(frame, nb, log):
#     win = TestPanel(nb, log)
#     return win


if __name__ == '__main__':
    import sys
    app = wx.App()
    frame = wx.Frame(None)
    TesPanel(frame, sys.stdout)
    frame.Show(True)
    app.MainLoop()
    # import sys, os, run
    # run.main(['', os.path.basename(sys.argv[0])] + sys.argv[1:])

