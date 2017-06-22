from ConditionNode import ConditionNode
from NodeStatus import *
import time


class IsRobotCloseTo(ConditionNode):
    def __init__(self, name, fluent, vrep_api):

        for i in list(fluent.parameters_dict.values()):
            name = name + '_' + str(i)

        ConditionNode.__init__(self, name)
        self.vrep = vrep_api
        self.name = name
        self.fluent = fluent
        self.to = self.fluent.parameters_dict['to']

    def Execute(self, args):
        if self.vrep.is_robot_close_2d(self.fluent.parameters_dict['to'], 0.32):
            self.SetStatus(NodeStatus.Success)
            self.SetColor(NodeColor.Green)
        else:
            self.SetStatus(NodeStatus.Failure)
            self.SetColor(NodeColor.Red)


class IsObjectGrasped(ConditionNode):
    def __init__(self, name, fluent, vrep_api):
        for i in list(fluent.parameters_dict.values()):
            name = name + '_' + str(i)
        ConditionNode.__init__(self, name)
        self.vrep = vrep_api
        self.name = name
        self.fluent = fluent

    def Execute(self, args):

        if  self.vrep.object_grasped_id is self.fluent.parameters_dict['object']:
            self.SetStatus(NodeStatus.Success)
            self.SetColor(NodeColor.Green)
        else:
            self.SetStatus(NodeStatus.Failure)
            self.SetColor(NodeColor.Red)


class IsObjectAt(ConditionNode):
    def __init__(self, name, fluent, vrep_api):
        for i in list(fluent.parameters_dict.values()):
            name = name + '_' + str(i)
        ConditionNode.__init__(self, name)
        self.vrep = vrep_api
        self.name = name
        self.fluent = fluent

    def Execute(self, args):

        if self.vrep.are_objects_close2d(self.fluent.parameters_dict['object'], self.fluent.parameters_dict['at'],0.12):
            self.SetStatus(NodeStatus.Success)
            self.SetColor(NodeColor.Green)
        else:
            self.SetStatus(NodeStatus.Failure)
            self.SetColor(NodeColor.Red)

class IsPathToObjectCollisionFree(ConditionNode):
    def __init__(self, name, fluent, vrep_api):
        for i in list(fluent.parameters_dict.values()):
            name = name + '_' + str(i)
        ConditionNode.__init__(self, name)
        self.vrep = vrep_api
        self.name = name
        self.fluent = fluent

    def Execute(self, args):
        is_collision, object_colliding_id = self.vrep.is_path_to_collision_free(self.fluent.parameters_dict['object'])

        if not is_collision:
            self.SetStatus(NodeStatus.Success)
            self.SetColor(NodeColor.Green)
        else:
            self.SetStatus(NodeStatus.Failure)
            self.SetColor(NodeColor.Red)