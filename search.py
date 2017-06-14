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
    action_open_door = ActionTemplate('OpenDoor',['door'],['DoorClosed'],['DoorOpen'])
    action_open_door.show()
    c = ConditionTest('DoorOpen')
    bt = extend_condition(c,[action_open_door])
    #new_draw_tree(bt)





def test():

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

    is_close_to_cube = IsRobotCloseTo('isCloseToCube',green_cube_id, vrep)
    is_cube_grasped = IsObjectGrasped('isCubeGraspedToCube',green_cube_id, vrep)

    move_to_cube = MoveCloseTo('MoveCloseToCube',green_cube_id,vrep)
    grasp_cube = GraspObject('Grasp',green_cube_id,vrep)

    fallback_2.AddChild(is_close_to_cube)
    fallback_2.AddChild(move_to_cube)

    sequence_1.AddChild(fallback_2)
    sequence_1.AddChild(grasp_cube)

    fallback_1.AddChild(is_cube_grasped)
    fallback_1.AddChild(sequence_1)
    bt = fallback_1
    draw_thread = threading.Thread(target=new_draw_tree, args=(bt,))
    draw_thread.start()

    while True:
        bt.Execute()
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
    test()