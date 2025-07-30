from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import logging
import uuid
from agent import create_agent

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="AI Agent Workshop",
    description="A simple AI agent API built with LangChain and FastAPI",
    version="1.0.0"
)

# Add CORS middleware for web frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize agent once at startup
try:
    agent = create_agent()
    logger.info("Agent initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize agent: {e}")
    agent = None

class Query(BaseModel):
    message: str
    session_id: str = None  # Optional session ID for conversation continuity
    
    class Config:
        json_schema_extra = {
            "example": {
                "message": "Hello, how are you?",
                "session_id": "optional-session-123"
            }
        }

class ChatResponse(BaseModel):
    reply: str
    session_id: str
    status: str = "success"

@app.get("/")
async def root():
    return {
        "message": "Welcome to the AI Agent Workshop API!",
        "endpoints": {
            "POST /chat": "Send a message to the AI agent",
            "GET /health": "Check API health status",
            "GET /docs": "View API documentation"
        },
        "version": "1.0.0"
    }

@app.post("/chat", response_model=ChatResponse)
async def chat(query: Query):
    if not agent:
        raise HTTPException(status_code=503, detail="Agent not available")
    
    try:
        logger.info(f"Received message: {query.message}")
        
        # Generate session ID if not provided (for conversation continuity)
        session_id = query.session_id or str(uuid.uuid4())
        
        # Create config with thread_id for checkpointer
        config = {"configurable": {"thread_id": session_id}}
        
        # LangGraph agent uses invoke with messages format and config
        response = agent.invoke({"messages": [("human", query.message)]}, config=config)
        
        # Extract the final AI message from the response
        final_message = response.get("messages", [])[-1]
        reply = final_message.content if hasattr(final_message, 'content') else str(final_message)
        
        logger.info(f"Agent response: {reply}")
        return ChatResponse(reply=reply, session_id=session_id)
        
    except Exception as e:
        logger.error(f"Error processing chat request: {e}")
        raise HTTPException(
            status_code=500, 
            detail="An error occurred while processing your request. Please try again."
        )

@app.get("/health")
async def health():
    agent_status = "ok" if agent else "unavailable"
    return {
        "status": "ok",
        "agent_status": agent_status,
        "version": "1.0.0"
    }
