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


import numpy as np

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



    def get_pose(self, object_id, relative_id):
        return self.get_position(object_id, relative_id) + self.get_orientation(object_id, relative_id)


    def set_pose(self, object_id, relative_id, pose):
        self.set_position(object_id, relative_id, pose[0:3])
        self.set_orientation(object_id, relative_id, pose[3:6])





    def close_connection(self):
        # Before closing the connection to V-REP, make sure that the last command sent out had time to arrive. You can guarantee this with (for example):
        vrep.simxGetPingTime(self.clientID)

        # Now close the connection to V-REP:
        vrep.simxFinish(self.clientID)

        print('Connection to remote API server closed')





    def get_inverse_position(self, position, dimension_id, type = 'cube'):
        if type is not 'cube':
            raise Exception('Cannot handle get_inverse_position for type', type)



    def get_closest_inverse_pose(self,object_id,ref_id,type = 'cube'):
        distance = 10000000000
        closest_inverse_pose = None
        dummy_id = self.get_id(b'Disc0')
        shift = 0.3

        #shift in x
        empty_position = [0,0,-0.03,0,0,0]
        empty_position[0] += shift
        self.set_pose(dummy_id,object_id,empty_position)
        self.set_orientation(dummy_id,object_id,[0,0,3.14/2])

        dummy_rel_position = self.get_position(dummy_id,ref_id)
        dummy_distance = np.linalg.norm(dummy_rel_position)
        if dummy_distance < distance:
            closest_inverse_pose = self.get_pose(dummy_id,-1)
            distance = dummy_distance

        empty_position = [0,0,-0.03,0,0,0]
        empty_position[0] -= shift

        self.set_pose(dummy_id,object_id,empty_position)
        self.set_orientation(dummy_id,object_id,[0,0,-3.14/2])
        dummy_rel_position = self.get_position(dummy_id,ref_id)
        dummy_distance = np.linalg.norm(dummy_rel_position)
        if dummy_distance < distance:
            closest_inverse_pose = self.get_pose(dummy_id,-1)
            distance = dummy_distance


        #shift in y
        empty_position = [0,0,-0.03,0,0,0]
        empty_position[1] += shift
        self.set_pose(dummy_id,object_id,empty_position)
        self.set_orientation(dummy_id,object_id,[0,0,3.14])

        dummy_rel_position = self.get_position(dummy_id,ref_id)
        dummy_distance = np.linalg.norm(dummy_rel_position)
        if dummy_distance < distance:
            closest_inverse_pose = self.get_pose(dummy_id,-1)
            distance = dummy_distance

        empty_position = [0,0,-0.03,0,0,0]
        empty_position[1] -= shift

        self.set_pose(dummy_id,object_id,empty_position)
        dummy_rel_position = self.get_position(dummy_id,ref_id)
        dummy_distance = np.linalg.norm(dummy_rel_position)
        if dummy_distance < distance:
            closest_inverse_pose = self.get_pose(dummy_id,-1)
            distance = dummy_distance


        return closest_inverse_pose



    def grasp_object(self,object_id,gripper_id):
        original_position = self.get_position(gripper_id,-1)
        self.set_position(gripper_id, object_id, [0,0,0])
        input('wait')

        vrep.simxSetIntegerSignal(self.clientID, b'gripperCommand', 0, vrep.simx_opmode_oneshot_wait)

        input('wait')

        self.set_position(gripper_id,-1,original_position)






