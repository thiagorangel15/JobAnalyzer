import spacy
import os
from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from urllib.parse import quote_plus
from transformers import pipeline
from transformers import AutoTokenizer  # Or BertTokenizer
from transformers import AutoModelForPreTraining  # Or BertForPreTraining for loading pretraining heads
from transformers import AutoModel  # or BertModel, for BERT without pretraining heads



# Load environment variables and MongoDB credentials
dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(dotenv_path)
mongo_password = os.getenv('MONGO_PASSWORD')
username = quote_plus("dbAdmin")
password = quote_plus(os.getenv('MONGO_PASSWORD'))
uri = f"mongodb+srv://{username}:{password}@jobanalyzermongo.dbjel.mongodb.net/?retryWrites=true&w=majority&appName=JobAnalyzerMongo"
client = MongoClient(uri, server_api=ServerApi('1'))
db = client['JobAnalyzerDB']
collection = db['Jobs']

# Load spacy model and BERT pipeline
nlp = spacy.load("pt_core_news_lg")

model = AutoModelForPreTraining.from_pretrained('neuralmind/bert-large-portuguese-cased')
tokenizer = AutoTokenizer.from_pretrained('neuralmind/bert-large-portuguese-cased', do_lower_case=False)
bert = pipeline("ner",model=model, tokenizer=tokenizer)



documents = collection.find({})


def preprocess_text(text: str) -> str:
    """
    Preprocess a text by removing stopwords and punctuation and lemmatizing the remaining words.

    Args:
        text (str): The input text.

    Returns:
        str: The preprocessed text.
    """
    doc = nlp(text)
    tokens = [token.lemma_ for token in doc if not token.is_stop and not token.is_punct]
    return " ".join(tokens)

def extract_keywords_spacy(text: str) -> list[str]:
    """Extract skills, languages, and tools from a text using Spacy."""
    doc = nlp(text)
    requirements: list[str] = []
    for entity in doc.ents:
        if entity.label_ in ("SKILL", "LANGUAGE", "TOOL"):
            requirements.append(entity.text)
    return requirements



def extract_keywords_bert(text: str) -> list[str]:
    """Extract skills, languages, and tools from a text using BERT."""
    entities = bert(text)
    requirements = [entity["word"] for entity in entities if entity["entity"] in ("B-SKILL", "I-SKILL")]
    return requirements  # type: list[str]
        
def extract_all_requirements(text: str) -> list[str]:
    """Extract skills, languages, and tools from a text using both Spacy and BERT."""
    preprocessed_text = preprocess_text(text)
    spacy_requirements = extract_keywords_spacy(preprocessed_text)
    bert_requirements = extract_keywords_bert(preprocessed_text)
    all_requirements = set(spacy_requirements + bert_requirements)
    return list(all_requirements)
def main() -> None:
    """Process job descriptions to extract skills, languages, and tools."""
    requirements = []
    for idx, document in enumerate(documents):
        print(f"Processing document {idx + 1}/{len(documents)}")
        preprocessed_text = preprocess_text(document["description"])
        extracted_requirements = extract_all_requirements(preprocessed_text)
        requirements.append(extracted_requirements)
        print(f"Ending document {idx + 1}/{len(documents)}")
    print(requirements)

if __name__ == '__main__':
    main()


