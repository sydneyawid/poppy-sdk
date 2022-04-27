import pypot.dynamixel
import time


class poppy_body_gesture():
    def __init__(self):
        super().__init__()
        self.dxl_io = pypot.dynamixel.DxlIO('COM3')
        self.emotion = ''
        self.servo_ids = {'torso_base': 33, 'chest_tilt_left_right': 34, 'chest_tilt_forward_backward': 35,
                          'neck_left_right': 68, 'neck_up_down': 69, 'left_inner_shoulder': 41,
                          'left_outer_shoulder': 42, 'left_bicep': 43, 'left_elbow': 44, 'right_inner_shoulder': 51,
                          'right_outer_shoulder': 52, 'right_bicep': 53, 'right_elbow': 54}
        self.keys = [keys for keys in self.servo_ids]
        self.position_list = []

    def scan_all_servo_limit(self):
        """ Method: poppy_scan_position_limit
            servo I.D's are set
            scans every dynamixel servo and prints out the servo I.D and corresponding
            angle limit.
        """
        with self.dxl_io as io_connect:
            ids = io_connect.scan([33, 34, 35, 68, 69, 41, 42, 43, 44, 51, 52, 53, 54])
            id_angle_limit = io_connect.get_angle_limit(ids)

            keys = [keys for keys in self.servo_ids]

            for i in range(len(ids)):
                print(f'{keys[i]}: Angle Limit = {id_angle_limit[i]}')

    def move_servo(self, servo_id, servo_position, servo_speed):
        """
        Control single servo motor with speed and position
        :param servo_id: id number of servo or use self.servo_ids and index using keys
        :param servo_position: position in degrees
        :param servo_speed: speed at which servo moves; 0-250
        :return: nothing
        """
        self.dxl_io.set_moving_speed({servo_id: servo_speed})
        self.dxl_io.set_goal_position({servo_id: servo_position})

    def get_servo_position(self, servo_id):
        """
        Get position of one servo using its servo id
        :param servo_id:id number of servo or use self.servo_ids and index using keys
        :return: current position of servo in degrees, value used only on python
        """
        return self.dxl_io.get_present_position((servo_id,))[0]

    def get_all_servo_position(self, print_list):
        """
        Scan and get all current servo positions and print
        :param print_list: True = print or False = don't print;
        :return: a list of all current positions
        """
        for keys in self.servo_ids:
            # print(keys)
            servo_position = self.get_servo_position(self.servo_ids[keys])
            self.position_list.append(servo_position)
            if print_list:
                print(f"{keys}: Position = {servo_position}")
        return self.position_list

    def pose_generator(self):
        """
        Use to create new body functions by getting current positions and printing out exact code to use
        to put in new function for new body gesture.
        PROPER USAGE: Put robot in desired pose then call this function
        :return: Nothing
        """
        self.position_list = self.get_all_servo_position(False)
        keys = [keys for keys in self.servo_ids]
        print('use the following lines of code for new position')
        print('servo_speed = 100')

        for i in range(len(self.position_list)):
            print(f"self.move_servo(self.servo_ids['{keys[i]}'],{self.position_list[i]}, servo_speed)")

    def set_to_idle_position(self):
        """
        Set robots pose to idle
        :return: Nothing
        """
        self.emotion = 'neutral'
        servo_speed = 100
        self.move_servo(self.servo_ids['torso_base'], 0.22, servo_speed)
        self.move_servo(self.servo_ids['chest_tilt_left_right'], 2.24, servo_speed)
        self.move_servo(self.servo_ids['chest_tilt_forward_backward'], 0.31, servo_speed)
        self.move_servo(self.servo_ids['neck_left_right'], 12.26, servo_speed)
        self.move_servo(self.servo_ids['neck_up_down'], 59.82, servo_speed)
        self.move_servo(self.servo_ids['left_inner_shoulder'], -0.13, servo_speed)
        self.move_servo(self.servo_ids['left_outer_shoulder'], 79.34, servo_speed)
        self.move_servo(self.servo_ids['left_bicep'], 0.04, servo_speed)
        self.move_servo(self.servo_ids['left_elbow'], -86.46, servo_speed)
        self.move_servo(self.servo_ids['right_inner_shoulder'], 0.57, servo_speed)
        self.move_servo(self.servo_ids['right_outer_shoulder'], -74.68, servo_speed)
        self.move_servo(self.servo_ids['right_bicep'], -0.4, servo_speed)
        self.move_servo(self.servo_ids['right_elbow'], 83.03, servo_speed)

    def set_to_T_position(self):
        """
        Set robots body pose to T position. Also use when re-assembling robot
        :return: Nothing
        """
        self.emotion = 'neutral'
        servo_speed = 100
        self.move_servo(self.servo_ids['torso_base'], 0, servo_speed)
        self.move_servo(self.servo_ids['chest_tilt_left_right'], 0, servo_speed)
        self.move_servo(self.servo_ids['chest_tilt_forward_backward'], 0, servo_speed)
        self.move_servo(self.servo_ids['neck_left_right'], 12.26, servo_speed)
        self.move_servo(self.servo_ids['neck_up_down'], 59.82, servo_speed)
        self.move_servo(self.servo_ids['left_inner_shoulder'], 0, servo_speed)
        self.move_servo(self.servo_ids['left_outer_shoulder'], 0, servo_speed)
        self.move_servo(self.servo_ids['left_bicep'], 0, servo_speed)
        self.move_servo(self.servo_ids['left_elbow'], 0, servo_speed)
        self.move_servo(self.servo_ids['right_inner_shoulder'], 0, servo_speed)
        self.move_servo(self.servo_ids['right_outer_shoulder'], 0, servo_speed)
        self.move_servo(self.servo_ids['right_bicep'], 0, servo_speed)
        self.move_servo(self.servo_ids['right_elbow'], 0, servo_speed)

    def set_to_happy(self):
        """
        Set robots body pose to happy
        :return: Nothing
        """
        servo_speed = 100
        self.set_to_idle_position()
        time.sleep(1)

        self.move_servo(self.servo_ids['left_inner_shoulder'], -93.58, servo_speed)
        self.move_servo(self.servo_ids['left_outer_shoulder'], 33.54, servo_speed)
        self.move_servo(self.servo_ids['left_bicep'], 1.89, servo_speed)
        self.move_servo(self.servo_ids['left_elbow'], -66.77, servo_speed)

        self.move_servo(self.servo_ids['right_inner_shoulder'], 89.36, servo_speed)
        self.move_servo(self.servo_ids['right_outer_shoulder'], -23.87, servo_speed)
        self.move_servo(self.servo_ids['right_bicep'], -2.15, servo_speed)
        self.move_servo(self.servo_ids['right_elbow'], 65.8, servo_speed)
        time.sleep(.5)

        for _ in range(3):
            self.move_servo(self.servo_ids['left_elbow'], -110.02, servo_speed)
            self.move_servo(self.servo_ids['right_elbow'], 114.86, servo_speed)
            time.sleep(.25)
            self.move_servo(self.servo_ids['left_elbow'], -66.77, servo_speed)
            self.move_servo(self.servo_ids['right_elbow'], 65.8, servo_speed)
            time.sleep(.25)
        self.set_to_neutral()

    def set_to_face_tracking(self):
        """
        Set robots pose for face tracking, does not use neck servos
        :return: Nothing
        """
        self.emotion = 'neutral'
        servo_speed = 100
        self.move_servo(self.servo_ids['torso_base'], 0.31, servo_speed)
        self.move_servo(self.servo_ids['chest_tilt_left_right'], 2.95, servo_speed)
        self.move_servo(self.servo_ids['chest_tilt_forward_backward'], 0.48, servo_speed)
        self.move_servo(self.servo_ids['left_inner_shoulder'], -3.03, servo_speed)
        self.move_servo(self.servo_ids['left_outer_shoulder'], 79.16, servo_speed)
        self.move_servo(self.servo_ids['left_bicep'], 1.45, servo_speed)
        self.move_servo(self.servo_ids['left_elbow'], -25.98, servo_speed)
        self.move_servo(self.servo_ids['right_inner_shoulder'], 2.59, servo_speed)
        self.move_servo(self.servo_ids['right_outer_shoulder'], -82.77, servo_speed)
        self.move_servo(self.servo_ids['right_bicep'], -1.63, servo_speed)
        self.move_servo(self.servo_ids['right_elbow'], 19.3, servo_speed)

    def set_to_neutral(self):
        """
        Set robots pose to neutral
        :return: Nothing
        """
        self.emotion = 'neutral'
        servo_speed = 100
        self.move_servo(self.servo_ids['torso_base'], 0.31, servo_speed)
        self.move_servo(self.servo_ids['chest_tilt_left_right'], 2.95, servo_speed)
        self.move_servo(self.servo_ids['chest_tilt_forward_backward'], 0.48, servo_speed)
        self.move_servo(self.servo_ids['neck_left_right'], 11.65, servo_speed)
        self.move_servo(self.servo_ids['neck_up_down'], 60.26, servo_speed)
        self.move_servo(self.servo_ids['left_inner_shoulder'], -3.03, servo_speed)
        self.move_servo(self.servo_ids['left_outer_shoulder'], 79.16, servo_speed)
        self.move_servo(self.servo_ids['left_bicep'], 1.45, servo_speed)
        self.move_servo(self.servo_ids['left_elbow'], -25.98, servo_speed)
        self.move_servo(self.servo_ids['right_inner_shoulder'], 2.59, servo_speed)
        self.move_servo(self.servo_ids['right_outer_shoulder'], -82.77, servo_speed)
        self.move_servo(self.servo_ids['right_bicep'], -1.63, servo_speed)
        self.move_servo(self.servo_ids['right_elbow'], 19.3, servo_speed)

    def set_to_sad(self):
        """
        Set robots pose to sad
        :return: Nothing
        """
        self.emotion = 'sad'
        servo_speed = 25
        self.move_servo(self.servo_ids['torso_base'], 0.4, servo_speed)
        self.move_servo(self.servo_ids['chest_tilt_left_right'], -11.21, servo_speed)
        self.move_servo(self.servo_ids['chest_tilt_forward_backward'], -0.04, servo_speed)
        self.move_servo(self.servo_ids['neck_left_right'], 8.75, servo_speed)
        self.move_servo(self.servo_ids['neck_up_down'], 30.2, servo_speed)
        self.move_servo(self.servo_ids['left_inner_shoulder'], -13.05, servo_speed)
        self.move_servo(self.servo_ids['left_outer_shoulder'], 79.87, servo_speed)
        self.move_servo(self.servo_ids['left_bicep'], 19.47, servo_speed)
        self.move_servo(self.servo_ids['left_elbow'], -19.82, 100)
        self.move_servo(self.servo_ids['right_inner_shoulder'], 9.19, servo_speed)
        self.move_servo(self.servo_ids['right_outer_shoulder'], -83.38, servo_speed)
        self.move_servo(self.servo_ids['right_bicep'], -8.48, servo_speed)
        self.move_servo(self.servo_ids['right_elbow'], 20.44, 100)

    def set_to_frightened(self):
        """
        Set robots pose to frightened
        :return: Nothing
        """
        self.emotion = 'frightened'
        servo_speed = 150

        self.move_servo(self.servo_ids['torso_base'], 0.4, servo_speed)
        self.move_servo(self.servo_ids['chest_tilt_left_right'], 21.58, servo_speed)
        self.move_servo(self.servo_ids['chest_tilt_forward_backward'], 0.84, servo_speed)
        self.move_servo(self.servo_ids['neck_left_right'], 35.03, servo_speed)
        self.move_servo(self.servo_ids['neck_up_down'], 64.66, servo_speed)

        self.move_servo(self.servo_ids['right_inner_shoulder'], 78.29, servo_speed)
        self.move_servo(self.servo_ids['right_outer_shoulder'], -96.75, servo_speed)
        self.move_servo(self.servo_ids['right_bicep'], -40.4, servo_speed)
        self.move_servo(self.servo_ids['right_elbow'], 99.21, servo_speed)

        self.move_servo(self.servo_ids['left_inner_shoulder'], -47.87, servo_speed)
        self.move_servo(self.servo_ids['left_outer_shoulder'], 66.24, servo_speed)
        self.move_servo(self.servo_ids['left_bicep'], 44.0, servo_speed)
        self.move_servo(self.servo_ids['left_elbow'], -114.59, servo_speed)

        time.sleep(2)

        # reset arms
        servo_speed = 100
        self.move_servo(self.servo_ids['left_inner_shoulder'], -3.03, servo_speed)
        self.move_servo(self.servo_ids['left_outer_shoulder'], 79.16, servo_speed)
        self.move_servo(self.servo_ids['left_bicep'], 1.45, servo_speed)
        self.move_servo(self.servo_ids['left_elbow'], -25.98, servo_speed)

        servo_speed = 75
        self.move_servo(self.servo_ids['torso_base'], 0.31, servo_speed)
        self.move_servo(self.servo_ids['chest_tilt_left_right'], 2.95, servo_speed)
        self.move_servo(self.servo_ids['chest_tilt_forward_backward'], 0.48, servo_speed)
        self.move_servo(self.servo_ids['neck_left_right'], 11.65, servo_speed)
        self.move_servo(self.servo_ids['neck_up_down'], 60.26, servo_speed)

        self.move_servo(self.servo_ids['right_inner_shoulder'], 2.59, servo_speed)
        self.move_servo(self.servo_ids['right_outer_shoulder'], -82.77, servo_speed)
        self.move_servo(self.servo_ids['right_bicep'], -1.63, servo_speed)
        self.move_servo(self.servo_ids['right_elbow'], 19.3, servo_speed)

    def set_to_wave_one_hand(self, right_hand, left_hand):
        servo_speed = 100

        if left_hand:
            self.move_servo(self.servo_ids['left_inner_shoulder'], -93.58, servo_speed)
            self.move_servo(self.servo_ids['left_outer_shoulder'], 33.54, servo_speed)
            self.move_servo(self.servo_ids['left_bicep'], 1.89, servo_speed)
            self.move_servo(self.servo_ids['left_elbow'], -66.77, servo_speed)
        if right_hand:
            self.move_servo(self.servo_ids['right_inner_shoulder'], 89.36, servo_speed)
            self.move_servo(self.servo_ids['right_outer_shoulder'], -23.87, servo_speed)
            self.move_servo(self.servo_ids['right_bicep'], -2.15, servo_speed)
            self.move_servo(self.servo_ids['right_elbow'], 65.8, servo_speed)
        time.sleep(1)

        for _ in range(3):
            if right_hand:
                self.move_servo(self.servo_ids['right_elbow'], 114.86, servo_speed)
                time.sleep(.25)
                self.move_servo(self.servo_ids['right_elbow'], 65.8, servo_speed)
            if left_hand:
                self.move_servo(self.servo_ids['left_elbow'], -110.02, servo_speed)
                time.sleep(.25)
                self.move_servo(self.servo_ids['left_elbow'], -66.77, servo_speed)
            time.sleep(.25)
        self.set_to_neutral()

    def set_to_confused(self):
        """
        Set robots pose to confused
        :return: Nothing
        """
        servo_speed = 100
        self.move_servo(self.servo_ids['torso_base'], 0.48, servo_speed)
        self.move_servo(self.servo_ids['chest_tilt_left_right'], 3.21, servo_speed)
        self.move_servo(self.servo_ids['chest_tilt_forward_backward'], 9.89, servo_speed)
        self.move_servo(self.servo_ids['neck_left_right'], -8.92, servo_speed)
        self.move_servo(self.servo_ids['neck_up_down'], 71.87, servo_speed)
        self.move_servo(self.servo_ids['left_inner_shoulder'], -30.64, servo_speed)
        self.move_servo(self.servo_ids['left_bicep'], -19.3, servo_speed)
        self.move_servo(self.servo_ids['left_elbow'], -137.63, servo_speed)
        self.move_servo(self.servo_ids['right_inner_shoulder'], 15.96, servo_speed)
        self.move_servo(self.servo_ids['right_outer_shoulder'], -102.2, servo_speed)
        self.move_servo(self.servo_ids['right_bicep'], 40.57, servo_speed)
        self.move_servo(self.servo_ids['right_elbow'], 139.82, servo_speed)
        servo_speed = 25
        self.move_servo(self.servo_ids['left_outer_shoulder'], 93.05, servo_speed)

        time.sleep(2)
        # shrug shoulders
        servo_speed = 50
        self.move_servo(self.servo_ids['right_inner_shoulder'], 27.21, servo_speed)
        self.move_servo(self.servo_ids['right_outer_shoulder'], -92.7, servo_speed)
        self.move_servo(self.servo_ids['left_inner_shoulder'], -41.01, servo_speed)
        self.move_servo(self.servo_ids['left_outer_shoulder'], 76.0, servo_speed)
        time.sleep(0.25)
        self.move_servo(self.servo_ids['right_inner_shoulder'], 15.96, servo_speed)
        self.move_servo(self.servo_ids['right_outer_shoulder'], -102.2, servo_speed)
        self.move_servo(self.servo_ids['left_inner_shoulder'], -30.64, servo_speed)
        self.move_servo(self.servo_ids['left_outer_shoulder'], 93.05, servo_speed)
        time.sleep(0.5)

        self.set_to_neutral()

    def set_to_angry(self):
        """
        Set robots pose to angry
        :return: Nothing
        """
        self.emotion = 'angry'

        servo_speed = 125
        self.move_servo(self.servo_ids['torso_base'], 0.22, servo_speed)
        self.move_servo(self.servo_ids['chest_tilt_left_right'], -2.33, servo_speed)
        self.move_servo(self.servo_ids['chest_tilt_forward_backward'], 0.75, servo_speed)
        self.move_servo(self.servo_ids['neck_left_right'], 22.81, servo_speed)
        self.move_servo(self.servo_ids['neck_up_down'], 51.91, servo_speed)
        self.move_servo(self.servo_ids['left_inner_shoulder'], -7.6, servo_speed)
        self.move_servo(self.servo_ids['left_outer_shoulder'], 22.2, servo_speed)
        self.move_servo(self.servo_ids['left_bicep'], 82.33, servo_speed)
        self.move_servo(self.servo_ids['right_inner_shoulder'], 14.55, servo_speed)
        self.move_servo(self.servo_ids['right_outer_shoulder'], -24.04, servo_speed)
        self.move_servo(self.servo_ids['right_bicep'], -93.58, servo_speed)

        time.sleep(0.25)
        servo_speed = 150
        self.move_servo(self.servo_ids['right_elbow'], 101.58, servo_speed)
        self.move_servo(self.servo_ids['left_elbow'], -101.49, servo_speed)

        time.sleep(3)

        # reset arms
        servo_speed = 150
        self.move_servo(self.servo_ids['right_bicep'], -1.63, servo_speed)
        self.move_servo(self.servo_ids['left_bicep'], 1.45, servo_speed)
        time.sleep(0.25)
        self.set_to_neutral()

    def set_to_sad_2(self):
        """
        Different variation of sad pose. Use to put robot to a different pose while sad
        :return: Nothing
        """
        servo_speed = 100
        self.move_servo(self.servo_ids['torso_base'], 0.48, servo_speed)
        self.move_servo(self.servo_ids['chest_tilt_left_right'], -11.91, servo_speed)
        self.move_servo(self.servo_ids['chest_tilt_forward_backward'], 0.13, servo_speed)
        self.move_servo(self.servo_ids['neck_left_right'], 9.19, servo_speed)
        self.move_servo(self.servo_ids['neck_up_down'], 58.77, servo_speed)
        self.move_servo(self.servo_ids['left_inner_shoulder'], -13.14, servo_speed)
        self.move_servo(self.servo_ids['left_outer_shoulder'], 79.69, servo_speed)
        self.move_servo(self.servo_ids['left_bicep'], 19.21, servo_speed)
        self.move_servo(self.servo_ids['left_elbow'], -20.09, servo_speed)
        self.move_servo(self.servo_ids['right_inner_shoulder'], 9.19, servo_speed)
        self.move_servo(self.servo_ids['right_outer_shoulder'], -83.3, servo_speed)
        self.move_servo(self.servo_ids['right_bicep'], -8.31, servo_speed)
        self.move_servo(self.servo_ids['right_elbow'], 19.91, servo_speed)

    def set_to_angry_2(self):
        """
        Different variation of angry pose. Use to put robot to a different pose while angry
        :return: Nothing
        """
        servo_speed = 100
        self.move_servo(self.servo_ids['torso_base'], 0.4, servo_speed)
        self.move_servo(self.servo_ids['chest_tilt_left_right'], -1.8, servo_speed)
        self.move_servo(self.servo_ids['chest_tilt_forward_backward'], 1.45, servo_speed)
        self.move_servo(self.servo_ids['neck_left_right'], 9.71, servo_speed)
        self.move_servo(self.servo_ids['neck_up_down'], 60.7, servo_speed)
        self.move_servo(self.servo_ids['left_inner_shoulder'], -7.6, servo_speed)
        self.move_servo(self.servo_ids['left_outer_shoulder'], 23.34, servo_speed)
        self.move_servo(self.servo_ids['left_bicep'], 82.07, servo_speed)
        self.move_servo(self.servo_ids['left_elbow'], -101.14, servo_speed)
        self.move_servo(self.servo_ids['right_inner_shoulder'], 4.26, servo_speed)
        self.move_servo(self.servo_ids['right_outer_shoulder'], -76.18, servo_speed)
        self.move_servo(self.servo_ids['right_bicep'], -42.07, servo_speed)
        self.move_servo(self.servo_ids['right_elbow'], 15.34, servo_speed)

    def set_to_frightened_2(self):
        """
        Different variation of frightened pose. Use to put robot to a different pose while frightened
        :return: Nothing
        """
        servo_speed = 100
        self.move_servo(self.servo_ids['torso_base'], 0.48, servo_speed)
        self.move_servo(self.servo_ids['chest_tilt_left_right'], 23.43, servo_speed)
        self.move_servo(self.servo_ids['chest_tilt_forward_backward'], 1.54, servo_speed)
        self.move_servo(self.servo_ids['neck_left_right'], 15.78, servo_speed)
        self.move_servo(self.servo_ids['neck_up_down'], 49.98, servo_speed)
        self.move_servo(self.servo_ids['left_inner_shoulder'], -22.99, servo_speed)
        self.move_servo(self.servo_ids['left_outer_shoulder'], 89.27, servo_speed)
        self.move_servo(self.servo_ids['left_bicep'], 28.0, servo_speed)
        self.move_servo(self.servo_ids['left_elbow'], -125.76, servo_speed)
        self.move_servo(self.servo_ids['right_inner_shoulder'], 31.34, servo_speed)
        self.move_servo(self.servo_ids['right_outer_shoulder'], -107.03, servo_speed)
        self.move_servo(self.servo_ids['right_bicep'], -66.42, servo_speed)
        self.move_servo(self.servo_ids['right_elbow'], 116.62, servo_speed)

    def set_to_confused_2(self):
        """
        Different variation of confused pose. Use to put robot to a different pose while confused
        :return: Nothing
        """
        servo_speed = 100
        self.move_servo(self.servo_ids['torso_base'], 0.75, servo_speed)
        self.move_servo(self.servo_ids['chest_tilt_left_right'], 3.82, servo_speed)
        self.move_servo(self.servo_ids['chest_tilt_forward_backward'], 10.77, servo_speed)
        self.move_servo(self.servo_ids['neck_left_right'], 7.34, servo_speed)
        self.move_servo(self.servo_ids['neck_up_down'], 68.62, servo_speed)
        self.move_servo(self.servo_ids['left_inner_shoulder'], -8.66, servo_speed)
        self.move_servo(self.servo_ids['left_outer_shoulder'], 72.92, servo_speed)
        self.move_servo(self.servo_ids['left_bicep'], -27.82, servo_speed)
        self.move_servo(self.servo_ids['left_elbow'], -17.27, servo_speed)
        self.move_servo(self.servo_ids['right_inner_shoulder'], 15.34, servo_speed)
        self.move_servo(self.servo_ids['right_outer_shoulder'], -102.29, servo_speed)
        self.move_servo(self.servo_ids['right_bicep'], 40.31, servo_speed)
        self.move_servo(self.servo_ids['right_elbow'], 122.68, servo_speed)

    def set_to_happy_no_neck(self):
        """
        Set robots body pose to happy
        :return: Nothing
        """
        servo_speed = 100
        self.move_servo(self.servo_ids['left_inner_shoulder'], -93.58, servo_speed)
        self.move_servo(self.servo_ids['left_outer_shoulder'], 33.54, servo_speed)
        self.move_servo(self.servo_ids['left_bicep'], 1.89, servo_speed)
        self.move_servo(self.servo_ids['left_elbow'], -66.77, servo_speed)

        self.move_servo(self.servo_ids['right_inner_shoulder'], 89.36, servo_speed)
        self.move_servo(self.servo_ids['right_outer_shoulder'], -23.87, servo_speed)
        self.move_servo(self.servo_ids['right_bicep'], -2.15, servo_speed)
        self.move_servo(self.servo_ids['right_elbow'], 65.8, servo_speed)
        time.sleep(1)

        for _ in range(3):
            self.move_servo(self.servo_ids['left_elbow'], -110.02, servo_speed)
            self.move_servo(self.servo_ids['right_elbow'], 114.86, servo_speed)
            time.sleep(.25)
            self.move_servo(self.servo_ids['left_elbow'], -66.77, servo_speed)
            self.move_servo(self.servo_ids['right_elbow'], 65.8, servo_speed)
            time.sleep(.25)
        self.set_to_neutral()

    def set_to_confused_no_neck(self):
        """
        Set robots pose to confused
        :return: Nothing
        """
        servo_speed = 100
        self.move_servo(self.servo_ids['torso_base'], 0.48, servo_speed)
        self.move_servo(self.servo_ids['chest_tilt_left_right'], 3.21, servo_speed)
        self.move_servo(self.servo_ids['chest_tilt_forward_backward'], 9.89, servo_speed)

        self.move_servo(self.servo_ids['left_inner_shoulder'], -30.64, servo_speed)
        self.move_servo(self.servo_ids['left_bicep'], -19.3, servo_speed)
        self.move_servo(self.servo_ids['left_elbow'], -137.63, servo_speed)

        self.move_servo(self.servo_ids['right_inner_shoulder'], 15.96, servo_speed)
        self.move_servo(self.servo_ids['right_outer_shoulder'], -102.2, servo_speed)
        self.move_servo(self.servo_ids['right_bicep'], 40.57, servo_speed)
        self.move_servo(self.servo_ids['right_elbow'], 139.82, servo_speed)
        servo_speed = 25
        self.move_servo(self.servo_ids['left_outer_shoulder'], 93.05, servo_speed)

        time.sleep(2)
        # shrug shoulders
        servo_speed = 50
        self.move_servo(self.servo_ids['right_inner_shoulder'], 27.21, servo_speed)
        self.move_servo(self.servo_ids['right_outer_shoulder'], -92.7, servo_speed)
        self.move_servo(self.servo_ids['left_inner_shoulder'], -41.01, servo_speed)
        self.move_servo(self.servo_ids['left_outer_shoulder'], 76.0, servo_speed)
        time.sleep(0.25)
        self.move_servo(self.servo_ids['right_inner_shoulder'], 15.96, servo_speed)
        self.move_servo(self.servo_ids['right_outer_shoulder'], -102.2, servo_speed)
        self.move_servo(self.servo_ids['left_inner_shoulder'], -30.64, servo_speed)
        self.move_servo(self.servo_ids['left_outer_shoulder'], 93.05, servo_speed)
        time.sleep(0.5)

        self.set_to_neutral()
