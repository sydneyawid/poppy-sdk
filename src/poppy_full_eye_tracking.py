from gaze_tracking import *
import cv2


class eye_tracker():
    def __init__(self, cap1, cap2):
        self.cap1 = cap1
        self.cap2 = cap2

    # For three by three eye tracking grid
    def three_by_three_eye_tracker(self):
        gaze = three_by_three_GazeTracking()

        while True:
            _one, frame1 = self.cap1.read()
            _two, frame2 = self.cap2.read()
            frame1 = cv2.resize(frame1, None, fx=1.5, fy=1.5)
            # Height and Width of the frame
            width = self.cap2.get(cv2.CAP_PROP_FRAME_WIDTH)
            height = self.cap2.get(cv2.CAP_PROP_FRAME_HEIGHT)
            # Cuts width and height into thirds for lines
            first_vert = int(frame2.shape[1] / 3)
            second_vert = int(frame2.shape[1] / 3) * 2
            first_horizontal = int(frame2.shape[0] / 3)
            second_horizontal = int(frame2.shape[0] / 3) * 2

            # Left Side Vertical Line
            cv2.line(frame2, (first_vert, 0), (first_vert, frame2.shape[0]), (255, 0, 0), 2, 1)
            # Right Side Vertical Line
            cv2.line(frame2, (second_vert, 0), (second_vert, frame2.shape[0]), (255, 0, 0), 2, 1)
            # Top Horizontal Line
            cv2.line(frame2, (0, first_horizontal), (frame2.shape[1], first_horizontal), (255, 0, 0), 2, 1)
            # Bottom Horizontal Line
            cv2.line(frame2, (0, second_horizontal), (frame2.shape[1], second_horizontal), (255, 0, 0), 2, 1)

            # Refreshes the frame looking at target
            gaze.refresh(frame1)

            # Calls annotated_frame methods on target camera
            new_frame = gaze.annotated_frame()

            # Initializes variables
            text = ""
            p1 = (0, 0)
            p2 = (0, 0)

            # If gaze is in a certain direction, change text and point for rectangles
            if gaze.is_right():
                text = "Looking right"
                p1 = (second_vert, first_horizontal)
                p2 = (int(width), second_horizontal)

            elif gaze.is_left():
                text = "Looking left"
                p1 = (0, first_horizontal)
                p2 = (first_vert, second_horizontal)

            elif gaze.is_center():
                text = "Looking center"
                p1 = (first_vert, first_horizontal)
                p2 = (second_vert, second_horizontal)

            elif gaze.is_up():
                text = "Looking up"
                p1 = (first_vert, 0)
                p2 = (second_vert, first_horizontal)

            elif gaze.is_down():
                text = "Looking down"
                p1 = (first_vert, second_horizontal)
                p2 = (second_vert, int(height))

            elif gaze.is_upright():
                text = "Looking upper right"
                p1 = (second_vert, 0)
                p2 = (int(width), first_horizontal)

            elif gaze.is_upleft():
                text = "Looking upper left"
                p1 = (0, first_horizontal)
                p2 = (first_vert, 0)

            elif gaze.is_downright():
                text = "Looking down right"
                p1 = (second_vert, second_horizontal)
                p2 = (int(width), int(height))

            elif gaze.is_downleft():
                text = "Looking down left"
                p1 = (0, second_horizontal)
                p2 = (first_vert, int(height))

            # Puts text on frame
            cv2.putText(new_frame, text, (60, 60), cv2.FONT_HERSHEY_DUPLEX, 2, (255, 0, 0), 2)
            # Draws rectangle where they are looking
            cv2.rectangle(frame2, p1, p2, (0, 0, 255), 3, 1)

            # Show both camera feeds
            cv2.imshow("Poppy Perspective", new_frame)
            cv2.imshow("Target Perspective", frame2)

            if cv2.waitKey(1) == 27:
                break

    # For two by two eye tracking
    def two_by_two_eye_tracker(self):
        gaze = two_by_two_GazeTracking()

        while True:
            _one, frame1 = self.cap1.read()
            _two, frame2 = self.cap2.read()
            frame1 = cv2.resize(frame1, None, fx=1.5, fy=1.5)

            # Cuts width and height into thirds for lines
            first_vert = int(frame2.shape[1] / 2)
            first_horizontal = int(frame2.shape[0] / 2)
            # Height and Width of the frame
            height = first_horizontal * 2
            width = first_vert * 2

            # Creates grid
            cv2.line(frame2, (first_vert, 0), (first_vert, frame2.shape[0]), (255, 0, 0), 2, 1)
            cv2.line(frame2, (0, first_horizontal), (frame2.shape[1], first_horizontal), (255, 0, 0), 2, 1)

            # Creates new frame for annotation
            gaze.refresh(frame1)
            new_frame = gaze.annotated_frame()
            text = ""

            # Initialize points for rectangles
            p1 = (0, 0)
            p2 = (0, 0)

            # If else block to highlight where the person is looking
            if gaze.is_upper_left():
                text = "Looking upper left"
                p1 = (0, 0)
                p2 = (first_vert, first_horizontal)

            elif gaze.is_upper_right():
                text = "Looking upper right"
                p1 = (first_vert, 0)
                p2 = (width, first_horizontal)

            elif gaze.is_lower_left():
                text = "Looking lower left"
                p1 = (0, first_horizontal)
                p2 = (first_vert, height)

            elif gaze.is_lower_right():
                text = "Looking lower right"
                p1 = (first_vert, first_horizontal)
                p2 = (width, height)

            # Draws rectangle on where they are looking and adds text
            cv2.putText(new_frame, text, (60, 60), cv2.FONT_HERSHEY_DUPLEX, 2, (255, 0, 0), 2)
            cv2.rectangle(frame2, p1, p2, (0, 0, 255), 3, 1)
            cv2.imshow("Demo", new_frame)
            cv2.imshow("frame2", frame2)

            if cv2.waitKey(1) == 27:
                break

    # For four by four eye tracking
    def four_by_four_eye_tracker(self):
        gaze = four_by_four_GazeTracking()


        while True:
            # Start camera feeds
            _one, frame1 = self.cap1.read()
            _two, frame2 = self.cap2.read()
            # Resize frame
            frame1 = cv2.resize(frame1, None, fx=1.5, fy=1.5)

            # Cuts width and height into thirds for lines
            first_vert = int(frame2.shape[1] / 4)
            first_horizontal = int(frame2.shape[0] / 4)
            second_vert = first_vert * 2
            second_horizontal = first_horizontal * 2
            third_vert = first_vert * 3
            third_horizontal = first_horizontal * 3
            # Height and Width of the frame
            height = int(frame2.shape[0])
            width = int(frame2.shape[1])

            # Creates 4x4 grid
            cv2.line(frame2, (first_vert, 0), (first_vert, frame2.shape[0]), (255, 0, 0), 2, 1)
            cv2.line(frame2, (second_vert, 0), (second_vert, frame2.shape[0]), (255, 0, 0), 2, 1)
            cv2.line(frame2, (third_vert, 0), (third_vert, frame2.shape[0]), (255, 0, 0), 2, 1)
            cv2.line(frame2, (0, first_horizontal), (frame2.shape[1], first_horizontal), (255, 0, 0), 2, 1)
            cv2.line(frame2, (0, second_horizontal), (frame2.shape[1], second_horizontal), (255, 0, 0), 2, 1)
            cv2.line(frame2, (0, third_horizontal), (frame2.shape[1], third_horizontal), (255, 0, 0), 2, 1)

            # Refreshes frame
            gaze.refresh(frame1)
            # Create annotated frame
            new_frame = gaze.annotated_frame()
            # Initializes variables
            text = ""
            p1 = (0, 0)
            p2 = (0, 0)

            # If else block to change text and draw a rectangle
            if gaze.is_far_up_far_left():
                text = "Looking Top Left Corner"
                p1 = (0, 0)
                p2 = (first_vert, first_horizontal)

            elif gaze.is_near_up_far_left():
                text = "Looking Near Up Far Left"
                p1 = (0, first_horizontal)
                p2 = (first_vert, second_horizontal)

            elif gaze.is_near_down_far_left():
                text = "Looking Near Down Far Left"
                p1 = (0, second_horizontal)
                p2 = (first_vert, third_horizontal)

            elif gaze.is_far_down_far_left():
                text = "Looking Bottom Left Corner"
                p1 = (0, third_horizontal)
                p2 = (first_vert, height)

            elif gaze.is_far_up_near_left():
                text = "Looking Far Up Near Left"
                p1 = (first_vert, 0)
                p2 = (second_vert, first_horizontal)

            elif gaze.is_near_up_near_left():
                text = "Looking Near Up Near Left"
                p1 = (first_vert, first_horizontal)
                p2 = (second_vert, second_horizontal)

            elif gaze.is_near_down_near_left():
                text = "Looking Near Down Near Left"
                p1 = (first_vert, second_horizontal)
                p2 = (second_vert, third_horizontal)

            elif gaze.is_far_down_near_left():
                text = "Looking Far Down Near Left"
                p1 = (first_vert, third_horizontal)
                p2 = (second_vert, height)

            elif gaze.is_far_up_near_right():
                text = "Looking Far Up Near Right"
                p1 = (second_vert, 0)
                p2 = (third_vert, first_horizontal)

            elif gaze.is_near_up_near_right():
                text = "Looking Near Up Near Right"
                p1 = (second_vert, first_horizontal)
                p2 = (third_vert, second_horizontal)

            elif gaze.is_near_down_near_right():
                text = "Looking Near Down Near Right"
                p1 = (second_vert, second_horizontal)
                p2 = (third_vert, third_horizontal)

            elif gaze.is_far_down_near_right():
                text = "Looking Far Down Near Right"
                p1 = (second_vert, third_horizontal)
                p2 = (third_vert, height)

            elif gaze.is_far_up_far_right():
                text = "Looking Top Right Corner"
                p1 = (third_vert, 0)
                p2 = (width, first_horizontal)

            elif gaze.is_near_up_far_right():
                text = "Looking Near Up Far Right"
                p1 = (third_vert, first_horizontal)
                p2 = (width, second_horizontal)

            elif gaze.is_near_down_far_right():
                text = "Looking Near Down Far Right"
                p1 = (third_vert, second_horizontal)
                p2 = (width, third_horizontal)

            elif gaze.is_far_down_far_right():
                text = "Looking Bottom Right Corner"
                p1 = (third_vert, third_horizontal)
                p2 = (width, height)

            # Puts text on frame
            cv2.putText(new_frame, text, (60, 60), cv2.FONT_HERSHEY_DUPLEX, 2, (255, 0, 0), 2)

            # Draws rectangle of where they are looking
            cv2.rectangle(frame2, p1, p2, (0, 0, 255), 3, 1)

            # Shows camera feeds
            cv2.imshow("Poppy Perspective", new_frame)
            cv2.imshow("Target Perspective", frame2)

            if cv2.waitKey(1) == 27:
                break



