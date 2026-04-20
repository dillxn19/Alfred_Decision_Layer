import json
import os
from dotenv import load_dotenv
from openai import OpenAI
from .models import ExtractedSignals, FinalDecision, ActionRequest

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def evaluate_action(request: ActionRequest) -> FinalDecision:
    system_prompt = "You are the alignment layer for an assistant. Analyze the conversation and extract the following in JSON format: intent_clarity_score from 1 to 10, risk_score from 1 to 10, missing_parameters as a list of strings, and rationale as a short string."
    
    user_prompt = f"Action: {request.action} History: {request.conversation_history} Latest: {request.latest_message}"
    
    try:
        response = client.chat.completions.create(
            model=os.getenv("MODEL_NAME"),
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            response_format={"type": "json_object"}
        )
        raw_output = response.choices[0].message.content
        parsed_data = json.loads(raw_output)
        signals = ExtractedSignals(**parsed_data)
        
    except Exception as error:
        return FinalDecision(
            decision="Ask a clarifying question",
            rationale="System error or timeout occurred. Defaulting to safe state.",
            raw_inputs=request.dict(),
            computed_signals={},
            prompt_sent=system_prompt,
            raw_model_output=str(error)
        )

    decision = "Execute silently"
    
    if signals.risk_score > 8:
        decision = "Refuse / escalate"
    elif signals.intent_clarity_score < 6 or len(signals.missing_parameters) > 0:
        decision = "Ask a clarifying question"
    elif signals.risk_score > 5:
        decision = "Confirm before executing"
    elif "email" in request.action.lower():
        decision = "Execute and tell the user after"
        
    return FinalDecision(
        decision=decision,
        rationale=signals.rationale,
        raw_inputs=request.dict(),
        computed_signals=signals.dict(),
        prompt_sent=system_prompt,
        raw_model_output=raw_output
    )