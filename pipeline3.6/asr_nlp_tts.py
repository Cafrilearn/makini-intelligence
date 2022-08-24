import sys 
import os
import json
import pyaudio
import pyttsx3

from jetson_voice import QuestionAnswer, ConfigArgParser
from vosk import Model, KaldiRecognizer  

rate = 16000
cwd = os.getcwd()
asr_model_path_s = cwd + r"/pipeline3.6/vosk-model-small-en-us-0.15/vosk-model-small-en-us-0.15" 
nlp_model = 'distilbert_qa_384'
top_k = 1  # show the top N answers

nlp_model = QuestionAnswer(nlp_model)  # load the QA model
asr_model = Model(asr_model_path_s)

recognizer = KaldiRecognizer(asr_model, rate)
cap = pyaudio.PyAudio()
engine = pyttsx3.init()

stream = cap.open(format=pyaudio.paInt16, channels=1, rate=rate, input=True, frames_per_buffer=8192)

engine.setProperty('rate', 150)
engine.setProperty('volume', 0.7)
stream.start_stream()

builtin_context = {
    "Amazon" : "The Amazon rainforest is a moist broadleaf forest that covers most of the Amazon basin of South America. "
               "This basin encompasses 7,000,000 square kilometres (2,700,000 sq mi), of which 5,500,000 square kilometres "
               "(2,100,000 sq mi) are covered by the rainforest. The majority of the forest is contained within Brazil, "
               "with 60% of the rainforest, followed by Peru with 13%, and Colombia with 10%.", 

    "Human Heart" : "Your heart beats about 90 times a minute. When you are grown up it will beat about 70 times a minute."
              "When you run oround, your body needs a lot more blood and oxygen. The more active you are, the more often your heart needs to beat to supply enough oxygen to the body."
}

context = builtin_context['Human Heart'] 
   
identity = 'Hello, my name is Makini, am here to help you, what do you want to learn from the context below?' 
print('\n' + identity + '\n')
print('\nContext:')
print(context) 

engine.say(identity)
engine.runAndWait()

while True:    
    try:
        data = stream.read(4096)

        if len(data)==0:
            break

        if recognizer.AcceptWaveform(data):
            result = recognizer.Result() 
            result_dict = json.loads(result)
            text_question = result_dict['text']

            print('\n Question : \n') 
            print(text_question)
            print('')

            query = {
            'context' : context,
            'question' : text_question
            }
            
            if(len(text_question) > 0):
                nlp_results = nlp_model(query, top_k=top_k)    
                nlp_results = [nlp_results]

                for result in nlp_results:
                    answer = result['answer']
                    print('Score: ', result['score'])                 
                    print('\n Answer: \n', answer) 
                    
                    engine.say(answer)
                    engine.runAndWait()

                    print('\n Did I give the correct answer? Ask me another question \n')

    except:
        print('input overflowed, trying again!')
        continue   


           

