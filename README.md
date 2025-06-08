# GCP Data Analyst Agent

This is an enhanced version of Google's [Data Science Agent sample](https://github.com/GoogleCloudPlatform/adk-samples/tree/main/python/agents/data-science) from the Agent Development Kit (ADK). The original agent provides a multi-agent system for data science workflows with BigQuery integration, analytics capabilities, and BQML support.

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
data_science/sub_agents/search/
├── __init__.py          # Empty (just copyright)
├── agent.py            # Contains search_agent = Agent(...)
└── prompts.py          # Contains return_instructions_search()
```

**Integration Points:**
- `data_science/sub_agents/__init__.py` - Imports `search_agent`
- `data_science/tools.py` - Contains `async def call_search_agent()`
- `data_science/agent.py` - Conditionally includes `call_search_agent` in tools

**Conditional Behavior:**
- When `ENABLE_GOOGLE_SEARCH=true`: Search agent is created and included in tools
- When `ENABLE_GOOGLE_SEARCH=false` or unset: Search agent is `None`, graceful fallback message

## Quick Start

### Prerequisites

- Python 3.11+
- Google Cloud Project with billing enabled
- BigQuery API enabled
- Vertex AI API enabled

### Installation

1. **Clone and setup:**
    ```bash
   git clone <your-repo-url>
   cd gcp-data-analyst-agent
    poetry install
    ```

2. **Environment setup:**
    ```bash
   cp .env.example .env
   # Edit .env with your Google Cloud project details
    ```

3. **Required environment variables:**
    ```bash
   export GOOGLE_CLOUD_PROJECT='your-project-id'
   export BQ_PROJECT_ID='your-bigquery-project-id'
   export BQ_DATASET_ID='your-dataset-id'
    ```

### Optional Setup

#### Your BigQuery Data
The agent works with any BigQuery dataset. Make sure your BigQuery dataset exists and update your environment variables:
        ```bash
        export BQ_DATASET_ID='your-dataset-name'
        ```

#### Google Search (Optional)
Enable real-time web search functionality:
    ```bash
    export ENABLE_GOOGLE_SEARCH=true
    ```

#### BQML Reference Documentation (Optional)
Set up RAG corpus with BigQuery ML documentation:
    ```bash
    python3 data_science/utils/reference_guide_RAG.py
    ```

#### Document Retrieval (Optional)
To enable custom business document retrieval, set up your own RAG corpus:
    ```bash
