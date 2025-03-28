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
        name="Asistente Segeplan Oficios",
        instructions="Eres un experimentado escritor de oficios. Tu tarea es ayudar a los usuarios a redactar oficios de manera clara y profesional.",
    )

    result = Runner.run_sync(agent, user_input)
    return jsonify({'response': result.final_output})

if __name__ == '__main__':
    app.run(debug=True)
