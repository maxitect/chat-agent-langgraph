from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from agent import create_agent

app = FastAPI(
    title="AI Agent Workshop",
    description="A simple AI agent API built with LangChain and FastAPI",
    version="1.0.0"
)
agent = create_agent()

class Query(BaseModel):
    message: str

@app.get("/")
async def root():
    return {
        "message": "Welcome to the AI Agent Workshop API!",
        "endpoints": {
            "POST /chat": "Send a message to the AI agent",
            "GET /health": "Check API health status",
            "GET /docs": "View API documentation"
        }
    }

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
