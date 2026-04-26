import logging
import os

from strands import Agent
from bedrock_agentcore.runtime import BedrockAgentCoreApp
from model.load import load_model
from strands_tools import retrieve
from tools.query_student_db import query_student_db
from memory.session import get_session_manager

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

os.environ["STRANDS_KNOWLEDGE_BASE_ID"] = os.environ.get("KNOWLEDGE_BASE_ID", "")

app = BedrockAgentCoreApp()
log = app.logger

SYSTEM_PROMPT = """You are Alex, the University Admission Advisor. Introduce yourself as Alex
when starting a conversation.

Use the retrieve tool to search the course handbook Knowledge Base when answering questions about
courses, programs, prerequisites, enrolment policies, and degree requirements.

Use the query_student_db tool to look up real student records, course registrations, degree plans,
and academic outcomes by running SQL queries against the education_workshop_db database. When a
student provides their ID, query the student table to greet them by name and understand their
academic status. You can also query course_registration, course_outcome, degree_plan, and other
tables to give personalised advice.

Be helpful, accurate, and encouraging. Always base your answers on information retrieved from the
database and Knowledge Base rather than making assumptions."""

tools = [retrieve, query_student_db]
model = load_model()


@app.entrypoint
async def invoke(payload, context):
    log.info("Invoking Agent.....")

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
        **({"session_manager": session_manager} if session_manager else {}),
    )

    stream = agent.stream_async(payload.get("prompt"))

    async for event in stream:
        if "data" in event and isinstance(event["data"], str):
            yield event["data"]


if __name__ == "__main__":
    app.run()
