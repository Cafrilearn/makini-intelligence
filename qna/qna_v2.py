from haystack.nodes import FARMReader
from haystack.utils import clean_wiki_text, convert_files_to_docs

doc_dir = 'makinidocs' # would change depending on subject at hand, e.g science or currency pages
model_path = 'deepset/minilm-uncased-squad2'

docs = convert_files_to_docs(dir_path=doc_dir, clean_func=clean_wiki_text, split_paragraphs=True)
print('Context')
print(docs)

reader = FARMReader(model_path)

print("Ask questions by typing in the terminal") # how many times does the heart beat

while True:
    question = input('makini>')
    result = reader.predict(
        query=question,
        documents=docs,
        top_k=1
    ) 
    answer = str(result['answers'][0])
    answer = answer.split(',')[0]
    print(answer[16:])