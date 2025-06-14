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

"""Test cases for the analytics agent and its sub-agents."""

import os
import sys
import pytest
import asyncio

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from deepeval import assert_test
from deepeval.metrics import AnswerRelevancyMetric
from deepeval.test_case import LLMTestCase
from tests.google_vertex_ai import GoogleVertexAI
from google.genai import types
from google.adk.artifacts import InMemoryArtifactService
from google.adk.sessions import Session, InMemorySessionService
from google.adk.runners import Runner
from data_analyst.agent import root_agent
from data_analyst.sub_agents import db_agent, ds_agent, bqml_agent
from data_analyst.tools import call_db_agent, call_ds_agent

pytest_plugins = ("pytest_asyncio",)

@pytest.fixture(scope="function")
async def test_setup():
    """Set up for test methods."""
    session_service = InMemorySessionService()
    artifact_service = InMemoryArtifactService()
    
    session = await session_service.create_session(
        app_name="DataAgent",
        user_id="test_user",
    )
    
    runner = Runner(
        app_name="DataAgent",
        agent=None,
        artifact_service=artifact_service,
        session_service=session_service,
    )
    
    return {
        "session": session,
        "user_id": "test_user",
        "session_id": session.id,
        "runner": runner
    }

async def _run_agent(setup, agent, query):
    """Helper method to run an agent and get the final response."""
    setup["runner"].agent = agent
    content = types.Content(role="user", parts=[types.Part(text=query)])
    events = list(
        setup["runner"].run(
            user_id=setup["user_id"], 
            session_id=setup["session_id"], 
            new_message=content
        )
    )

    last_event = events[-1]
    final_response = "".join(
        [part.text for part in last_event.content.parts if part.text]
    )
    return final_response


@pytest.mark.asyncio
@pytest.mark.root_agent
async def test_root_agent_basic_functionality(test_setup):
    """Test the root agent with a basic query."""
    setup = await test_setup
    query = "Hello! Can you help me with data analysis?"
    response = await _run_agent(setup, root_agent, query)
    print(f"Root agent response: {response}")
    assert response is not None
    assert len(response) > 0

@pytest.mark.asyncio
@pytest.mark.db_agent
async def test_db_agent_can_handle_env_query(test_setup):
    """Test the db_agent with a query from environment variable."""
    setup = await test_setup
    query = "what tables are available in the dataset?"
    response = await _run_agent(setup, db_agent, query)
    print(f"DB agent response: {response}")
    assert response is not None

    # DeepEval Assertion
    model = GoogleVertexAI(model_name="gemini-2.0-flash-001", project=os.environ["GOOGLE_CLOUD_PROJECT"], location="us-central1")
    metric = AnswerRelevancyMetric(threshold=0.7, model=model)
    test_case = LLMTestCase(input=query, actual_output=response)
    assert_test(test_case, [metric])

@pytest.mark.asyncio
@pytest.mark.ds_agent
async def test_ds_agent_can_be_called_from_root(test_setup):
    """Test the ds_agent from the root agent."""
    setup = await test_setup
    query = "analyze the customer data and create a simple visualization"
    response = await _run_agent(setup, root_agent, query)
    print(f"DS agent via root response: {response}")
    assert response is not None

@pytest.mark.asyncio
@pytest.mark.bqml
async def test_bqml_agent_can_check_for_models(test_setup):
    """Test that the bqml_agent can check for existing models."""
    setup = await test_setup
    query = "Are there any existing models in the dataset?"
    response = await _run_agent(setup, bqml_agent, query)
    print(f"BQML agent response: {response}")
    assert response is not None

@pytest.mark.asyncio
@pytest.mark.bqml
async def test_bqml_agent_can_execute_code(test_setup):
    """Test that the bqml_agent can execute BQML code."""
    setup = await test_setup
    query = """
    I want to train a BigQuery ML model on the customer data for prediction.
    Please show me an execution plan. 
    """
    response = await _run_agent(setup, bqml_agent, query)
    print(f"BQML execution plan response: {response}")
    assert response is not None

