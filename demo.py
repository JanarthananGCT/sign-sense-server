# Importing Libraries

import numpy as np
from flask import Flask, Response
import cv2
import os, sys
import time
import operator

from string import ascii_uppercase

# import tkinter as tk
from PIL import Image, ImageTk

from keras.models import model_from_json


app = Flask(__name__)
class Application:
    def __init__(self):
        self.vs = cv2.VideoCapture("video1.mp4")
        self.current_image = None
        self.current_image2 = None
        self.json_file = open("model_new.json", "r")
        self.model_json = self.json_file.read()
        self.json_file.close()

        self.loaded_model = model_from_json(self.model_json)
        self.loaded_model.load_weights("model_new.h5")

        self.json_file_dru = open("model-bw_dru.json" , "r")
        self.model_json_dru = self.json_file_dru.read()
        self.json_file_dru.close()

        self.loaded_model_dru = model_from_json(self.model_json_dru)
        self.loaded_model_dru.load_weights("model-bw_dru.h5")
        self.json_file_tkdi = open("model-bw_tkdi.json" , "r")
        self.model_json_tkdi = self.json_file_tkdi.read()
        self.json_file_tkdi.close()

        self.loaded_model_tkdi = model_from_json(self.model_json_tkdi)
        self.loaded_model_tkdi.load_weights("model-bw_tkdi.h5")
        self.json_file_smn = open("model-bw_smn.json" , "r")
        self.model_json_smn = self.json_file_smn.read()
        self.json_file_smn.close()

        self.loaded_model_smn = model_from_json(self.model_json_smn)
        self.loaded_model_smn.load_weights("model-bw_smn.h5")

        self.ct = {}
        self.ct['blank'] = 0
        self.blank_flag = 0
        self.cword = ""

        for i in ascii_uppercase:
            self.ct[i] = 0
        
        print("Loaded model from disk")

        # self.root = tk.Tk()
        # self.root.title("Sign Language To Text Conversion")
        # self.root.protocol('WM_DELETE_WINDOW', self.destructor)
        # self.root.geometry("900x900")

        # self.panel = tk.Label(self.root)
        # self.panel.place(x = 100, y = 10, width = 580, height = 580)
        
        # self.panel2 = tk.Label(self.root) # initialize image panel
        # self.panel2.place(x = 400, y = 65, width = 275, height = 275)

        # self.T = tk.Label(self.root)
        # self.T.place(x = 60, y = 5)
        # self.T.config(text = "Sign Language To Text Conversion", font = ("Courier", 30, "bold"))

        # self.panel3 = tk.Label(self.root) # Current Symbol
        # self.panel3.place(x = 500, y = 540)

        # self.T1 = tk.Label(self.root)
        # self.T1.place(x = 10, y = 540)
        # self.T1.config(text = "Character :", font = ("Courier", 30, "bold"))

        # self.panel4 = tk.Label(self.root) # Word
        # self.panel4.place(x = 220, y = 595)

        # self.T2 = tk.Label(self.root)
        # self.T2.place(x = 10,y = 595)
        # self.T2.config(text = "Word :", font = ("Courier", 30, "bold"))

        # self.panel5 = tk.Label(self.root) # Sentence
        # self.panel5.place(x = 350, y = 645)

        # self.T3 = tk.Label(self.root)
        # self.T3.place(x = 10, y = 645)
        # self.T3.config(text = "Sentence :",font = ("Courier", 30, "bold"))

        # self.T4 = tk.Label(self.root)
        # self.T4.place(x = 250, y = 690)
        # self.T4.config(text = "Suggestions :", fg = "red", font = ("Courier", 30, "bold"))

        # self.bt1 = tk.Button(self.root, command = self.action1, height = 0, width = 0)
        # self.bt1.place(x = 26, y = 745)

        # self.bt2 = tk.Button(self.root, command = self.action2, height = 0, width = 0)
        # self.bt2.place(x = 325, y = 745)

        # self.bt3 = tk.Button(self.root, command = self.action3, height = 0, width = 0)
        # self.bt3.place(x = 625, y = 745)
