#      ******************************************************************
#      *                                                                *
#      *                         DPiRobot Libary                        *
#      *                                                                *
#      *            Stan Reifel                     8/24/2022           *
#      *                                                                *
#      ******************************************************************

from DPiNetwork import DPiNetwork
dpiNetwork = DPiNetwork()


#
# DPiNetwork DPiRobot commands  
#
_CMD_DPiROBOT__PING                                            = 0x00   
_CMD_DPiROBOT__INITIALIZE                                      = 0x01 
_CMD_DPiROBOT__GET_ROBOT_STATE                                 = 0x02    # robot_GetRobotState
_CMD_DPiROBOT__DISABLE_ROBOT_MOTORS                            = 0x03    # enable / disable the stepper motors
_CMD_DPiROBOT__HOME_ROBOT                                      = 0x04    # robot_prepareForMotion / HomeRobot
_CMD_DPiROBOT__ADD_WAYPOINT                                    = 0x05    # robot_AddWaypoint
_CMD_DPiROBOT__ADD_WAYPOINT_ROBOT_COORDS                       = 0x06    # robot_AddWaypoint_RobotCoords
_CMD_DPiROBOT__CALCULATE_CURRENT_POSITION                      = 0x07    # robot_GetCurrentPosition
_CMD_DPiROBOT__CALCULATE_CURRENT_POSITION_ROBOT_COORDS         = 0x08    # robot_GetCurrentPosition_RobotCoords
_CMD_DPiROBOT__GET_CURRENT_POSITION                            = 0x09
_CMD_DPiROBOT__BUFFER_WAYPOINTS_BEFORE_STARTING                = 0X0a

_CMD_DPiROBOT__SET_ROBOT_TYPE                                  = 0x11    # robot_SetRobotType
_CMD_DPiROBOT__SET_ROBOT_DEFAULT_ACCELERATION                  = 0x12    # robot_SetRobotDefaultAcceleration
_CMD_DPiROBOT__SET_ROBOT_DEFAULT_JUNCTION_DEVIATION            = 0x13    # robot_SetRobotDefaultJunctionDeviation
_CMD_DPiROBOT__SET_ROBOT_MIN_MAX_X                             = 0x14    # robot_SetRobotMinMaxX
_CMD_DPiROBOT__SET_ROBOT_MIN_MAX_Y                             = 0x15    # robot_SetRobotMinMaxY
_CMD_DPiROBOT__SET_ROBOT_MIN_MAX_Z                             = 0x16    # robot_SetRobotMinMaxZ
_CMD_DPiROBOT__SET_HOMING_SPEED                                = 0x17    # robot_SetHomingSpeed
_CMD_DPiROBOT__SET_HOMING_METHOD                               = 0x18    # robot_SetHomingMethod
_CMD_DPiROBOT__SET_MAX_HOMING_DISTANCE_DEG_OR_MM               = 0x19    # robot_SetMaxHomingDistanceDegOrMM

_CMD_DPiROBOT__LIN_DELTA_SET_STEPS_PER_MM                      = 0x21    # robot_LinDelta_SetStepsPerMM
_CMD_DPiROBOT__LIN_DELTA_SET_ARM_LENGTH                        = 0x22    # robot_LinDelta_SetArmLength
_CMD_DPiROBOT__LIN_DELTA_SET_TOWER_AND_END_EFFECTOR_RADIUS     = 0x23    # robot_LinDelta_SetTowerAndEndEffectorRadius
_CMD_DPiROBOT__LIN_DELTA_SET_MAX_JOINT_POS                     = 0x24    # robot_LinDelta_SetMaxJointPos

_CMD_DPiROBOT__ROT_DELTA_SET_STEPS_PER_DEGREE                  = 0x31    # robot_RotDelta_SetStepsPerDegree
_CMD_DPiROBOT__ROT_DELTA_SET_ARM_LENGTH                        = 0x32    # robot_RotDelta_SetArmLengths
_CMD_DPiROBOT__ROT_DELTA_SET_BASE_AND_END_EFFECTOR_RADIUS      = 0x33    # robot_RotDelta_SetBaseAndEndEffectorRadius
_CMD_DPiROBOT__ROT_DELTA_SET_UPPER_ARM_HOME_ANGLE_DEGREES      = 0x34    # robot_RotDelta_SetUpperArmHomeAngleDegrees
_CMD_DPiROBOT__ROT_DELTA_SET_MIN_MAX_JOINT_ANGLES              = 0x35    # robot_RotDelta_SetMinMaxJointAngles

