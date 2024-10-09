import requests
import os
from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from bs4 import BeautifulSoup

dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(dotenv_path)

mongo_password = os.getenv('MONGO_PASSWORD')

uri = f"mongodb+srv://dbAdmin:{mongo_password}@jobanalyzermongo.dbjel.mongodb.net/?retryWrites=true&w=majority&appName=JobAnalyzerMongo"
client = MongoClient(uri, server_api=ServerApi('1'))

def findJob(desiredJob, url=None):
    if url is None:
        url = "https://jobdataapi.com/api/jobs/?country_code=BR&region_id=6&title=" + desiredJob
    
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception if the response status code is not 200
        
        data = response.json()
        jobs = []
        
        for job in data['results']:
            description = job.get('description')
            soup = BeautifulSoup(description, 'html.parser')
            textDescription = soup.get_text()
            
            jobs.append({'title': desiredJob, 'description': textDescription})
        
        next_url = data.get('next')
        
        if next_url is not None:
            jobs.extend(findJob(desiredJob, next_url))
        
        return jobs
    
    except requests.exceptions.RequestException as e:
        print(f"Ocorreu um erro na requisição: {e}")
        return []

def insertJobs(jobs):

    try:
        
        db = client['JobAnalyzerDB']
        collection = db['Jobs']  
        
        collection.delete_many({})
        print("Coleção limpa com sucesso")
        
        
        collection.insert_many(jobs)  
        print("Jobs inserted successfully")
    except Exception as e:
        print(f"Error: {e}")


def main():
    desiredJob = input("Digite o nome da vaga desejada: ")
    
    jobs = findJob(desiredJob)
    
    if jobs:
        insertJobs(jobs)
    else:
        print("Nenhum resultado encontrado")

if __name__ == '__main__':
    main()