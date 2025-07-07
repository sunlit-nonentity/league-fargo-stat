# LeagueFargoStat

**LeagueFargoStat** is a work-in-progress stat tracker for the Amsterdam Billiards League, designed to automate the process of scraping match data, calculating player statistics, and generating a personalized dashboard — similar to FargoRate.

### Project Goals

- Automatically log in to the Amsterdam Billiards league portal using your personal credentials
- Extract and structure player standings and match history
- Store data securely in cloud infrastructure (e.g., AWS RDS or DynamoDB)
- Develop a ratigh algorithm to measure skill progression over time
- Build a secure and scalable dashboard (CLI + Web)
- Enable multi-user access via secure credential storage (AWS Secrets Manager)
- Schedule Automatic updates using AWS Lambda and CloudWatch
- Export data to CSV and Excel

----------------------------------------------------------------------

### Tech Stack

#### Languages
- Python (scraper, CLI, database layer, AWS Lambda logic)
- Typescript (future web app/dashboard development)

#### AWS Tools
- **AWS Secrets Manager** - Securely store user credentials
- **AWS Lambda** - Scheduled scraping via serverless automation
- **AWS RDS / DynamoDB** - Scalable, cloud-hosting database
- **AWS CloudWatch** - Cron-based job triggering and monitoring
- **AWS S3** - (optional) Storing exports or intermediate data files

#### Libraries & Tools
- 'requests', 'beautifulsoup4', 'python-dotenv', 'sqlite3'
- Streamlit (for rapid dashboard prototyping)
- GitHub (version control and CI/CD)

----------------------------------------------------------------------

### Status

This project is in active development. The current CLI-based scraper can:

- Log in to the league portal using user credentials
- Retrieve individual standings and match history
- Store structured data in a local SQLite database
- Export or inspect data via CLI interface

Next phases:

- Backend migration to AWS
- Rating algorithm logic
- Web interface in Typescript or Streamlit
- Multi-user support with credential-based session tracking

----------------------------------------------------------------------

### Project Structure (Local Prototype)

'''bash
PoolRatingScraper/
├── cli_interface.py
├── scraper.py
├── lambda_function.py
├── database.py
├── config.json
├── requirements.txt
├── .env
├── core/
│   ├── auth.py
│   ├── standings.py
│   ├── scouting.py
│   └── database.py
└── README.md
