# -*-coding:utf8-*-
__author__ = "Federico Fancellu"


from basic_ucca import convert
from ConfigParser import ConfigParser
from nltk.tokenize import sent_tokenize
import xml.etree.ElementTree as ET
import node
from tree import Tree
from sentence import Sentence

def extract_data(data_dummy):
    tree = ET.parse(data_dummy)
    root = tree.getroot()
    p = convert.from_standard(root)
    return p

def correct_split(split_sents,root_nodes):
    """
    Correct the segmentation error of the automatic splitter to make the scenes correspond to actual sentences.
    Input:
        - a list with all sentences split by the tokenizer
        - the root nodes
    Returns: a list of better segmented sentences.
    """
    sentences_nodes = list()
    correct = True
    current_word_index = 1
    i=0
    sent = []
    while i < len(split_sents):
        sent.extend(split_sents[i].split())
        start_index = current_word_index
        end_index = current_word_index + len(sent) - 1
        current_root_nodes = filter(lambda x: x.get_start_pos()>=start_index and x.get_end_pos()<=end_index,root_nodes)
        current_root_nodes_indexes = map(lambda x: (x.get_start_pos(),x.get_end_pos()),current_root_nodes)
        if current_root_nodes_indexes!=[]:
            if current_root_nodes_indexes[-1][-1]==end_index:
                sentence = Sentence(' '.join(sent),
                        start_index,
                        end_index)
                sentences_nodes.append(
                    (sentence,current_root_nodes)
                    )
                current_word_index = end_index + 1
                sent = []

        i+=1

    return sentences_nodes

def split_sents(passage):
    """
    Split the paragraph and the DAG into sentences. The DAG is also transformed into a tree representation.
    """
    # Node 1.1 is always a root FN node
    outgoing_edges = passage.layer('1').all[0].outgoing
    # root_nodes: H, U, L nodes at the top
    root_nodes = map(lambda x: node.Internal(x.child,x.tag),outgoing_edges)
    words = passage.layer('0').all
    par = ' '.join(map(lambda x: x.text,words))
    tok_par_nodes = correct_split(sent_tokenize(par),root_nodes)
    # current_index starts at 1 like the nodes
    current_index = 1
    for sent,head_nodes in tok_par_nodes:
        for head_node in head_nodes:
            tree = Tree(head_node)
            tree.fill_tree()
            tree.print_tree()
            # tree.print_nodes()


if __name__=="__main__":
    config = ConfigParser()
    config.read("/Users/ffancellu/git/ucca/config.cfg")
    p = extract_data(config.get("data_dummy","d"))
    split_sents(p)
