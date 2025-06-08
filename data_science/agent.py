# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Top level agent for data agent multi-agents.

-- it get data from database (e.g., BQ) using NL2SQL
-- then, it use NL2Py to do further data analysis as needed
"""
import os
from datetime import date

from google.genai import types

from google.adk.agents import Agent
from google.adk.agents.callback_context import CallbackContext
from google.adk.tools import load_artifacts
from google.adk.tools.retrieval.vertex_ai_rag_retrieval import VertexAiRagRetrieval
from vertexai.preview import rag

from .sub_agents import bqml_agent, search_agent
from .sub_agents.bigquery.tools import (
    get_database_settings as get_bq_database_settings,
)
from .prompts import return_instructions_root
from .tools import call_db_agent, call_ds_agent, call_search_agent

date_today = date.today()

# Create optional tools and sub-agents based on configuration

def create_document_retrieval_tool():
    """Create document retrieval tool only if BUSINESS_RAG_CORPUS is configured."""
    business_rag_corpus = os.getenv("BUSINESS_RAG_CORPUS")
    if business_rag_corpus:
        return VertexAiRagRetrieval(
            name='retrieve_documentation',
            description=(
                'Use this tool to retrieve relevant business documentation, KPIs, formulas, '
                'domain-specific knowledge, and schema information when answering questions '
                'that require business context or data interpretation guidance. '
                'This is separate from technical BQML documentation.'
            ),
            rag_resources=[
                rag.RagResource(rag_corpus=business_rag_corpus)
            ],
            similarity_top_k=5,
            vector_distance_threshold=0.6,
        )
    return None

def should_enable_bqml():
    """Check if BQML agent should be enabled."""
    # Enable BQML by default, but allow disabling via environment variable
    return os.getenv("ENABLE_BQML", "true").lower() in ("true", "1", "yes", "on")

def should_enable_google_search():
    """Check if Google Search should be enabled."""
    return search_agent is not None


# Create optional components
document_retrieval = create_document_retrieval_tool()
enable_bqml = should_enable_bqml()
enable_google_search = should_enable_google_search()


def setup_before_agent_call(callback_context: CallbackContext):
    """Setup the agent."""

    # setting up database settings in session.state
    if "database_settings" not in callback_context.state:
        db_settings = dict()
        db_settings["use_database"] = "BigQuery"
        callback_context.state["all_db_settings"] = db_settings

    # setting up schema in instruction
    if callback_context.state["all_db_settings"]["use_database"] == "BigQuery":
        callback_context.state["database_settings"] = get_bq_database_settings()
        schema = callback_context.state["database_settings"]["bq_ddl_schema"]

        callback_context._invocation_context.agent.instruction = (
            return_instructions_root()
            + f"""

    --------- The BigQuery schema of the relevant data with a few sample rows. ---------
    {schema}

    """
        )


root_agent = Agent(
    model=os.getenv("ROOT_AGENT_MODEL"),
    name="db_ds_multiagent",
    instruction=return_instructions_root(),
    global_instruction=(
        f"""
        You are a Data Science and Data Analytics Multi Agent System.
        Todays date: {date_today}
        """
    ),
    sub_agents=[bqml_agent] if enable_bqml else [],
    tools=[
        call_db_agent,
        call_ds_agent,
        load_artifacts,
    ] + ([call_search_agent] if enable_google_search else []) + ([document_retrieval] if document_retrieval else []),
    before_agent_callback=setup_before_agent_call,
    generate_content_config=types.GenerateContentConfig(temperature=0.01),
)
