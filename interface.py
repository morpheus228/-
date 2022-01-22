import tensorflow as tf
from tensorflow.keras.models import load_model
from tkinter import *
import tkinter as tk
import win32gui
from PIL import ImageGrab, Image
import numpy as np

model = load_model('model.hdf5')

def predict_digit(img):
    images = np.array(img)[None, ...][:, :, :, 0:1]
    images = tf.image.resize(images,(28, 28))
    res = model.predict(images)[0]
    return np.argmax(res), max(res)
    
class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        
        self.x = self.y = 0
        self.time = 0
        # Создание элементов
        self.canvas = tk.Canvas(self, width=500, height=500, bg = "black", cursor="cross")
        self.label = tk.Label(self, text="", font=("Helvetica", 48))
        self.button_clear = tk.Button(self, text = "Очистить", command = self.clear_all)
        
        # Сетка окна
        self.canvas.grid(row=0, column=0, pady=2, sticky='w', )
        self.label.grid(row=0, column=1,pady=2, padx=2)
        self.button_clear.grid(row=1, column=0, pady=2)
        self.canvas.bind("<B1-Motion>", self.draw_lines)
        
        
    def classify_number(self):
        HWND = self.canvas.winfo_id() 
        rect = win32gui.GetWindowRect(HWND) # получаем координату холста
        im = ImageGrab.grab(rect)
        digit, acc = predict_digit(im)
        self.label.configure(text= str(digit))
        
    def clear_all(self): 
        self.canvas.delete("all")
        
    def draw_lines(self, event):
        self.time = 0
        self.x = event.x
        self.y = event.y
        r=20
        self.canvas.create_oval(self.x-r, self.y-r, self.x + r, self.y + r, fill='white', outline='white')

app = App()

while True:
    app.time += 1
    if app.time > 5000:
        app.classify_number()
        app.time = 0
    app.update()