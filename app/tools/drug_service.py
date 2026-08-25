import httpx
from app.config import settings


async def search_drug(drug_name: str):
    url = f"{settings.OPENFDA_BASE_URL}/drug/label.json"
    params = {"search": f"openfda.generic_name:{drug_name}", "limit": 1}

    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)

        if response.status_code != 200:
            return {"error": f"No data found for drug: {drug_name}"}

        data = response.json()
        result = data["results"][0]
        openfda = result.get("openfda", {})

        return {
            "generic_name": openfda.get("generic_name", ["Unknown"])[0],
            "brand_name": openfda.get("brand_name", ["Unknown"])[0],
            "manufacturer": openfda.get("manufacturer_name", ["Unknown"])[0],
            "purpose": result.get("purpose", ["N/A"])[0],
            "warnings": result.get("warnings", ["N/A"])[0][:500],
        }
