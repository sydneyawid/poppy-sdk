from os import listdir
from os.path import isfile, join
import cv2 as cv


class poppy_face():
    # Initializes class variables
    # Passes in path to folder containing face images
    def __init__(self, file_path):
        super().__init__()
        self.file_path = file_path
        self.image_files = self.format_surface()
        self.window_state = True
        self.emotion = None
        self.face = None
        self.window_name = 'Poppy Face'
        self.timer = 0
        self.counter = 0

    def format_surface(self):
        # returns two dictionary: 1st = surfaces , 2nd = surface rectangles
        directory_files = [f for f in listdir(self.file_path) if isfile(join(self.file_path, f))]
        file_names = [f'{file_name.replace(".png", "")}' for file_name in directory_files]

        # Creates path to files
        directory_files_full = [self.file_path + directory_files[i] for i in range(len(directory_files))]
        directory_dictionary = {file_names[i]: directory_files_full[i] for i in range(len(directory_files_full))}

        return directory_dictionary

    # Reads file into opencv to display
    def setup_image(self, face_emotion):
        face_image = cv.imread(self.image_files[face_emotion])
        return face_image

    # Creates fullscreen window on poppy's face
    def display_emotion(self, facial_emotion, delay):
        image = self.setup_image(facial_emotion)
        cv.namedWindow(self.window_name, cv.WINDOW_NORMAL)
        cv.moveWindow(self.window_name, 1920, 0)
        cv.setWindowProperty(self.window_name, cv.WND_PROP_FULLSCREEN, cv.WINDOW_FULLSCREEN)
        cv.imshow(self.window_name, image)
        cv.waitKey(delay)

    # Displays emotion and changes the emotion displayed depending on keyboard press
    def face_display(self):
        image = self.setup_image('neutral')
        cv.namedWindow(self.window_name, cv.WINDOW_NORMAL)
        cv.moveWindow(self.window_name, 1920, 0)
        cv.setWindowProperty(self.window_name, cv.WND_PROP_FULLSCREEN, cv.WINDOW_FULLSCREEN)

        while True:
            cv.imshow(self.window_name, image)
            pressed_key = cv.waitKey(1)

            if pressed_key == ord('h'):
                image = self.setup_image('happy')

            elif pressed_key == ord('s'):
                image = self.setup_image('sad')

            elif pressed_key == ord('p'):
                image = self.setup_image('surprise')

            elif pressed_key == ord('c'):
                image = self.setup_image('confused')

            elif pressed_key == ord('n'):
                image = self.setup_image('neutral')

            elif pressed_key == ord('q'):
                image = self.setup_image('EOHTLC')

            elif pressed_key == 27:
                break
