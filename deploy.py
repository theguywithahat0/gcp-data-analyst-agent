import os
from dotenv import load_dotenv
import vertexai
from vertexai.preview.reasoning_engines import AdkApp
from vertexai import agent_engines
from data_analyst.agent import root_agent as agent

# Load environment variables from .env file
load_dotenv()

PROJECT_ID = os.environ["GOOGLE_CLOUD_PROJECT"]
LOCATION = "us-central1"
STAGING_BUCKET = f"gs://{os.environ['GOOGLE_CLOUD_PROJECT']}-adk-staging"
AGENT_WHL_FILE = "dist/data_analyst-0.1-py3-none-any.whl"

vertexai.init(
    project=PROJECT_ID,
    location=LOCATION,
    staging_bucket=STAGING_BUCKET,
)

# Pass required environment variables for the agent
env_vars = {
    "BIGQUERY_AGENT_MODEL": os.getenv("BIGQUERY_AGENT_MODEL"),
    # Add other necessary env vars from your .env file here
    "ROOT_AGENT_MODEL": os.getenv("ROOT_AGENT_MODEL"),
    "ANALYTICS_AGENT_MODEL": os.getenv("ANALYTICS_AGENT_MODEL"),
    "BASELINE_NL2SQL_MODEL": os.getenv("BASELINE_NL2SQL_MODEL"),
    "BQML_AGENT_MODEL": os.getenv("BQML_AGENT_MODEL"),
    "CHASE_NL2SQL_MODEL": os.getenv("CHASE_NL2SQL_MODEL"),
    "BQ_DATASET_ID": os.getenv("BQ_DATASET_ID"),
    "BQ_PROJECT_ID": os.getenv("BQ_PROJECT_ID"),
    "BQML_RAG_CORPUS_NAME": os.getenv("BQML_RAG_CORPUS_NAME"),
    "CODE_INTERPRETER_EXTENSION_NAME": os.getenv("CODE_INTERPRETER_EXTENSION_NAME"),
    "NL2SQL_METHOD": os.getenv("NL2SQL_METHOD"),
}

app = AdkApp(agent=agent)

remote_app = agent_engines.create(
    app,
    display_name="gcp-data-analyst-agent",
    requirements=[AGENT_WHL_FILE],
    extra_packages=[AGENT_WHL_FILE],
    env_vars=env_vars,
)

print(remote_app)
print(f"Deployment finished. Resource name: {remote_app.resource_name}") 