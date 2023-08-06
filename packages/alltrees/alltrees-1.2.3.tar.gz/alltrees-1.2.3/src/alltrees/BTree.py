
class Node:
    def __init__(self,leaf=False):
        self.leaf = leaf
        self.keys = []
        self.children = []
    
class BTree:
    def __init__(self,order):
        self.root = Node(True)
        self.order = order
    
    def addKey(self,key):
        root = self.root
        order = self.order
        if len(root.keys)==2*order-1:
            temp = Node()
            self.root = temp
            temp.children.insert(0,root)
            self.__split_child(temp,0)
            self.__insert_nf(temp,key)
        else:
            self.__insert_nf(root,key)
    
    def __split_child(self,node,ind):
        main_node = node.children[ind]
        split_node = Node(leaf = main_node.leaf)
        order = self.order
        node.children.insert(ind+1,split_node)
        node.keys.insert(ind,main_node.keys[order-1])
        split_node.keys = main_node.keys[order:(2*order)-1]
        main_node.keys = main_node.keys[0:order-1]
        if not main_node.leaf:
            split_node.children = main_node.children[order:2*order]
            main_node.children = main_node.children[0:order]
    
    def __insert_nf(self,node,key):
        i = len(node.keys)-1
        if node.leaf:
            node.keys.append(None)
            while i>=0 and key < node.keys[i]:
                node.keys[i+1] = node.keys[i]
                i-=1
            node.keys[i+1] = key
        
        else:
            while i>=0 and key < node.keys[i]:
                i-=1
            i+=1
            if len(node.children[i].keys)==2*self.order-1:
                self.__split_child(node,i)
                if key>node.keys[i]:
                    i+=1
            self.__insert_nf(node.children[i],key)
    
    def addKeyList(self,nodelist):
        if type(nodelist)!=type(list()):
            raise Exception("Expected a list")
        if len(nodelist)<1:
            raise Exception("Received a blank list")
        else:
            for node in nodelist:
                if type(node)!=type("") and type(node)!=type(0) and type(node)!=type(1.0):
                    raise Exception("Expected a string or int or float as values in the list")
                else:
                    self.addKey(node)

    def getHeight(self,temp=None):
        if temp is None:
            temp = self.root
            if temp is None:
                return 0
        if len(temp.children)!=0:
            left = self.getHeight(temp.children[0])
        else:
            left = 0
        return left+1

    def findMin(self,temp=None):
        if temp is None:
            temp = self.root
            if len(temp.keys)==0:
                return None
        if len(temp.children)!=0:
            return self.findMin(temp.children[0])
        else:
            return temp.keys[0]
    
    def findMax(self,temp=None):
        if temp is None:
            temp = self.root
            if len(temp.keys)==0:
                return None
        if len(temp.children)!=0:
            return self.findMax(temp.children[-1])
        else:
            return temp.keys[-1]

    def searchKey(self, key, node=None, j=0):
        if node is not None:
            i = 0
            while i < len(node.keys) and key > node.keys[i]:
                i += 1
            if i < len(node.keys) and key == node.keys[i]:
                return (node, self.getHeight(node), j+1, i+1)
            elif node.leaf:
                return None
            else:
                return self.searchKey(key, node.children[i], i)
        else:
            return self.searchKey(key, self.root)

    def __print(self,node,counter=0):
        print(counter,"-->",end=" ")
        for i in node.keys:
            print(i, end=" ")
        if len(node.children) > 0:
            print()
            for i in node.children:
                self.__print(i,counter+1)

    def printtree(self):
        if len(self.root.keys)!=0:
            self.__print(self.root)
            print()
        else:
            print("Empty BTree")

    def __deletefunc(self, node, key):
        order = self.order
        i = 0
        if len(self.root.children)==0 and len(self.root.keys)==1 and self.root.keys[0]==key and node==self.root:
            val = str(input("Do you want to delete the only node left in the tree? (Y|N)"))
            if val.lower()=="y" or val.lower()=="yes":
                pass
            else:
                print("Aborting Delete...")
                return -1
        while i < len(node.keys) and key > node.keys[i]:
            i += 1
        if node.leaf:
            if i < len(node.keys) and node.keys[i] == key:
                node.keys.pop(i)
                return
            return

        if i < len(node.keys) and node.keys[i] == key:
            return self.__delete_internal_node(node, key, i)
        elif len(node.children[i].keys) >= order:
            self.__deletefunc(node.children[i], key)
        else:
            if i != 0 and i + 2 < len(node.children):
                if len(node.children[i - 1].keys) >= order:
                    self.__delete_sibling(node, i, i - 1)
                elif len(node.children[i + 1].keys) >= order:
                    self.__delete_sibling(node, i, i + 1)
                else:
                    self.__delete_merge(node, i, i + 1)
            elif i == 0:
                if len(node.children[i + 1].keys) >= order:
                    self.__delete_sibling(node, i, i + 1)
                else:
                    self.__delete_merge(node, i, i + 1)
            elif i + 1 == len(node.children):
                if len(node.children[i - 1].keys) >= order:
                    self.__delete_sibling(node, i, i - 1)
                else:
                    self.__delete_merge(node, i, i - 1)
            self.__deletefunc(node.children[i], key)

    # Delete internal node
    def __delete_internal_node(self, node, key, i):
        order = self.order
        if node.leaf:
            if node.keys[i] == key:
                node.keys.pop(i)
                return
            return

        if len(node.children[i].keys) >= order:
            node.keys[i] = self.__delete_predecessor(node.children[i])
            return
        elif len(node.children[i + 1].keys) >= order:
            node.keys[i] = self.__delete_successor(node.children[i + 1])
            return
        else:
            self.__delete_merge(node, i, i + 1)
            self.__delete_internal_node(node.children[i], key, self.order - 1)

    # Delete the predecessor
    def __delete_predecessor(self, node):
        if node.leaf:
            return node.keys.pop()
        n = len(node.keys) - 1
        if len(node.children[n].keys) >= self.order:
            self.__delete_sibling(node, n + 1, n)
        else:
            self.__delete_merge(node, n, n + 1)
        self.__delete_predecessor(node.children[n])

    # Delete the successor
    def __delete_successor(self, node):
        if node.leaf:
            return node.keys.pop(0)
        if len(node.children[1].keys) >= self.order:
            self.__delete_sibling(node, 0, 1)
        else:
            self.__delete_merge(node, 0, 1)
        self.__delete_successor(node.children[0])

    # Delete resolution
    def __delete_merge(self, node, i, j):
        cnode = node.children[i]
        if j > i:
            rsnode = node.children[j]
            cnode.keys.append(node.keys[i])
            for k in range(len(rsnode.keys)):
                cnode.keys.append(rsnode.keys[k])
                if len(rsnode.children) > 0:
                    cnode.children.append(rsnode.children[k])
            if len(rsnode.children) > 0:
                cnode.children.append(rsnode.children.pop())
            new = cnode
            node.keys.pop(i)
            node.children.pop(j)
        else:
            lsnode = node.children[j]
            lsnode.keys.append(node.keys[j])
            for i in range(len(cnode.keys)):
                lsnode.keys.append(cnode.keys[i])
                if len(cnode.children) > 0:
                    lsnode.children.append(cnode.children[i])
            if len(cnode.children) > 0:
                lsnode.children.append(cnode.children.pop())
            new = lsnode
            node.keys.pop(j)
            node.children.pop(i)

        if node == self.root and (len(node.keys) == 0 or node.keys[0]==None):
            self.root = new

    # Delete the sibling
    def __delete_sibling(self, node, i, j):
        cnode = node.children[i]
        if i < j:
            rsnode = node.children[j]
            cnode.keys.append(node.keys[i])
            node.keys[i] = rsnode.keys[0]
            if len(rsnode.children) > 0:
                cnode.children.append(rsnode.children[0])
                rsnode.children.pop(0)
            rsnode.keys.pop(0)
        else:
            lsnode = node.children[j]
            cnode.keys.insert(0, node.keys[i - 1])
            node.keys[i - 1] = lsnode.keys.pop()
            if len(lsnode.children) > 0:
                cnode.children.insert(0, lsnode.children.pop())
    
    def deleteKey(self,key):
        pos = self.searchKey(key)
        if pos is not None:
            return self.__deletefunc(self.root,key)
        else:
            print("Key Not Found")
            return None
    
    def deleteAll(self):
        if self.root is not None:
            while len(self.root.keys)!=0:
                val = self.deleteKey(self.root.keys[0])
                if val==-1:
                    return False
        return True

# tree = BTree(3)

# # for i in range(10):
# #     tree.addKey(i)

# keylist = []
# for i in range(20):
#     keylist.append(i)

# tree.addKeyList(keylist)
# print("Printing Tree")
# tree.printtree()

# tree.deleteKey(0)
# print("Printing Tree")
# tree.printtree()
# pos = tree.searchKey(6)
# if pos is not None:
#     print("\nFound at height",pos[1],"child number",pos[2],"key number",pos[3])
# else:
#     print("\nNot Found")

# print(tree.findMin(),tree.findMax())
# tree.deleteAll()
# print("Printing Tree")
# tree.printtree()