
#AVL tree for early movie data set lookup.

class AVL:
        def __init__(self):
                self._root = None
                self._total = 0
                
        def getRoot(self):
                return self._root
        def getTotal(self):
                return self._total

        class Node:
                def __init__(self, height: int, value: str):
                        self._value = (value, 1)
                        self._height = 0
                        self._left = None
                        self._right = None

                def value(self):
                        return self._value[0]

        def getLeaf(self, root: Node):
                if root._left == None:
                        return 1
                else:
                        return 1 + self.getLeaf(root._right)

        def add(self, value: str):
                self._total += 1
                if( self._root == None ):
                        self._root = self.Node( 0, value )
                        
                else:
                        self.add_traversal(value, self._root)
                        self._root = self.check_height( value, self._root)

        def add_traversal(self, value: str, root: Node):
                if( root._value[0] == value ):
                        root._value = (root._value[0], root._value[1] +1)
                        
                elif( root._value[0] > value): 
                        if( root._left == None ):
                                root._left = self.Node(0, value)
                        else:
                                self.add_traversal(value, root._left)
                                root._left = self.check_height( value, root._left )
                                
                elif( root._value[0] < value):
                        if( root._right == None):
                                root._right = self.Node(0, value)
                        else:
                                self.add_traversal(value, root._right)
                                root._right = self.check_height( value, root._right )

        def find( self, value: str ) -> bool:
                return self.contains( value, self._root )

        def search( self, value: str ) -> bool:
                return self.contains(value, self.getRoot())
        
        def contains( self, value: str, root: Node ) -> bool:
                if( root == None ):
                        return False
                elif( root._value[0] == value ):
                        return True
                elif( root._value[0] > value ):
                        return self.contains( value, root._left )
                elif( root._value[0] < value ): 
                        return self.contains( value, root._right)
                
        def check_height( self, value: str, root: Node) -> Node:
                leftHeight = -1 if( root._left == None ) else (root._left._height)
                rightHeight = -1 if( root._right == None ) else (root._right._height)
                difference = leftHeight - rightHeight

                if( difference < -1 ):
                        if( self.contains( value, root._right._right ) ):
                                return self.RR( root )
                        elif( self.contains( value, root._right._left) ):
                                return self.RL( root )
                        
                elif( difference > 1 ):
                        if( self.contains( value, root._left._left ) ):
                                return self.LL( root )
                        elif( self.contains( value, root._left._right ) ):
                                return self.LR( root )
                else:
                        return root
                
        def LL(self, root: Node) -> Node:
                tempNode = root._left
                root._left = root._right
                tempNode._right = root
                tempNode._right._height = tempNode._height - 1
                root = tempNode
                return root
                
        def LR(self, root: Node):
                tempNode = root._left._right
                tempNode._height = root._left._height
                root._left._right = tempNode._left
                tempNode._left = root._left
                tempNode._left._height = tempNode._height -1
                root._left = tempNode._right
                temp._right = root
                temp._right._height = tempNode._height -1
                root = tempNode
                return tempNode
        
        def RR(self, root: Node):
                tempNode = root._right
                root._right = root._left
                tempNode._left = root
                tempNode._left_height = tempNode._height - 1
                root = tempNode
                return root
        
        def RL(self, root: Node):
                tempNode = root._right._left
                tempNode._height = root._right._height
                root._right._left = tempNode._right
                tempNode._right = root._right
                tempNode._right._height = tempNode._height -1
                root._right = tempNode._left
                temp._left = root
                temp._left._height = tempNode._height -1
                root = tempNode
                return tempNode

        def printString(self):
                print(self.dict_toString(self.toString(self._root)))

        def returnString(self):
                return self.toString(self._root)

        #right root left, took from my CS 161 traversing trees class
        def toString(self, root: Node) -> dict: 
                treeDict = dict()
                if( root._right != None ):
                        treeDict.update( self.toString( root._right ) )

                treeDict[root._value[0]] = root._value[1]
                if( root._left != None ):
                        treeDict.update( self.toString( root._left ))
                return treeDict

        def dict_toString(self, string_dict: dict ) -> str:
                string_output = "Output:\n"
                 #found a similar sorting example from my ICS 33 lab
                temp = sorted(string_dict.items(), key = lambda a: (a[1], a[0]))
                for x,y in sorted(temp, key = lambda a: (a[1]), reverse = True):
                        string_output += "{} - {}\n".format(x,y)
                return string_output
        
