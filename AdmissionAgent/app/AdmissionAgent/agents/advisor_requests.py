import os

from strands import Agent, tool
from strands.models.bedrock import BedrockModel
from strands.tools.mcp import MCPClient
from mcp.client.streamable_http import streamablehttp_client
from tools.query_student_db import query_student_db

SYSTEM_PROMPT = """You are a student services evaluator. Before submitting any advisor request, you must:

1. Assess whether the request is reasonable and complex enough to warrant a formal advisor request.
2. Use query_student_db to check the student's academic record for supporting evidence.
3. Only submit the request via the MCP tools if the request is justified by the evidence.
4. For trivial or unsupported requests, provide helpful guidance instead of submitting.

Available request types: course_override, advisor_meeting, program_change, special_consideration.

Be thorough in your evaluation but respectful to the student."""


@tool
def route_to_advisor_requests(query: str, student_id: str = "") -> str:
    """Route a request to the student services evaluator for formal advisor requests such as
    course overrides, advisor meetings, program changes, and special considerations.

    Args:
        query: The student's request or question about advisor services.
        student_id: Optional student ID to look up their record for validation.
    """
    with MCPClient(lambda: streamablehttp_client(os.environ["ADVISOR_MCP_URL"])) as mcp_client:
        mcp_tools = mcp_client.list_tools_sync()
        agent = Agent(
            model=BedrockModel(model_id="us.anthropic.claude-sonnet-4-6"),
            tools=[query_student_db, *mcp_tools],
            system_prompt=SYSTEM_PROMPT,
        )
        prompt = f"[Student ID: {student_id}] {query}" if student_id else query
        return str(agent(prompt))