@pytest.mark.asyncio
@pytest.mark.root_agent
async def test_root_agent_tool_availability():
    """Test that the root agent has the expected tools."""
    # Check that root_agent has the expected tools
    tool_names = []
    for tool in root_agent.tools:
        if hasattr(tool, '__name__'):
            tool_names.append(tool.__name__)
        elif hasattr(tool, 'name'):
            tool_names.append(tool.name)
        else:
            tool_names.append(str(type(tool)))
    
    print(f"Available tools: {tool_names}")
    
    # Verify we have the expected basic tools
    assert "call_db_agent" in tool_names, "DB agent should be present"
    assert "call_ds_agent" in tool_names, "DS agent should be present"
    assert "load_artifacts" in tool_names, "load_artifacts should be present"
    
    # Check if document retrieval is available (depends on BUSINESS_RAG_CORPUS)
    has_doc_retrieval = any("retrieve_documentation" in str(tool) for tool in root_agent.tools)
    print(f"Document retrieval available: {has_doc_retrieval}")

@pytest.mark.asyncio
@pytest.mark.root_agent
async def test_root_agent_sub_agents():
    """Test that the root agent has the expected sub-agents."""
    # Check that root_agent has BQML sub-agent
    sub_agent_names = [agent.name for agent in root_agent.sub_agents]
    print(f"Available sub-agents: {sub_agent_names}")
    
    # BQML should always be enabled in our simplified framework
    assert len(root_agent.sub_agents) > 0, "Root agent should have sub-agents"
    assert any("bqml" in name.lower() or "bq_ml" in name.lower() for name in sub_agent_names), "BQML agent should be present"

@pytest.mark.asyncio
@pytest.mark.integration
async def test_root_agent_database_integration(test_setup):
    """Test that the root agent can successfully call the database agent."""
    setup = await test_setup
    query = "Show me the schema of the available tables"
    response = await _run_agent(setup, root_agent, query)
    print(f"Database integration response: {response}")
    assert response is not None
    assert len(response) > 50  # Should be a substantial response

@pytest.mark.asyncio
@pytest.mark.integration
async def test_root_agent_bqml_integration(test_setup):
    """Test that the root agent can route to BQML agent when requested."""
    setup = await test_setup
    query = "I want to use BigQuery ML to create a model. Can you help me?"
    response = await _run_agent(setup, root_agent, query)
    print(f"BQML integration response: {response}")
    assert response is not None
    # Should mention BQML or machine learning
    assert any(keyword in response.lower() for keyword in ["bqml", "bigquery ml", "machine learning", "model"])

@pytest.mark.asyncio
@pytest.mark.simplified_framework
async def test_simplified_framework_no_search():
    """Test that our simplified framework has no search functionality."""
    # Verify that search-related functionality is completely removed
    tool_names = [tool.__name__ for tool in root_agent.tools if hasattr(tool, '__name__')]
    
    # Should not have any search-related tools
    search_related = [name for name in tool_names if 'search' in name.lower()]
    assert len(search_related) == 0, f"Found search-related tools: {search_related}"
    
    print("✅ Simplified framework correctly has no search functionality")
    print(f"Available tools: {tool_names}")

@pytest.mark.asyncio
@pytest.mark.simplified_framework
async def test_simplified_framework_always_bqml():
    """Test that BQML is always enabled in our simplified framework."""
    # BQML should always be present as a sub-agent
    assert len(root_agent.sub_agents) > 0, "Should have sub-agents"
    
    sub_agent_names = [agent.name for agent in root_agent.sub_agents]
    has_bqml = any("bqml" in name.lower() or "bq_ml" in name.lower() for name in sub_agent_names)
    assert has_bqml, f"BQML should always be enabled. Sub-agents: {sub_agent_names}"
    
    print("✅ BQML is always enabled in simplified framework")
    print(f"Sub-agents: {sub_agent_names}")
