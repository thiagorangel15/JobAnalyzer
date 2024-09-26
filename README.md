# Job Finder

This project is a job finder application that uses an API to search for job listings based on a desired job title. It retrieves job descriptions and inserts them into a MongoDB database.

## Getting Started

To get started with the Job Finder application, follow these steps:

1. Clone the repository: git clone https://github.com/your-username/job-finder.git
2. Install the required dependencies: pip install -r requirements.txt (WIP)
3. Set up the MongoDB database:
- Create a `.env` file in the root directory of the project and add the following line:
  ```
  MONGO_PASSWORD=your_mongo_password
  ```
- Replace `your_mongo_password` with your actual MongoDB password.

4. Run the application: python main.py
5. Follow the prompts to enter the desired job title and search for jobs.

## Usage

To use the Job Finder application, simply run the `main.py` file and follow the prompts to enter the desired job title and search for jobs. The application will retrieve job descriptions from the API and insert them into the MongoDB database.

## Requirements

- Python 3.x
- requests
- pymongo
- beautifulsoup4
- dotenv

## License

This project is licensed under the [MIT License](LICENSE).

## Contact

For any questions or issues, you can reach out to me at thiagorangeldasilva43@gmail.com.
