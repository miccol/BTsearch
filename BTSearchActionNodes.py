import sys
sys.path.insert(0, 'bt/')
#
from ActionNode import ActionNode
from NodeStatus import *
import time


class ActionTest(ActionNode):

    def __init__(self,name):
        ActionNode.__init__(self,name)


    def Execute(self,args):
        self.SetStatus(NodeStatus.Running)
        self.SetColor(NodeColor.Gray)

        while self.GetStatus() == NodeStatus.Running:
            #print self.name + ' executing'
            time.sleep(10)

        self.SetStatus(NodeStatus.Success)
        self.SetColor(NodeColor.Green)




class MoveCloseTo(ActionNode):

    def __init__(self,name,object_id, vrep_api):
        ActionNode.__init__(self,name)
        self.vrep = vrep_api
        self.name = name
        self.object_id = object_id

    def Execute(self,args):
        self.SetStatus(NodeStatus.Running)
        self.SetColor(NodeColor.Gray)
        print('Executing Action', self.name)
        self.vrep.move_close_to_object(self.object_id)
        self.SetStatus(NodeStatus.Failure)
        self.SetColor(NodeColor.Green)


class GraspObject(ActionNode):

    def __init__(self,name,object_id, vrep_api):
        ActionNode.__init__(self,name)
        self.vrep = vrep_api
        self.name = name
        self.object_id = object_id

    def Execute(self,args):
        self.SetStatus(NodeStatus.Running)
        self.SetColor(NodeColor.Gray)
        print('Executing Action', self.name)
        self.vrep.grasp_object(self.object_id)
        self.SetStatus(NodeStatus.Success)
        self.SetColor(NodeColor.Green)

class DropObject(ActionNode):

    def __init__(self,name, vrep_api):
        ActionNode.__init__(self,name)
        self.vrep = vrep_api
        self.name = name

    def Execute(self,args):
        self.SetStatus(NodeStatus.Running)
        self.SetColor(NodeColor.Gray)
        print('Executing Action', self.name)
        self.vrep.drop_object(self)
        self.SetStatus(NodeStatus.Success)
        self.SetColor(NodeColor.Green)