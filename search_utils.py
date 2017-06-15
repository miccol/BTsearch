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




class SearchUtils:
    def __init__(self, all_action_templates, all_action_nodes, all_condition_nodes, vrep_api):
        self.all_action_templates = all_action_templates
        self.all_action_nodes = all_action_nodes
        self.all_condition_nodes = all_condition_nodes
        self.vrep = vrep_api


    def sample_action(self, name, fluent):
        for action in self.all_action_nodes:
            if action.generic_name is name:
                action.fluent = fluent
                return action
        raise Exception('Cannot Sample Action', name)

    def sample_fluent(self, fluent):

        if fluent.type is 'is_robot_close_to':
            print('FOUND: IsRobotCloseTo')
            return IsRobotCloseTo(fluent.name, fluent, self.vrep)
        elif fluent.type is 'is_object_at':
            print('FOUND: IsObjectAt')
            return IsObjectAt(fluent.name, fluent, self.vrep)
        elif fluent.type is 'is_object_grasped':
            print('FOUND: IsObjectGrasped')
            return IsObjectGrasped(fluent.name, fluent, self.vrep)

        raise Exception('Cannot Sample fluent:', fluent.name)



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
                for c in action.conditions:
                    bt.AddChild(self.sample_fluent(c))
                bt.AddChild(self.sample_action(action.name,condition.fluent))
        return bt

    def extend_condition(self,condition):
        bt = FallbackNode('Fallback')
        bt.AddChild(condition)
        bt.AddChild(self.get_subtree_for(condition))

        return bt


    def expand_tree(self,bt):
        if bt.nodeType is 'Condition':
            print('Condition status', bt.GetStatus())

        if bt.nodeType is 'Condition' and bt.GetStatus() is NodeStatus.Failure:
            print('found the condition to expand:', bt.name)
            return self.extend_condition(bt)
        elif bt.nodeType is 'Sequence':
            print('the node is a sequence', bt.name)
            for index,child in enumerate(bt.GetChildren()):
                print('Expanding child:', child.name)
                bt.SetChild(index,self.expand_tree(child))
        elif bt.nodeType is 'Selector':
            print('the node is a fallback', bt.name)
            for index,child in enumerate(bt.GetChildren()):
                self.expand_tree(child)
        return bt #no changes done to this specific node

