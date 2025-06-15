# GCP Data Analyst Agent 🤖

An enhanced multi-agent system for data science and analytics workflows, built on Google's Agent Development Kit (ADK). This agent automatically manages database queries, data analysis, machine learning with BigQuery ML, and provides intelligent document retrieval through RAG (Retrieval-Augmented Generation).

## 🎉 Status: Production Ready

✅ **Fully Deployed & Tested** - Agent successfully deployed and verified working  
✅ **RAG Corpora Configured** - Both BQML and Business RAG corpora operational  
✅ **Permission Issues Resolved** - All authentication and access issues fixed  
✅ **Enhanced Deployment** - Automated RAG setup and comprehensive error handling  

## 🏗️ Architecture

This is a **multi-agent system** with specialized capabilities:

- **🎯 Root Agent**: Orchestrates conversations and routes to specialized sub-agents
- **🔍 BigQuery Sub-Agent**: Natural language to SQL conversion and query execution  
- **📊 Analytics Sub-Agent**: Python code generation and execution for data analysis
- **🤖 BQML Sub-Agent**: Machine learning model training and inference with BigQuery ML
- **🔍 Search Sub-Agent**: Real-time web search using Google Custom Search API
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

   # Models (using Gemini 2.0 Flash by default)
   ROOT_AGENT_MODEL=gemini-2.0-flash-001
   BIGQUERY_AGENT_MODEL=gemini-2.0-flash-001
   ANALYTICS_AGENT_MODEL=gemini-2.0-flash-001
   BQML_AGENT_MODEL=gemini-2.0-flash-001

   # Optional: Google Search (for web search capabilities)
   GOOGLE_SEARCH_API_KEY=your-search-api-key
   GOOGLE_SEARCH_ENGINE_ID=your-search-engine-id

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
│   ├── bqml/               # BigQuery ML workflows
│   └── search/             # Web search capabilities
├── tests/                       # Comprehensive test suite
├── deploy.py                    # Enhanced deployment script
├── .env                        # Environment configuration
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
| `ROOT_AGENT_MODEL` | Root agent model | `gemini-2.0-flash-001` | ✅ |
| `BUSINESS_RAG_CORPUS` | Business RAG corpus name | Auto-generated | ❌ |
| `BQML_RAG_CORPUS_NAME` | BQML RAG corpus name | Auto-generated | ❌ |
| `ENABLE_BQML` | Enable BQML functionality | `true` | ❌ |
| `GOOGLE_SEARCH_API_KEY` | Google Search API key | - | ❌ |
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

### Monitoring and Observability

- **Deployment Logs**: Comprehensive logging with structured output
- **Agent Performance**: Real-time monitoring via GCP Agent Engine console
- **RAG Corpus Status**: Health checks and accessibility validation
- **Error Tracking**: Detailed error messages with resolution guidance
- **Resource Monitoring**: Track usage and performance metrics

## 🔍 Testing Your Agent

After successful deployment, test your agent through multiple channels:

### 1. GCP Console (Recommended)
- Visit the provided Agent Engine URL in GCP Console
- Use the Sessions tab for interactive testing
- Monitor performance and logs in real-time

### 2. API Integration
Use the following endpoints for direct agent access:
- **Query Endpoint**: `https://us-central1-aiplatform.googleapis.com/v1/projects/jh-testing-project/locations/us-central1/reasoningEngines/7972611589561909248:query`
- **Stream Endpoint**: `https://us-central1-aiplatform.googleapis.com/v1/projects/jh-testing-project/locations/us-central1/reasoningEngines/7972611589561909248:streamQuery?alt=sse`

Important usage notes:
1. **Session Management**:
   - Each conversation requires a unique session
   - Sessions are created automatically on first query
   - Maintain the same session ID for continued conversations

2. **Authentication**:
   - Use Google Cloud authentication
   - Ensure proper IAM permissions are set
   - Use `gcloud auth application-default login` for local testing

3. **Making Requests**:
   ```python
   import requests
   import google.auth.transport.requests
   import google.oauth2.credentials

   # Get credentials
   credentials, project = google.auth.default()
   auth_req = google.auth.transport.requests.Request()
   credentials.refresh(auth_req)

   # Headers for authentication
   headers = {
       'Authorization': f'Bearer {credentials.token}',
       'Content-Type': 'application/json',
   }

   # Example query request
   query_data = {
       "prompt": "Your question here",
       "temperature": 0.2
   }

   # For regular queries
   response = requests.post(QUERY_ENDPOINT, headers=headers, json=query_data)

   # For streaming responses
   with requests.get(STREAM_ENDPOINT, headers=headers, stream=True) as response:
       for line in response.iter_lines():
           if line:
               # Process SSE response
               print(line.decode('utf-8'))
   ```

