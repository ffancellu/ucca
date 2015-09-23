# -*-coding:utf8-*-
__author__ = "Federico Fancellu"

class Node(object):

    def __init__(self,node,tag):
        self.node = node
        self.tag = tag    
        self.outgoing_edges = self.node.outgoing
        self._id = self.node.ID
        # take into account that a node might have multiple parents?
        self.parents = []
        
    def get_node(self):
        return self.node

    def get_tag(self):
        return self.tag

    def get_parents(self):
        return self.parents

    def get_outgoing_edges(self):
        return self.outgoing_edges

    def get_ID(self):
        return self._id

    def add_parent(self,parent_n):
        self.parents.append(parent_n)

    def __str__(self,current_level=0,prev_level=0):
        if isinstance(self,Terminal):
            o = "\t"*level+"%s %s\n" % (self.tag,self.text)
        elif isinstance(self,Internal):
            o = "\t"*level+self.tag+"\n"
            for c in self._children:
                o+= c.__str__(level+1)
        return o
            

class Internal(Node):

    def __init__(self,node,tag):
        super(Internal,self).__init__(node,tag)
        self.start_pos = self.node.start_position
        self.end_pos = self.node.end_position
        self._children = []

    def get_children(self):
        return self._children

    def get_start_pos(self):
        return self.start_pos

    def get_end_pos(self):
        return self.end_pos

    def add_child(self,child_n):
        self._children.append(child_n)

    def add_children(self,children_list):
        self._children.extend(children_list)

class Terminal(Node):

    def __init__(self,node,tag,text):
        super(Terminal,self).__init__(node,tag)
        self.text = text

    def set_text(self,text):
        self.text = text

    def get_text(self):
        return self.text
