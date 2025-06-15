# GCP Data Analyst Agent 🤖

An enhanced multi-agent system for data science and analytics workflows, built on Google's Agent Development Kit (ADK). This agent automatically manages database queries, data analysis, machine learning with BigQuery ML, and provides intelligent document retrieval through RAG (Retrieval-Augmented Generation).

## 🎉 Status: Production Ready

✅ **Fully Deployed & Tested** - Agent successfully deployed and verified working  
✅ **RAG Corpora Configured** - Both BQML and Business RAG corpora operational  
✅ **Permission Issues Resolved** - All authentication and access issues fixed  
✅ **Enhanced Deployment** - Automated RAG setup and comprehensive error handling  
✅ **Verification Script** - Automated testing of all agent capabilities

## 🏗️ Architecture

This is a **multi-agent system** with specialized capabilities:

- **🎯 Root Agent**: Orchestrates conversations and routes to specialized sub-agents
- **🔍 BigQuery Sub-Agent**: Natural language to SQL conversion and query execution  
- **📊 Analytics Sub-Agent**: Python code generation and execution for data analysis
- **🤖 BQML Sub-Agent**: Machine learning model training and inference with BigQuery ML
- **📚 RAG Integration**: Intelligent document retrieval for business context and BQML documentation

## ✨ Key Features

### 🚀 **Conversational Data Analysis**
- Natural language queries for complex data analysis
- Automatic SQL generation and execution
- Python code generation for advanced analytics
- Interactive data visualization and reporting

### 🧠 **Machine Learning Integration**
- BigQuery ML model creation and training
- Model evaluation and inference
- Automated feature engineering suggestions
- ML workflow orchestration

### 📚 **Intelligent Document Retrieval**
- **BQML RAG**: 89 curated Google documentation files for BigQuery ML
- **Business RAG**: Custom business documentation and KPIs
- Context-aware responses using relevant documentation

### 🔧 **Smart Infrastructure**
- Automatic RAG corpus creation and management
- Environment-aware deployment with validation
- Comprehensive error handling and logging
- Production-ready configuration with fallbacks
- Automated verification and testing

## 🚀 Quick Start

### Prerequisites

1. **Google Cloud Project** with the following APIs enabled:
   - Vertex AI API
   - BigQuery API
   - Cloud Storage API
   - Agent Engine API

2. **Authentication**: 
   ```bash
   gcloud auth application-default login
   gcloud config set project YOUR_PROJECT_ID
   ```

3. **Python Environment**:
   ```bash
   # Install Poetry (if not installed)
   curl -sSL https://install.python-poetry.org | python3 -

   # Install dependencies
   poetry install
   ```

### Configuration

1. **Copy and configure environment variables**:
   ```bash
   cp .env.example .env
   # Edit .env with your specific values
   ```

2. **Key Environment Variables**:
   ```bash
   # Required
   GOOGLE_CLOUD_PROJECT=your-project-id
   BQ_PROJECT_ID=your-project-id
   BQ_DATASET_ID=your-dataset-id
   AGENT_RESOURCE_NAME=your-deployed-agent-resource-name

   # Models (using Gemini 2.0 Flash by default)
   ROOT_AGENT_MODEL=gemini-2.0-flash-001
   BIGQUERY_AGENT_MODEL=gemini-2.0-flash-001
   ANALYTICS_AGENT_MODEL=gemini-2.0-flash-001
   BQML_AGENT_MODEL=gemini-2.0-flash-001

   # RAG Corpora (auto-created during deployment)
   BUSINESS_RAG_CORPUS=auto-generated
   BQML_RAG_CORPUS_NAME=auto-generated
   ```

### Deployment

1. **Build the agent package**:
   ```bash
   poetry build --format=wheel --output=dist
   ```

2. **Deploy to GCP Agent Engine**:
   ```bash
   poetry run python deploy.py
   ```

   The enhanced deployment script will automatically:
   - ✅ **Validate Environment**: Check all required configurations
   - ✅ **RAG Corpus Management**: Check existing or create new RAG corpora
   - ✅ **BQML Documentation**: Auto-populate with 89 Google BQML docs
   - ✅ **Business RAG Setup**: Create empty corpus ready for your documents
   - ✅ **Agent Deployment**: Deploy with all configurations and dependencies
   - ✅ **Verification**: Provide endpoints and console URLs for testing
   - ✅ **Error Recovery**: Graceful handling of permission and configuration issues

3. **Verify Deployment**:
   ```bash
   poetry run python verify_deployment.py
   ```

   The verification script will:
   - ✅ **Test Connection**: Verify agent connectivity
   - ✅ **Query Testing**: Run sample queries to test functionality
   - ✅ **Sub-Agent Testing**: Verify all sub-agents are working
   - ✅ **RAG Testing**: Validate document retrieval capabilities
   - ✅ **Error Handling**: Check error handling and recovery

## 🧠 RAG Corpus Management

### BQML RAG Corpus
- **Content**: 89 curated Google BigQuery ML documentation files from `gs://cloud-samples-data/adk-samples/data-science/bqml`
- **Includes**: Comprehensive documentation for:
  - ARIMA_PLUS, AutoML Tables, K-means clustering
  - PCA, Wide-and-Deep, Autoencoder models
  - XGBoost, Linear/Logistic Regression
  - Model evaluation, hyperparameter tuning
  - Best practices and optimization techniques
- **Purpose**: Provides expert-level BQML guidance and syntax
- **Auto-Creation**: Automatically created and populated during deployment

### Business RAG Corpus  
- **Content**: Your custom business documentation, KPIs, and domain knowledge
- **Purpose**: Provides business context for data analysis and decision-making
- **Auto-Creation**: Empty corpus created during deployment, ready for your documents
- **Usage**: Upload documents via GCP Console RAG API, or programmatically

