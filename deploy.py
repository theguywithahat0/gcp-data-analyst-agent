import os
import logging
from dotenv import load_dotenv, set_key
import vertexai
from vertexai.preview.reasoning_engines import AdkApp
from vertexai import agent_engines
from vertexai import rag
from data_analyst.agent import root_agent as agent

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables from .env file
load_dotenv()

PROJECT_ID = os.environ["GOOGLE_CLOUD_PROJECT"]
LOCATION = "us-central1"
STAGING_BUCKET = f"gs://{os.environ['GOOGLE_CLOUD_PROJECT']}-adk-staging"
AGENT_WHL_FILE = "dist/data_analyst-0.1-py3-none-any.whl"

def check_or_create_bqml_rag_corpus():
    """Check if BQML RAG corpus exists, create if not."""
    existing_corpus_name = os.getenv("BQML_RAG_CORPUS_NAME")
    
    if existing_corpus_name:
        try:
            # Try to access the existing corpus
            logger.info(f"Checking existing BQML RAG corpus: {existing_corpus_name}")
            corpus = rag.get_corpus(existing_corpus_name)
            logger.info("✅ BQML RAG corpus exists and is accessible")
            return existing_corpus_name
        except Exception as e:
            logger.warning(f"⚠️  Existing BQML RAG corpus not accessible: {e}")
            logger.info("Will create a new one...")
    
    logger.info("📚 Creating BQML RAG corpus with Google's documentation...")
    
    try:
        # Configure embedding model
        embedding_model_config = rag.RagEmbeddingModelConfig(
            vertex_prediction_endpoint=rag.VertexPredictionEndpoint(
                publisher_model="publishers/google/models/text-embedding-005"
            )
        )
        
        backend_config = rag.RagVectorDbConfig(
            rag_embedding_model_config=embedding_model_config
        )
        
        # Create the corpus
        bqml_corpus = rag.create_corpus(
            display_name="bqml_referenceguide_corpus",
            backend_config=backend_config,
        )
        
        corpus_name = bqml_corpus.name
        logger.info(f"✅ Created BQML RAG corpus: {corpus_name}")
        
        # Ingest Google's BQML documentation
        logger.info("📄 Ingesting BQML documentation (89 files)...")
        
        transformation_config = rag.TransformationConfig(
            chunking_config=rag.ChunkingConfig(
                chunk_size=512,
                chunk_overlap=100,
            ),
        )
        
        # Google's curated BQML documentation
        paths = ["gs://cloud-samples-data/adk-samples/data-science/bqml"]
        
        rag.import_files(
            corpus_name,
            paths,
            transformation_config=transformation_config,
            max_embedding_requests_per_min=1000,
        )
        
        logger.info("✅ Successfully imported BQML documentation")
        
        # Update .env file
        set_key(".env", "BQML_RAG_CORPUS_NAME", corpus_name)
        logger.info(f"📝 Updated .env with BQML_RAG_CORPUS_NAME: {corpus_name}")
        
        return corpus_name
        
    except Exception as e:
        logger.error(f"❌ Failed to create BQML RAG corpus: {e}")
        logger.info("Agent will deploy without BQML RAG functionality")
        return None

def check_or_create_business_rag_corpus():
    """Check if Business RAG corpus exists, create if not."""
    existing_corpus_name = os.getenv("BUSINESS_RAG_CORPUS")
    
    if existing_corpus_name:
        try:
            # Try to access the existing corpus
            logger.info(f"Checking existing Business RAG corpus: {existing_corpus_name}")
            corpus = rag.get_corpus(existing_corpus_name)
            logger.info("✅ Business RAG corpus exists and is accessible")
            return existing_corpus_name
        except Exception as e:
            logger.warning(f"⚠️  Existing Business RAG corpus not accessible: {e}")
            logger.info("Will create a new one...")
    
    logger.info("📊 Creating Business RAG corpus...")
    
    try:
        # Configure embedding model
        embedding_model_config = rag.RagEmbeddingModelConfig(
            vertex_prediction_endpoint=rag.VertexPredictionEndpoint(
                publisher_model="publishers/google/models/text-embedding-005"
            )
        )
        
        backend_config = rag.RagVectorDbConfig(
            rag_embedding_model_config=embedding_model_config
        )
        
        # Create the corpus
        business_corpus = rag.create_corpus(
            display_name="business_documentation_corpus",
            backend_config=backend_config,
        )
        
        corpus_name = business_corpus.name
        logger.info(f"✅ Created Business RAG corpus: {corpus_name}")
        logger.info("📝 Note: You can now upload your business documents to this corpus")
        
        # Update .env file
        set_key(".env", "BUSINESS_RAG_CORPUS", corpus_name)
        logger.info(f"📝 Updated .env with BUSINESS_RAG_CORPUS: {corpus_name}")
        
        return corpus_name
        
    except Exception as e:
        logger.error(f"❌ Failed to create Business RAG corpus: {e}")
        logger.info("Agent will deploy without Business RAG functionality")
        return None

