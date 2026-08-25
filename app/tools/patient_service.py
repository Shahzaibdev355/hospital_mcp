from app.database.postgres_client import get_postgres_connection


def get_patient(patient_id: str):

    conn = get_postgres_connection()

    try:
        cursor = conn.cursor()

        query = """
            select
                patient_id,
                name,
                age,
                gender,
                blood_group,
                department,
                admission_date,
                status
            from patients
            where patient_id = %s;
        """

        cursor.execute(query, (patient_id,))
        patient = cursor.fetchone()

        if not patient:
            return {
                "error": f"Patient {patient_id} not found"
            }

        return {
            "patient_id": patient[0],
            "name": patient[1],
            "age": patient[2],
            "gender": patient[3],
            "blood_group": patient[4],
            "department": patient[5],
            "admission_date": str(patient[6]),
            "status": patient[7],
        }

    finally:
        cursor.close()
        conn.close()