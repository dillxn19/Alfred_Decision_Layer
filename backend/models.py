from pydantic import BaseModel
from typing import List, Optional

class ActionRequest(BaseModel):
    action: str
    latest_message: str
    conversation_history: str

class ExtractedSignals(BaseModel):
    intent_clarity_score: int 
    risk_score: int
    missing_parameters: List[str]
    rationale: str

class FinalDecision(BaseModel):
    decision: str
    rationale: str
    raw_inputs: dict
    computed_signals: dict
    prompt_sent: str
    raw_model_output: str