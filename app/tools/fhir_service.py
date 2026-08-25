import httpx
from app.config import settings


async def get_observations(patient_name: str):
    async with httpx.AsyncClient() as client:
        # Step 1: find patient by name to get FHIR patient id
        patient_res = await client.get(
            f"{settings.FHIR_BASE_URL}/Patient",
            params={"name": patient_name},
        )

        if patient_res.status_code != 200:
            return {"error": f"Patient search failed for: {patient_name}"}

        patient_data = patient_res.json()
        entries = patient_data.get("entry", [])

        if not entries:
            return {"error": f"No FHIR patient found for: {patient_name}"}

        fhir_patient_id = entries[0]["resource"]["id"]

        # Step 2: get observations for that patient id
        obs_res = await client.get( 
            f"{settings.FHIR_BASE_URL}/Observation",
            params={"patient": fhir_patient_id, "_count": 5},
        )

        if obs_res.status_code != 200:
            return {"error": "Failed to fetch observations"}

        obs_data = obs_res.json()
        obs_entries = obs_data.get("entry", [])

        if not obs_entries:
            return {"error": f"No observations found for patient: {patient_name}"}

        results = []
        for e in obs_entries:
            resource = e["resource"]
            code = resource.get("code", {}).get("text") or resource.get("code", {}).get(
                "coding", [{}]
            )[0].get("display", "Unknown")
            value = resource.get("valueQuantity", {})
            results.append(
                {
                    "observation": code,
                    "value": value.get("value"),
                    "unit": value.get("unit"),
                    "date": resource.get("effectiveDateTime", "N/A"),
                }
            )

        return {
            "patient_name": patient_name,
            "fhir_patient_id": fhir_patient_id,
            "observations": results,
        }
