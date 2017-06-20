from ControlNode import ControlNode
from NodeStatus import *
import time

class SequenceNode(ControlNode):

    def __init__(self,name):
        ControlNode.__init__(self,name)
        self.nodeType = 'Sequence'



    def Execute(self,args = None):
        #print 'Starting Children Threads'
        self.SetStatus(NodeStatus.Idle)
        print('Tick Reached the Sequence Node')


        if True:
        # if self.GetStatus() != NodeStatus.Success and self.GetStatus() != NodeStatus.Failure:

            #check if you have to tick a new child or halt the current
            i = 0
            #try:
            for c in self.Children:
                i = i + 1

                if c.GetStatus() == NodeStatus.Idle:
                    #print 'starting tread ' + c.name + ' from thread ' + str(thread.get_ident())
                    #thread.start_new_thread(c.Execute,())
                    print("SENDING TICK TO:", c.name)
                    if c.nodeType == 'Action':
                        c.SendTick()
                    else:
                        c.Execute(args)
                    print("TICK SENT TO:", c.name)
                    # print '???' + str(i)

                while c.GetStatus() == NodeStatus.Idle:
                    print("+++++++++++++++++++++++++++********************************+++++++++++++++++WAITING FOR :",
                          c.name)
                    time.sleep(0.1)
                print("The child ", c.name ," has responded")


                if c.GetStatus() == NodeStatus.Running:
                    self.SetStatus(NodeStatus.Running)
                    self.SetColor(NodeColor.Gray)
                  #  print 'Breaking'  + str(i)
                    self.HaltChildren(i + 1)
                    break
                elif c.GetStatus() == NodeStatus.Success:
                    c.SetStatus(NodeStatus.Idle)
                    self.SetStatus(NodeStatus.Running)

                    if i == len(self.Children):
                        self.SetStatus(NodeStatus.Success)
                        self.SetColor(NodeColor.Green)
                        break
                        #while self.GetStatus() != NodeStatus.Idle:
                            #time.sleep(0.1)

                elif c.GetStatus() == NodeStatus.Failure:
                    c.SetStatus(NodeStatus.Idle)
                    self.HaltChildren(i + 1)
                    self.SetStatus(NodeStatus.Failure)
                    self.SetColor(NodeColor.Red)

                    #while self.GetStatus() != NodeStatus.Idle:
                    #       time.sleep(0.1)
                    #print 'Failure'  + str(i)
                    break

                else:
                    raise Exception('Node ' +self.name + ' does not recognize the status of child ' + str(i) +'. (1 is the first)' )
        #print 'SEQUENCE DONE'


           # except:
             #   print 'Error'

