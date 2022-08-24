
import logging 

from haystack.nodes import FARMReader, BM25Retriever
from haystack.utils import clean_wiki_text, fetch_archive_from_http, print_answers,\
     convert_files_to_docs, launch_es
from haystack.document_stores import  SQLDocumentStore
from haystack.pipelines import ExtractiveQAPipeline 

#logging
logging.basicConfig(format="%(levelname)s - %(name)s -  %(message)s", level=logging.WARNING)
logging.getLogger("haystack").setLevel(logging.INFO)

#start docker  for elastic server
launch_es()  

# DocumentStore: holds all your data
document_store = SQLDocumentStore()

# downlaod game of thrones docs
# Let's first fetch some documents that we want to query
# Here: 517 Wikipedia articles for Game of Thrones
doc_dir = "data/tutorial1"
s3_url = "https://s3.eu-central-1.amazonaws.com/deepset.ai-farm-qa/datasets/documents/wiki_gameofthrones_txt1.zip"
fetch_archive_from_http(url=s3_url, output_dir=doc_dir)

# Convert files to dicts
# You can optionally supply a cleaning function that is applied to each doc (e.g. to remove footers)
# It must take a str as input, and return a str.
docs = convert_files_to_docs(dir_path=doc_dir, clean_func=clean_wiki_text, split_paragraphs=True)


# We now have a list of dictionaries that we can write to our document store.
# If your texts come from a different source (e.g. a DB), you can of course skip convert_files_to_dicts() and create the dictionaries yourself.
# The default format here is:
# {
#    'content': "<DOCUMENT_TEXT_HERE>",
#    'meta': {'name': "<DOCUMENT_NAME_HERE>", ...}
# }
# (Optionally: you can also add more key-value-pairs here, that will be indexed as fields in Elasticsearch and

# can be accessed later for filtering or shown in the responses of the Pipeline)

# Let's have a look at the first 3 entries:
print('The first three documents')
print(docs[:3])

# Now, let's write the dicts containing documents to our DB.
print('Writing into document store')
document_store.write_documents(docs)

# Clean & load your documents into the DocumentStore
#doc_dir = '/makinidocs'
#dicts = convert_files_to_docs(dir_path=doc_dir, clean_func=clean_wiki_text, split_paragraphs=True)
#document_store.write_documents(dicts)


# Retriever: A Fast and simple algo to identify the most promising candidate documents
retriever = BM25Retriever(document_store)


# Reader: Powerful but slower neural network trained for QA
model_name_1 = "deepset/roberta-base-squad2"
model_name_2 = 'deepset/minilm-uncased-squad2'
reader = FARMReader(model_name_or_path=model_name_2)
print('makini>finished loading model')

# Pipeline: Combines all the components
pipe = ExtractiveQAPipeline(reader, retriever)


# Voilà! Ask a question!
question = "Who is the father of Sansa Stark?"
prediction = pipe.run(query=question)
print_answers(prediction)

