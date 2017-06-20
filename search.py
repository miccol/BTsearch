import sys
sys.path.insert(0, 'bt/')
from SequenceNode import SequenceNode
from FallbackNode import FallbackNode
from NewDraw import new_draw_tree
from BTSearchActionNodes import *
from BTSearchConditionNodes import *
from search_utils import *
from vrep_api import vrep_api
import threading

import uuid


class Sample:
    def __init__(self):
        self.robot_position
        self.object_position
        self.position
        self.hand
        self.boolean


class ConstraintOperativeSubspace:
    def __init__(self, variables, constraints):
        self.variables = variables
        self.constraints = constraints

class Fluent:
    def __init__(self, name, type, parameters_dict):
        self.parameters_dict = parameters_dict
        self.name = name
        self.type = type
        self.nodeType = 'Condition'
        self.nodeClass = 'Leaf'
        self.uuid = uuid.uuid4()
        print('Fluent name:', self.name,'Fluent id:', self.uuid)

    def GetColor(self):
        return NodeColor.Black

    def __copy__(self):
        cls = self.__class__
        newobject = cls.__new__(cls)
        newobject.__dict__.update(self.__dict__)
        newobject.parameters_dict = self.parameters_dict
        newobject.name = self.name
        newobject.type = self.type
        return newobject


class ActionTemplate:
    def __init__(self,name,parameters,conditions,effects,cos):
        self.name = name
        self.parameters = {}  # dictionary
        for p in parameters:
            self.parameters.update({p : None})
        self.conditions = conditions #list
        self.effects = effects #list
        self.cos = cos
        self.nodeType = 'Action'
        self.nodeClass = 'Leaf'


    def GetColor(self):
        return NodeColor.Black
    def show(self):
        print('Name: ', self.name)
        print('Parameters: ', self.parameters)
        print('Conditions: ', self.conditions)
        print('Effect: ', self.effects)

def main():
    print('The program has started')
    drop_cube_at = ActionTemplate('DropAt',['cube','p'],['is_cube_grasped','is_close_to_pos'],['is_cube_at'])
    drop_cube_at.show()
    c = ConditionTest('is_cube_at')
    bt = extend_condition(c,[drop_cube_at])
    new_draw_tree(bt)





def test():


    #definition of action templates
    all_action_tmpls = []

    #fluents
    is_robot_close_to_fl = Fluent('is_robot_close_to','is_robot_close_to', {'robot': 0, 'to': 0})
    is_grasped_fl = Fluent('is_object_grasped','is_object_grasped', {'object': 0, 'hand':0})



    move_close_to_tmpl = ActionTemplate('move_close_to',['object'],[],['robot','to'], ConstraintOperativeSubspace(['object','robot'],['','']))
    drop_at_tmpl = ActionTemplate('drop',['object','at'],[is_grasped_fl,is_robot_close_to_fl],['object','at'], ConstraintOperativeSubspace(['p','o'],['']))
    grasp_tmpl = ActionTemplate('grasp',['object'],[is_robot_close_to_fl],['object','hand'], ConstraintOperativeSubspace(['o'],['']))


    all_action_tmpls.append(move_close_to_tmpl)
    all_action_tmpls.append(drop_at_tmpl)
    all_action_tmpls.append(grasp_tmpl)

    vrep = vrep_api()

    green_cube_id = vrep.get_id(b'greenRectangle1')
    goal_id = vrep.get_id(b'goalRegion')

    vrep.open_gripper()


    search = SearchUtils(all_action_tmpls, vrep)


    # is_cube_at_goal_fl = Fluent('is_cube_at_goal','is_object_at', {'object': green_cube_id, 'at': goal_id})
    #
    # abstract_bt = is_cube_at_goal_fl
    # bt = search.sample_fluent(is_cube_at_goal_fl)
    #
    # sampled_bt = search.sample_tree(is_cube_at_goal_fl, {'object': green_cube_id, 'at': goal_id})
    #
    # new_draw_tree(sampled_bt)
    #
    # new_abs_tree = search.extend_fluent(abstract_bt)
    # new_draw_tree(new_abs_tree)
    # sampled_bt = search.sample_tree(new_abs_tree,{'object': green_cube_id, 'at': goal_id})
    # new_draw_tree(sampled_bt)
    # sampled_bt.Halt()
    # sampled_bt.Execute(None)
    # print('********************Searching for failed fluent:')
    #
    # id =  search.get_failed_fluent_id(sampled_bt, new_abs_tree)
    # print('********************ID:', id)
    # new_abs_tree = search.expand_abstract_tree(new_abs_tree, id)
    # new_draw_tree(new_abs_tree)
    # sampled_bt = search.sample_tree(new_abs_tree,{'object': green_cube_id, 'at': goal_id})
    # new_draw_tree(sampled_bt)

    abstract_bt = Fluent('is_cube_at_goal','is_object_at', {'object': green_cube_id, 'at': goal_id})
    # new_draw_tree(abstract_bt)
    sample = {'object': green_cube_id, 'at': goal_id}
    sampled_bt = search.sample_tree(abstract_bt, sample)
    # new_draw_tree(sampled_bt)

    while True:
        sampled_bt.Halt()
        sampled_bt.Execute(None)
        if sampled_bt.GetStatus() is NodeStatus.Failure:
            id = search.get_failed_fluent_id(sampled_bt, abstract_bt)
            abstract_bt = search.expand_abstract_tree(abstract_bt, id)
            # new_draw_tree(abstract_bt)
            sampled_bt = search.sample_tree(abstract_bt, sample)
            # new_draw_tree(sampled_bt)

    return
    root = SequenceNode('root')
    root.AddChild(bt)
    draw_thread = threading.Thread(target=new_draw_tree, args=(root,))
    draw_thread.start()

    while True:
        bt.Halt()
        bt.Execute(None)
        # new_draw_tree(bt)
        if bt.GetStatus() is NodeStatus.Failure:
            bt = search.expand_tree(bt)
            root.SetChild(0,bt)
            bt.Halt()


    vrep.close_connection()

if __name__ == "__main__":
    #main()
    test()