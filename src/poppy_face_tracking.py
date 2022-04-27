from poppy_servo_control import poppy_body_gesture
import cv2 as cv

class poppy_tracking():

    def __init__(self, capture):
        self.capture = capture
        self.haarCas = None
        self.isTrue = None
        self.faceRectangle = None
        self.frame = None
        self.grayFrame = None
        self.rows, self.cols, self.channels = 0, 0, 0
        self.window_state = True
        self.x_mid_point = 0
        self.y_mid_point = 0

        self.poppy_body = poppy_body_gesture()
        self.poppy_body.set_to_neutral()
        self.servo_pos_neck_left_right = 12.26
        self.servo_pos_neck_up_down = 59.82

    def main_window(self):
        """
        Main window that will show face that is being tracked and cross-hairs
        :return: Nothing
        """
        while self.window_state:
            self.isTrue, self.frame = self.capture.read()
            self.rows, self.cols, self.channels = self.frame.shape  # gets pixel resolution of display window

            self.frame = cv.flip(self.frame, 1)  # creates mirror effect between camera and screen
            self.grayFrame = cv.cvtColor(self.frame, cv.COLOR_BGR2GRAY)
            self.haarCas = cv.CascadeClassifier('Haar_faceRecog.xml')

            self.faceRectangle = self.haarCas.detectMultiScale(self.grayFrame, scaleFactor=1.2, minNeighbors=4)

            for (x, y, w, h) in self.faceRectangle:
                cv.rectangle(self.frame, (x, y), (x + w, y + h), (0, 0, 255), thickness=2)
                self.x_mid_point = int((x + x + w) / 2)  # mid-point of rectangle on face
                self.y_mid_point = int((y + y + h) / 2)  # mid-point of rectangle on face
                
                # check location of the face with reference to the screen. if subjects face is on left side of 
                # mid-point of the screen, then poppy moves head to the right since poppy and the subject are looking
                # at each other. The numbers being used like 280 and 360 were determined by the developer and these 
                # numbers take into account a threshold region that the robot will not do any action. These regions 
                # help with keeping the robots servos stable when subjects face goes to left or right side and top or
                # bottom of the screen. 
                if self.x_mid_point < 280:
                    self.servo_pos_neck_left_right -= 1
                    self.poppy_body.move_servo(self.poppy_body.servo_ids['neck_left_right'],
                                               self.servo_pos_neck_left_right, 0)
                # if subjects face is on the right side of screen then poppy moves head to its left
                elif self.x_mid_point > 360:
                    self.servo_pos_neck_left_right += 1
                    self.poppy_body.move_servo(self.poppy_body.servo_ids['neck_left_right'],
                                               self.servo_pos_neck_left_right, 0)
                # if subjects face is above the mid-point of the screen
                if self.y_mid_point < 210:
                    self.servo_pos_neck_up_down += 1
                    self.poppy_body.move_servo(self.poppy_body.servo_ids['neck_up_down'],
                                               self.servo_pos_neck_up_down, 0)
                # if subjects face is below the mid-point of the screen
                elif self.y_mid_point > 270:
                    self.servo_pos_neck_up_down -= 1
                    self.poppy_body.move_servo(self.poppy_body.servo_ids['neck_up_down'],
                                               self.servo_pos_neck_up_down, 0)
            # generate a grid reference and crosshair to visually see how the subjects face is being tracked. 
            self.grid_reference(self.cols, self.rows, False)
            self.face_crosshair(self.x_mid_point, self.y_mid_point)

            # show on other screen
            cv.namedWindow('Detected Faces')
            cv.moveWindow('Detected Faces', 1980, 0)
            cv.imshow('Detected Faces', self.frame)

            if cv.waitKey(1) == 27:
                self.window_state = False

        self.capture.release()
        cv.destroyAllWindows()

        cv.waitKey()

    def grid_reference(self, cols, rows, reference_squares):
        """
        Grid on screen, blue lines; shows the center of the screen at the Y and X axis
        :param cols: column resolution of the window that pops up
        :param rows: row resolution of the window that pops up
        :param reference_squares: True or False; True = show squares or False = don't show squares
        :return: Nothing
        """
        cv.line(self.frame, (int(cols/2), 0), (int(cols/2), rows), (255, 0, 0), 2)  # Vertical blue line, Y-axis
        cv.line(self.frame, (0, int(rows/2)), (cols, int(rows/2)), (255, 0, 0), 2)  # Horizontal blue line, X-axis
        if reference_squares:
            # draw rectangles
            cv.rectangle(self.frame, (200, 120), (440, 340), (255, 255, 255), thickness=3)
            cv.rectangle(self.frame, (260, 180), (380, 300), (255, 255, 255), thickness=3)

    def face_crosshair(self, xMidPoint, yMidPoint):
        """
        Cross-hair on face; moves along with detected face
        :param xMidPoint: mid-point at x-axis of the square on detected face
        :param yMidPoint:mid-point at y-axis of the square on detected face
        :return: Nothing
        """
        cv.line(self.frame, (xMidPoint, 0), (xMidPoint, 480), (0, 255, 0), 2)
        cv.line(self.frame, (0, yMidPoint), (640, yMidPoint), (0, 255, 0), 2)


