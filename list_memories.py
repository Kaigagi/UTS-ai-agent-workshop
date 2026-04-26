import os
import boto3
from dotenv import load_dotenv

load_dotenv()

MEMORY_ID = os.environ["MEMORY_ADMISSION_AGENT_MEMORY_ID"]
ACTOR_ID = "default-actor"

client = boto3.client("bedrock-agentcore")

# List semantic facts
print("=== Semantic Facts ===")
response = client.list_memory_records(
    memoryId=MEMORY_ID,
    namespace=f"/users/{ACTOR_ID}/facts",
)
for record in response.get("memoryRecordSummaries", []):
    print(f"  - {record.get('content', {}).get('text', '')}")

# List user preferences
print("\n=== User Preferences ===")
response = client.list_memory_records(
    memoryId=MEMORY_ID,
    namespace=f"/users/{ACTOR_ID}/preferences/",
)
for record in response.get("memoryRecordSummaries", []):
    print(f"  - {record.get('content', {}).get('text', '')}")