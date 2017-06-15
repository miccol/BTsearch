import sys
sys.path.insert(0, 'bt/')
#
from BehaviorTree import *
from SequenceNode import SequenceNode
from FallbackNode import FallbackNode
from ActionTest import ActionTest
from ConditionTest import ConditionTest
from BTSearchActionNodes import *
from BTSearchConditionNodes import *
from search import Fluent

import copy


class SearchUtils:
    def __init__(self, all_action_templates, all_action_nodes, all_condition_nodes, vrep_api):
        self.all_action_templates = all_action_templates
        self.all_action_nodes = all_action_nodes
        self.all_condition_nodes = all_condition_nodes
        self.vrep = vrep_api


    def sample_action(self, name, fluent):

        action = None
        if name is 'move_close_to':
            action = MoveCloseTo('move_close_to_'+str(fluent.parameters_dict['to']), fluent.parameters_dict, self.vrep)
        elif name is 'grasp':
            action = GraspObject('grasp_'+str(fluent.parameters_dict['object']), fluent.parameters_dict, self.vrep)
        elif name is 'drop':
            action = DropObject('drop_at_'+str(fluent.parameters_dict['at']), fluent.parameters_dict, self.vrep)
        else:
            raise Exception('Cannot Sample Action', name)

        return action, fluent.parameters_dict

    def sample_fluent(self, fluent, param = None):
        print('FLUENT', str(fluent.parameters_dict))

        parameters = copy.deepcopy(fluent.parameters_dict)


        if fluent.type is 'is_robot_close_to':
            print('TRY: IsRobotCloseTo',str(param))
            if param:
                try:
                    parameters['to'] = param['to']
                except:
                    try:
                        parameters['to'] = param['at']
                    except:
                        parameters['to'] = param['object']
            new_fluent = Fluent(fluent.name,fluent.type, parameters)
            print('OLD fluent', str(fluent.parameters_dict), 'NEW fluent', str(new_fluent.parameters_dict))
            print('FOUND: IsRobotCloseTo',str(new_fluent.parameters_dict))

            return IsRobotCloseTo(new_fluent.name, new_fluent, self.vrep)
        elif fluent.type is 'is_object_at':
            if param : parameters['at'] = param['at']
            print('FOUND: IsObjectAt',str(parameters))
            new_fluent = Fluent(fluent.name,fluent.type, parameters)
            return IsObjectAt(new_fluent.name, new_fluent, self.vrep)
        elif fluent.type is 'is_object_grasped':
            print('TRY: IsObjectGrasped',str(param))
            if param : parameters['object'] = param['object']
            print('FOUND: IsObjectGrasped',str(parameters))
            new_fluent = Fluent(fluent.name,fluent.type, parameters)
            return IsObjectGrasped(new_fluent.name, new_fluent, self.vrep)

        raise Exception('Cannot Sample fluent:', luent.name)



    def sample_condition(self, name):
        for condition in self.all_condition_nodes:
            if condition.generic_name is name:
                return condition
        raise Exception('Cannot Sample Condition', name)

    def get_subtree_for(self,condition):
        bt = None
        for action in self.all_action_templates:
            print('Trying with action', action.name, 'Effects', action.effects, 'Condition fluents', condition.fluent.parameters_dict.keys())
            if set(action.effects).issubset(set(condition.fluent.parameters_dict.keys())):
                print('The action ', action.name, ' can hold ', condition.name)
                bt = SequenceNode('seq')
                new_action, new_fluent = self.sample_action(action.name,condition.fluent)
                for c in action.conditions:
                    bt.AddChild(self.sample_fluent(c,new_fluent))
                bt.AddChild(new_action)
        if len(bt.GetChildren()) is 1:
            bt = bt.Children[0]
        return bt

    def extend_condition(self,condition):
        bt = FallbackNode('Fallback')
        bt.AddChild(condition)
        bt.AddChild(self.get_subtree_for(condition))

        return bt


    def expand_tree(self,bt):
        if bt.nodeType is 'Condition' and bt.GetStatus() is NodeStatus.Failure:
            print('found the condition to expand:', bt.name)
            return self.extend_condition(bt)
        elif bt.nodeType is 'Sequence':
            print('the node is a sequence', bt.name)
            for index,child in enumerate(bt.GetChildren()):
                bt.SetChild(index,self.expand_tree(child))
        elif bt.nodeType is 'Selector':
            print('the node is a fallback', bt.name)
            for index,child in enumerate(bt.GetChildren()):
                self.expand_tree(child)
        return bt #no changes done to this specific node



    def sample_tree(self,bt):
        pass