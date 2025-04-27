import os
from random import randint
from flask import Flask, render_template, request, session, jsonify
from dotenv import load_dotenv

from agent import OpenAIChatAgent

# Load environment variables
load_dotenv()

# Flask app
application = Flask(__name__)
application.secret_key = os.getenv("FLASK_SECRET_KEY")

# ========== Set up Agent ========== #
openai_agent = OpenAIChatAgent()

# Session storage
store = {}

def get_session_state(session_id: str) -> dict:
    """Retrieve the session state for a given session ID.

    If the session ID does not exist in the store, initialize it.

    Args:
        session_id (str): The unique identifier for the user session.

    Returns:
        dict: The session state containing message history.
    """
    if session_id not in store:
        store[session_id] = {"messages": []}
    return store[session_id]

def update_session_state(session_id: str, new_state: dict):
    """Update the session state for a given session ID.

    Args:
        session_id (str): The unique identifier for the user session.
        new_state (dict): The new state to save, typically containing messages.
    """
    store[session_id] = {"messages": new_state["messages"]}

def get_completion(user_input: str, session_id: str) -> dict:
    """Generate a response from the agent and update the session state.

    Args:
        user_input (str): The user's message input.
        session_id (str): The session identifier.

    Returns:
        dict: The response data containing the assistant's reply and token usage information.
    """
    state = get_session_state(session_id)

    # Prepare the prompt
    input_prompt = user_input

    # Query the agent
    response_data = openai_agent.chat(prompt=input_prompt)

    # Update session state
    updated_messages = state["messages"] + [
        {"role": "user", "content": user_input},
        {"role": "assistant", "content": response_data["response"]}
    ]
    update_session_state(session_id, {"messages": updated_messages})

    return response_data

# ========== Routes ========== #

@application.route("/")
def home():
    """Render the homepage and initialize session if not present.

    Returns:
        flask.Response: The rendered HTML homepage.
    """
    if 'session_id' not in session:
        session['session_id'] = str(randint(0, 9999))
    return render_template("./index.html")

@application.route("/get")
def get_bot_response():
    """Handle user input, interact with the agent, and return the response.

    Returns:
        flask.Response: A JSON response containing the agent's reply and token usage stats.
    """
    user_text = request.args.get('msg')
    session_id = session.get('session_id')

    response_data = get_completion(user_text, session_id)

    return jsonify({
        "response": response_data["response"],
        "prompt_tokens": response_data["prompt_tokens"],
        "completion_tokens": response_data["completion_tokens"],
        "total_tokens": response_data["total_tokens"],
        "cost_in": response_data["cost_in"],
        "cost_out": response_data["cost_out"],
        "cost_total": response_data["cost_total"],
    })

# ========== Main ========== #

if __name__ == "__main__":
    application.debug = True
    application.run()