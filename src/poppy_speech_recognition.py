import os
import pandas as pd
import random
import pyautogui
import time
from playsound import playsound
from threading import Thread
import string
import speech_recognition as sr
from poppy_servo_control import poppy_body_gesture


class poppy_speech():
    # Initialize static variables for use by class
    def __init__(self, csv_path, folder_path, faces_path, input_index):
        self.csv_path = csv_path
        self.folder_path = folder_path
        self.faces_path = faces_path
        self.body_gesture = poppy_body_gesture()
        self.input_index = input_index
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone(device_index=input_index)
        self.greeting_reply_path = self.audio_reply()[0]
        self.farewell_reply_path = self.audio_reply()[5]
        self.name_reply_path = self.audio_reply()[1]
        self.common_reply_path = self.audio_reply()[2]
        self.status_reply_path = self.audio_reply()[3]
        self.nu_reply_path = self.audio_reply()[4]
        self.greeting_text = self.phrase_generation()[0]
        self.farewell_phrase = self.phrase_generation()[1]
        self.name_question = self.phrase_generation()[2]
        self.common_responses = self.phrase_generation()[3]
        self.status_responses = self.phrase_generation()[4]


    def phrase_generation(self):
        # Returns lists of phrases for text matching
        df = pd.read_csv(self.csv_path)
        greeting_text = df['Greetings'].dropna().to_list()
        farewell_phrase = df["Farewell"].dropna().to_list()
        name_question = df["Name"].dropna().to_list()
        common_phrases = df["common_phrases"].dropna().to_list()
        status_question = df["status_questions"].dropna().to_list()

        return greeting_text, farewell_phrase, name_question, common_phrases, status_question

    def audio_reply(self):
        # Returns path to each individual child folder absolute path
        subfolders = [f.path for f in os.scandir(self.folder_path) if f.is_dir()]

        common_reply_path = subfolders[0]
        farewell_reply_path = subfolders[1]
        greeting_reply_path = subfolders[2]
        name_reply_path = subfolders[3]
        nounderstand_reply_path = subfolders[4]
        status_reply_path = subfolders[5]
        return greeting_reply_path, name_reply_path, common_reply_path, status_reply_path, nounderstand_reply_path,\
               farewell_reply_path

    def google_sr_st(self):
        # Returns the text converted from speech
        # Using the microphone, pass the audio stream
        with self.microphone as source:
            # Sits for a second to filter background noise
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
            print("Talk to the robot")

            # Try to pass the audio stream into a variable
            try:
                audio = self.recognizer.listen(source, timeout=5)

            except sr.WaitTimeoutError:
                print("I did not hear you")
                return "I did not hear you"

        # Use audio variable to recognize what is said using google
        # Returns text
        try:
            text = self.recognizer.recognize_google(audio)
            print(text)
            text = text.translate(str.maketrans('', '', string.punctuation))
            return text
        except sr.UnknownValueError:
            print("I could not understand you")
            return "something"


    def greeting(self):
        # When greeting text is matched, play sound, gesture, and change face to happy, then back to neutral
        print("greeting identified")
        pyautogui.press("h")
        happy_thread = Thread(target=self.body_gesture.set_to_happy_no_neck)
        happy_thread.start()
        time.sleep(1.25)
        reply_files = os.listdir(self.greeting_reply_path)
        rand = random.randrange(0, len(reply_files), 1)
        full_file_path = self.greeting_reply_path + "\\" + reply_files[rand]
        playsound(full_file_path)
        pyautogui.press("n")


    def farewell(self):
        # When farewell text is matched, play sound, gesture, and change face to sad and then close the program
        print("farewell detected")
        pyautogui.press("s")
        wave_thread = Thread(target=self.body_gesture.set_to_wave_one_hand, args=(True, False))
        wave_thread.start()
        time.sleep(1.25)
        reply_files = os.listdir(self.farewell_reply_path)
        rand = random.randrange(0, len(reply_files), 1)
        full_file_path = self.farewell_reply_path + "\\" + reply_files[rand]
        print("playing sound")
        playsound(full_file_path)
        pyautogui.press("esc")


    def name(self):
        # When name asked text is matched, play sound, and change face to surprised, then back to neutral
        print("name question asked")
        pyautogui.press("p")
        reply_files = os.listdir(self.name_reply_path)
        rand = random.randrange(0, len(reply_files), 1)
        full_file_path = self.name_reply_path + "\\" + reply_files[rand]
        playsound(full_file_path)
        pyautogui.press("n")


    def common_phrases(self, index):
        # Index of text matched in excel
        # When common question asked text is matched, play sound, and change face to slight smile, then back to neutral
        print("common phrase asked")
        pyautogui.press("q")
        reply_files = os.listdir(self.common_reply_path)
        full_file_path = self.common_reply_path + "\\" + reply_files[index]
        playsound(full_file_path)
        pyautogui.press("n")

    def status_question(self, index):
        # Index of text matched in excel
        # When status question asked text is matched, play sound, and keep face as neutral
        print("status question asked")
        reply_files = os.listdir(self.status_reply_path)
        full_file_path = self.common_reply_path + "\\" + reply_files[index]
        playsound(full_file_path)

    def no_understanding(self):
        # If the text is not matched, gesture and change face to confused then to neutral
        print("can't understand what was said")
        pyautogui.press("c")
        confused_thread = Thread(target=self.body_gesture.set_to_confused_no_neck)
        confused_thread.start()
        time.sleep(1.25)
        reply_files = os.listdir(self.nu_reply_path)
        rand = random.randrange(0, len(reply_files), 1)
        full_file_path = self.nu_reply_path + "\\" + reply_files[rand]
        playsound(full_file_path)
        pyautogui.press("n")

    def response_module(self):
        # Gets text from speech
        text = self.google_sr_st()

        # If else block to match text
        # Once text is matched, spawns a thread for response
        # Returns off if farewell is matched to end main while loop
        if text.lower() in self.greeting_text:
            response_process = Thread(name="response_process", target=self.greeting)
            response_process.start()
            response_process.join()
            on = True
            return on

        elif text.lower() in self.name_question:
            response_process = Thread(name="response_process", target=self.name)
            response_process.start()
            response_process.join()
            on = True
            return on

        elif text.lower() in self.common_responses:
            index = self.common_responses.index(text.lower())
            response_process = Thread(name="response_process", target=self.common_phrases,
                                                args=(index,))
            response_process.start()
            response_process.join()
            on = True
            return on

        elif text.lower() in self.farewell_phrase:
            response_process = Thread(name="response_process", target=self.farewell)
            response_process.start()
            response_process.join()
            on = False
            return on

        elif text.lower() in self.status_responses:
            index = self.common_responses.index(text.lower())
            response_process = Thread(name="response_process", target=self.status_question, args=(index,))
            response_process.start()
            response_process.join()
            on = True
            return on

        else:
            response_process = Thread(name="response_process", target=self.no_understanding)
            response_process.start()
            response_process.join()
            on = True
            return on


