from applications.data_collector.src.main.data_collector import db, create_app, AdverseEvent, Drug, Reaction
from flask import Flask, request, jsonify
import os

app = create_app()
app.app_context().push()

"""
Find the number of deaths associated with a given drug in the database
"""
@app.route("/deaths-by-drugs/<drug_name>")
def deaths_by_drug(drug_name):
    try:
        count = db.session.query(AdverseEvent)\
            .join(Drug)\
            .filter(Drug.drug_name.ilike(f"%{drug_name}%"))\
            .filter(AdverseEvent.seriousness_death == True)\
            .count()
        
        return jsonify({
            "drug": drug_name, 
            "associated_deaths": count
            })
    
    except Exception as e:
        return jsonify({"Error": str(e)}), 500

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
Find the drug with the most associated deaths in the database
"""
@app.route("/most-associated-deaths")
def most_associated_deaths():
    try:
        result = (
            db.session.query(Drug.drug_name, db.func.count().label("death_count"))
            .join(AdverseEvent)
            .filter(AdverseEvent.seriousness_death == True)
            .group_by(Drug.drug_name)
            .order_by(db.desc("death_count"))
            .first()
        )

        if result:
            return jsonify({
                "drug": result.drug_name,
                "associated_deaths": result.death_count
            })
        else:
            return jsonify({"Error": "No drug-related deaths found in database."})
    
    except Exception as e:
        return jsonify({"Error": str(e)}), 500
    

"""

"""
@app.route("/most-common-reaction")
def most_common_reaction():
    try:
        result = (
            db.session.query(Reaction.reaction_medical_term, db.func.count().label("count"))
            .group_by(Reaction.reaction_medical_term)
            .order_by(db.desc("count"))
            .first()
        )
        if result:
            return jsonify({
                "reaction": result.reaction_medical_term,
                "count": result.count
            })
        else:
            return jsonify({"Error": "No reactions found."})

    except Exception as e:
        return jsonify({"Error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True, port=5050)
    

    # @app.route('/analyze', methods=['POST'])
# def analyze_data():
#     try:
#         input_data = request.get_json()
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500