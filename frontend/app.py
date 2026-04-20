import streamlit as st
import requests

st.set_page_config(page_title="Alfred Decision Engine", layout="wide")

st.title("Alfred Execution Decision Layer")
st.markdown("A contextual decision engine for evaluating assistant actions.")

scenarios = {
    "Custom Input": {"action": "", "latest_message": "", "conversation_history": ""},
    "Easy: Weekly Sync": {
        "action": "Schedule a 30 minute meeting",
        "latest_message": "Put a 30 min sync with David on my calendar for tomorrow at 10 AM.",
        "conversation_history": "David agreed to meet tomorrow morning."
    },
    "Easy: Standard Reply": {
        "action": "Draft email reply",
        "latest_message": "Just say thanks and I will review it by Friday.",
        "conversation_history": "Received a project proposal from Sarah."
    },
    "Ambiguous: Missing Time": {
        "action": "Reschedule meeting",
        "latest_message": "Move my meeting with Emma.",
        "conversation_history": "User has a 2 PM meeting with Emma today."
    },
    "Ambiguous: Unclear Entity": {
        "action": "Send document",
        "latest_message": "Send the deck to him.",
        "conversation_history": "Earlier user was talking to both John and Michael about the Q3 presentation."
    },
    "Risky: External Partner Discount": {
        "action": "send email reply to external partner",
        "latest_message": "Yep, send it",
        "conversation_history": "alfred_ drafted a reply to Acme proposing a discount and asked for confirmation user said Actually hold off until legal reviews pricing language a few minutes later user said Yep, send it."
    },
    "Risky: Destructive Action": {
        "action": "Bulk delete emails",
        "latest_message": "Just delete everything from my inbox from last week.",
        "conversation_history": "User is annoyed by spam emails."
    }
}

col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.subheader("Context & Input")
    selected_scenario = st.selectbox("Load a Scenario", list(scenarios.keys()))
    
    with st.form("decision_form"):
        action = st.text_input("Action", value=scenarios[selected_scenario]["action"])
        latest_message = st.text_input("Latest User Message", value=scenarios[selected_scenario]["latest_message"])
        conversation_history = st.text_area("Conversation History", value=scenarios[selected_scenario]["conversation_history"], height=150)
        
        submit_button = st.form_submit_button("Evaluate Decision", use_container_width=True)

with col2:
    st.subheader("Evaluation Results")
    if submit_button:
        payload = {
            "action": action,
            "latest_message": latest_message,
            "conversation_history": conversation_history
        }
        
        with st.spinner("Analyzing context..."):
            try:
                response = requests.post("http://localhost:8000/evaluate", json=payload)
                data = response.json()
                
                st.success(f"**Decision:** {data.get('decision')}")
                st.info(f"**Rationale:** {data.get('rationale')}")
                
                with st.expander("Look Under the Hood"):
                    st.markdown("### Inputs")
                    st.json(data.get("raw_inputs"))
                    
                    st.markdown("### Computed Signals")
                    st.json(data.get("computed_signals"))
                    
                    st.markdown("### Prompt Sent to Model")
                    st.text(data.get("prompt_sent"))
                    
                    st.markdown("### Raw Model Output")
                    st.text(data.get("raw_model_output"))
                    
            except Exception as e:
                st.error("Failed to connect to the backend server. Make sure FastAPI is running.")