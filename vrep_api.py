try:
    import vrep
except:
    print ('--------------------------------------------------------------')
    print ('"vrep.py" could not be imported. This means very probably that')
    print ('either "vrep.py" or the remoteApi library could not be found.')
    print ('Make sure both are in the same folder as this file,')
    print ('or appropriately adjust the file "vrep.py"')
    print ('--------------------------------------------------------------')
    print ('')

class vrep_api:
    def __init__(self):
        vrep.simxFinish(-1)  # just in case, close all opened connections
        self.clientID = vrep.simxStart(b'127.0.0.1', 19999, True, True, 5000, 5)  # Connect to V-REP
        if self.clientID != -1:
            print('Connected to remote API server')

        else:
            print('Failed connecting to remote API server')



    def get_id(self, name):

        error_id, target_id = vrep.simxGetObjectHandle(self.clientID, name, vrep.simx_opmode_oneshot_wait)

        if error_id:
            raise Exception('Error! id:' ,name, ' is not in the scene')
        else:
            return target_id


    def get_position(self, object_id, relative_id):

        error_id, position = vrep.simxGetObjectPosition(self.clientID, object_id, relative_id,
                                                        vrep.simx_opmode_oneshot_wait)

        if error_id:
            raise Exception('Error! cannot retrive pose of' ,object_id)
        else:
            return position


    def get_orientation(self, object_id, relative_id):

        error_id, orientation = vrep.simxGetObjectOrientation(self.clientID, object_id, relative_id,
                                                              vrep.simx_opmode_oneshot_wait)

        if error_id:
            raise Exception('Error! cannot retrive position of' ,object_id)
        else:
            return orientation


    def set_position(self, object_id, relative_id, position):

        error_id = vrep.simxSetObjectPosition(self.clientID, object_id, relative_id, position,
                                              vrep.simx_opmode_oneshot_wait)

        if error_id:
            raise Exception('Error! cannot set position of', object_id)


    def set_orientation(self, object_id, relative_id, orientation):

        error_id = vrep.simxSetObjectOrientation(self.clientID, object_id, relative_id, orientation,
                                                 vrep.simx_opmode_oneshot_wait)

        if error_id:
            raise Exception('Error! cannot set orientation of', object_id)

    def close_connection(self):
        # Before closing the connection to V-REP, make sure that the last command sent out had time to arrive. You can guarantee this with (for example):
        vrep.simxGetPingTime(self.clientID)

        # Now close the connection to V-REP:
        vrep.simxFinish(self.clientID)

        print('Connection to remote API server closed')