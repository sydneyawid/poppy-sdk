import threading
import cv2
import time
import win32gui
import win32com.client
from poppy_speech_recognition import poppy_speech
from poppy_face_tracking import poppy_tracking
from poppy_face_display import poppy_face
from poppy_emotion_recognition import poppy_emotion_recognizer
from poppy_servo_control import poppy_body_gesture

# Paths to phrases csv file, audio folder, and path to image faces
path_to_csv = ""
audio_folder = ""
faces_path = ""
model_path = ""

# Use 1 if using builtin/only microphone
input_index = 1
run = True

# Main call
if __name__ == '__main__':
    # Cap1 is camera on poppy, cap2 is camera looking at poppy
    cap1 = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    # Initialize emotion recognition
    emotion_recognition = poppy_emotion_recognizer(cap1, model_path)
    # Initialize face tracking
    face_tracking = poppy_tracking(cap1)
    # Initialize speech class
    speech = poppy_speech(path_to_csv, audio_folder, faces_path, input_index)
    # Initialize face display
    face_display = poppy_face(faces_path, model_path)
    # Initialize body gestures
    body_gesture = poppy_body_gesture()

    # Set poppy to robot
    body_gesture.set_to_neutral()

    # Create face tracking process
    face_tracking_process = threading.Thread(target=face_tracking.main_window, args=())
    emotion_detection_process = threading.Thread(target=poppy_emotion_recognizer.main_window, args=())
    face_display_process = threading.Thread(target=face_display.face_display)
    # Starting threading processes
    face_tracking_process.start()
    emotion_detection_process.start()
    face_display_process.start()
    # Sleep until processes start
    time.sleep(15)

    # Runs until farewell text is detected
    while run:
        # Makes sure the opencv face display is active window
        target_window = win32gui.FindWindow(None, 'Poppy Face')
        shell = win32com.client.Dispatch("WScript.Shell")
        shell.SendKeys('%')
        win32gui.SetForegroundWindow(target_window)

        # Run speech module for interaction
        run = speech.response_module()