_CMD_DPiROBOT__MOTOR_DRIVER_SET_DRIVER_TYPE                    = 0x41    # motorDriver_SetDriverType
_CMD_DPiROBOT__MOTOR_DRIVER_SET_DRIVER_MICROSTEPPING           = 0x42    # motorDriver_SetDriverMicrostepping
_CMD_DPiROBOT__MOTOR_DRIVER_SET_REVERSE_DIRECTION_FLAG         = 0x43    # motorDriver_SetReverseStepDirectionFlag


#
# other constants used by this class
#
_DPiNETWORK_TIMEOUT_PERIOD_MS = 5
_DPiNETWORK_BASE_ADDRESS = 0x14


class DPiRobot:
    #
    # values for CMD_DPiROBOT__SET_ROBOT_TYPE
    #
    ROBOT_TYPE_ROTATIONAL_DELTA = 1
    ROBOT_TYPE_LINEAR_DELTA = 2
    ROBOT_TYPE_CARTESIAN = 3

    #
    # values for motorDriverType
    #
    MOTOR_DRIVER_TYPE_DRV8825 = 1
    MOTOR_DRIVER_TYPE_DM542T = 2

    #
    # values for CMD_DPiROBOT__SET_HOMING_METHOD
    #
    HOMING_METHOD_LIMIT_SWITCHES = 1
    HOMING_METHOD_NONE = 3

    #
    # values for CMD_DPiROBOT__GET_ROBOT_STATE
    #
    STATE_COMMUNICATION_FAILURE = 1             # getting the robot's state failed
    STATE_NOT_READY = 2                         # robot is not ready to accept commands from the host
    STATE_MOTORS_DISABLED = 3                   # motors are disabled
    STATE_NOT_HOMED = 4                         # motors enabled but robot not homed (either hasn't homed or homing failed)
    STATE_HOMING = 5                            # robot is running the homing procedure 
    STATE_STOPPED = 6                           # robot is stopped, waiting for waypoints from the hose
    STATE_PREPARING_TO_MOVE = 7                 # robot has received 1 or more waypoints but hasn't started moving yet
    STATE_MOVING = 8                            # moving to next waypoint
    STATE_WAYPOINT_BUFFER_FULL_FLAG = 0x80      # this bit set in status byte if waypoint buffer is full

    #
    # status values for CMD_DPiROBOT__GET_CURRENT_POSITION
    #
    GET_CURRENT_POSITION_NOT_READY = 1
    GET_CURRENT_POSITION_UNKNOWN = 2
    GET_CURRENT_POSITION_READY = 3

    #
    # attributes local to this class
    #
    _slaveAddress = _DPiNETWORK_BASE_ADDRESS
    _commErrorCount = 0


    #
    # constructor for the DPiRobot class
    #
    def __init__(self):
        pass


    # ---------------------------------------------------------------------------------
    #                                 Private functions 
    # ---------------------------------------------------------------------------------

    #
    # send a command to the DPiRobot, command's additional data must have already been "Pushed". 
    # After this function returns data from the device is retrieved by "Popping"
    #    Enter:  command = command byte
    #    Exit:   True returned on success, else False
    #
    def __sendCommand(self, command: int):
        (results, failedCount) = dpiNetwork.sendCommand(self._slaveAddress, command, _DPiNETWORK_TIMEOUT_PERIOD_MS)
        self._commErrorCount += failedCount;
        return results

    #
    # push a float with 0 digits right of the decimal, as an int32_t, to the transmit buffer 
    #  Enter:  float value 
    #
    def __pushFltPoint0ToInt32(self, value: float):
        dpiNetwork.pushInt32(int(round(value)))

    #
    # push a float with 3 digits right of the decimal, as an int32_t, to the transmit buffer
    #  Enter:  float value 
    #
    def __pushFltPoint3ToInt32(self, value: float):
        dpiNetwork.pushInt32(int(round(value * 1000.0)))

    #
    # push a float with 1 digit right of the decimal, as an int16_t, to the transmit buffer
    #
    def __pushFltPoint1ToInt16(self, value: float):
        dpiNetwork.pushInt16(int(round(value * 10.0)))

    #
    # pop an int16_t, to a float with 1 digits right of the decimal, from the receive buffer
    #
    def __popInt16ToFltPoint1(self):
        return float(dpiNetwork.popInt16()) / 10.0

 
    # ---------------------------------------------------------------------------------
    #                     Public setup and configuration functions 
    # ---------------------------------------------------------------------------------

    #
    # set the DPiRobot board number
    #    Enter:  boardNumber = DPiRobot board number (0 - 3)
    #
    def setBoardNumber(self, boardNumber: int):
        self._slaveAddress = _DPiNETWORK_BASE_ADDRESS + boardNumber
        

    #
    # ping the board
    #    Exit:   True returned on success, else False
    #
    def ping(self):
        return self.__sendCommand(_CMD_DPiROBOT__PING)


    #
    # initialize the board to its "power on" configuration
    #    Exit:   True returned on success, else False
    #
    def initialize(self):
        return self.__sendCommand(_CMD_DPiROBOT__INITIALIZE)


    #
    # disable the stepper motors
    #    Exit:   True returned on success, else False
    #
    def disableMotors(self):
        return self.__sendCommand(_CMD_DPiROBOT__DISABLE_ROBOT_MOTORS)


    #
    # get the count of communication errors
    #    Exit:   0 return if no errors, else count of errors returned
    #
    def getCommErrorCount(self):
        return self._commErrorCount


    # ---------------------------------------------------------------------------------
    #           Public functions for getting the robot's status and position
    # ---------------------------------------------------------------------------------

    #
    # get the robot's status
    #  Exit:   [0]: True returned on success, else False
    #          [1]: Robot status:
    #                  .STATE_NOT_READY = robot is not ready to accept commands from the host
    #                  .STATE_MOTORS_DISABLED = motors are disabled
    #                  .STATE_NOT_HOMED = motors enabled but robot not homed (either hasn't homed or homing failed)
    #                  .STATE_HOMING = robot is running the homing procedure 
    #                  .STATE_STOPPED = robot is stopped, waiting for waypoints from the hose
    #                  .STATE_PREPARING_TO_MOVE = robot has received 1 or more waypoints but hasn't started moving yet
    #                  .STATE_MOVING = moving to next waypoint
    #
    def getRobotStatus(self):
        if self.__sendCommand(_CMD_DPiROBOT__GET_ROBOT_STATE) != True:
            return False, self.STATE_COMMUNICATION_FAILURE

        return True, dpiNetwork.popUint8() & 0x7f


    #
    # get the robot's status along with waypoint buffer full flag
    #  Exit:   [0]: True returned on success, else False
    #          [1]: Robot status:
    #                  .STATE_COMMUNICATION_FAILURE = getting the robot's state failed
    #                  .STATE_NOT_READY = robot is not ready to accept commands from the host
    #                  .STATE_MOTORS_DISABLED = motors are disabled
    #                  .STATE_NOT_HOMED = motors enabled but robot not homed (either hasn't homed or homing failed)
    #                  .STATE_HOMING = robot is running the homing procedure 
    #                  .STATE_STOPPED = robot is stopped, waiting for waypoints from the hose
    #                  .STATE_PREPARING_TO_MOVE = robot has received 1 or more waypoints but hasn't started moving yet
    #                  .STATE_MOVING = moving to next waypoint
    #          [2]: True returned waypoint buffer is full
    #
    def getRobotStatusWithWaypointBufferFullFlg(self):
        if self.__sendCommand(_CMD_DPiROBOT__GET_ROBOT_STATE) != True:
            return False, self.STATE_COMMUNICATION_FAILURE, False

        status = dpiNetwork.popUint8()
        if status & 0x80 != 0:
            waypointBufferFulFlg = True
        else:
            waypointBufferFulFlg = False
            
        status = status & 0x7f
        
        return True, status, waypointBufferFulFlg


    #
    # get robot's current absolute position in the User's Cartesian Coordinates System, these values 
    # updates while in motion, values are signed with units in millimeters
    # Note: This command executes in ~3ms on a Pi4 (1.4ms with the C library)
    #  Exit:   [0]: True returned on success, false on communication error or the robot doesn't know its position
    #          [1]: X coordinate
    #          [2]: Y coordinate
    #          [3]: Z coordinate
    #
    def getCurrentPosition(self):
        #
        # start by requesting that the robot calculates its position
        #
        if self.__sendCommand(_CMD_DPiROBOT__CALCULATE_CURRENT_POSITION) != True:
            return False, 0, 0, 0

        #
        # get the position from the robot, looping until the data is ready
        #
        for _i in range(6):
            if self.__sendCommand(_CMD_DPiROBOT__GET_CURRENT_POSITION) != True:
                return False, 0, 0, 0

            X =  self.__popInt16ToFltPoint1()
            Y =  self.__popInt16ToFltPoint1()
            Z =  self.__popInt16ToFltPoint1()
            getPositionStatus = dpiNetwork.popInt8()

            if getPositionStatus == self.GET_CURRENT_POSITION_READY:
                return True, X, Y, Z

            if getPositionStatus == self.GET_CURRENT_POSITION_UNKNOWN:
                return False, 0, 0, 0

        return False, 0, 0, 0


    #
    # get robot's current absolute position in the Robot's Cartesian Coordinates System, these values 
    # updates while in motion, values are signed with units in millimeters
    # Note: This command executes in ~3ms on a Pi4 (1.4ms with the C library)
    #  Exit:   [0]: True returned on success, false on communication error or the robot doesn't know its position
    #          [1]: X coordinate
    #          [2]: Y coordinate
    #          [3]: Z coordinate
    #
    def getCurrentPosition_RobotCoords(self):
        #
        # start by requesting that the robot calculates its position
        #
        if self.__sendCommand(_CMD_DPiROBOT__CALCULATE_CURRENT_POSITION_ROBOT_COORDS) != True:
            return False, 0, 0, 0

        #
        # get the position from the robot, looping until the data is ready
        #
        for _i in range(6):
            if self.__sendCommand(_CMD_DPiROBOT__GET_CURRENT_POSITION) != True:
                return False, 0, 0, 0

            X =  self.__popInt16ToFltPoint1()
            Y =  self.__popInt16ToFltPoint1()
            Z =  self.__popInt16ToFltPoint1()
            getPositionStatus = dpiNetwork.popInt8()

            if getPositionStatus == self.GET_CURRENT_POSITION_READY:
                return True, X, Y, Z

            if getPositionStatus == self.GET_CURRENT_POSITION_UNKNOWN:
                return False, 0, 0, 0

        return False, 0, 0, 0
 

    # ---------------------------------------------------------------------------------
    #                       Public functions that control the robot
    # ---------------------------------------------------------------------------------

    #
    # add a waypoint (using the User's Cartesian Coordinate System). This will return 
    # right away unless the waypoint buffer is full (in which case it will busy-wait).
    # Note: this command executes in ~4ms on a Pi4 (2.8ms for the C version of this library)
    #    Enter:  X, Y, Z = position to move to, values are signed with units in 
    #               millimeters  (−3276.8mm to 3276.7mm)
    #            speed = speed to travel in mm/sec
    #    Exit:   True returned on success, else False
    #
    def addWaypoint(self, X: float, Y: float, Z: float, speed: float):
        #
        # loop if waypoint buffer is full
        #
        while True:
            #
            # get the robot's status including if the waypoint buffer is full
            #
            results, _status, waypointBufferFullFlg = self.getRobotStatusWithWaypointBufferFullFlg()
            if results != True:
                return False

            #
            # stop waiting if the waypoint buffer is not full
            #
            if waypointBufferFullFlg == False:
                break

        #
        # there is room in the buffer, send the waypoint now
        #
        self.__pushFltPoint1ToInt16(X)
        self.__pushFltPoint1ToInt16(Y)
        self.__pushFltPoint1ToInt16(Z)
        self.__pushFltPoint1ToInt16(speed)
        return self.__sendCommand(_CMD_DPiROBOT__ADD_WAYPOINT)


    #
    # add a waypoint (using the Robot's Cartesian Coordinate System). This will return 
    # right away unless the waypoint buffer is full (in which case it will busy-wait).
    # Note: this command executes in ~4ms on a Pi4 
    #    Enter:  X, Y, Z = position to move to, values are signed with units in 
    #               millimeters  (−3276.8mm to 3276.7mm)
    #            speed = speed to travel in mm/sec
    #    Exit:   True returned on success, else False
    #
    def addWaypoint_RobotCoords(self, X: float, Y: float, Z: float, speed: float):
        #
        # loop if waypoint buffer is full
        #
        while True:
            #
            # get the robot's status including if the waypoint buffer is full
            #
            results, _status, waypointBufferFullFlg = self.getRobotStatusWithWaypointBufferFullFlg()
            if results != True:
                return False

            #
            # stop waiting if the waypoint buffer is not full
            #
            if waypointBufferFullFlg == False:
                break

        #
        # there is room in the buffer, send the waypoint now
        #
        self.__pushFltPoint1ToInt16(X)
        self.__pushFltPoint1ToInt16(Y)
        self.__pushFltPoint1ToInt16(Z)
        self.__pushFltPoint1ToInt16(speed)
        return self.__sendCommand(_CMD_DPiROBOT__ADD_WAYPOINT_ROBOT_COORDS)


    #
    # in some situations buffering waypoints can result in a more "fluid" motion,
    # preventing the robot from briefly stopping between each point as it moves  
    # along a continous path; to use: 1) while the robot is stopped, call this
    # function to enable buffering  2) send the robot all the waypoints along
    # the path  3)after sending the final waypoint immediately call this function
    # again to stop buffering.
    #
    def bufferWaypointsBeforeStartingToMove(self, bufferFlg: bool):
        dpiNetwork.pushUint8(bufferFlg)
        return self.__sendCommand(_CMD_DPiROBOT__BUFFER_WAYPOINTS_BEFORE_STARTING)


    #
    # wait while the robot is moving, return when it has stopped
    #    Exit:   True returned on success, else False
    #
    def waitWhileRobotIsMoving(self):
        self.bufferWaypointsBeforeStartingToMove(False)      # stop buffering waypoints if that was enabled

        while True:
            #
            # get the robot's status
            #
            results, robotStatus = self.getRobotStatus()
            if results != True:
                return False

            #
            # return if status indicates the robot has stopped
            #
            if not ((robotStatus == self.STATE_MOVING) or (robotStatus == self.STATE_PREPARING_TO_MOVE) or
                    (robotStatus == self.STATE_HOMING)):
                return True


    #
    # home the robot, if motors are disabled then enable them first
    #    Enter:  alwaysHomeFlg = True to always run homing procedure
    #                          = False to only run homing procedure if needed
    #    Exit:   True returned on success, else False
    #
    def homeRobot(self, alwaysHomeFlg: bool):
        #
        # verify communication with the robot is working
        #
        results, robotStatus = self.getRobotStatus()
        if (results != True) or (robotStatus == self.STATE_NOT_READY):
            return False

        #
        # start the robot homing
        #
        dpiNetwork.pushUint8(alwaysHomeFlg)
        if self.__sendCommand(_CMD_DPiROBOT__HOME_ROBOT) != True:
            return False

        #
        # check the robot's status until homing is complete
        #
        while True:
            results, robotStatus = self.getRobotStatus()
            if results != True:
                return False

            if robotStatus != self.STATE_HOMING:
                break

        #
        # check if homing failed
        #
        if robotStatus != self.STATE_STOPPED:
            return False

        #
        # homing successful
        #
        return True


