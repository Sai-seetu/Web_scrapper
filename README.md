
# Web_scrapper
A Python-based web scraping application leveraging modern frameworks and tools.
- Accepts query or URL
- Fireworks LLM integration for link generation
- Scraping via Playwright
- Dynamic API link creation and toggle
- Scheduled scraping with APScheduler

## Prerequisites

- **Python 3.8+** installed on your system.
- **Git** for cloning the repository.
- **PostgreSQL** running locally or accessible for database operations.

## Dependencies

Install the following Python packages (from `requirements.txt`):

- Flask
- gunicorn
- playwright
- langgraph
- fireworks-ai
- python-dotenv
- flask_sqlalchemy
- psycopg2-binary
- APScheduler
- requests
- langchain
- langchain-fireworks
- Flask-Migration
  
## How to Clone This Project

1. Install Git (if you don’t have it already):  
   - Download and install Git from https://git-scm.com/downloads.

2. Open your terminal or command prompt.

3. Navigate to the folder where you want to save the project:  
   For example:
   ```bash
   cd path/to/your/folder
   ```

4. Copy the project’s clone URL:  
   - For HTTPS:  
     https://github.com/Sai-seetu/Web_scrapper.git  
   - For SSH (requires SSH key setup):  
     git@github.com:Sai-seetu/Web_scrapper.git

5. Run the git clone command:  
   For HTTPS:
   ```bash
   git clone https://github.com/Sai-seetu/Web_scrapper.git
   ```
   Or for SSH:
   ```bash
   git clone git@github.com:Sai-seetu/Web_scrapper.git
   ```

6. Change into the project directory:
   ```bash
   cd Web_scrapper
   ```

7. Create a new service in pgAdmin ( PostgreSQL )
  * At the workspace, go to services,  register a new service like
  IN GENERAL
  ```bash
  * give SERVICE name
  ```
  IN CONNECTIONS
  ```bash
  DB_host = localhost
  DB_port = 5432
  DB_name = ScraperDB
  DB_USER = your_username
  DB_password = your_password
  ```
* Open your new services near the Services option, and create a new table for the Database.
* Make sure to update your DATABASE_URL according to your password and table name in the .env file
  ```bash
  example: DATABASE_URL=postgresql://postgres:your_password@localhost:5432/your_tablename
   ```
* Now, in the VS Code terminal, run these commands
  ```bash
  pip install psycopg2-binary
  pip install python-dotenv
  ```

## You now have a local copy of the project on your machine!

## Run Locally
```bash
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
playwright install
python run.py
```

