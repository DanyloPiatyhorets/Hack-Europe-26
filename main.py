# Fast API backend

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from langgraph.types import interrupt, Command
from typing import TypedDict

# 1. Define State and Graph
class AgentState(TypedDict):
    document_id: str
    proposed_changes: list
    final_status: str

def analyze_node(state: AgentState):
    # Mock data as instructed
    mock_changes = [{
        "change_id": "1",
        "original_text": "Net 30 payment terms.",
        "proposed_text": "Net 60 payment terms.",
        "rationale": "Company standard policy dictates Net 60.",
        "estimated_value_saved": "$500"
    }]
    return {"proposed_changes": mock_changes}

def human_review_node(state: AgentState):
    # The graph stops executing here. 
    # When resumed via the API, req.approved_changes is assigned to human_response.
    human_response = interrupt(state["proposed_changes"])
    
    # Overwrite the state with ONLY the items the human explicitly approved.
    return {"proposed_changes": human_response}

def execute_node(state: AgentState):
    # Final action execution (e.g., Stripe API)
    return {"final_status": "Executed via Stripe"}

# Build Graph
builder = StateGraph(AgentState)
builder.add_node("analyze", analyze_node)
builder.add_node("hitl", human_review_node)
builder.add_node("execute", execute_node)
builder.add_edge(START, "analyze")
builder.add_edge("analyze", "hitl")
builder.add_edge("hitl", "execute")
builder.add_edge("execute", END)

memory = MemorySaver()
graph = builder.compile(checkpointer=memory)

# 2. FastAPI Setup
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allows your Lovable React app to connect
    allow_methods=["*"],
    allow_headers=["*"],
)

class StartReq(BaseModel):
    thread_id: str

class ResumeReq(BaseModel):
    thread_id: str
    approved_changes: list

@app.post("/start")
def start_workflow(req: StartReq):
    config = {"configurable": {"thread_id": req.thread_id}}
    graph.invoke({"document_id": "contract_abc123"}, config)
    
    current_state = graph.get_state(config)
    if current_state.next:
        # Extract the payload passed to interrupt()
        interrupt_data = current_state.tasks[0].interrupts[0].value
        return {"status": "paused", "data": interrupt_data}
    return {"status": "completed"}

@app.post("/resume")
def resume_workflow(req: ResumeReq):
    config = {"configurable": {"thread_id": req.thread_id}}
    
    # Push the human's approved array back into the paused graph
    graph.invoke(Command(resume=req.approved_changes), config)
    
    # Retrieve the final state to send back to the React UI
    final_state = graph.get_state(config).values
    
    return {
        "status": "completed", 
        "final_state": final_state
    }