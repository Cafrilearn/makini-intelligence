from vosk import Model, KaldiRecognizer   

rate = 16000
model_path_s = r"/home/makini/jetson-voice/pipeline3.6/vosk-model-small-en-us-0.15/vosk-model-small-en-us-0.15" 
model_path = r"/home/makini/jetson-voice/pipeline3.6/vosk-model-small-en-us-0.15/vosk-model-small-en-us-0.15"

asr_model = Model(model_path)
recognizer = KaldiRecognizer(asr_model, rate)

print('Loaded the model')