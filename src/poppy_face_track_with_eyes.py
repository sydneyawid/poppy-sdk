import cv2 as cv
import numpy as np
from poppy_face_display import poppy_face
import random
from poppy_servo_control import poppy_body_gesture


class poppy_tracking():
    def __init__(self, capture, image_path, model_path):
        super().__init__()
        self.face_rectangle = None
        self.capture = capture
        self.haar_cascade = cv.CascadeClassifier(model_path)
        self.isTrue = None
        self.faceRectangle = None
        self.frame = None
        self.gray_frame = None
        self.rows, self.cols, self.channels = 0, 0, 0
        self.window_state = True
        self.detected_faces_window = 'Detected Faces'
        self.x_mid_point = 0
        self.y_mid_point = 0

        self.face_attributes_path = image_path
        self.face = poppy_face(self.face_attributes_path)
        self.face_image = self.face.setup_image('neutral')
        self.display_face_window = 'Display Face'

        self.x = None
        self.y = None
        self.w = None
        self.h = None

        self.red = (0, 0, 255)
        self.green = (0, 255, 0)
        self.blue = (255, 0, 0)

        # list to hold the index of the biggest or target face and the rest of the faces
        self.biggest_holder = []
        self.other_face_index = []

        # variables to store values for a reference rectangle
        self.top_y_lim = 0
        self.left_x_lim = 0
        self.bottom_y_lim = 0
        self.right_x_lim = 0

        # variables for idle_face_display function
        self.count = 0
        self.do_once = True
        self.random_number = 0
        self.random_index_number = 0
        self.idle_face_keys = ['EONLC', 'EONMC', 'EONML', 'EONMR']
        self.another_random_number = 0

        self.poppy_body = poppy_body_gesture()
        self.poppy_body.set_to_neutral()
        self.servo_pos_neck_left_right = 12.26
        self.servo_pos_neck_up_down = 59.82

    def main_window(self):
        while self.window_state:
            self.isTrue, self.frame = self.capture.read()
            self.rows, self.cols, self.channels = self.frame.shape  # gets pixel resolution of display window

            # calculate upper, lower, left, and right limits as seen on the screen
            self.top_y_lim = int(self.rows / 4) + 70
            self.bottom_y_lim = int(self.rows * (3 / 4)) - 70
            self.left_x_lim = int(self.cols / 4) + 70
            self.right_x_lim = int(self.cols * (3 / 4)) - 70

            # setup frame, gray frame, and haar cascade
            self.frame = cv.flip(self.frame, 1)  # creates mirror effect between camera and screen
            self.gray_frame = cv.cvtColor(self.frame, cv.COLOR_BGR2GRAY)

            self.face_rectangle = self.haar_cascade.detectMultiScale(self.gray_frame, scaleFactor=1.1, minNeighbors=4)

            # check if face_rectangle is returning a tuple or list; if tuple then no face detected
            if isinstance(self.face_rectangle, tuple):
                cv.putText(self.frame, 'No Face Detected', (50, 50), cv.FONT_HERSHEY_SIMPLEX, 1,
                           self.blue, 2, cv.LINE_4)
                self.idle_face_display()
                cv.imshow(self.display_face_window, self.face_image)
                cv.imshow(self.detected_faces_window, self.frame)

                if cv.waitKey(1) == 27:
                    self.window_state = False
                continue
            else:
                # calculate areas of all detected face on a frame
                areas = [np.round(np.sqrt(np.square(w) + np.square(h))) for (x, y, w, h) in self.face_rectangle]
                a_biggest = np.argmax(areas)
                for i in range(len(areas)):
                    if areas[i] != np.max(areas):
                        self.other_face_index.append(i)
                biggest = self.face_rectangle[a_biggest]
                self.biggest_holder.append(biggest)

            for (x, y, w, h) in self.biggest_holder:
                # nested for loop used to display other detected faces with minimal disturbance to the target face
                for ind in self.other_face_index:
                    (self.x, self.y, self.w, self.h) = self.face_rectangle[ind]
                    cv.rectangle(self.frame, (self.x, self.y), (self.x + self.w, self.y + self.h),
                                 self.red, thickness=2)
                # reset the biggest face holder and other faces index list. This prevents unnecessary rectangles to
                # be displayed on the screen. Also, if used with servos, will prevent confusion on target.
                self.biggest_holder = []
                self.other_face_index = []
                # show the biggest face which is also the target and calculate mid-points of the rectangle around the
                # face
                self.x, self.y, self.w, self.h = x, y, w, h
                cv.rectangle(self.frame, (x, y), (x + w, y + h), self.green, thickness=2)
                self.x_mid_point = int((x + x + w) / 2)  # mid-point of rectangle on face
                self.y_mid_point = int((y + y + h) / 2)  # mid-point of rectangle on face

                self.track_with_neck()

                self.helpful_lines(crosshair=True, reference_line=False, reference_rectangle=True)

            # open window for video camera
            cv.namedWindow(self.detected_faces_window)
            cv.moveWindow(self.detected_faces_window, 0, 0)
            cv.imshow(self.detected_faces_window, self.frame)

            # open window for face
            self.face_location_and_display()
            cv.namedWindow(self.display_face_window, cv.WINDOW_NORMAL)
            cv.moveWindow(self.display_face_window, 1920, 0)
            cv.setWindowProperty(self.display_face_window, cv.WND_PROP_FULLSCREEN, cv.WINDOW_FULLSCREEN)
            cv.imshow(self.display_face_window, self.face_image)

            # press esc to close window
            if cv.waitKey(1) == 27:
                self.window_state = False

        self.capture.release()
        cv.destroyAllWindows()
        cv.waitKey()

    def helpful_lines(self, crosshair, reference_line, reference_rectangle):
        """
        Generate helpful reference lines and shapes on the window that shows the camera feed
        :param crosshair: True or False, shows and follows the biggest face on the frame
        :param reference_line: True or False, used to know where the mid-points of the x-axis and y-axis
        :param reference_rectangle: True or False, shows the rectangle that determines where eyes are going to look
        :return:
        """
        if crosshair:
            cv.line(self.frame, (self.x_mid_point, 0), (self.x_mid_point, self.y_mid_point - int(self.h / 2)),
                    (0, 255, 0), 2)
            cv.line(self.frame, (self.x_mid_point, self.y_mid_point + int(self.h / 2)),
                    (self.x_mid_point, self.rows), (0, 255, 0), 2)

            cv.line(self.frame, (0, self.y_mid_point), (self.x_mid_point - int(self.w / 2), self.y_mid_point),
                    (0, 255, 0), 2)
            cv.line(self.frame, (self.x_mid_point + int(self.w / 2), self.y_mid_point),
                    (self.cols, self.y_mid_point), (0, 255, 0), 2)
        if reference_line:
            cv.line(self.frame, (int(self.cols / 2), 0), (int(self.cols / 2), self.rows), (255, 0, 0),
                    2)  # Vertical blue line, Y-axis
            cv.line(self.frame, (0, int(self.rows / 2)), (self.cols, int(self.rows / 2)), (255, 0, 0),
                    2)  # Horizontal blue line, X-axis
        if reference_rectangle:
            cv.rectangle(self.frame, (self.left_x_lim, self.top_y_lim), (self.right_x_lim, self.bottom_y_lim),
                         (255, 255, 255), thickness=3)

    def face_location_and_display(self):
        # check if face is within the white rectangle on x-axis
        if self.right_x_lim > self.x_mid_point > self.left_x_lim:
            # check if face is within white rectangle on y-axis
            if self.bottom_y_lim > self.y_mid_point > self.top_y_lim:
                self.face_image = self.face.setup_image('EOHTMC')
            # check if face is outside and at top of screen
            elif self.top_y_lim > self.y_mid_point > 0:
                self.face_image = self.face.setup_image('EOHTUC')
            # check if face is outside and at bottom of screen
            else:
                self.face_image = self.face.setup_image('EOHTLC')

        # check if face is outside white rectangle and left side of the screen
        elif self.x_mid_point < self.left_x_lim:
            # check if face is on left middle side
            if self.bottom_y_lim > self.y_mid_point > self.top_y_lim:
                self.face_image = self.face.setup_image('EOHTML')
            elif self.y_mid_point < self.top_y_lim:
                self.face_image = self.face.setup_image('EOHTUL')
            elif self.y_mid_point > self.bottom_y_lim:
                self.face_image = self.face.setup_image('EOHTLL')
        # check if face is outside white rectangle and right side of the screen
        else:
            if self.bottom_y_lim > self.y_mid_point > self.top_y_lim:
                self.face_image = self.face.setup_image('EOHTMR')
            elif self.y_mid_point < self.top_y_lim:
                self.face_image = self.face.setup_image('EOHTUR')
            elif self.y_mid_point > self.bottom_y_lim:
                self.face_image = self.face.setup_image('EOHTLR')
        self.blink_eyes('sleepy', 'sleepy')

    def blink_eyes(self, image_1, image_2):
        if self.do_once:
            self.random_number = random.randint(20, 25)
            self.face_image = self.face.setup_image(image_1)
            self.do_once = False

        self.count += 1

        if self.random_number == self.count:
            self.face_image = self.face.setup_image(image_2)
            self.count = 0
            self.do_once = True

    def idle_face_display(self):
        self.face_image = self.face.setup_image(self.idle_face_keys[self.random_index_number])
        self.blink_eyes('neutral_eye_close', 'neutral_eye_close')

        self.another_random_number = random.randint(5, 10)
        if self.random_number - self.another_random_number == self.count:
            self.random_index_number = random.randint(0, len(self.idle_face_keys) - 1)
            self.face_image = self.face.setup_image(self.idle_face_keys[self.random_index_number])

    def track_with_neck(self):
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
