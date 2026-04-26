from strands import Agent

agent = Agent(
    model="us.anthropic.claude-sonnet-4-6",
    system_prompt="You are a helpful university admission assistant. You help prospective students learn about courses, programs, and the application process."
)

agent("What kind of help can you provide to a prospective student?")

# Test 