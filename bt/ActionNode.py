from abc import ABCMeta
from LeafNode import LeafNode
import threading
import time
from NodeStatus import *

class ActionNode(LeafNode):
    def __init__(self, name, param = ''):
        LeafNode.__init__(self, name)
        self.nodeType = 'Action'
        self.param = param
        self.generic_name = name

        self.lock = threading.Lock()
        self.tick_received = False
        self.is_destroyed = False

        self.execution_thread = threading.Thread(target=self.wait_for_tick, args=(None,))
        self.execution_thread.start()


    def wait_for_tick(self,args):
        while not self.is_destroyed:
            print('Acquiring Lock 1')
            self.lock.acquire()
            if self.tick_received:
                print('Tick Received')
                self.lock.release()
                print('Releasing Lock 1')

                self.Execute(args)
                print('Acquiring Lock 2')

                self.lock.acquire()
                print('Tick received is now FALSE')
            else:
                print('Tick NOT Received', self.tick_received)
            self.tick_received = False
            self.lock.release()
            print('Releasing Lock 2')

            time.sleep(0.1)


    def SendTick(self):
        print('Acquiring Lock 3')

        with self.lock:
            if not self.tick_received:
                print('Tick received is now TRUE')
                self.SetStatus(NodeStatus.Running)
                self.tick_received = True
        print('Releasing Lock 3')

    def Halt(self):
        print('Acquiring Lock 4')
        super(ActionNode, self).Halt()
        with self.lock:
             self.tick_received = False
        print('Releasing Lock 4')

