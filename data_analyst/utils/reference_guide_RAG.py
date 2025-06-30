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
from pathlib import Path
from dotenv import load_dotenv, set_key
import vertexai
from vertexai import rag


# Define the path to the .env file
env_file_path = Path(__file__).parent.parent.parent / ".env"
print(env_file_path)

# Load environment variables from the specified .env file
load_dotenv(dotenv_path=env_file_path)

PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
corpus_name = os.getenv("BQML_RAG_CORPUS_NAME")

# Get configuration from environment variables
display_name = os.getenv("RAG_CORPUS_DISPLAY_NAME", "bqml_referenceguide_corpus")
rag_data_source = os.getenv("RAG_DATA_SOURCE_PATH", "gs://cloud-samples-data/adk-samples/data-science/bqml")
embedding_model = os.getenv("RAG_EMBEDDING_MODEL", "text-embedding-005")

paths = [rag_data_source]  # Supports Google Cloud Storage and Google Drive Links


# Initialize Vertex AI API once per session
LOCATION = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")
vertexai.init(project=PROJECT_ID, location=LOCATION)


def create_RAG_corpus():
    # Create RagCorpus
    # Configure embedding model using environment variable
    embedding_model_config = rag.RagEmbeddingModelConfig(
        vertex_prediction_endpoint=rag.VertexPredictionEndpoint(
            publisher_model=f"publishers/google/models/{embedding_model}"
        )
    )

    backend_config = rag.RagVectorDbConfig(
        rag_embedding_model_config=embedding_model_config
    )

    bqml_corpus = rag.create_corpus(
        display_name=display_name,
        backend_config=backend_config,
    )

    write_to_env(bqml_corpus.name)

    return bqml_corpus.name


def ingest_files(corpus_name):
    # Get chunking configuration from environment variables
    chunk_size = int(os.getenv("RAG_CHUNK_SIZE", "512"))
    chunk_overlap = int(os.getenv("RAG_CHUNK_OVERLAP", "100"))
    max_requests_per_min = int(os.getenv("RAG_MAX_EMBEDDING_REQUESTS_PER_MIN", "1000"))

    transformation_config = rag.TransformationConfig(
        chunking_config=rag.ChunkingConfig(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
        ),
    )

    rag.import_files(
        corpus_name,
        paths,
        transformation_config=transformation_config,  # Optional
        max_embedding_requests_per_min=max_requests_per_min,  # Optional
    )

    # List the files in the rag corpus
    rag.list_files(corpus_name)


def rag_response(query: str) -> str:
    """Retrieves contextually relevant information from a RAG corpus.

    Args:
        query (str): The query string to search within the corpus.

    Returns:
        vertexai.rag.RagRetrievalQueryResponse: The response containing retrieved
        information from the corpus.
    """
    corpus_name = os.getenv("BQML_RAG_CORPUS_NAME")

    # Get retrieval configuration from environment variables
    top_k = int(os.getenv("RAG_TOP_K", "3"))
    vector_distance_threshold = float(os.getenv("RAG_VECTOR_DISTANCE_THRESHOLD", "0.5"))

    rag_retrieval_config = rag.RagRetrievalConfig(
        top_k=top_k,  # Optional
        filter=rag.Filter(vector_distance_threshold=vector_distance_threshold),  # Optional
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


def write_to_env(corpus_name):
    """Writes the corpus name to the specified .env file.

    Args:
        corpus_name: The name of the corpus to write.
    """

    load_dotenv(env_file_path)  # Load existing variables if any

    # Set the key-value pair in the .env file
    set_key(env_file_path, "BQML_RAG_CORPUS_NAME", corpus_name)
    print(f"BQML_RAG_CORPUS_NAME '{corpus_name}' written to {env_file_path}")


if __name__ == "__main__":
    # rag_corpus = rag.list_corpora()

    corpus_name = os.getenv("BQML_RAG_CORPUS_NAME")

    print("Creating the corpus.")
    corpus_name = create_RAG_corpus()
    print(f"Corpus name: {corpus_name}")

    print(f"Importing files to corpus: {corpus_name}")
    ingest_files(corpus_name)
    print(f"Files imported to corpus: {corpus_name}")
