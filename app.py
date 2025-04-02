from flask import Flask, request, jsonify
from flask_cors import CORS
from agents import Agent, Runner, RunConfig
import os
import asyncio

app = Flask(__name__)
CORS(app, resources={
    r"/*": {
        "origins": [
            "http://localhost:5173",
            "http://127.0.0.1:5173",
            "https://iasegeplan.redciudadana.org/login"
        ]
    }
})

openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    raise ValueError("OPENAI_API_KEY not found in environment variables")

def run_agent_sync(agent, user_input, run_config):
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    return loop.run_until_complete(Runner.run(agent, user_input, run_config=run_config))

@app.route('/api/agent', methods=['POST'])
def agent_response():
    data = request.json
    user_input = data.get('input', '')

    agent = Agent(
        name="Asistente Segeplan Oficios",
        instructions="Eres un experimentado escritor de oficios. Tu tarea es ayudar a los usuarios a redactar oficios de manera clara y profesional.",
    )

    run_config = RunConfig(model="gpt-4o-mini")

    result = run_agent_sync(agent, user_input, run_config)
    return jsonify({'response': result.final_output})

if __name__ == '__main__':
    app.run(debug=True)
