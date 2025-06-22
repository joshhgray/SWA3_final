# FDA Adverse Events Explorer

This project fetches real-world adverse drug event data from the [openFDA API](https://open.fda.gov/apis/drug/event/).
It is a modular micorservices architecture with:
1. Data Collector - Fetches and stores event data from openFDA in a PostgreSQL relational database.
2. Data Analyzer - Provides API endpoints for querying the database.
3. Frontend - Dash web app to explore drug event data with plotly visualizations.
4. Monitoring - Basic prometheus metrics and health check endpoints.

## Setup
1. Clone repo and navigate to root directory
```bash
git clone https://github.com/joshhgray/SWA3_final.git
cd SWA3_final
```
2. Create a venv and install dependencies:
```bash
python -m venv venv
source venv/bin/activate

pip install -r requirements.txt
```

3. Configure environment variables (Connect to openFDA and connect a database):
```bash
 OPEN_FDA_KEY=your_openfda_key # API key from openFDA (optional)
 DATABASE_URL=sqlite:///:memory: # or your own PostgreSQL/SQLite URI

 # Flags for runtime behaviour
 INIT_DB=true # create tables and seed data
 TESTING=false # enables test configs - automatically uses in memory database
 BACKEND_API=http://127.0.0.1:5050 # used by frontend Dash app
```

4. Run the collector
```bash
python applications/data_collector/src/main/data_collector.py
```

5. Run the frontend 
```bash
python applications/frontend/src/main/app.py
```
Runs on: http://localhost:8050

## Testing
To run unit and integration tests:
```bash
python -m unittest discover
pytest
```
Test Coverage includes:
- Data collection, processing, and saving
- API route responses
- Frontend app loading
- Database interaction and analysis functions

## Monitoring and Metrics
- See /metrics for prometheus metrics output
- See /health-check to confirm server is running
- See /db-health-check to confirm database connectivity

## Notes
- Data from openFDA is publicly available health data. It does NOT indicate causation between reactions and drugs presented. It is NOT meant to be used as medical advise or to inform any medical decisions. This app is for educational and demonstrational purposes only.
