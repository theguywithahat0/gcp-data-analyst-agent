import os
import vertexai
from dotenv import load_dotenv

# NEW: Import necessary authentication libraries
import google.auth
from google.auth import impersonated_credentials

from data_analyst.agent import root_agent
from vertexai import agent_engines

# Load environment variables from .env file
load_dotenv()

def deploy_agent():
    """Deploys the data analyst agent to Vertex AI Agent Engine."""

    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    location = os.getenv("GOOGLE_CLOUD_LOCATION")
    staging_bucket = os.getenv("GOOGLE_CLOUD_STORAGE_BUCKET")
    service_account_email = os.getenv("AGENT_SERVICE_ACCOUNT")

    if not all([project_id, location, staging_bucket, service_account_email]):
        raise ValueError(
            "Missing required environment variables: GOOGLE_CLOUD_PROJECT, "
            "GOOGLE_CLOUD_LOCATION, GOOGLE_CLOUD_STORAGE_BUCKET, AGENT_SERVICE_ACCOUNT"
        )

    # NEW: Create credentials that impersonate the target service account.
    # This ensures that the deployed agent runs with the correct permissions.
    print(f"Creating credentials to impersonate service account: {service_account_email}")
    creds, _ = google.auth.default(
        scopes=["https://www.googleapis.com/auth/cloud-platform"]
    )
    impersonated_creds = impersonated_credentials.Credentials(
        source_credentials=creds,
        target_principal=service_account_email,
        target_scopes=["https://www.googleapis.com/auth/cloud-platform"],
        lifetime=3600,
    )

    print(f"Initializing Vertex AI for project '{project_id}' in '{location}'...")
    # UPDATED: Initialize the SDK with the impersonated credentials.
    vertexai.init(
        project=project_id,
        location=location,
        staging_bucket=f"gs://{staging_bucket}",
        credentials=impersonated_creds,
    )

    print("Deploying agent to Vertex AI Agent Engine...")
    remote_app = agent_engines.create(
        agent_engine=root_agent,
        requirements=[
            "google-cloud-aiplatform[adk,agent-engines]",
            "python-dotenv",
            "immutabledict",
            "sqlglot",
            "db-dtypes",
            "regex",
            "tabulate",
            "pydantic",
            "google-cloud-bigquery",
            "llama-index",
            "cloudpickle",
        ],
        display_name="Data Analyst Agent",
        description="An agent for data analysis with BigQuery, analytics, and ML capabilities.",
    )

    print(f"Agent '{remote_app.display_name}' created. Deploying...")
    # UPDATED: The service_account is no longer passed here,
    # as the entire session is now authenticated.
    remote_app.deploy()

    print(f"Agent '{remote_app.display_name}' deployed successfully.")
    print(f"Resource name: {remote_app.resource_name}")


if __name__ == "__main__":
    deploy_agent() 