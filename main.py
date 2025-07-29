from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from agent import create_agent

app = FastAPI(title="AI Agent Workshop")
agent = create_agent()

class Query(BaseModel):
    message: str

@app.post("/chat")
async def chat(query: Query):
    try:
        reply = agent.run(query.message)
        return {"reply": reply}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health():
    return {"status": "ok"}
