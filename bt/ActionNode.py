from abc import ABCMeta
from LeafNode import LeafNode


class ActionNode(LeafNode):
    __metaclass__ = ABCMeta  # abstract class
    def __init__(self, name, param = ''):

        LeafNode.__init__(self, name + '(' + param + ')')
        self.nodeType = 'Action'
        self.param = param
        self.generic_name = name
