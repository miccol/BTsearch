import sys
sys.path.insert(0, 'bt/')
from SequenceNode import SequenceNode
from FallbackNode import FallbackNode
from NewDraw import new_draw_tree

from ActionTest import ActionTest
from ConditionTest import ConditionTest

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
    def Print(self):
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
    def Print(self):
        print('Name: ', self.name)
        # print('Parameters: ', self.parameters)
        # print('Conditions: ', self.conditions)
        # print('Effect: ', self.effects)

def main():
    print('The program has started')
    drop_cube_at = ActionTemplate('DropAt',['cube','p'],['is_cube_grasped','is_close_to_pos'],['is_cube_at'])
    c = ConditionTest('is_cube_at')
    bt = extend_condition(c,[drop_cube_at])
    new_draw_tree(bt)


def test2():
    vrep = vrep_api()

    green_cube_id = vrep.get_id(b'greenRectangle1')
    youbot_ref_id = vrep.get_id(b'youBot_backReference')
    inv_pose = vrep.get_closest_inverse_pose(green_cube_id, youbot_ref_id)
    youbot_pose = vrep.get_pose(youbot_ref_id,-1)
    vrep.is_object_between_poses(youbot_pose, inv_pose, 0.4)

def test():


    #definition of action templates
    all_action_tmpls = []

    #fluents
    is_robot_close_to_fl = Fluent('is_robot_close_to','is_robot_close_to', {'robot': 0, 'to': 0})
    is_robot_close_to_fl2 = Fluent('is_robot_close_to','is_robot_close_to', {'robot': 0, 'to': 0})
    is_grasped_fl = Fluent('is_object_grasped','is_object_grasped', {'object': 0, 'hand':0})

    is_path_to_object_collision_free_fl = Fluent('is_path_to_object_collision_free_fl','is_path_to_object_collision_free', {'path': 0, 'object': 0})


    move_close_to_tmpl = ActionTemplate('move_close_to',['object'],[is_path_to_object_collision_free_fl],['robot','to'], ConstraintOperativeSubspace(['object','robot'],['','']))
    drop_at_tmpl = ActionTemplate('drop',['object','at'],[is_grasped_fl,is_robot_close_to_fl],['object','at'], ConstraintOperativeSubspace(['p','o'],['']))
    grasp_tmpl = ActionTemplate('grasp',['object'],[is_robot_close_to_fl2],['object','hand'], ConstraintOperativeSubspace(['o'],['']))


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



    root_test = FallbackNode('Fallback')

    condition_test = ConditionTest('C')
    action_test = ActionTest('A')

    root_test.AddChild(condition_test)
    root_test.AddChild(action_test)

    root = SequenceNode('root')
    root.AddChild(sampled_bt)
    draw_thread = threading.Thread(target=new_draw_tree, args=(root,))
    draw_thread.start()
    #
    # while True:
    #     print('Ticking the Tree')
    #     root_test.Execute(None)
    #     time.sleep(2)


    while True:
        print('Ticking the Tree')
        sampled_bt.Execute(None)
        if sampled_bt.GetStatus() is NodeStatus.Failure:
            input("-----------------Extending the Tree-----------------")
            id = search.get_failed_fluent_id(sampled_bt, abstract_bt)
            abstract_bt = search.expand_abstract_tree(abstract_bt, id)
            sampled_bt = search.sample_tree(abstract_bt, sample)
            root.SetChild(0,sampled_bt)
        elif sampled_bt.GetStatus() is NodeStatus.Success:
            print('Done!')
            break
        time.sleep(1)

    sampled_bt.Halt()
    sampled_bt.Execute(None)

    vrep.close_connection()

if __name__ == "__main__":
    #main()
    test()
    # test2()