import json
import logging
import os

import boto3
import streamlit as st
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))

logger = logging.getLogger(__name__)

RUNTIME_ARN = os.environ["AGENTCORE_RUNTIME_ARN"]
agentcore_client = boto3.client("bedrock-agentcore", region_name="us-east-1")


def invoke_agent(prompt: str, session_id: str) -> str:
    """Send a prompt to the deployed AgentCore runtime and return the text response."""
    response = agentcore_client.invoke_agent_runtime(
        agentRuntimeArn=RUNTIME_ARN,
        runtimeSessionId=session_id,
        payload=json.dumps({"prompt": prompt}).encode(),
        contentType="application/json",
        accept="application/json",
    )
    raw = response["response"].read().decode("utf-8")
    chunks = []
    for line in raw.splitlines():
        if line.startswith("data: "):
            chunks.append(json.loads(line[6:]))
    return "".join(chunks)


# --- Streamlit UI ---

st.set_page_config(page_title="University Admission Advisor", page_icon="🎓")
st.title("🎓 University Admission Advisor")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "session_id" not in st.session_state:
    import uuid
    st.session_state.session_id = str(uuid.uuid4())

WELCOME_MESSAGE = """👋 Welcome! I'm your **University Admission Advisor**. I can help you with:

- 📚 **Course Discovery** — Find courses, programs, and degree plans
- ✅ **Prerequisites** — Check what you need before enrolling
- 📋 **Enrolment Policies** — Understand admission requirements and processes
- 🎓 **Personalised Advice** — Tell me your Student ID and I'll look up your records

Ask me anything to get started!"""

if not st.session_state.chat_history:
    with st.chat_message("assistant"):
        st.markdown(WELCOME_MESSAGE)

for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

ERROR_MESSAGE = "⚠️ Sorry, I'm having trouble responding right now. Please try again in a moment."

if prompt := st.chat_input("Ask about courses, programs, or prerequisites..."):
    st.session_state.chat_history.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            with st.spinner("Thinking..."):
                response = invoke_agent(prompt, st.session_state.session_id)
            st.markdown(response)
        except Exception as e:
            logger.error("AgentCore API error: %s", e, exc_info=True)
            response = ERROR_MESSAGE
            st.error(response)
    st.session_state.chat_history.append({"role": "assistant", "content": response})
    st.rerun()
