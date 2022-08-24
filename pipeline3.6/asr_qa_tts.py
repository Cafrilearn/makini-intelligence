import json 
import logging
import pyaudio
import pyttsx3

from vosk import Model, KaldiRecognizer

rate = 44100
model_path = "vosk-model-small-en-us-0.15"

asr_model = Model(model_path)
recognizer = KaldiRecognizer(asr_model, rate)
cap = pyaudio.PyAudio()
engine = pyttsx3.init()

stream = cap.open(format=pyaudio.paInt16, channels=1, rate=rate, input=True, frames_per_buffer=8192)
voices = engine.getProperty('voices')

engine.setProperty('rate', 125)
engine.setProperty('volume', 0.5)
engine.setProperty('voice', voices[2].id)

print('Hello, starting asking any questions now')

stream.start_stream()

while True:
    data = stream.read(4096)
    if len(data) == 0:
        break

    if recognizer.AcceptWaveform(data):
        result = recognizer.Result()
        result_dict = json.loads(result)
        text_result = result_dict['text']
        if(len(text_result) > 0):
            # stop listening temporarily to process current audio
            stream.stop_stream()
            print(f'\n Heard : {text_result} \n ')
            text_result_output = f'You asked, {text_result}'

            engine.say(text_result_output) 

            built_in_context = {
                'interest': 'In finance and economics, interest is payment from a borrower or\
                                            deposit-taking financial institution to a lender or depositor of an amount \
                                            above repayment of the principal sum (that is, the amount borrowed), \
                                            at a particular rate. It is distinct from a fee which the borrower may \
                                            pay the lender or some third party',

                'africa': 'Africa is the second largest continent in the world with a total area of \
                                            around 11.73 million square miles. This  accounts for 5.7 percent of the earth’s \
                                            surface as well as 20 percent of the total surface of land on our planet.',
                'conservation': "Conservation is really not that hard, you just go out and wing it",
               
                'heart': 'Your heart beats about 90 times a minute.\
                                        When you are grown up it will beat about 70 times a minute.\
                                        When you run around, your body needs a lot more blood and oxygen.',
                
                "computers": "Computers are really cool and everybody should learn how to use them and know all things"
            }

            answer = ''

            if 'heart' in text_result or 'hat' in text_result or 'hut' in text_result:
                answer = built_in_context['heart']

            elif 'interest' in text_result or 'intrest' in text_result:
                answer = built_in_context['interest']

            elif 'africa' in text_result or 'afrika' in text_result:
                answer = built_in_context['africa']

            elif 'computer' in text_result or 'computers' in text_result:
                answer = built_in_context['computers']

            elif 'conservation' in text_result or 'conservation' in text_result:
                answer = built_in_context['conservation']

            else:
                answer = 'I could not find the most suitable answer to your question at the moment,\
                         I only have information about the human heart, interest in finance and a fan fact about africa.'

            engine.say(answer)
            engine.runAndWait()

            # start the stream again, as it was stopped to prevent repeating the microphone echo
            stream.start_stream()
