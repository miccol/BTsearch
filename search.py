import sys
sys.path.insert(0, 'bt/')
from SequenceNode import SequenceNode
from FallbackNode import FallbackNode
from NewDraw import new_draw_tree
from search_utils import *
from vrep_api import vrep_api

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

    vrep = vrep_api()

    vrep.close_connection()

if __name__ == "__main__":
    main()