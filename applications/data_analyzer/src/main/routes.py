from flask import request, jsonify
from applications.data_collector.src.main.data_collector import db, AdverseEvent, Drug, Reaction
from applications.data_analyzer.src.main.data_analyzer import get_top_drugs, get_age_distribution_for_drug, get_top_reactions_by_age
import os

"""
ROUTES
"""
def register_routes(app):
    """
    Initialize the database (conditional).
    """
    if os.getenv("INIT_DB", "false").lower() == "true":
        with app.app_context():
            db.create_all()

            # populate test db if in testing/debugging mode
            if app.config["TESTING"] or os.getenv("TESTING") == "true":
                # populate test database if empty
                if not db.session.query(Drug).first():
                    from scripts.populate_test_db import populate_test_db
                    populate_test_db(app)


    """
    List all (or limit amount) of drugs in database
    """ 
    @app.route("/drugs")
    def list_all_drugs():
        try:
            # limit output
            limit = request.args.get("limit", default=50, type=int)

            drugs = db.session.query(Drug.drug_name).distinct().order_by(Drug.drug_name).limit(limit).all()
            drugs_list = [drug[0] for drug in drugs if drug[0]]
            return jsonify({"drugs": drugs_list})

        except Exception as e:
            return jsonify({"Error": str(e)}), 500
        
    """
    Get the top 50 most common drugs in the database.
    """
    @app.route("/top-drugs")
    def top_drugs():
        try:
            limit = request.args.get("limit", default=50, type=int)
            return jsonify({"drugs": get_top_drugs(limit)})

        except Exception as e:
            return jsonify({"Error": str(e)}), 500
        
    """
    Show drug usage across different age groups for a given drug
    """
    @app.route("/drug-by-age-groups/<drug_name>")
    def drug_by_age_groups(drug_name):
        try:
            return jsonify({
                "drugs": drug_name,
                "age_distribution": get_age_distribution_for_drug(drug_name)
            })
 
        except Exception as e:
            return jsonify({"Error": str(e)}), 500
        
    """
    Show top reactions per age group for a given drug
    """
    @app.route("/top-reactions-by-age/<drug_name>")
    def top_reactions_by_age(drug_name):
        try:
            return jsonify({
                "drugs": drug_name,
                "age_distribution": get_top_reactions_by_age(drug_name)
            })
        
        except Exception as e:
            return jsonify({"Error": str(e)}), 500
        

    """
    Health check
    """
    # uptime check
    @app.route("/health-check")
    def health_check():
        return jsonify({"status": "I'm healthy"}), 200
    
    # datebase check
    @app.route("/db-health-check")
    def db_health_check():
        try:
            db.session.query(Drug).first()
            return jsonify({"status": "Database connected"}), 200
        except Exception as e:
            return jsonify({"status": "unavailable", "error": str(e)}), 500