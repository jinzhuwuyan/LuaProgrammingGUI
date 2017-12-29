from LuaProgrammingGUI.test.view.view_process import TreeMixin
class Condition_Tree_Container(TreeMixin.TreeModel):

    def __init__(self, *args, **kwargs):
        TreeMixin.TreeModel.__init__(self, *args, **kwargs)
        self.modeldata = []


    def GetItem(self, indices):
        text, children, childrendata = 'root', self.items, {}
        print 'Getting Condition_Tree_Container item is %s, indices is %s  ' % (str(self.items), str(indices))
        for index in indices:
            text, children, childrendata = self.items[index]
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
