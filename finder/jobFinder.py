import requests
import os
from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from bs4 import BeautifulSoup
from urllib.parse import quote_plus

dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(dotenv_path)

username = quote_plus("dbAdmin")
password = quote_plus(os.getenv('MONGO_PASSWORD'))

uri = f"mongodb+srv://{username}:{password}@jobanalyzermongo.dbjel.mongodb.net/?retryWrites=true&w=majority&appName=JobAnalyzerMongo"
client = MongoClient(uri, server_api=ServerApi('1'))

def find_jobs(desired_job: str, url: str | None = None) -> list[dict]:
    """
    Find jobs from jobdataapi.com.

    Args:
        desired_job (str): The desired job title.
        url (str | None, optional): The url for the API. Defaults to None.

    Returns:
        list[dict]: A list of dictionaries containing the job title and description.
    """
    if url is None:
        url = f"https://jobdataapi.com/api/jobs/?country_code=BR&region_id=6&title={desired_job}"

    try:
        response = requests.get(url)
        response.raise_for_status()

        data = response.json()
        jobs = []

        for job in data["results"]:
            description = job.get("description")
            soup = BeautifulSoup(description, "html.parser")
            text_description = soup.get_text()

            jobs.append({"title": desired_job, "description": text_description})

        next_url = data.get("next")

        if next_url is not None:
            jobs.extend(find_jobs(desired_job, next_url))

        return jobs

    except requests.exceptions.RequestException as e:
        print(f"Erro na requisi o: {e}")
        return []

def insert_jobs(jobs: list[dict]) -> None:
    """
    Insert a list of jobs into the MongoDB database.

    Args:
        jobs (list[dict]): A list of dictionaries containing the job title and description.

    Returns:
        None
    """
    if not jobs:
        print("Nenhum job encontrado")
        return
    try:
        job_analyzer_db = client["JobAnalyzerDB"]
        jobs_collection = job_analyzer_db["Jobs"]

        jobs_collection.delete_many({})
        jobs_collection.insert_many(jobs)
    except Exception as e:
        print(f"Erro ao inserir os jobs no banco de dados: {e}")


def main() -> None:
    desired_job = input("Digite o nome da vaga desejada: ")

    jobs = find_jobs(desired_job)

    if jobs:
        insert_jobs(jobs)
    else:
        print("Nenhum resultado encontrado")

if __name__ == '__main__':
    main()