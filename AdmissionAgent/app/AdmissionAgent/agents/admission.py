import os

from strands import Agent, tool
from strands.models.bedrock import BedrockModel
from strands_tools import retrieve
from tools.query_student_db import query_student_db

os.environ["STRANDS_KNOWLEDGE_BASE_ID"] = os.environ.get("KNOWLEDGE_BASE_ID", "")

SYSTEM_PROMPT = """You are Alex, the University Admission Advisor.

Use the retrieve tool to search the course handbook Knowledge Base when answering questions about
courses, programs, prerequisites, enrolment policies, and degree requirements.

Use the query_student_db tool to look up real student records, course registrations, degree plans,
and academic outcomes by running SQL queries against the education_workshop_db database. When a
student provides their ID, query the student table to greet them by name and understand their
academic status.

Be helpful, accurate, and encouraging. Always base your answers on information retrieved from the
database and Knowledge Base rather than making assumptions."""


@tool
def route_to_admission(query: str, student_id: str = "") -> str:
    """Route a query to the Admission Advisor agent for course discovery, prerequisites,
    enrolment policies, degree planning, and student record lookups.

    Args:
        query: The user's question about admissions, courses, or student records.
        student_id: Optional student ID to look up their profile.
    """
    agent = Agent(
        model=BedrockModel(model_id="us.anthropic.claude-sonnet-4-6"),
        tools=[retrieve, query_student_db],
        system_prompt=SYSTEM_PROMPT,
    )
    prompt = f"[Student ID: {student_id}] {query}" if student_id else query
    return str(agent(prompt))
