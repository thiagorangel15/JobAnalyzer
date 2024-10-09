import spacy
import os
from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.server_api import ServerApi

dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(dotenv_path)

mongo_password = os.getenv('MONGO_PASSWORD')

uri = f"mongodb+srv://dbAdmin:{mongo_password}@jobanalyzermongo.dbjel.mongodb.net/?retryWrites=true&w=majority&appName=JobAnalyzerMongo"
client = MongoClient(uri, server_api=ServerApi('1'))
db = client['JobAnalyzerDB']
collection = db['Jobs']

nlp = spacy.load("pt_core_news_lg")

documents = collection.find({})


def preprocess_text(text):
    doc = nlp(text)
    tokens = [token.lemma_ for token in doc if not token.is_stop and not token.is_punct]
    return " ".join(tokens)

def extract_keywords_spacy(text):
    doc = nlp(text)
    requirements = []
    for ent in doc.ents:
         print(f"Entidade detectada: {ent.text} - Label: {ent.label_}")
         if ent.label_ in ["SKILL","LANGUAGE","TOOL"]:
            requirements.append(ent.text)
    return requirements
        

all_requirements = []
for document in documents:
    preprocessed_text = preprocess_text(document['description'])
    requirements_spacy = extract_keywords_spacy(preprocessed_text)
    all_requirements.append(requirements_spacy)



print(all_requirements)



