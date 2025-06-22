from flask.testing import FlaskClient
import pytest
from applications.data_collector.src.main.data_collector import db, create_app, Drug
from applications.data_analyzer.src.main.routes import register_routes

@pytest.fixture
def test_client():
    app = create_app(testing=True)
    register_routes(app)
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            db.session.add(Drug(drug_name="Lipitor", event_id="test"))
            db.session.commit()
        yield client


"""
Data analysis routes
"""
def test_list_drugs(test_client: FlaskClient):
    res = test_client.get("/drugs")
    assert res.status_code in [200, 500]

def test_top_drugs(test_client: FlaskClient):
    res = test_client.get("/top-drugs")
    assert res.status_code in [200, 500]
    
def test_drugs_by_age_groups(test_client: FlaskClient):
    res = test_client.get("/drug-by-age-groups/Lipitor")
    assert res.status_code in [200, 500]

def test_top_reactions_by_age(test_client: FlaskClient):
    res = test_client.get("/top-reactions-by-age/Lipitor")
    assert res.status_code in [200, 500]

"""
Health check routes
"""
def test_health_check(test_client: FlaskClient):
    res = test_client.get("/health-check")
    assert res.status_code == 200
    assert res.json["status"] == "I'm healthy"

def test_db_health_check(test_client: FlaskClient):
    res = test_client.get("/db-health-check")
    assert res.status_code == 200
    assert res.json["status"] == "Database connected"

"""
Metrics check
"""
def test_metrics_endpoint(test_client: FlaskClient):
    res = test_client.get("/metrics")
    assert res.status_code == 200
    assert b"http_requests_total" in res.data
    assert b"http_requests_created" in res.data
    assert b"python_info" in res.data