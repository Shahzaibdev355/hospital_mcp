from app.tools.patient_service import get_patient as patient_service
from app.tools.drug_service import search_drug as drug_service
from app.tools.fhir_service import get_observations as fhir_service
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("hospital_mcp")


@mcp.tool()
def get_patient(patient_id: str):
    """Get patient info by patient_id"""
    return patient_service(patient_id)


@mcp.tool()
async def search_drug(drug_name: str):
    """Search drug information by generic name (e.g. aspirin)"""

    return await drug_service(drug_name)


@mcp.tool()
async def get_observations(patient_name: str):
    """Get latest observations for a patient by name (from HAPI FHIR test server)"""
    return await fhir_service(patient_name)


if __name__ == "__main__":
    mcp.run(transport="streamable-http")