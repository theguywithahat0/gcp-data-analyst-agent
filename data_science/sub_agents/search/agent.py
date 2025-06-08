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

"""Search agent for handling Google Search functionality."""

import os

from google.adk.agents import Agent
from google.adk.tools import google_search

from .prompts import return_instructions_search


# Only create the search agent if Google Search is enabled
search_agent = None

if os.getenv("ENABLE_GOOGLE_SEARCH", "false").lower() == "true":
    search_agent = Agent(
        model=os.getenv("SEARCH_AGENT_MODEL", "gemini-2.0-flash-exp"),
        name="search_agent",
        instruction=return_instructions_search(),
        tools=[google_search],
    ) 