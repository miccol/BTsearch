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

        self.lock = threading.RLock()
        print("-----------------CREATING LOCK FOR------------", name)
        self.tick_received = False
        self.execution_thread = threading.Thread(target=self.wait_for_tick, args=(None,))
        self.execution_thread.start()



    def wait_for_tick(self,args):
        while True:
            self.lock.acquire()
            if self.tick_received:
                self.lock.release()
                self.Execute(args)

                print('Acquiring lock 2')
                self.lock.acquire()
                print('Acquiring lock 2 DONE')

                self.tick_received = False
            self.lock.release()
            time.sleep(0.1)


    def SendTick(self):
        print('Acquiring lock 3')
        with self.lock:
            if not self.tick_received:
                self.tick_received = True
        print('Acquiring lock 3 DONE')


    def Halt(self):
        super(ActionNode, self).Halt()
        with self.lock:
             self.tick_received = False

