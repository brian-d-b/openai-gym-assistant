import os
import re
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the API key from the environment variables
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("No API key found in environment variables.")

# Initialize the OpenAI client
client = OpenAI(api_key=api_key)

# Create an Assistant
assistant = client.beta.assistants.create(
    name="Gym Assistant",
    instructions="""
    You are a fitness assistant with the goal of suggesting workouts based on my recent gym activity.
    You will read my recent gym activity and suggest a workout routine that aligns with my fitness goals.
    Please always keep in mind the principles of progressive overload, balanced training, and proper recovery.
    Do not ever tell me to hydrate or eat properly, as I am already aware of these general health guidelines. 

    Know this: I am following a PPL (Push, Pull, Legs) routine. In my home gym, I have the following equipment:
    - Squat rack
    - Barbell
    - Dumbbells
    - Bench
    - Pull-up bar
    - 2 adjustable pulley cable machines
    - Landmine attachment
    - Row bar
    - Lat pulldown bar
    - Tricep rope
    - A variety of plates and dumbbells
    """,
    tools=[],
    model="gpt-4o"
)

# Create a Thread
thread = client.beta.threads.create()

# Add the first message to the Thread
# Reads the initial workout from a local file
with open(".\initial-workout.txt", "r") as f:
    content = f.read()
    message_1 = client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=content
    )

# Output the Assistant, Thread, and Messages details
with open("assistant_id.txt", "w") as f:
    f.write(f"Assistant ID: {assistant.id}")

with open("thread_id.txt", "w") as f:
    f.write(f"Thread ID: {thread.id}")

print(f"Assistant ID: {assistant.id}")
print(f"Thread ID: {thread.id}")
print(f"First Message ID: {message_1.id}")
