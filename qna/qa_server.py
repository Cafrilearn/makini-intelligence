import socket

from threading import Thread
from haystack.nodes import FARMReader
from haystack.utils import clean_wiki_text, convert_files_to_docs

doc_dir = 'makinidocs' # would change depending on subject at hand, e.g science or currency pages
model_path = 'deepset/minilm-uncased-squad2'
port = 15631

docs = convert_files_to_docs(dir_path=doc_dir, clean_func=clean_wiki_text, split_paragraphs=True)
print('Context:\n', docs) 

reader = FARMReader(model_path)
ss = socket.socket()

ss.bind(("", port))
ss.listen() 

print("Makini engine has been initialized successfully, waiting for requests from clients now.") 
def client_task (client_conn, addr):
    while True:
        data = client_conn.recv(1000)
        message_request = data.decode() 
        print(message_request)

        result = reader.predict(
            query=message_request,
            documents=docs,
            top_k=1
        ) 
        answer = str(result['answers'][0])
        answer = answer.split(',')[0]
        answer = answer[16:]
        print(answer)        
        client_conn.sendall(answer.encode())
                
while True:
    conn, addr = ss.accept()
    print('got connection from client at addr :' , addr)
    t = Thread(target = client_task, args = (conn,addr))
    t.start()