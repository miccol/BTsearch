from ControlNode import ControlNode
from NodeStatus import *
import time

class FallbackNode(ControlNode):

    def __init__(self,name):
        ControlNode.__init__(self,name)
        self.nodeType = 'Selector'


    def Execute(self,args = None):
        #print 'Starting Children Threads'
        self.SetStatus(NodeStatus.Idle)
        print('Tick Reached the Fallback Node')

        if True:
        # if self.GetStatus() != NodeStatus.Success and self.GetStatus() != NodeStatus.Failure:
            #check if you have to tick a new child or halt the current
            i = 0
            #try:
            for c in self.Children:
                i = i + 1

                print("SENDING TICK TO:", c.name)

                if c.nodeType == 'Action':
                    c.SendTick()
                else:
                    c.Execute(args)
                print("TICK SENT TO:", c.name)

                while c.GetStatus() == NodeStatus.Idle:
                    print("+++++++++++++++++++++++++++********************************+++++++++++++++++WAITING FOR :", c.name)
                    time.sleep(0.1)
                print("The child ", c.name ," has responded")

                if c.GetStatus() == NodeStatus.Running:
                    self.SetStatus(NodeStatus.Running)
                    self.SetColor(NodeColor.Gray)
                  #  print 'Breaking'  + str(i)
                    self.HaltChildren(i + 1)
                    break
                elif c.GetStatus() == NodeStatus.Failure:
                    c.SetStatus(NodeStatus.Idle)

                    if i == len(self.Children):
                        self.SetStatus(NodeStatus.Failure)
                        self.SetColor(NodeColor.Red)
                        break

                elif c.GetStatus() == NodeStatus.Success:
                    if c.nodeClass is not 'Leaf':
                        c.SetStatus(NodeStatus.Idle)
                    self.HaltChildren(i + 1)
                    self.SetStatus(NodeStatus.Success)
                    self.SetColor(NodeColor.Green)
                    break




                else:
                    raise Exception('Node ' +self.name + ' does not recognize the status of child # ' + str(i) +'. (1 is the first)' )



