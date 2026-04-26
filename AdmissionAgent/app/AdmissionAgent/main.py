import logging
import os

from strands import Agent
from strands.agent.conversation_manager import SlidingWindowConversationManager
from bedrock_agentcore.runtime import BedrockAgentCoreApp
from model.load import load_model
from agents.admission import route_to_admission
from agents.advisor_requests import route_to_advisor_requests
from memory.session import get_session_manager

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

os.environ["STRANDS_KNOWLEDGE_BASE_ID"] = os.environ.get("KNOWLEDGE_BASE_ID", "")

app = BedrockAgentCoreApp()
log = app.logger

SYSTEM_PROMPT = """You are the Student Services Orchestrator. Your role is to analyse student queries
and route them to the right specialist agent.

When a student identifies themselves (provides a student ID), remember it and pass it along
to the specialist agents.

Routing rules:
- **Information lookups** → route_to_admission: course discovery, prerequisites, enrolment policies,
  degree requirements, program information, student record queries, academic progress checks.
- **Action requests** → route_to_advisor_requests: course overrides, advisor meeting requests,
  program changes, special consideration applications, or any request that requires formal submission.

Always pass the student_id parameter if the student has identified themselves.
Summarise the specialist's response clearly for the student. Do not attempt to answer
academic questions directly — always delegate to the appropriate specialist."""

tools = [route_to_admission, route_to_advisor_requests]
model = load_model()


@app.entrypoint
async def invoke(payload, context):
    log.info("Invoking Orchestrator Agent.....")

    session_id = payload.get("session_id", "default-session")
    actor_id = payload.get("actor_id", "default-actor")

    try:
        session_manager = get_session_manager(session_id, actor_id)
    except KeyError:
        logger.warning("MEMORY_ADMISSION_AGENT_MEMORY_ID not set, running without session memory")
        session_manager = None

    agent = Agent(
        model=model,
        system_prompt=SYSTEM_PROMPT,
        tools=tools,
        conversation_manager=SlidingWindowConversationManager(window_size=40),
        **({"session_manager": session_manager} if session_manager else {}),
    )

    stream = agent.stream_async(payload.get("prompt"))

    async for event in stream:
        if "data" in event and isinstance(event["data"], str):
            yield event["data"]


if __name__ == "__main__":
    app.run()
