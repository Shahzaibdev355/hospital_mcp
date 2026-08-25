from fastapi import FastAPI
from pydantic import BaseModel
from app.agent.agent import run_agent

app = FastAPI(title="Hospital Agent API")


class QueryRequest(BaseModel):
    query: str


@app.post("/query")
async def query_agent(req: QueryRequest):
    result = await run_agent(req.query)
    return result


@app.get("/health")
def health():
    return {"status": "ok"}



