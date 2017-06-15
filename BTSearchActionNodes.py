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

    def __init__(self,name,parameters_dict, vrep_api):
        # for i in list(parameter_dict.keys()):
        #     name = name + '_' + i
        ActionNode.__init__(self,name)
        self.vrep = vrep_api
        self.name = name
        self.parameters_dict = parameters_dict
        print('******************************************Creating Action', self.name)


    def Execute(self,args):
        print('******************************************Executing Action', self.name)
        self.SetStatus(NodeStatus.Running)
        self.SetColor(NodeColor.Gray)
        print('Executing Action', self.name)
        self.vrep.move_close_to_object(self.parameters_dict['to'])
        self.SetStatus(NodeStatus.Failure)
        self.SetColor(NodeColor.Green)


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
        print('Executing Action', self.name)
        self.vrep.grasp_object(self.parameters_dict['object'])
        self.SetStatus(NodeStatus.Success)
        self.SetColor(NodeColor.Green)

class DropObject(ActionNode):

    def __init__(self,name, parameters_dict, vrep_api):
        ActionNode.__init__(self,name)
        self.vrep = vrep_api
        self.name = name
        self.parameters_dict = parameters_dict

    def Execute(self,args):
        self.SetStatus(NodeStatus.Running)
        self.SetColor(NodeColor.Gray)
        print('Executing Action', self.name)
        self.vrep.drop_object()
        self.SetStatus(NodeStatus.Success)
        self.SetColor(NodeColor.Green)