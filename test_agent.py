import vertexai
from vertexai import agent_engines
import os
import uuid

# --- Configuration ---
PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT")
LOCATION = "us-central1"
# The full resource name of your deployed agent
AGENT_RESOURCE_NAME = "projects/115564817055/locations/us-central1/reasoningEngines/1155287653629820928" 
# --- End Configuration ---

def query_agent(prompt: str):
    """Initializes Vertex AI and queries the deployed agent."""
    if not PROJECT_ID:
        raise ValueError("Please set the GOOGLE_CLOUD_PROJECT environment variable.")

    vertexai.init(project=PROJECT_ID, location=LOCATION)

    remote_agent = agent_engines.get(AGENT_RESOURCE_NAME)

    print(f"Querying agent with: '{prompt}'...")
    
    # Generate a random user ID for this test
    user_id = str(uuid.uuid4())

    response_stream = remote_agent.stream_query(message=prompt, user_id=user_id)
    
    print("\\n--- Agent Response ---")
    for chunk in response_stream:
        if "output" in chunk:
            print(chunk["output"], end="")
    print("\\n----------------------\\n")


if __name__ == "__main__":
    # Example query
    example_prompt = "What are the total sales for the last quarter in the 'sales' dataset?"
    try:
        query_agent(example_prompt)
    except Exception as e:
        print(f"An error occurred: {e}") 