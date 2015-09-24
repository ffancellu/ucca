# -*-coding:utf8-*-
__author__ = "Federico Fancellu"

from collections import deque
import node

class Tree:

    def __init__(self,root):
        self.root = root
        # find a mor meaningful way to order these nodes
        self.nodes = {}
        self.nodes[self.root.get_ID()] = self.root

    def fill_tree(self):
        """Traverse the root depth-first"""
        queue = deque([self.root])
        while queue:
            current_node = queue.popleft()
            cn_depth = current_node.get_depth()
            # expand
            if not isinstance(current_node,node.Terminal):
                for edge in current_node.get_outgoing_edges():
                    tag = edge.tag
                    child = edge.child
                    nn_depth = cn_depth+1
                    if tag=="T":
                        next_node = node.Terminal(child,tag,child.text,nn_depth)
                    else: 
                        next_node = node.Internal(child,tag,nn_depth)
                    current_node.add_child(next_node)
                    # set parent
                    next_node.add_parent(current_node)
                    self.nodes[next_node.get_ID()] = next_node
                    queue.append(next_node)

    def print_nodes(self):
        """Print out the nodes"""

        for _id,n in self.nodes.iteritems():
            print _id
            if isinstance(n[1],node.Internal):
                print "internal: ",n.tag
            elif isinstance(n[1],node.Terminal):
                print "Terminal: ",n.tag,n.text

    def print_tree_indent(self):
        return self.root.print_node_indent()

    def print_tree_penn(self):
        return self.root.print_node_penn()

    def get_root(self):
        return self.root

