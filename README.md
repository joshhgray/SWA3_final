# FDA Adverse Events Collector

This project fetches real-world adverse drug event data from the [openFDA API](https://open.fda.gov/apis/drug/even/), processes the results, and stores them in a relational database using SQLAlchemy and Flask.

## Setup
1. Navigate to project root directory
2. Create a venv and install dependencies:

```bash
python -m venv venv
source venv/bin/activate

pip install -r requirements.txt
```

3. Configure environment variables (Connect to openFDA and connect a database):
```bash
 OPEN_FDA_KEY=your_openfda_key # API key from openFDA
 DATABASE_URL=postgresql://your_db_url # PostgreSQL connect URI
```

4. Run the collector
```bash
python applications/data_collector/src/main/data_collector.py
```
This will:
- Connect to the openFDA API
- Fetch drug event data
- Process and store it in the database

5. Testing
To run unit and integration tests:
```bash
python -m unittest discover
```

**Notes
- Tables are automatically created at runtime via db.create_all() when the script runs inside an application context
- You can customize the number of API calls, delay between them, and filtering by editing the __main__ block in data_collector.py
-