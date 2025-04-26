from database import SessionLocal
import models

# Programs list
programs = [
    {
        "name": "Tuberculosis",
        "description": "A disease that affects the lungs. Preventive measure: TB treatment and monitoring."
    },
    {
        "name": "Malaria",
        "description": "Mosquito-borne disease causing fever and chills. Preventive measure: Antimalarial therapy and education."
    },
    {
        "name": "HIV/AIDS",
        "description": "Virus that attacks the immune system. Preventive measure: ARV therapy and counseling."
    },
    {
        "name": "Diabetes",
        "description": "Condition affecting blood sugar levels. Preventive measure: Blood sugar monitoring and insulin."
    },
    {
        "name": "Hypertension",
        "description": "High blood pressure condition. Preventive measure: Blood pressure monitoring and medication."
    },
    {
        "name": "Asthma",
        "description": "Respiratory condition causing difficulty in breathing. Preventive measure: Inhaler therapy and triggers education."
    },
    {
        "name": "COVID-19",
        "description": "Viral respiratory illness. Preventive measure: Vaccination and treatment."
    },
    {
        "name": "Cancer",
        "description": "Uncontrolled cell growth. Preventive measure: Chemotherapy and support."
    },
    {
        "name": "Mental Health",
        "description": "Emotional and psychological well-being conditions. Preventive measure: Therapy and support groups."
    },
    {
        "name": "Nutrition",
        "description": "Diet-related wellness. Preventive measure: Dietary planning and supplementation."
    }
]

# Clients list
clients = [
    { "name": "John Ndungu", "email": "johnndungu@example.com", "program_ids": [1, 2] },
    { "name": "Mark Gitonga", "email": "markgitonga@example.com", "program_ids": [2, 3] },
    { "name": "Gladys Wamuyu", "email": "gladyswamuyu@example.com", "program_ids": [3] },
    { "name": "Pesh Muthaiga", "email": "peshmuthaiga@example.com", "program_ids": [4, 5] },
    { "name": "Betty Mkamba", "email": "bettymkamba@example.com", "program_ids": [5] },
    { "name": "Alvin Kamau", "email": "alvinkamau@example.com", "program_ids": [6, 7] },
    { "name": "Evans Egonga", "email": "evansegonga@example.com", "program_ids": [7] },
    { "name": "Evans Msani", "email": "evansmsani@example.com", "program_ids": [1, 9] },
    { "name": "Griffins Elegwa", "email": "griffinselectwa@example.com", "program_ids": [2, 10] },
    { "name": "Elvis Njoronge", "email": "elvisnjoronge@example.com", "program_ids": [3, 5] },
    
]

def add_programs_and_clients():
    db = SessionLocal()

    try:
        # Add health programs
        for program in programs:
            db_program = models.HealthProgram(
                name=program["name"],
                description=program["description"]
            )
            db.add(db_program)
        db.commit()
        print(" Health programs inserted.")

        # Fetch all programs from DB
        programs_in_db = db.query(models.HealthProgram).all()
        program_dict = {program.id: program for program in programs_in_db}

        # Add clients and enroll them into multiple programs
        for client in clients:
            db_client = models.Client(
                name=client["name"],
                email=client["email"]
            )
            # Attach multiple programs
            db_client.programs = [program_dict[program_id] for program_id in client["program_ids"]]
            db.add(db_client)

        db.commit()
        print(" Clients and their program enrollments inserted.")

    except Exception as e:
        print(" Error occurred:", e)
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    add_programs_and_clients()