4. **Best Practices**:
   - Keep temperature low (0.2) for analytical queries
   - Use streaming endpoint for real-time responses
   - Handle rate limits and timeouts appropriately
   - Implement proper error handling

5. **Debugging Tips**:
   - Check response status codes
   - Verify authentication token is valid
   - Monitor query execution time
   - Use proper session management

### 3. SDK Integration
```python
import vertexai
from vertexai import agent_engines

# Initialize
vertexai.init(project="your-project", location="us-central1")

# Get agent
agent = agent_engines.get("your-agent-resource-name")

# Query with session
for event in agent.stream_query(
    user_id="user123",
    session_id="session456", 
    message="What tables are available?"
):
    print(event)
```

### Example Queries to Try

**Data Exploration:**
- "Show me the schema of available tables"
- "What are the top 10 customers by revenue?"
- "Analyze sales trends over the last 12 months"

**Machine Learning:**
- "Train a clustering model on customer data"
- "Create a time series forecast for sales"
- "How do I optimize a BigQuery ML model for better performance?"

**Business Intelligence:**
- "What's our customer acquisition cost trend?"
- "Generate a cohort analysis for user retention"
- "Create a dashboard showing key business metrics"

## 🛠️ Development

### Local Development
```bash
# Install dependencies
poetry install

# Run tests
poetry run pytest

# Build package
poetry build --format=wheel --output=dist

# Local testing with ADK Runner
poetry run adk-runner --agent data_analyst.agent:root_agent
```

### Testing
```bash
# Run all tests
poetry run pytest

# Run with coverage
poetry run pytest --cov=data_analyst

# Run specific test categories
poetry run pytest tests/test_agents.py -v
```

## 🔧 Troubleshooting

### Common Issues and Solutions

#### 1. Permission Denied Errors
**Symptom**: `403 PERMISSION_DENIED` errors during deployment or agent queries
**Solution**: 
- Verify GCP authentication: `gcloud auth application-default login`
- Check IAM permissions for Vertex AI, BigQuery, and Cloud Storage
- Ensure project ID is correct in `.env`

#### 2. RAG Corpus Access Issues
**Symptom**: Agent responds but mentions limited source information
**Solution**:
- Check RAG corpus IDs in `.env` file
- Verify corpus exists in correct project/location
- Re-run deployment to recreate RAG corpora: `poetry run python deploy.py`

#### 3. Agent Not Responding
**Symptom**: Agent processes queries but returns no conversational response
**Solution**:
- This was a known issue with incorrect RAG corpus configuration (now resolved)
- Ensure latest deployment with fixed RAG setup
- Check agent logs in GCP Console for detailed error messages

#### 4. Deployment Failures
**Symptom**: Deployment script fails with various errors
**Solution**:
- Check all required APIs are enabled in GCP
- Verify sufficient quotas for Vertex AI and BigQuery
- Review deployment logs for specific error messages
- Ensure staging bucket exists and is accessible

### Getting Help

1. **Check Logs**: Review GCP Console logs for detailed error information
2. **Validate Environment**: Ensure all required environment variables are set
3. **Test Permissions**: Verify IAM roles and API access
4. **Review Documentation**: Check Google's ADK and Vertex AI documentation

## 📚 Documentation & Resources

- [Google Agent Development Kit](https://cloud.google.com/vertex-ai/generative-ai/docs/agent-engine/overview)
- [BigQuery ML Documentation](https://cloud.google.com/bigquery/docs/bqml-introduction)
- [Vertex AI RAG Documentation](https://cloud.google.com/vertex-ai/generative-ai/docs/rag-overview)
- [Gemini 2.0 Flash Model](https://cloud.google.com/vertex-ai/generative-ai/docs/model-reference/gemini)

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes with tests
4. Commit your changes (`git commit -m 'Add amazing feature'`)
5. Push to the branch (`git push origin feature/amazing-feature`)
6. Open a Pull Request

### Development Guidelines
- Add tests for new functionality
- Update documentation for API changes
- Follow existing code style and patterns
- Ensure all tests pass before submitting

## 📄 License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with Google's Agent Development Kit (ADK)
- Enhanced with production-ready features and comprehensive error handling
- Includes curated BigQuery ML documentation from Google Cloud samples
- Inspired by modern data science and MLOps best practices

---

**🚀 Ready for Production** | Built with ❤️ using Google's Agent Development Kit

*Last Updated: January 2025 - Fully tested and production-ready*
