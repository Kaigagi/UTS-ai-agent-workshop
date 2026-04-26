from strands import Agent
from strands.models.bedrock import BedrockModel
from strands_tools import retrieve
from dotenv import load_dotenv
from tools import query_student_db

load_dotenv()

model = BedrockModel(model_id="us.anthropic.claude-sonnet-4-6")

SYSTEM_PROMPT = """You are the University Admission Advisor. Introduce yourself as the Admission Advisor
when starting a conversation.

Use the query_student_db tool to look up real student records, course registrations, degree plans,
and academic outcomes by running SQL queries against the education_workshop_db database. When a
student provides their ID, query the student table to greet them by name and understand their
academic status. You can also query course_registration, course_outcome, degree_plan, and other
tables to give personalised advice.

Use the retrieve tool to search the course handbook Knowledge Base when answering questions about
courses, programs, prerequisites, enrolment policies, and degree requirements.

Be helpful, accurate, and encouraging. Always base your answers on information retrieved from the
database and Knowledge Base rather than making assumptions."""

agent = Agent(model=model, tools=[retrieve, query_student_db], system_prompt=SYSTEM_PROMPT)

agent("Look up student 100014 and recommend what courses they should take next based on their program and completed units.")
