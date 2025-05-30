from .sub_agents.PhysicsAgent.agent import PhysicsAgent
from .sub_agents.MathAgent.agent import MathAgent

from google.adk.agents import Agent

import os
GOOGLE_API_KEY= os.getenv("GOOGLE_API_KEY")

# extract tutor_role instructions
current_dir = os.path.dirname(os.path.abspath(__file__))
role_path = os.path.join(current_dir, "tutor_role.txt" )
with open(role_path, 'r', encoding="utf-8") as file:
    INS = file.read()
    

tutor_agent = Agent(
    name = "tutor_agent",
    model = "gemini-2.0-flash",
    description="Tutor Agent",
    instruction=INS,
    sub_agents=[PhysicsAgent, MathAgent],
    
)
