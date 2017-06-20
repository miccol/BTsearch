from ConditionNode import ConditionNode
from NodeStatus import *
from random import *
import time
class ConditionTest(ConditionNode):

    def __init__(self,name):
        ConditionNode.__init__(self,name)
        self.i = 0


    def Execute(self, args):
        x = 10
        if self.i < x:
            self.i = self.i + 1
            self.SetStatus(NodeStatus.Failure)
            self.SetColor(NodeColor.Red)
            print ('checking ' + str(self.name) + ' FAILURE:', self.i )
        else:
            self.SetStatus(NodeStatus.Success)
            self.SetColor(NodeColor.Green)

            print ('checking ' + str(self.name) + ' SUCCESS')



