from abc import ABCMeta
from LeafNode import LeafNode
import threading
import time

class ActionNode(LeafNode):
    def __init__(self, name, param = ''):
        LeafNode.__init__(self, name)
        self.nodeType = 'Action'
        self.param = param
        self.generic_name = name

        self.lock = threading.Lock()
        print("-----------------CREATING LOCK FOR------------", name)
        self.tick_received = False
        self.execution_thread = threading.Thread(target=self.wait_for_tick, args=(None,))
        self.execution_thread.start()



    def wait_for_tick(self,args):
        while True:
            if self.tick_received:
                # print('Sending TICK to: ', self.name)
                self.tick_received = False
                self.Execute(args)
            time.sleep(0.1)


    def SendTick(self):
        if True:
            if not self.tick_received:
                self.tick_received = True


    def Halt(self):
        super(ActionNode, self).Halt()
        # with self.lock:
        #     self.tick_received = False

