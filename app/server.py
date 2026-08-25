from app.tools.patient_service import get_patient as patient_service
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("hospital_mcp")

@mcp.tool()
def get_patient(patient_id: str):
    """Get patient info by patient_id"""
    return patient_service(patient_id)