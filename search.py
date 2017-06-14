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


class ActionTemplate:
    def __init__(self,name,parameters,conditions,effects):
        self.name = name
        self.parameters = {}  # dictionary
        for p in parameters:
            self.parameters.update({p : None})
        self.conditions = conditions #list
        self.effects = effects #list

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



    all_action_tmpls = []
    all_action_nodes = []
    all_condition_nodes = []

    move_close_to_tmpl = ActionTemplate('move_close_to_cube',['object'],[],['is_close_to_cube'])

    drop_at_tmpl = ActionTemplate('drop',['object','p'],['is_cube_grasped','is_close_to_goal'],['is_cube_close_to_goal'])

    grasp_tmpl = ActionTemplate('grasp',['object'],['is_close_to_cube'],['is_cube_grasped'])

    vrep = vrep_api()

    youbot_vehicle_target_id = vrep.get_id(b'youBot_vehicleTargetPosition')
    youbot_ref_id = vrep.get_id(b'youBot_vehicleReference')

    youbot_gripper_target_id = vrep.get_id(b'youBot_gripperPositionTarget')

    green_cube_id = vrep.get_id(b'greenRectangle1')
    goal_id = vrep.get_id(b'goalRegion')


    vrep.open_gripper()
    sequence_1 = SequenceNode('Sequence')
    fallback_1 = FallbackNode('Fallback')
    fallback_2 = FallbackNode('Fallback')

    is_close_to_cube = IsRobotCloseTo('is_close_to_cube',green_cube_id, vrep)
    is_close_to_goal = IsRobotCloseTo('is_close_to_goal',goal_id, vrep)

    is_cube_grasped = IsObjectGrasped('is_cube_grasped',green_cube_id, vrep)
    is_cube_close_to_goal = IsObjectCloseTo('is_cube_close_to_goal',green_cube_id, goal_id, vrep)

    move_to_cube = MoveCloseTo('move_close_to_cube',green_cube_id,vrep)
    grasp_cube = GraspObject('grasp',green_cube_id,vrep)
    drop_cube = DropObject('drop',vrep)


    fallback_2.AddChild(is_close_to_cube)
    fallback_2.AddChild(move_to_cube)

    sequence_1.AddChild(fallback_2)
    sequence_1.AddChild(grasp_cube)

    fallback_1.AddChild(is_cube_grasped)
    fallback_1.AddChild(sequence_1)
    #draw_thread = threading.Thread(target=new_draw_tree, args=(bt,))
    #draw_thread.start()




    all_action_tmpls.append(move_close_to_tmpl)
    all_action_tmpls.append(drop_at_tmpl)
    all_action_tmpls.append(grasp_tmpl)

    all_action_nodes.append(move_to_cube)
    all_action_nodes.append(grasp_cube)
    all_action_nodes.append(drop_cube)

    all_condition_nodes.append(is_close_to_cube)
    all_condition_nodes.append(is_cube_grasped)
    all_condition_nodes.append(is_cube_close_to_goal)
    all_condition_nodes.append(is_close_to_goal)

    search = SearchUtils(all_action_tmpls, all_action_nodes, all_condition_nodes)


    bt = is_cube_close_to_goal


    while True:
        bt.Execute(None)
        new_draw_tree(bt)
        if bt.GetStatus() is NodeStatus.Failure:
            input('ExpandingTree')
            bt = search.expand_tree(bt)


    # vrep.move_close_to_object(green_cube_id)
    #
    # input('wait')
    # vrep.grasp_object(green_cube_id)
    # input('wait')
    #
    # vrep.move_close_to_object(goal_id,'goal')
    #
    # while not vrep.is_robot_close_2d(goal_id,0.3):
    #     print('robot still fall from goal')
    #
    #
    # print('robot close to goal')
    vrep.drop_object()
    vrep.close_connection()

if __name__ == "__main__":
    #main()
    test()