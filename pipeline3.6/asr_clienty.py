import json 
import pyaudio
import pyttsx3
import socket

from threading import Thread
from vosk import Model, KaldiRecognizer

rate = 44100
port = 15631
ip_address = '127.0.0.1'
model_path = "vosk-model-small-en-us-0.15"

asr_model = Model(model_path)
recognizer = KaldiRecognizer(asr_model, rate)
cap = pyaudio.PyAudio()
engine = pyttsx3.init()
client = socket.socket()

stream = cap.open(format=pyaudio.paInt16, channels=1, rate=rate, input=True, frames_per_buffer=8192)
voices = engine.getProperty('voices')

engine.setProperty('rate', 125)
engine.setProperty('volume', 0.5)
engine.setProperty('voice', voices[2].id)
client.connect((ip_address, port)) 

def send_receive_data() :
    print('Hello, start asking any questions now')
    stream.start_stream()

    while True:  
        print("Listening for questions")
        data = stream.read(4096)
        if len(data) == 0:
                break

        if recognizer.AcceptWaveform(data):
            result = recognizer.Result()
            result_dict = json.loads(result)
            text_question = result_dict['text']
            if(len(text_question)>0):
                print(text_question)
                client.sendall(text_question.encode())   
                stream.stop_stream()
                
                #wait for respponse from makini server
                while True:
                    print('waiting for response from makini server engine')
                    data = client.recv(1000) 
                    answer = data.decode()
                    if(len(answer)>0):
                        print(answer)
                        engine.say(answer)
                        engine.runAndWait()
                        stream.start_stream()
                        break

 
send_receive_data()