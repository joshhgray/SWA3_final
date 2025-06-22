from applications.data_collector.src.main.data_collector import db, AdverseEvent, Drug, Reaction
from sqlalchemy import case, func, desc
import os

def get_top_drugs(limit=50):
    # function separated from route so it can be called in dash for dropdown menu
    results = (
        db.session.query(Drug.drug_name, func.count().label("count"))
        .group_by(Drug.drug_name)
        .order_by(func.count().desc())
        .limit(limit)
        .all()
    )
    return [drug[0] for drug in results]

def get_age_distribution_for_drug(drug_name):
    # split into age groups - based on MeSH - https://pmc.ncbi.nlm.nih.gov/articles/PMC1794003/
    age_groups = case(
        (AdverseEvent.patient_age <= 2, "0-2"),
        (AdverseEvent.patient_age <= 5, "3-5"),
        (AdverseEvent.patient_age <= 12, "6-12"),
        (AdverseEvent.patient_age <= 18, "13-18"),
        (AdverseEvent.patient_age <= 44, "19-44"),
        (AdverseEvent.patient_age <= 64, "45-64"),
        (AdverseEvent.patient_age <= 79, "65-79"),
        (AdverseEvent.patient_age >=80, "80+"),
    else_="unknown").label("age_group")

    results = (
        db.session.query(age_groups, func.count().label("count"))
        .select_from(AdverseEvent)
        .join(Drug, Drug.event_id == AdverseEvent.safety_report_id)
        .filter(Drug.drug_name.ilike(f"%{drug_name}%"))
        .group_by(age_groups)
        .order_by(age_groups)
        .all()
    )

    return [{"age_group": r[0], "count": r[1]} for r in results]

def get_top_reactions_by_age(drug_name):
    # split into age groups - based on MeSH - https://pmc.ncbi.nlm.nih.gov/articles/PMC1794003/
    age_groups = case(
        (AdverseEvent.patient_age <= 2, "0-2"),
        (AdverseEvent.patient_age <= 5, "3-5"),
        (AdverseEvent.patient_age <= 12, "6-12"),
        (AdverseEvent.patient_age <= 18, "13-18"),
        (AdverseEvent.patient_age <= 44, "19-44"),
        (AdverseEvent.patient_age <= 64, "45-64"),
        (AdverseEvent.patient_age <= 79, "65-79"),
        (AdverseEvent.patient_age >=80, "80+"),
    else_="unknown").label("age_group")

    results = (
        db.session.query(age_groups, Reaction.reaction_medical_term, func.count().label("count"))
        .select_from(AdverseEvent)
        .join(Drug, Drug.event_id == AdverseEvent.safety_report_id)
        .join(Reaction, Reaction.event_id == AdverseEvent.safety_report_id)
        .filter(Drug.drug_name.ilike(f"%{drug_name}%"))
        .group_by(age_groups, Reaction.reaction_medical_term)
        .order_by(age_groups, desc("count"))
        .all()
    )

    group_dict = {}
    for age_group, reaction, count in results:
        if age_group not in group_dict:
            group_dict[age_group] = {"reaction": reaction, "count": count}

    return group_dict