def main():
    """Main deployment function."""
    logger.info("🚀 Starting GCP Data Analyst Agent Deployment (Simplified Framework)")
    logger.info(f"📍 Project: {PROJECT_ID}")
    logger.info(f"📍 Location: {LOCATION}")
    
    # Initialize Vertex AI
    vertexai.init(
        project=PROJECT_ID,
        location=LOCATION,
        staging_bucket=STAGING_BUCKET,
    )
    
    # Setup RAG corpora
    logger.info("🧠 Setting up RAG corpora...")
    bqml_corpus = check_or_create_bqml_rag_corpus()
    business_corpus = check_or_create_business_rag_corpus()
    
    # Check for Code Interpreter
    code_interpreter_name = os.getenv("CODE_INTERPRETER_EXTENSION_NAME")
    if not code_interpreter_name:
        logger.warning("⚠️  CODE_INTERPRETER_EXTENSION_NAME is not set in your .env file.")
        logger.warning("The data science agent (nl2py) will not work without it.")
        logger.warning("Please create a separate Reasoning Engine for the code interpreter,")
        logger.warning("and add its resource name to the .env file.")

    # Pass required environment variables for the simplified agent
    # Note: Our simplified framework has fewer environment variables
    env_vars = {
        "ROOT_AGENT_MODEL": os.getenv("ROOT_AGENT_MODEL"),
        "ANALYTICS_AGENT_MODEL": os.getenv("ANALYTICS_AGENT_MODEL"),
        "BASELINE_NL2SQL_MODEL": os.getenv("BASELINE_NL2SQL_MODEL"),
        "BIGQUERY_AGENT_MODEL": os.getenv("BIGQUERY_AGENT_MODEL"),
        "BQML_AGENT_MODEL": os.getenv("BQML_AGENT_MODEL"),
        "CHASE_NL2SQL_MODEL": os.getenv("CHASE_NL2SQL_MODEL"),
        "BQ_DATASET_ID": os.getenv("BQ_DATASET_ID"),
        "BQ_PROJECT_ID": os.getenv("BQ_PROJECT_ID"),
        "BQML_RAG_CORPUS_NAME": bqml_corpus,
        "BUSINESS_RAG_CORPUS": business_corpus,
        "CODE_INTERPRETER_EXTENSION_NAME": code_interpreter_name,
        "NL2SQL_METHOD": os.getenv("NL2SQL_METHOD"),
        # Note: ENABLE_BQML and search-related variables removed in simplified framework
    }
    
    # Remove None values
    env_vars = {k: v for k, v in env_vars.items() if v is not None}
    
    logger.info("🏗️  Creating simplified agent...")
    logger.info("📋 Framework features:")
    logger.info("  • ✅ BQML (always enabled)")
    logger.info("  • ✅ Database queries")
    logger.info("  • ✅ Data science analysis")
    logger.info("  • ❌ Google Search (removed)")
    logger.info("  • ✅ Document retrieval (optional)")
    
    app = AdkApp(agent=agent)
    
    try:
        remote_app = agent_engines.create(
            app,
            display_name="gcp-data-analyst-agent",
            requirements=[AGENT_WHL_FILE],
            extra_packages=[AGENT_WHL_FILE],
            env_vars=env_vars,
        )
        
        logger.info("🎉 Deployment successful!")
        logger.info(f"📋 Resource name: {remote_app.resource_name}")
        logger.info(f"🌐 Agent Engine URL: https://console.cloud.google.com/vertex-ai/agents/locations/{LOCATION}/agent-engines/{remote_app.resource_name.split('/')[-1]}")
        
        print("\n" + "="*70)
        print("🎉 GCP Data Analyst Agent Deployed Successfully!")
        print(f"📋 Resource: {remote_app.resource_name}")
        print("🧠 RAG Corpora Status:")
        print("🚀 Framework Features:")
        print("  • ✅ BQML (always enabled)")
        print("  • ✅ Database queries")
        print("  • ✅ Data science analysis")
        print("  • ✅ Document retrieval")
        print("="*70)
        
        return remote_app
        
    except Exception as e:
        logger.error(f"❌ Deployment failed: {e}")
        raise

if __name__ == "__main__":
    main() 