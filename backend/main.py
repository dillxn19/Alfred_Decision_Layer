from fastapi import FastAPI, HTTPException
from .models import ActionRequest, FinalDecision
from .decision_engine import evaluate_action

app = FastAPI(title="Alfred Decision Layer API")

@app.post("/evaluate", response_model=FinalDecision)
def evaluate(request: ActionRequest):
    try:
        decision_trace = evaluate_action(request)
        return decision_trace
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))