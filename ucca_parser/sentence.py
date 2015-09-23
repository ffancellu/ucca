# -*-coding:utf8-*-
__author__ = "Federico Fancellu"

class Sentence:

    def __init__(self,string,start_pos,end_pos):
        self.string = string
        self.start_pos = start_pos
        self.end_pos = end_pos

    def get_string(self):
        return self.string

    def get_start_pos(self):
        return self.start_pos

    def get_end_pos(self):
        return self.end_pos
