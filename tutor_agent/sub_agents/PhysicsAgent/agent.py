from turtle import mode
from google.adk.agents import Agent

from .helper import convert_units
from .helper2 import find_constant

import os

# Get the absolute path to the current file's directory
current_dir = os.path.dirname(os.path.abspath(__file__))
# Path to the agent_role.txt in the same folder
role_path = os.path.join(current_dir, "agent_role.txt")
role_path2 = os.path.join(current_dir, "description.txt")

with open(role_path, 'r', encoding="utf-8") as file:
    INS = file.read()

with open(role_path2, 'r', encoding="utf-8") as file:
    DES = file.read()

PhysicsAgent = Agent(
    name="PhysicsAgent",
    model = "gemini-2.0-flash",
    description=DES,
    instruction=INS,
    tools=[convert_units, find_constant]
) 

