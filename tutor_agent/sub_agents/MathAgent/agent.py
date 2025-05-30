from google.adk.agents import Agent
from .helper_calculator import parse_equation
import os

# extract decription and instruction from agent_role and agent_description
current_dir = os.path.dirname(os.path.abspath(__file__))
role_path = os.path.join(current_dir, "agent_role.txt")
role_path2 = os.path.join(current_dir, "agent_description.txt")

with open(role_path, 'r', encoding="utf-8") as file:
    INSTRUCTION = file.read()

with open(role_path2, 'r', encoding="utf-8") as file:
    DESCRIPTION = file.read()
GOOGLE_API_KEY= os.getenv("GOOGLE_API_KEY")

MathAgent = Agent(
    name = "MathAgent",
    model = "gemini-2.0-flash",
    description=DESCRIPTION,
    instruction=INSTRUCTION,
    tools = [parse_equation]
)