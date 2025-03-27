from flask import Flask, request, jsonify
from agents import Agent, Runner
import os

app = Flask(__name__)

openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    raise ValueError("OPENAI_API_KEY not found in environment variables")

@app.route('/api/agent', methods=['POST'])
def agent_response():
    data = request.json
    user_input = data.get('input', '')

    # Define the agent
    agent = Agent(
        name="Assistant",
        instructions="You are a helpful assistant that provides concise responses."
    )

    result = Runner.run_sync(agent, user_input)
    return jsonify({'response': result.final_output})

if __name__ == '__main__':
    app.run(debug=True)