export BUSINESS_RAG_CORPUS='projects/your-project/locations/us-central1/ragCorpora/your-business-corpus-id'
    ```

**Note**: 
- Replace `your-project` and `your-business-corpus-id` with your actual values
- This is separate from the BQML technical documentation corpus
- Use this for business-specific documents, KPIs, and domain knowledge

## Usage

### CLI Mode
    ```bash
    poetry run adk run data_science
    ```

### Web UI Mode
    ```bash
    poetry run adk web
    ```
Then select `data_science` from the dropdown.

## Example Interactions

**Data Exploration:**
```
User: What data do you have access to?
Agent: I have access to two tables: train and test. Both contain sales data with columns: id, date, country, store, product, and num_sold.
```

**Analytics:**
```
User: Create a visualization showing sales by country
Agent: [Generates Python code and creates a bar chart visualization]
```

**Machine Learning:**
```
User: Can you train a forecasting model?
Agent: I can help you train ARIMA, ARIMA_PLUS, or other BQML forecasting models. What time series data would you like to forecast?
```

**Real-time Information (when Google Search enabled):**
```
User: What are the latest trends in data science?
Agent: [Uses Google Search to find current information about data science trends]
```

## Testing

Run the test suite:
```bash
poetry install --with=dev
poetry run pytest tests
```

### Test Coverage

Current test coverage: **51%** with **7/7 tests passing** ✅

- ✅ **Database Agent**: Tests SQL query execution
- ✅ **Data Science Agent**: Tests root agent integration with sub-agents
- ✅ **BQML Agent**: Tests model checking functionality  
- ✅ **BQML Agent**: Tests execution planning workflow
- ✅ **Google Search Disabled**: Tests that search is properly disabled by default
- ✅ **Google Search Logic**: Tests conditional logic and configuration
- ✅ **Google Search Integration**: Tests graceful handling when disabled

To run tests with coverage report:
```bash
poetry run pytest tests/ --cov=data_science --cov-report=term-missing
```

**Google Search Testing Notes**: 
- Tests verify proper configuration and conditional behavior
- Search agent isolation prevents Google API "multiple tools" limitation
- Tests pass in both enabled/disabled states
- Production functionality requires Google Search API access

## Deployment on Vertex AI Agent Engine

### Prerequisites for Production Deployment

Before deploying to Vertex AI Agent Engine, you need to set up authentication for production use.

**Important**: This is different from development authentication!
- **Development**: Uses your personal credentials (`gcloud auth application-default login`)
- **Production**: Uses Google-managed Vertex AI service account with BigQuery permissions

### Step 1: Set Up IAM Permissions

When you deploy to Vertex AI Agent Engine, Google automatically creates a **Reasoning Engine Service Agent** to run your agent. You need to grant this service account permissions to access BigQuery.

1. **Get your project number:**
   ```bash
   export GOOGLE_CLOUD_PROJECT=your-project-id
   export GOOGLE_CLOUD_PROJECT_NUMBER=$(gcloud projects describe $GOOGLE_CLOUD_PROJECT --format="value(projectNumber)")
   ```

2. **Grant BigQuery permissions to the Agent Engine service account:**
   ```bash
   export RE_SA="service-${GOOGLE_CLOUD_PROJECT_NUMBER}@gcp-sa-aiplatform-re.iam.gserviceaccount.com"
   
   gcloud projects add-iam-policy-binding ${GOOGLE_CLOUD_PROJECT} \
       --member="serviceAccount:${RE_SA}" \
       --condition=None \
       --role="roles/bigquery.user"
   
   gcloud projects add-iam-policy-binding ${GOOGLE_CLOUD_PROJECT} \
       --member="serviceAccount:${RE_SA}" \
       --condition=None \
       --role="roles/bigquery.dataViewer"
   
   gcloud projects add-iam-policy-binding ${GOOGLE_CLOUD_PROJECT} \
       --member="serviceAccount:${RE_SA}" \
       --condition=None \
       --role="roles/aiplatform.user"
   ```

**Note**: This service account is automatically created by Google - you don't create it manually. The `@gcp-sa-aiplatform-re.iam.gserviceaccount.com` domain indicates it's a Google-managed service agent specifically for AI Platform Reasoning Engine.

### Step 2: Deploy Your Agent

1. **Build the wheel:**
   ```bash
   poetry build --format=wheel --output=deployment
   ```

2. **Deploy to Vertex AI:**
   ```bash
   cd deployment/
   python3 deploy.py --create
   ```

   This will output a resource ID like:
   ```
   projects/************/locations/us-central1/reasoningEngines/7737333693403889664
   ```

3. **Test your deployed agent:**
   ```bash
   export RESOURCE_ID=your-resource-id
   export USER_ID=test-user
   python test_deployment.py --resource_id=$RESOURCE_ID --user_id=$USER_ID
   ```

4. **Delete the agent (when needed):**
   ```bash
   python3 deploy.py --delete --resource_id=$RESOURCE_ID
   ```

### How Production Authentication Works

Once deployed:
- **Users interact** with your agent via Vertex AI API
- **No BigQuery credentials required** from end users
- **Agent uses service account** to query BigQuery on behalf of users
- **Multi-tenant**: Multiple users can use the same agent safely
- **Secure**: Users never see BigQuery directly, only agent responses

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
