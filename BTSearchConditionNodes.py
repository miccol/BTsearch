from ConditionNode import ConditionNode
from NodeStatus import *
import time


class IsRobotCloseTo(ConditionNode):
    def __init__(self, name, object_id, vrep_api):
        ConditionNode.__init__(self, name)
        self.vrep = vrep_api
        self.name = name
        self.object_id = object_id

    def Execute(self, args):


        if self.vrep.is_robot_close_2d(self.object_id, 0.32):
            self.SetStatus(NodeStatus.Success)
            self.SetColor(NodeColor.Green)
        else:
            self.SetStatus(NodeStatus.Failure)
            self.SetColor(NodeColor.Red)


class IsObjectGrasped(ConditionNode):
    def __init__(self, name, object_id, vrep_api):
        ConditionNode.__init__(self, name)
        self.vrep = vrep_api
        self.name = name
        self.object_id = object_id

    def Execute(self, args):
        if  self.vrep.object_grasped_id is self.object_id:
            self.SetStatus(NodeStatus.Success)
            self.SetColor(NodeColor.Green)
        else:
            print('Object Not grasped')
            self.SetStatus(NodeStatus.Failure)
            self.SetColor(NodeColor.Red)


class IsObjectCloseTo(ConditionNode):
    def __init__(self, name, object_1_id, object_2_id, vrep_api):
        ConditionNode.__init__(self, name)
        self.vrep = vrep_api
        self.name = name
        self.object_1_id = object_1_id
        self.object_2_id = object_2_id

    def Execute(self, args):

        if self.vrep.are_objects_close(self.object_1_id, self.object_2_id,0.01):
            self.SetStatus(NodeStatus.Success)
            self.SetColor(NodeColor.Green)
        else:
            self.SetStatus(NodeStatus.Failure)
            self.SetColor(NodeColor.Red)