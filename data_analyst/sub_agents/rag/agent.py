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

import os
from google.adk.agents import Agent
from vertexai.preview import rag
from dotenv import load_dotenv

load_dotenv()


def rag_retrieval_tool(query: str) -> str:
    """Retrieves contextually relevant information from a RAG corpus.

    Args:
        query (str): The query string to search within the corpus.

    Returns:
        str: The response containing retrieved information from the corpus.
    """
    corpus_name = os.getenv("RAG_CORPUS")

    rag_retrieval_config = rag.RagRetrievalConfig(
        top_k=10,  # Optional
        filter=rag.Filter(vector_distance_threshold=0.6),  # Optional
    )
    response = rag.retrieval_query(
        rag_resources=[
            rag.RagResource(
                rag_corpus=corpus_name,
            )
        ],
        text=query,
        rag_retrieval_config=rag_retrieval_config,
    )
    return str(response)


# Create the RAG agent
rag_agent = Agent(
    model='gemini-2.5-flash',
    name='rag_retrieval_agent',
    instruction=(
        "You are a specialized knowledge retrieval agent that helps find relevant information from the RAG corpus. "
        "When given a query, use the rag_retrieval_tool to find relevant documentation and knowledge. "
        "Always provide the retrieved information in a clear, organized manner and highlight the most relevant parts. "
        "If no relevant information is found, clearly state that and suggest refining the query."
    ),
    tools=[
        rag_retrieval_tool,
    ]
) 