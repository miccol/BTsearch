import sys
sys.path.insert(0, 'bt/')
#
from ActionNode import *
from NodeStatus import *
import time
import threading


class MoveCloseTo(ActionNode):

    def __init__(self,name,parameters_dict, vrep_api):
        # for i in list(parameter_dict.keys()):
        #     name = name + '_' + i
        ActionNode.__init__(self,name)
        self.vrep = vrep_api
        self.name = name
        self.parameters_dict = parameters_dict


    def Execute(self,args):
        self.SetStatus(NodeStatus.Running)
        self.SetColor(NodeColor.Gray)
        self.vrep.move_close_to_object(self.parameters_dict['to'])

        while self.GetStatus() == NodeStatus.Running:
            #print self.name + ' executing'
            print('Executing Action', self.name)
            time.sleep(0.1)
        # self.SetStatus(NodeStatus.Success)
        # self.SetColor(NodeColor.Green)


class GraspObject(ActionNode):

    def __init__(self,name,parameters_dict, vrep_api):
        # for i in list(parameter_dict.keys()):
        #     name = name + '_' + i
        ActionNode.__init__(self,name)
        self.vrep = vrep_api
        self.name = name
        self.parameters_dict = parameters_dict

    def Execute(self,args):
        self.SetStatus(NodeStatus.Running)
        self.SetColor(NodeColor.Gray)
        self.vrep.grasp_object(self.parameters_dict['object'])
        while self.GetStatus() == NodeStatus.Running:
            #print self.name + ' executing'
            print('Executing Action', self.name)
            #print('The object grasped is: ', self.vrep.object_grasped_id)

            time.sleep(1)


class DropObject(ActionNode):

    def __init__(self,name, parameters_dict, vrep_api):
        ActionNode.__init__(self, name)
        self.vrep = vrep_api
        self.parameters_dict = parameters_dict


    def Execute(self,args):
        self.SetStatus(NodeStatus.Running)
        self.SetColor(NodeColor.Gray)
        self.vrep.drop_object()
        while self.GetStatus() == NodeStatus.Running:
            #print self.name + ' executing'
            print('Executing Action', self.name)
            time.sleep(0.1)

        # self.SetStatus(NodeStatus.Success)
        # self.SetColor(NodeColor.Green)

    def Halt(self):
        if self.GetStatus() == NodeStatus.Running:
            ActionNode.Halt(self)
            self.vrep.init_arm()