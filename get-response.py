import os
import re
from openai import OpenAI
from dotenv import load_dotenv
import datetime

# Get the current date
current_date = datetime.date.today()

# Format the date as "MM/DD/YYYY"
today = current_date.strftime("%m/%d/%Y")


# Load environment variables from .env file
load_dotenv()

# Get the API key from the environment variables
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("No API key found in environment variables.")

# Initialize the OpenAI client
client = OpenAI(api_key=api_key)

# Function to read ID from a local file
def read_id_from_file(file_path):
    with open(file_path, 'r') as file:
        return file.readline().strip().split(": ")[1]

# Function to add a new workout message
def add_workout_message(thread_id, workout_details):
    message = client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=workout_details
    )
    return message

# Read IDs from the local files
assistant_id = read_id_from_file('assistant_id.txt')
thread_id = read_id_from_file('thread_id.txt')

# New workout details input
# Read workout details from a local file
with open('.\most-recent-workout.txt', 'r') as file:
    workout_details = file.read().strip()

# Add the workout message
new_message = add_workout_message(thread_id, workout_details)

# Output the details of the new message
print(f"New Message ID: {new_message.id}")
print(f"Thread ID: {thread_id}")
print(f"Content: {workout_details}")

# Create and poll a run to get the assistant's response
run = client.beta.threads.runs.create_and_poll(
    thread_id=thread_id,
    assistant_id=assistant_id,
    instructions=f"""
        Provide the next workout routine based on the user's latest workout and fitness goals.
            Every time I work out, I will provide the date and the exercises I did. Based on that information, suggest a workout routine for the next day.
            Do not give me anything involving hydration, rest, nutrition, or advice outside of programming my workouts.


    Ensure progressive overload by slightly increasing the weight or reps compared to previous similar workouts.

    Every time I work out, I will provide the date and the exercises I did. Based on that information, suggest a workout routine for the next day.

    Key techniques to enhance workout effectiveness:
    - Engage target muscles (Mind-Muscle Connection)
    - Vary tempo (e.g., slow eccentric, fast concentric)
    - Regularly switch exercises
    - Use drop sets and supersets for intensity
    - Include isometric holds and partial reps
    - Apply rest-pause and constant tension methods
    - Focus on eccentric training
    - Mix rep ranges for diverse muscle fiber stimulation
    - Prioritize compound movements for overall growth

    Example conversation:
    User:
    X/XX/XXXX
    OHP 100 5x5
    Bench 200 5x5
    Tricep pushdown 100 8x3
    Ran 1 mile bpm
    3000 calories burned
    Weight

    Example Output Formatting:
    Tomorrow: Push day

    Overhead Press: 105lb 5x5 (5lb increase)
    Bench Press: 205lb 5x5 (5lb increase)
    Dumbbell Fly: 3x10
    Tricep Dips: 3x12 (add weight if possible)
    Cable Lateral Raises: 3x15
    
    today is: {today}. Give me a workout routine for tomorrow. Keep some minimal variation / tips to spice things up.
    """
)

# Check the run status and get the messages
if run.status == 'completed':
    messages = client.beta.threads.messages.list(thread_id=thread_id).data
    # Get the latest assistant response
    assistant_response = None
    for message in messages:
        if message.role == 'assistant':
            assistant_response = message.content
            break
else:
    print(f"Run status: {run.status}")

if assistant_response:
    # Join the text content from the message parts
    response_text = ''.join([part.text.value for part in assistant_response])

    # Replace newline characters with <br> tags for HTML formatting
    formatted_response = re.sub(r'\n', '<br>', response_text)

    # Replace markdown asterisks for bold formatting
    formatted_response = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', formatted_response)

    # Create the HTML content
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>ChatGPT Response</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 20px;
                padding: 0;
                background-color: #f4f4f9;
                color: #333;
            }}
            .response {{
                background-color: #fff;
                border: 1px solid #ccc;
                padding: 20px;
                margin-bottom: 20px;
                border-radius: 8px;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                white-space: pre-wrap;
            }}
            h1 {{
                text-align: center;
                color: #444;
            }}
            strong {{
                font-weight: bold;
            }}
        </style>
    </head>
    <body>
        <h1>ChatGPT Response</h1>
        <div class='response'>{formatted_response}</div>
    </body>
    </html>
    """

    # Write the HTML content to a file
    html_file_path = "chatgpt_response.html"
    with open(html_file_path, "w") as html_file:
        html_file.write(html_content)

    print(f"HTML file created: {html_file_path}")
else:
    print("No assistant response found.")
