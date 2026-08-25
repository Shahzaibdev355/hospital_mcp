from app.tools.patient_service import get_patient as patient_service
from app.tools.drug_service import search_drug as drug_service
from app.tools.fhir_service import get_observations as fhir_service

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("hospital_mcp", host="127.0.0.1", port=8000)

@mcp.tool()
def get_patient(patient_id: str):
    """
    Get patient admission info from the HOSPITAL'S INTERNAL DATABASE.
    Use ONLY when the user gives a patient ID in the format P1001-P1005
    (our own hospital records — NOT external/synthetic/FHIR patients).
    """
    return patient_service(patient_id)


@mcp.tool()
async def search_drug(drug_name: str):
    """Search drug information by generic name (e.g. aspirin) from openFDA."""

    return await drug_service(drug_name)


@mcp.tool()
async def get_observations(patient_name: str):
    """
    Get clinical observations/vitals/lab results from the EXTERNAL FHIR TEST SERVER.
    Use when the user mentions a patient NAME (not our internal P-numbers),
    especially names like 'Synthetic Patient SYN-XXXXXX' or any FHIR/EHR patient.
    """
    
    return await fhir_service(patient_name)


if __name__ == "__main__":
    mcp.run(transport="streamable-http")