# 

        self.str = ""
        self.word = " "
        self.current_symbol = "Empty"
        self.photo = "Empty"
        self.video_loop()
        self.resultword = ""


    def video_loop(self):
        while True:
                
            ok, frame = self.vs.read()

            if ok:

                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

                blur = cv2.GaussianBlur(gray, (5, 5), 2)

                th3 = cv2.adaptiveThreshold(blur, 255 ,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)

                ret, res = cv2.threshold(th3, 70, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
                
                self.resultword = self.predict(res)
                print(self.resultword)
                if len(self.resultword) >2:
                    return self.resultword
                # return self.resultword

                # self.current_image2 = Image.fromarray(res)

                # imgtk = ImageTk.PhotoImage(image = self.current_image2)

                # self.panel2.imgtk = imgtk
                # self.panel2.config(image = imgtk)

                # self.panel3.config(text = self.current_symbol, font = ("Courier", 30))

                # self.panel4.config(text = self.word, font = ("Courier", 30))

                # self.panel5.config(text = self.str,font = ("Courier", 30))
            else:
                print("not fine")
        
    def predict(self, test_image):

        test_image = cv2.resize(test_image, (128, 128))

        result = self.loaded_model.predict(test_image.reshape(1, 128, 128, 1))


        result_dru = self.loaded_model_dru.predict(test_image.reshape(1 , 128 , 128 , 1))

        result_tkdi = self.loaded_model_tkdi.predict(test_image.reshape(1 , 128 , 128 , 1))

        result_smn = self.loaded_model_smn.predict(test_image.reshape(1 , 128 , 128 , 1))

        prediction = {}

        prediction['blank'] = result[0][0]

        inde = 1

        for i in ascii_uppercase:

            prediction[i] = result[0][inde]

            inde += 1

        #LAYER 1

        prediction = sorted(prediction.items(), key = operator.itemgetter(1), reverse = True)

        self.current_symbol = prediction[0][0]


        #LAYER 2

        if(self.current_symbol == 'D' or self.current_symbol == 'R' or self.current_symbol == 'U'):

            prediction = {}

            prediction['D'] = result_dru[0][0]
            prediction['R'] = result_dru[0][1]
            prediction['U'] = result_dru[0][2]

            prediction = sorted(prediction.items(), key = operator.itemgetter(1), reverse = True)

            self.current_symbol = prediction[0][0]

        if(self.current_symbol == 'D' or self.current_symbol == 'I' or self.current_symbol == 'K' or self.current_symbol == 'T'):

            prediction = {}

            prediction['D'] = result_tkdi[0][0]
            prediction['I'] = result_tkdi[0][1]
            prediction['K'] = result_tkdi[0][2]
            prediction['T'] = result_tkdi[0][3]

            prediction = sorted(prediction.items(), key = operator.itemgetter(1), reverse = True)

            self.current_symbol = prediction[0][0]

        if(self.current_symbol == 'M' or self.current_symbol == 'N' or self.current_symbol == 'S'):

            prediction1 = {}

            prediction1['M'] = result_smn[0][0]
            prediction1['N'] = result_smn[0][1]
            prediction1['S'] = result_smn[0][2]

            prediction1 = sorted(prediction1.items(), key = operator.itemgetter(1), reverse = True)

            if(prediction1[0][0] == 'S'):

                self.current_symbol = prediction1[0][0]

            else:

                self.current_symbol = prediction[0][0]
        
        if(self.current_symbol == 'blank'):

            for i in ascii_uppercase:
                self.ct[i] = 0

        self.ct[self.current_symbol] += 1

        if(self.ct[self.current_symbol] > 40):
            self.cword += self.current_symbol
            
            
            # for i in ascii_uppercase:

            #     print(self.current_symbol, "1")
            #     if i == self.current_symbol:
            #         print(self.current_symbol, "2")
            #         continue

            #     tmp = self.ct[self.current_symbol] - self.ct[i]

            #     if tmp < 0:
            #         tmp *= -1

            #     if tmp <= 20:
            #         self.ct['blank'] = 0

            #         for i in ascii_uppercase:
            #             self.ct[i] = 0
            #         return

            self.ct['blank'] = 0

            for i in ascii_uppercase:
                print(self.ct[i], "d")
                self.ct[i] = 0

            if self.current_symbol == 'blank':

                if self.blank_flag == 0:
                    self.blank_flag = 1

                    if len(self.str) > 0:
                        self.str += " "

                    self.str += self.word
                
                    self.word = ""
                    print("dummy")

            else:

                if(len(self.str) > 16):
                    self.str = ""

                self.blank_flag = 0

                self.word += self.current_symbol
                print(self.current_symbol)
                print(self.word)
        return self.cword

            
    def destructor(self):

        print("Closing Application...")

        self.root.destroy()
        self.vs.release()
        cv2.destroyAllWindows()

# print("Starting Application...")

# (Application()).root.mainloop()
@app.route('/')
def index():
    return "Hello"

@app.route('/video_feed')
def video_feed():
    res = Application().video_loop()
    print(res)
    return res

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
