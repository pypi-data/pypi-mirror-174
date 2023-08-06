# B+ tee in python


import math

# Node creation
class Node:
    def __init__(self, order):
        self.order = order
        self.values = []
        self.keys = []
        self.nextKey = None
        self.parent = None
        self.leaf = False

    # Insert at the leaf
    def _insert_at_leaf(self, value, key):
        if self.values:
            temp1 = self.values
            for i in range(len(temp1)):
                if value == temp1[i]:
                    self.keys[i].append(key)
                    break
                elif value < temp1[i]:
                    self.values = self.values[:i] + [value] + self.values[i:]
                    self.keys = self.keys[:i] + [[key]] + self.keys[i:]
                    break
                elif i + 1 == len(temp1):
                    self.values.append(value)
                    self.keys.append([key])
                    break
        else:
            self.values = [value]
            self.keys = [[key]]


# B plus tree
class BplusTree:
    def __init__(self, order):
        self.root = Node(order)
        self.root.leaf = True

    # Insert operation
    def addNode(self, value, key):
        value = str(value)
        old_node = self.__search(value)
        old_node._insert_at_leaf(value, key)

        if len(old_node.values) == old_node.order:
            node1 = Node(old_node.order)
            node1.leaf = True
            node1.parent = old_node.parent
            mid = int(math.ceil(old_node.order / 2)) - 1
            node1.values = old_node.values[mid + 1:]
            node1.keys = old_node.keys[mid + 1:]
            node1.nextKey = old_node.nextKey
            old_node.values = old_node.values[:mid + 1]
            old_node.keys = old_node.keys[:mid + 1]
            old_node.nextKey = node1
            self.__insert_in_parent(old_node, node1.values[0], node1)

    def addNodeList(self,nodelist):
        if type(nodelist)!=type(list()):
            raise Exception("Expected a list")
        if len(nodelist)<1:
            raise Exception("Received a blank list")
        else:
            for node in nodelist:
                if len(node)!=2:
                    raise Exception("Expected a key-value pair tuple as values in the list")
                else:
                    if type(node[0])!=type("") or type(node[1])!=type(""):
                        raise Exception("Expected a string key-value pair")
                    self.addNode(node[0],node[1])

    # Search operation for different operations
    def __search(self, value):
        current_node = self.root
        while current_node.leaf == False:
            temp2 = current_node.values
            for i in range(len(temp2)):
                if value == temp2[i]:
                    current_node = current_node.keys[i + 1]
                    break
                elif value < temp2[i]:
                    current_node = current_node.keys[i]
                    break
                elif i + 1 == len(current_node.values):
                    current_node = current_node.keys[i + 1]
                    break
        return current_node

    # Find the node
    def searchKeyValue(self, value, key):
        l = self.__search(value)
        for i, item in enumerate(l.values):
            if item == value:
                if key in l.keys[i]:
                    return True
                else:
                    return False
        return False

    # Inserting at the parent
    def __insert_in_parent(self, n, value, ndash):
        if self.root == n:
            rootNode = Node(n.order)
            rootNode.values = [value]
            rootNode.keys = [n, ndash]
            self.root = rootNode
            n.parent = rootNode
            ndash.parent = rootNode
            return

        parentNode = n.parent
        temp3 = parentNode.keys
        for i in range(len(temp3)):
            if temp3[i] == n:
                parentNode.values = parentNode.values[:i] + [value] + parentNode.values[i:]
                parentNode.keys = parentNode.keys[:i + 1] + [ndash] + parentNode.keys[i + 1:]
                if len(parentNode.keys) > parentNode.order:
                    parentdash = Node(parentNode.order)
                    parentdash.parent = parentNode.parent
                    mid = int(math.ceil(parentNode.order / 2)) - 1
                    parentdash.values = parentNode.values[mid + 1:]
                    parentdash.keys = parentNode.keys[mid + 1:]
                    value_ = parentNode.values[mid]
                    if mid == 0:
                        parentNode.values = parentNode.values[:mid + 1]
                    else:
                        parentNode.values = parentNode.values[:mid]
                    parentNode.keys = parentNode.keys[:mid + 1]
                    for j in parentNode.keys:
                        j.parent = parentNode
                    for j in parentdash.keys:
                        j.parent = parentdash
                    self.__insert_in_parent(parentNode, value_, parentdash)

    # Delete a node
    def delete(self, value, key):
        node_ = self.__search(value)

        temp = 0
        for i, item in enumerate(node_.values):
            if item == value:
                temp = 1

                if key in node_.keys[i]:
                    if len(node_.keys[i]) > 1:
                        node_.keys[i].pop(node_.keys[i].index(key))
                    elif node_ == self.root:
                        node_.values.pop(i)
                        node_.keys.pop(i)
                    else:
                        node_.keys[i].pop(node_.keys[i].index(key))
                        del node_.keys[i]
                        node_.values.pop(node_.values.index(value))
                        self.__deleteEntry(node_, value, key)
                else:
                    print("Value not in Key")
                    return -1
        if temp == 0:
            print("Value not in Tree")
            return -1

    def findMin(self,temp=None):
        if temp is None:
            temp = self.root
            if len(temp.values)==0:
                return None
        if len(temp.keys)!=0:
            if type(temp.keys[0])==type(self.root):
                return self.findMin(temp.keys[0])
            return temp.values[0]
        else:
            return temp.values[0]

    def findMax(self,temp=None):
        if temp is None:
            temp = self.root
            if len(temp.values)==0:
                return None
        if len(temp.keys)!=0:
            if type(temp.keys[-1])==type(self.root):
                return self.findMax(temp.keys[-1])
            else:
                return temp.values[-1]
        else:
            return temp.values[-1]

    def getHeight(self,temp=None,counter=1):
        if temp is None:
            temp = self.root
            if temp is None:
                return 0
        if not temp.leaf and len(temp.keys)!=0 and type(temp.keys[0])==type(self.root):
            return self.getHeight(temp.keys[0],counter+1)
        else:
            return counter

    # Delete an entry
    def __deleteEntry(self, node_, value, key):

        if not node_.leaf:
            for i, item in enumerate(node_.keys):
                if item == key:
                    node_.keys.pop(i)
                    break
            for i, item in enumerate(node_.values):
                if item == value:
                    node_.values.pop(i)
                    break

        if self.root == node_ and len(node_.keys) == 1:
            val = str(input("Do you want to delete the only node left in the tree? (Y|N) "))
            if val.lower()=="y" or val.lower()=="yes":
                pass
            else:
                print("Aborting Delete...")
                return -1
            self.root = node_.keys[0]
            node_.keys[0].parent = None
            del node_
            return

        elif (len(node_.keys) < int(math.ceil(node_.order / 2)) and node_.leaf == False) or (len(node_.values) < int(math.ceil((node_.order - 1) / 2)) and node_.leaf == True):

            is_predecessor = 0
            parentNode = node_.parent
            PrevNode = -1
            NextNode = -1
            PrevK = -1
            PostK = -1
            for i, item in enumerate(parentNode.keys):

                if item == node_:
                    if i > 0:
                        PrevNode = parentNode.keys[i - 1]
                        PrevK = parentNode.values[i - 1]

                    if i < len(parentNode.keys) - 1:
                        NextNode = parentNode.keys[i + 1]
                        PostK = parentNode.values[i]

            if PrevNode == -1:
                ndash = NextNode
                value_ = PostK
            elif NextNode == -1:
                is_predecessor = 1
                ndash = PrevNode
                value_ = PrevK
            else:
                if len(node_.values) + len(NextNode.values) < node_.order:
                    ndash = NextNode
                    value_ = PostK
                else:
                    is_predecessor = 1
                    ndash = PrevNode
                    value_ = PrevK

            if len(node_.values) + len(ndash.values) < node_.order:
                if is_predecessor == 0:
                    node_, ndash = ndash, node_
                ndash.keys += node_.keys
                if not node_.leaf:
                    ndash.values.append(value_)
                else:
                    ndash.nextKey = node_.nextKey
                ndash.values += node_.values

                if not ndash.leaf:
                    for j in ndash.keys:
                        j.parent = ndash

                self.__deleteEntry(node_.parent, value_, node_)
                del node_
            else:
                if is_predecessor == 1:
                    if not node_.leaf:
                        ndashpm = ndash.keys.pop(-1)
                        ndashkm_1 = ndash.values.pop(-1)
                        node_.keys = [ndashpm] + node_.keys
                        node_.values = [value_] + node_.values
                        parentNode = node_.parent
                        for i, item in enumerate(parentNode.values):
                            if item == value_:
                                parentNode.values[i] = ndashkm_1
                                break
                    else:
                        ndashpm = ndash.keys.pop(-1)
                        ndashkm = ndash.values.pop(-1)
                        node_.keys = [ndashpm] + node_.keys
                        node_.values = [ndashkm] + node_.values
                        parentNode = node_.parent
                        for i, item in enumerate(parentNode.values):
                            if item == value_:
                                parentNode.values[i] = ndashkm
                                break
                else:
                    if not node_.leaf:
                        ndashp0 = ndash.keys.pop(0)
                        ndashk0 = ndash.values.pop(0)
                        node_.keys = node_.keys + [ndashp0]
                        node_.values = node_.values + [value_]
                        parentNode = node_.parent
                        for i, item in enumerate(parentNode.values):
                            if item == value_:
                                parentNode.values[i] = ndashk0
                                break
                    else:
                        ndashp0 = ndash.keys.pop(0)
                        ndashk0 = ndash.values.pop(0)
                        node_.keys = node_.keys + [ndashp0]
                        node_.values = node_.values + [ndashk0]
                        parentNode = node_.parent
                        for i, item in enumerate(parentNode.values):
                            if item == value_:
                                parentNode.values[i] = ndash.values[0]
                                break

                if not ndash.leaf:
                    for j in ndash.keys:
                        j.parent = ndash
                if not node_.leaf:
                    for j in node_.keys:
                        j.parent = node_
                if not parentNode.leaf:
                    for j in parentNode.keys:
                        j.parent = parentNode

    # def deleteAll(self):
    #     if self.root is not None:
    #         while len(self.root.values)!=0:
    #             node = self.__search(self.root.values[0])
    #             print(self.root.values[0],node.keys)
    #             val = self.delete(self.root.values[0],node.keys[0][0])
    #             if val==-1:
    #                 return False
    #     return True   

    # Print the tree
    def __print(self,node,counter=1):
        print(" ",counter,"-->",end=" ")
        for i in node.values:
            print(i, end=" ")
        if not node.leaf:
            print()
            for i in node.keys:
                self.__print(i,counter+1)


    def printtree(self):
        if len(self.root.keys)!=0:
            self.__print(self.root)
            print()

        else:
            print("Empty B+ Tree")


# record_len = 3
# bplustree = BplusTree(record_len)
# bplustree.addNode('5', '11')
# bplustree.addNode('15', '21')
# bplustree.addNode('25', '31')
# bplustree.addNode('35', '41')
# bplustree.addNode('45', '10')
# bplustree.addNode('55','12')
# bplustree.addNode('65','61')
# bplustree.addNode('75','98')
# bplustree.addNodeList([('85','87'),('95','17')])
# bplustree.printtree()
# bplustree.delete('35','31')
# bplustree.printtree()
# if(bplustree.searchKeyValue('5', '33')):
#     print("Found")
# else:
#     print("Not found")
# print(bplustree.findMax())
# print(bplustree.findMin())
# print(bplustree.getHeight())