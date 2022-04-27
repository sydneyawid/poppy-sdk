# Emotion recognition for social robot poppy
import cv2 as cv
from deepface import DeepFace
import numpy as np


class poppy_emotion_recognizer():

    def __init__(self, capture):
        super().__init__()
        self.video_capture = capture
        self.window_state = True
        self.emotions = ['angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral']
        self.new_emotion_label = ['Angry', 'Disgusted', 'Frightened', 'Happy', 'Sad', 'Surprised', 'Neutral',
                                  'No Face Detected']
        self.backends = ['opencv', 'ssd', 'dlib', 'mtcnn', 'retinaface']

    def main_window(self):
        """
        Window that will pop up to show face and emotion that is being read
        :return: Nothing
        """
        while self.window_state:
            isTrue, frame = self.video_capture.read()
            frame = cv.flip(frame, 1)  # creates mirror effect between camera and screen

            grayFrame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

            haarCas = cv.CascadeClassifier('Haar_faceRecog.xml')

            faceRectangle = haarCas.detectMultiScale(grayFrame, scaleFactor=1.1, minNeighbors=4)
            biggest_holder = []

            # check if faceRectangle is returning a tuple or list
            if isinstance(faceRectangle, tuple):
                continue
            else:
                areas = [np.round(np.sqrt(np.square(w) + np.square(h))) for x, y, w, h in faceRectangle]
                a_biggest = np.argmax(areas)
                biggest = faceRectangle[a_biggest]
                biggest_holder.append(biggest)

            dominantEmotion = []

            for (x, y, w, h) in biggest_holder:
                try:
                    analyzeEmotion = DeepFace.analyze(frame, actions=["emotion"], detector_backend=self.backends[0])
                    dominantEmotion = analyzeEmotion['dominant_emotion']
                    face_region = analyzeEmotion['region']
                    cv.rectangle(frame, (face_region['x'], face_region['y']), (face_region['x']+face_region['w'],
                                                                               face_region['y']+face_region['h']),
                                 (255, 0, 255), thickness=2)

                except:
                    cv.putText(frame, 'No Face Detected', (x, y - 5), cv.FONT_HERSHEY_SIMPLEX, 1,
                               (0, 255, 255), 2, cv.LINE_4)

                emotion_index = self.emotion_label(str(dominantEmotion))
                # print emotion on detected face
                cv.putText(frame, self.new_emotion_label[emotion_index], (x, y - 5), cv.FONT_HERSHEY_SIMPLEX, 2,
                           (100, 255, 255), 2, cv.LINE_4)

            cv.namedWindow('Emotion Recognizer')
            cv.moveWindow('Emotion Recognizer', 2000, 0)
            cv.imshow('Emotion Recognizer', frame)  # show window

            # press 'esc' to stop program
            if cv.waitKey(1) == 27:
                self.window_state = False

        self.video_capture.release()
        cv.destroyAllWindows()

        cv.waitKey()

    @staticmethod
    def emotion_label(dominant_emotion):
        """
        Changes the emotion label that is printed out on the screen
        :param dominant_emotion: emotion detected by the model
        :return: index of new label
        """
        # check what dominant emotion was detected, based on detected emotion return index for new
        # emotion label and print the new emotion label
        match dominant_emotion:
            case 'angry':
                return 0
            case 'disgust':
                return 1
            case 'fear':
                return 2
            case 'happy':
                return 3
            case 'sad':
                return 4
            case 'surprise':
                return 5
            case 'neutral':
                return 6
            case _:
                return 7
