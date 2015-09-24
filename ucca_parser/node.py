# -*-coding:utf8-*- 
__author__ = "Federico Fancellu"

class Node(object):

    def __init__(self,node,tag,depth):
        self.node = node
        self.depth = depth
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

    def get_depth(self):
        return self.depth

    def add_parent(self,parent_n):
        self.parents.append(parent_n)

    def print_node_indent(self,level=0):
        if isinstance(self,Terminal):
            o = str(self.depth)+"\t"*level+"(%s %s\n" % (self.tag,self.text)
        elif isinstance(self,Internal):
            o = str(self.depth)+"\t"*level+"(%s\n" % (self.tag)
            for c in self._children:
                o+= c.print_node_indent(level+1)
        return o

    def print_node_penn(self):
        res = ""
        indented_str = self.print_node_indent()
        spl_lines = indented_str.split("\n")
        for i in xrange(len(spl_lines)-2):
            current_line = spl_lines[i]
            next_line = spl_lines[i+1]
            tabs_current = int(current_line[0])
            tabs_next = int(next_line[0])
            if tabs_current>=tabs_next:
                p = abs(tabs_next-tabs_current)+1
                res+=current_line+")"*p+"\n"
            else: res+=current_line + "\n"
        last=spl_lines[-2]
        res+=last+")"*(int(last[0])+1)
        return res

        
class Internal(Node):

    def __init__(self,node,tag,depth):
        super(Internal,self).__init__(node,tag,depth)
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

    def __init__(self,node,tag,text,depth=0):
        super(Terminal,self).__init__(node,tag,depth)
        self.text = text

    def set_text(self,text):
        self.text = text

    def get_text(self):
        return self.text
