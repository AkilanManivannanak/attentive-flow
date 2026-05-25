from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from backend.schemas import WorkflowRequest, WorkflowResponse
from backend.workflows.compiler import compile_workflow

app = FastAPI(
    title="AttentiveFlow API",
    description="Agentic cross-channel marketing workflow generator",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def health_check():
    return {
        "status": "ok",
        "message": "AttentiveFlow API is running",
    }


@app.post("/generate-workflow", response_model=WorkflowResponse)
def generate_workflow(request: WorkflowRequest):
    try:
        workflow = compile_workflow(request.brief)
        return WorkflowResponse(workflow=workflow)

    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))
