import os

from bedrock_agentcore.memory.integrations.strands.config import AgentCoreMemoryConfig, RetrievalConfig
from bedrock_agentcore.memory.integrations.strands.session_manager import AgentCoreMemorySessionManager


def get_session_manager(session_id: str, actor_id: str) -> AgentCoreMemorySessionManager:
    """Build an AgentCoreMemorySessionManager from the memory ID env var."""
    config = AgentCoreMemoryConfig(
        memory_id=os.environ["MEMORY_ADMISSION_AGENT_MEMORY_ID"],
        session_id=session_id,
        actor_id=actor_id,
        retrieval_config={
            "/users/{actorId}/facts": RetrievalConfig(top_k=5, relevance_score=0.5),
            "/users/{actorId}/preferences/": RetrievalConfig(top_k=5, relevance_score=0.5),
        },
    )
    return AgentCoreMemorySessionManager(agentcore_memory_config=config)
