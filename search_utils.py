import sys
sys.path.insert(0, 'bt/')
#
from BehaviorTree import *
from SequenceNode import SequenceNode
from FallbackNode import FallbackNode
from ActionTest import ActionTest
from ConditionTest import ConditionTest

def get_subtree_for(condition,all_action_templates):
    bt = None
    for action in all_action_templates:
        if condition in action.effects:
            print('The action ', action.name, ' can hold ', condition)
            bt = SequenceNode('seq')
            for c in action.conditions:
                bt.AddChild(ConditionTest(c))
            bt.AddChild(ActionTest(action.name))
    return bt


def extend_condition(condition,all_action_templates):
    bt = FallbackNode('F')
    bt.AddChild(condition)
    bt.AddChild(get_subtree_for(condition.name,all_action_templates))

    return bt