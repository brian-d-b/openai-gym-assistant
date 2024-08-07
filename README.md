# openai-gym-assistant
Creates a 4o assistant to recommend gym workouts


HOW TO:

1) Create a file called .env the contents should be: OPENAI_API_KEY=key
2) Edit the prompts in create-assistant.py to your liking
3) Run create-assistant.py
4) Edit most-recent-workout.txt and put in your most recent workout and the date.
5) Run get-response.py
6) View ChatGPT_Response.HTML




# Sample Output

![image](https://github.com/user-attachments/assets/9e8e89f7-57a8-4669-881e-73e0e46c4843)


# Sample Input
## initial-workout.txt:
8/8/2024
- Squats 225lb 5x5
- Deadlift 315lb 3x5
- Leg press 400lb 4x10
- Ran 2 miles

## most-recent-workout.txt

8/9/2024
- OHP 100lb 5x5
- Bench 200lb 5x5
- Tricep pushdown 50lb 4x10
- Pushups 3x10
- Face pulls 3x10
- Ran 2 miles

