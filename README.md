# GCP Data Analyst Agent

This is an enhanced version of Google's [Data Science Agent sample](https://github.com/GoogleCloudPlatform/adk-samples/tree/main/python/agents/data-science) from the Agent Development Kit (ADK). It provides a multi-agent system for data science workflows with BigQuery integration, analytics capabilities, and BQML support, ready to be deployed on Vertex AI.

## Quick Start

### Prerequisites

*   Python 3.11+ and [Poetry](httpss://python-poetry.org/docs/#installation)
*   [Google Cloud SDK](https://cloud.google.com/sdk/docs/install) installed and authenticated.
*   A Google Cloud Project with billing, BigQuery, and Vertex AI APIs enabled.

### 1. Setup

First, clone the repository and install the required Python dependencies using Poetry.

```bash
git clone <your-repo-url>
cd gcp-data-analyst-agent
poetry install
```

Next, create a `.env` file from the example template. This file will hold the environment variables your agent needs to connect to the correct GCP resources.

```bash
cp .env.example .env
```

Now, open the `.env` file and fill in the values for your specific GCP project and BigQuery dataset.

### 2. Deployment to Vertex AI

With the setup complete, deploying the agent to a managed, serverless environment on Vertex AI is a two-step process.

First, package the agent's code into a Python wheel file. This command builds the wheel and places it in a `dist/` directory.

```bash
poetry build --format=wheel
```

Second, run the deployment script. This script reads your `.env` file, connects to your GCP project, and uploads the agent and its dependencies to a new Vertex AI Agent Engine.

```bash
poetry run python3 deploy.py
```

If successful, the script will print the resource name of your newly deployed agent, which will look something like this:
`projects/your-project-number/locations/us-central1/reasoningEngines/your-agent-id`

### 3. Testing the Deployed Agent

Once the agent is deployed, you can test it by running the `test_agent.py` script. This script sends a sample query to your agent and prints the streaming response.

Before running it, open `test_agent.py` and replace the placeholder `AGENT_RESOURCE_NAME` with the full resource name you received from the deployment step.

After updating the resource name, run the test script:

```bash
poetry run python3 test_agent.py
```

You should see the agent's response streamed to your console.

## Local Development and Testing

You can run unit tests to ensure the agent's components are working correctly.

```bash
poetry install --with=dev
poetry run pytest tests/
```

## What's Enhanced

This version includes several improvements over the original Google sample:

### 🔧 **Fixed Issues**
- **Fixed broken unit tests**: Converted from `unittest.TestCase` to `pytest` with proper async/await handling
- **Fixed deployment script**: Corrected wheel file path issues in the deployment process
- **Improved error handling**: Better graceful handling of missing environment variables

### 🚀 **New Features**
- **Document Retrieval Tool**: Generic RAG-based document retrieval using Vertex AI RAG corpus
- **Google Search Integration**: Real-time web search capabilities for current information (with proper sub-agent architecture)
- **Enhanced Tool Architecture**: More modular and extensible tool system

### 🧹 **Code Quality Improvements**
- **Generic Design**: Removed domain-specific references to make the agent reusable
- **Better Documentation**: Cleaner, more comprehensive setup instructions
- **Streamlined Codebase**: Removed unnecessary files and improved organization

## Architecture

The agent maintains the original multi-agent architecture with an additional search capability:

- **Root Agent**: Orchestrates between specialized sub-agents
- **BigQuery Sub-Agent**: Natural language to SQL conversion and query execution
- **Analytics Sub-Agent**: Python code generation and execution for data analysis
- **BQML Sub-Agent**: Machine learning model training and inference with BigQuery ML
- **Search Sub-Agent**: Real-time web search using Google Search API (conditionally enabled)

### Google Search Architecture

The Google Search functionality follows the established sub-agent pattern:

```
data_analyst/sub_agents/search/
├── __init__.py          # Empty (just copyright)
├── agent.py            # Contains search_agent = Agent(...)
└── prompts.py          # Contains return_instructions_search()
```

**Integration Points:**
- `data_analyst/sub_agents/__init__.py` - Imports `search_agent`
- `data_analyst/tools.py` - Contains `async def call_search_agent()`
- `data_analyst/agent.py` - Conditionally includes `call_search_agent` in tools

**Conditional Behavior:**
- When `ENABLE_GOOGLE_SEARCH=true`: Search agent is created and included in tools
- When `ENABLE_GOOGLE_SEARCH=false` or unset: Search agent is `None`, graceful fallback message

## Configuration Options

### Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `GOOGLE_CLOUD_PROJECT` | Your Google Cloud project ID | Yes | - |
| `BQ_PROJECT_ID` | BigQuery project ID | Yes | - |
| `BQ_DATASET_ID` | BigQuery dataset ID | Yes | - |
| `BUSINESS_RAG_CORPUS` | RAG corpus for business document retrieval | No | - |
| `BQML_RAG_CORPUS_NAME` | BQML reference documentation corpus | No | - |
| `ENABLE_BQML` | Enable BigQuery ML agent | No | `true` |
| `ENABLE_GOOGLE_SEARCH` | Enable Google Search tool | No | `false` |
| `NL2SQL_METHOD` | SQL generation method: `BASELINE` or `CHASE` | No | `BASELINE` |
| `CODE_INTERPRETER_EXTENSION_NAME` | Pre-existing Code Interpreter extension | No | - |

### Advanced Configuration

- **Custom SQL Generation**: Set `NL2SQL_METHOD=CHASE` to use the CHASE-SQL method
- **Code Interpreter**: Provide existing extension name to avoid creating duplicates
- **Document Retrieval**: Configure your own RAG corpus for domain-specific knowledge
- **Google Search**: Enable with `ENABLE_GOOGLE_SEARCH=true` for real-time web search

### Deployment Configurations

You can customize the agent's capabilities at deployment time using environment variables:

#### **Minimal Configuration** (Database + Analytics only)
```bash
export ENABLE_BQML=false
export ENABLE_GOOGLE_SEARCH=false
# Only database queries and Python analytics available
```

#### **Analytics + ML Configuration** (No external search)
```bash
export ENABLE_GOOGLE_SEARCH=false
# Database, analytics, and BQML available (no web search)
```

#### **Full Configuration** (All features)
```bash
export ENABLE_BQML=true
export ENABLE_GOOGLE_SEARCH=true
export BUSINESS_RAG_CORPUS='your-corpus-id'
# All features available
```

### Google Search Configuration Details

The Google Search functionality is implemented as a separate sub-agent to avoid Google API limitations:

**When Enabled (`ENABLE_GOOGLE_SEARCH=true`):**
- Creates dedicated search sub-agent with Google Search tool
- Adds `call_search_agent` to root agent tools
- Provides real-time web search capabilities
- Uses your existing Google Cloud credentials

**When Disabled (`ENABLE_GOOGLE_SEARCH=false` or unset):**
- Search sub-agent is `None`
- `call_search_agent` not included in root agent tools
- Function returns helpful message when called directly
- No impact on other agent functionality

**Architecture Benefits:**
- Isolates search functionality to avoid Google API "multiple tools" limitation
- Maintains consistent tool calling pattern (`call_search_agent` like `call_db_agent`)
- Preserves all existing functionality while adding search capability
- Follows established ADK patterns from official samples

### RAG Architecture

The system uses **two separate RAG corpora** for different purposes:

1. **BQML Technical Documentation** (`BQML_RAG_CORPUS_NAME`)
   - Contains BigQuery ML reference documentation
   - Auto-generated via `reference_guide_RAG.py`
   - Used by BQML agent for ML syntax and model guidance
   - **Purpose**: Technical ML queries

2. **Business Documentation** (`BUSINESS_RAG_CORPUS`)
   - Contains your business-specific documents, KPIs, schemas
   - Manually configured with your domain knowledge
   - Used by root agent for business context
   - **Purpose**: Business and domain queries

**Important**: Keep these separate to avoid query confusion and content mixing.

## What's Different from the Original

This enhanced version builds upon Google's excellent foundation while adding:

1. **Production Readiness**: Fixed tests and deployment issues
2. **Extensibility**: Generic document retrieval and web search tools
3. **Maintainability**: Cleaner codebase with better error handling
4. **Flexibility**: Configurable components that work with or without optional features
5. **Google Search Integration**: Proper sub-agent architecture following ADK best practices

## Contributing

This project maintains compatibility with the original Google ADK sample while adding enhancements. When contributing:

- Keep the multi-agent architecture intact
- Maintain backward compatibility with the original APIs
- Add comprehensive tests for new features
- Follow the existing code style and patterns
- Follow the established sub-agent patterns for new functionality

## License

Licensed under the Apache License, Version 2.0. See the original Google sample for full license details.

## Troubleshooting

### Common Issues

| Issue | Solution |
|-------|----------|
| Import errors | Ensure all dependencies are installed: `poetry install` |
| Missing environment variables | Copy `.env.example` to `.env` and fill in your values |
| BigQuery permission errors | Ensure your Google Cloud credentials have BigQuery access |
| Code Interpreter creation fails | Check that Vertex AI API is enabled in your project |
| **Google Search not working** | Set `ENABLE_GOOGLE_SEARCH=true` and ensure you have proper Google Cloud credentials |

### Google Search Tool Information

The Google Search tool implementation:

- **Architecture**: Implemented as a separate sub-agent following ADK patterns
- **Conditional**: Enabled/disabled via `ENABLE_GOOGLE_SEARCH` environment variable
- **API Isolation**: Prevents Google API "multiple tools" limitation by isolating search functionality
- **No additional setup**: Uses your existing Google Cloud credentials
- **Graceful fallback**: Returns helpful message when search is disabled

**Why a separate sub-agent?**
Google's API has a limitation: "Multiple tools are supported only when they are all search tools." By implementing search as a separate sub-agent that only contains the Google Search tool, we avoid this limitation while maintaining clean architecture.

**Test Coverage:**
All Google Search functionality is thoroughly tested:
- ✅ Proper configuration when enabled/disabled
- ✅ Conditional logic for tool inclusion
- ✅ Graceful handling of disabled state
- ✅ Integration with root agent tool system

## Acknowledgments

Based on the [Data Science Agent sample](https://github.com/GoogleCloudPlatform/adk-samples/tree/main/python/agents/data-science) from Google Cloud's Agent Development Kit. Thanks to the Google Cloud team for the excellent foundation.
