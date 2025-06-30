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

"""Web search sub-agent for data analyst."""

import os

from google.adk.agents import Agent
from google.adk.tools import google_search

search_agent = Agent(
    model=os.getenv("ROOT_AGENT_MODEL", "gemini-2.5-flash"),
    name="search_agent",
    instruction="""
    You are a web search specialist agent that helps find current information from the internet.
    
    Your capabilities:
    - Search for real-time information, news, and updates
    - Find technical documentation and research papers
    - Gather market data, trends, and current events
    - Verify facts and get up-to-date information
    
    When searching:
    - Be thorough and use specific search terms
    - Provide relevant, accurate information with sources
    - Include publication dates when available
    - Summarize findings clearly and concisely
    
    Always cite sources and be factual in your responses.
    """,
    tools=[google_search],
) 