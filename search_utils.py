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
    def __init__(self, all_action_templates, vrep_api):
        self.all_action_templates = all_action_templates
        self.vrep = vrep_api


    def sample_action_template(self, action_tmpl, parameters_dict):
        new_parameters_dict = copy.deepcopy(parameters_dict)
        action = None
        if action_tmpl.name is 'move_close_to':
            parameters_dict['to'] = parameters_dict['to']
            new_parameters_dict['to'] = new_parameters_dict['to']
            action = MoveCloseTo('move_close_to_'+str(new_parameters_dict['to']), new_parameters_dict, self.vrep)
        elif action_tmpl.name is 'grasp':
            parameters_dict['to'] = parameters_dict['object']
            new_parameters_dict['to'] = new_parameters_dict['object']
            action = GraspObject('grasp_'+str(new_parameters_dict['object']), new_parameters_dict, self.vrep)
        elif action_tmpl.name is 'drop':
            parameters_dict['to'] = parameters_dict['at']
            new_parameters_dict['to'] = new_parameters_dict['at']

            action = DropObject('drop_at_'+str(new_parameters_dict['at']), new_parameters_dict, self.vrep)
        else:
            raise Exception('Cannot Sample Action Template ', action_tmpl.name)

        return action


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
        # print('FLUENT', str(fluent.parameters_dict))

        # parameters = copy.deepcopy(fluent.parameters_dict)
        parameters = fluent.parameters_dict


        if fluent.type is 'is_robot_close_to':
            # print('TRY: IsRobotCloseTo',str(param))
            if param:
                try:
                    parameters['to'] = param['to']
                except:
                    try:
                        parameters['to'] = param['at']
                    except:
                        parameters['to'] = param['object']
            new_fluent = Fluent(fluent.name,fluent.type, parameters)
            # print('OLD fluent', str(fluent.parameters_dict), 'NEW fluent', str(new_fluent.parameters_dict))
            print('SAMPLE FOR FLUENT', fluent.name, ' FOUND: IsRobotCloseTo',str(new_fluent.parameters_dict))

            return IsRobotCloseTo(new_fluent.name, new_fluent, self.vrep)
        elif fluent.type is 'is_object_at':
            if param : parameters['at'] = param['at']
            print('SAMPLE FOR FLUENT', fluent.name, ' FOUND: IsObjectAt',str(parameters))
            new_fluent = Fluent(fluent.name,fluent.type, parameters)
            return IsObjectAt(new_fluent.name, new_fluent, self.vrep)
        elif fluent.type is 'is_object_grasped':
            # print('TRY: IsObjectGrasped',str(param))
            if param : parameters['object'] = param['object']
            print('SAMPLE FOR FLUENT', fluent.name, ' FOUND: IsObjectGrasped',str(parameters))
            new_fluent = Fluent(fluent.name,fluent.type, parameters)
            return IsObjectGrasped(new_fluent.name, new_fluent, self.vrep)
        elif fluent.type is 'is_path_to_object_collision_free':
            # print('TRY: IsObjectGrasped',str(param))
            if param :
                try:
                    parameters['object'] = param['to']
                except:
                    try:
                        parameters['object'] = param['at']
                    except:
                            parameters['object'] = param['object']

            print('SAMPLE FOR FLUENT', fluent.name, ' FOUND: IsObjectGrasped',str(parameters))
            new_fluent = Fluent(fluent.name,fluent.type, parameters)
            return IsPathToObjectCollisionFree(new_fluent.name, new_fluent, self.vrep)
        raise Exception('Cannot Sample fluent:', fluent.name)



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


    def get_abstract_subtree_for(self,fluent):
        bt = None
        for action in self.all_action_templates:
            print('Trying with action', action.name, 'Effects', action.effects, 'Condition fluents', fluent.parameters_dict.keys())
            if set(action.effects).issubset(set(fluent.parameters_dict.keys())):
                print('The action ', action.name, ' can hold ', fluent.name)
                bt = SequenceNode('seq')
                for c in action.conditions:
                    bt.AddChild(c)
                bt.AddChild(action)

        if bt is None:
            raise Exception('Cannot find action with effects', fluent.parameters_dict.keys())
        return bt

        if len(bt.GetChildren()) is 1:
            bt = bt.Children[0]



    def extend_condition(self,condition):
        bt = FallbackNode('Fallback')
        bt.AddChild(condition)
        bt.AddChild(self.get_subtree_for(condition))

        return bt


    def extend_fluent(self,fluent):

        #create new fluent


        if fluent.type is 'is_robot_close_to':
            parameters = {'to': fluent.parameters_dict['to'], 'robot': 0}
        elif fluent.type is 'is_object_at':
            parameters = {'at': fluent.parameters_dict['at'], 'object': fluent.parameters_dict['object']}
        elif fluent.type is 'is_object_grasped':
            parameters = {'object': fluent.parameters_dict['object'], 'hand': 0}
        elif fluent.type is 'is_path_to_object_collision_free_fl':
            parameters = {'object': fluent.parameters_dict['object']}
        else:
            raise Exception('Cannot Extend fluent:', fluent.type)


        new_fluent = Fluent(fluent.name,fluent.type,parameters)
        bt = FallbackNode('Fallback')
        bt.AddChild(new_fluent)
        bt.AddChild(self.get_abstract_subtree_for(new_fluent))

        return bt
    #
    # def get_failed_fluent_id(self,bt, idx = 0):
    #     if bt.nodeClass is not 'Leaf':
    #         #search for fluent id
    #         new_idx = idx
    #         is_failed = False
    #         for child in bt.GetChildren():
    #             new_idx, is_failed = self.get_failed_fluent_id(child, new_idx)
    #             if is_failed:
    #                 print('Failing fluent found: ',new_idx)
    #                 return new_idx, True
    #         if not is_failed:
    #             return new_idx + 1, False
    #
    #     else:
    #         if bt.nodeType is 'Condition' and bt.GetStatus() is NodeStatus.Failure:
    #             print('ID FOUNDDDDDDDDDDDDDDDDDD:', idx, 'name:', bt.name)
    #             return idx + 1, True
    #         else:
    #             return idx + 1, False

    def get_failed_fluent_id(self,bt, abstract_bt):
        if bt.nodeClass is not 'Leaf':
            #search for fluent id
            for child_index, child in enumerate(bt.GetChildren()):
                child_id = self.get_failed_fluent_id(child, abstract_bt.GetChildren()[child_index])
                if child_id is not -1:
                    print('Failing fluent id found: ', child_id)
                    return child_id
            return -1

        else:
            if bt.nodeType is 'Condition' and bt.GetStatus() is NodeStatus.Failure:
                print('ID FOUNDDDDDDDDDDDDDDDDDD:', abstract_bt.uuid, 'name:', bt.name)
                return abstract_bt.uuid
            else:
                return -1




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


    def expand_abstract_tree(self,bt, id):
        print('Trying with: ', bt.name)
        if bt.nodeType is 'Condition':
            print('Trying with ID: ', bt.uuid)

        if bt.nodeType is 'Condition' and bt.uuid == id:
            print('found the fluent to expand:', bt.name)
            return self.extend_fluent(bt)
        elif bt.nodeType is 'Sequence':
            print('the node is a sequence', bt.name)
            for index,child in enumerate(bt.GetChildren()):
                bt.SetChild(index,self.expand_abstract_tree(child, id))
        elif bt.nodeType is 'Selector':
            print('the node is a fallback', bt.name)
            for index,child in enumerate(bt.GetChildren()):
                self.expand_abstract_tree(child, id)
        return bt #no changes done to this specific node



    # def expand_abstract_tree(self,bt, id):
    #     print('Trying with: ', bt.name)
    #     if bt.nodeType is 'Condition':
    #         print('Trying with ID: ', bt.uuid)
    #
    #     if bt.nodeType is 'Condition' and bt.uuid == id:
    #         print('found the fluent to expand:', bt.name)
    #         return self.extend_fluent(bt)
    #     elif bt.nodeType is 'Sequence':
    #         print('the node is a sequence', bt.name)
    #         for index,child in enumerate(bt.GetChildren()):
    #             bt.SetChild(index,self.expand_abstract_tree(child, id))
    #     elif bt.nodeType is 'Selector':
    #         print('the node is a fallback', bt.name)
    #         for index,child in enumerate(bt.GetChildren()):
    #             self.expand_abstract_tree(child, id)
    #     return bt #no changes done to this specific node



    def get_reachability_graph(self,abstract_tree):
        pass

    def sample_reachability_graph(self,rg):
        pass

    def sample_tree(self,abstract_tree, sample):
        sampled_tree = copy.deepcopy(abstract_tree)
        if sampled_tree.__class__.__name__ is 'Fluent':
            return self.sample_fluent(sampled_tree,sample)

        elif sampled_tree.__class__.__name__ is 'ActionTemplate':
            return self.sample_action_template(sampled_tree,sample)
        else:
            #reverse if this is a sequence composition
            if sampled_tree.nodeType is 'Sequence':
                sampled_tree.ReverseChildren()
                abstract_tree.ReverseChildren()
                for index,child in enumerate( sampled_tree.GetChildren()):
                    sampled_child = self.sample_tree(abstract_tree.GetChildren()[index], sample)
                    sampled_tree.SetChild(index,sampled_child)
                sampled_tree.ReverseChildren()
                abstract_tree.ReverseChildren()
            else:
                for index,child in enumerate(sampled_tree.GetChildren()):
                    sampled_child = self.sample_tree(abstract_tree.GetChildren()[index], sample)
                    sampled_tree.SetChild(index,sampled_child)
            return sampled_tree




