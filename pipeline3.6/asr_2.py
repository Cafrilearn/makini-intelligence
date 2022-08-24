
from vosk import Model, KaldiRecognizer
import sys
import os
import wave

wave_file_path = '/home/makini/jetson-voice/pipeline/python_example_test.wav'
wf = wave.open(wave_file_path, "rb")
if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getcomptype() != "NONE":
    print ("Audio file must be WAV format mono PCM.")
    raise
    exit (1)

model = Model(lang="en-us")

# You can also specify the possible word or phrase list as JSON list, the order doesn't have to be strict
rec = KaldiRecognizer(model, wf.getframerate(), '["oh one two three four five six seven eight nine zero", "[unk]"]')

while True:
    data = wf.readframes(4000)
    if len(data) == 0:
        break
    if rec.AcceptWaveform(data):
        print(rec.Result())
    else:
        print(rec.PartialResult())

print(rec.FinalResult())