### RAG Corpus Validation
The deployment script includes comprehensive RAG corpus validation:
- **Accessibility Check**: Verifies corpus exists and is accessible
- **Permission Validation**: Ensures proper IAM permissions
- **Content Verification**: Confirms successful document ingestion
- **Fallback Handling**: Graceful degradation if RAG is unavailable

## 🔧 Usage Examples

### Basic Data Analysis
```
User: "How many customers do we have in each country?"
Agent: [Generates SQL, executes query, provides results and analysis]
```

### Advanced Analytics
```
User: "Create a visualization showing sales trends by month with forecasting"
Agent: [Generates Python code, creates visualizations, provides insights]
```

### Machine Learning with RAG
```
User: "Train a logistic regression model to predict customer churn"
Agent: [Uses BQML RAG to find best practices, generates optimized BQML code, trains model]
```

### Business Context Queries
```
User: "What's our customer lifetime value calculation methodology?"
Agent: [Retrieves business documentation, provides context-aware response]
```

## 🏗️ Project Structure

```
gcp-data-analyst-agent/
├── data_analyst/                 # Main agent package
│   ├── agent.py                 # Root agent configuration
│   ├── prompts.py               # Agent instructions and prompts
│   ├── tools.py                 # Agent orchestration tools
│   └── sub_agents/              # Specialized sub-agents
│       ├── bigquery/            # SQL generation and execution
│       ├── analytics/           # Python data analysis
│       └── bqml/                # BigQuery ML workflows
├── tests/                       # Comprehensive test suite
├── deploy.py                    # Enhanced deployment script
├── verify_deployment.py         # Deployment verification script
├── .env                         # Environment configuration
├── pyproject.toml              # Python project configuration
├── poetry.lock                 # Dependency lock file
└── README.md                   # This documentation
```

## 🚀 Advanced Features

### Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `GOOGLE_CLOUD_PROJECT` | GCP Project ID | - | ✅ |
| `BQ_PROJECT_ID` | BigQuery Project ID | - | ✅ |
| `BQ_DATASET_ID` | BigQuery Dataset ID | - | ✅ |
| `AGENT_RESOURCE_NAME` | Deployed agent resource name | - | ✅ |
| `ROOT_AGENT_MODEL` | Root agent model | `gemini-2.0-flash-001` | ✅ |
| `BUSINESS_RAG_CORPUS` | Business RAG corpus name | Auto-generated | ❌ |
| `BQML_RAG_CORPUS_NAME` | BQML RAG corpus name | Auto-generated | ❌ |
| `ENABLE_BQML` | Enable BQML functionality | `true` | ❌ |
| `NL2SQL_METHOD` | SQL generation method | `BASELINE` | ❌ |

### Enhanced Deployment Features

The deployment script provides enterprise-grade features:

1. **🔍 Pre-flight Validation**: Comprehensive environment and permission checks
2. **🧠 Intelligent RAG Setup**: Automatic corpus creation with validation
3. **📚 Content Management**: Auto-population of BQML documentation
4. **🔄 Environment Updates**: Automatic `.env` file updates with resource IDs
5. **📊 Deployment Logging**: Detailed logging for troubleshooting
6. **🛡️ Error Recovery**: Graceful handling of common deployment issues
7. **✅ Post-deployment Verification**: Endpoint validation and testing guidance

### Verification Script

The `verify_deployment.py` script provides comprehensive testing:

1. **🔍 Connection Testing**:
   - Verifies agent connectivity
   - Tests session creation and management
   - Validates response formatting

2. **🚀 Functionality Testing**:
   - Tests basic data queries
   - Verifies sub-agent routing
   - Checks RAG integration
   - Validates BQML capabilities

3. **📊 Response Validation**:
   - Formats responses for readability
   - Validates response structure
   - Checks error handling
   - Monitors performance

4. **🔧 Debugging Features**:
   - Detailed logging
   - Response formatting
   - Error tracing
   - Performance monitoring

### Monitoring and Observability

- **Deployment Logs**: Comprehensive logging with structured output
- **Agent Performance**: Real-time monitoring via GCP Agent Engine console
- **RAG Corpus Status**: Health checks and accessibility validation
- **Error Tracking**: Detailed error messages with resolution guidance
- **Resource Monitoring**: Track usage and performance metrics

## 🔍 Testing Your Agent

After successful deployment, test your agent through multiple channels:

### 1. Automated Verification
```bash
poetry run python verify_deployment.py
```
This will run a comprehensive suite of tests to verify all agent capabilities.

### 2. GCP Console (Recommended)
- Visit the provided Agent Engine URL in GCP Console
- Use the Sessions tab for interactive testing
- Monitor performance and logs in real-time

### 3. API Integration
Use the following endpoints for direct agent access:
- **Query Endpoint**: `https://us-central1-aiplatform.googleapis.com/v1/[AGENT_RESOURCE_NAME]:query`
- **Stream Endpoint**: `https://us-central1-aiplatform.googleapis.com/v1/[AGENT_RESOURCE_NAME]:streamQuery?alt=sse`

Important usage notes:
1. **Session Management**:
   - Each conversation requires a unique session
   - Sessions are created automatically on first query
   - Session state is maintained for context awareness

2. **Response Handling**:
   - Responses include structured data and natural language
   - SQL results are formatted for readability
   - Error messages include resolution guidance
   - Performance metrics are included in response metadata

3. **Best Practices**:
   - Start with simple queries to verify functionality
   - Test each sub-agent's capabilities separately
   - Validate RAG integration with specific queries
   - Monitor response times and performance
   - Use the verification script for regression testing

## 🛠️ Development

### Local Development
```