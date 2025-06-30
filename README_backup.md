# Data Analyst Agent - Complete Setup Guide

**🏗️ Built on Google ADK Samples**

This data-analyst agent is built upon and customized from the original [Google ADK (Agent Development Kit) Samples repository](https://github.com/google/adk-samples), specifically the `data-science` agent. We extend our heartfelt gratitude to the Google AI Platform team and all contributors to the original ADK samples repository for providing this excellent foundation.

## Credits & Acknowledgments

**Original Repository:** [google/adk-samples](https://github.com/google/adk-samples)  
**Original Agent:** `python/agents/data-science`  
**License:** Apache License 2.0  
**Copyright:** 2025 Google LLC  

**Key Contributors:**
- Google AI Platform Team
- ADK Development Team  
- Original data-science agent authors
- All contributors to the adk-samples repository

**Our Customizations:**
- ✅ Configured for existing infrastructure (no new resource creation)
- ✅ Fixed SQL validation issues for production readiness
- ✅ Added comprehensive environment variable management
- ✅ Removed all hardcoded values for security and portability
- ✅ Enhanced deployment procedures and testing workflows
- ✅ Created detailed setup documentation for real-world usage

---

This guide documents the complete process of setting up, configuring, building, deploying, and testing the customized data-analyst agent with your existing Google Cloud infrastructure.

## Overview

**▶️ Watch the Video Walkthrough:** [How to build a Data Science agent with ADK](https://www.youtube.com/watch?v=efcUXoMX818)

The data-analyst agent is a sophisticated multi-agent system designed for advanced data analysis using existing Google Cloud infrastructure. This project demonstrates how multiple specialized agents can work together to handle different aspects of the data pipeline, from data retrieval to advanced analytics and machine learning.

The system is built to interact with BigQuery, perform complex data manipulations, generate data visualizations, and execute machine learning tasks using BigQuery ML (BQML). The agent can generate both text responses and visuals, including plots and graphs for comprehensive data analysis and exploration.

## Agent Details

| Feature | Description |
| --- | --- |
| **Interaction Type:** | Conversational |
| **Complexity:**  | Advanced |
| **Agent Type:**  | Multi Agent |
| **Components:**  | Tools, AgentTools, Session Memory, RAG |
| **Vertical:**  | All (Applicable across industries needing advanced data analysis) |

### Architecture
![Data Analyst Architecture](python/agents/data-analyst/data-science-architecture.png)

### Key Features

*   **Multi-Agent Architecture:** Utilizes a top-level agent that orchestrates sub-agents, each specialized in a specific task.
*   **Database Interaction (NL2SQL):** Employs a Database Agent to interact with BigQuery using natural language queries, translating them into SQL.
*   **Data Science Analysis (NL2Py):** Includes a Data Science Agent that performs data analysis and visualization using Python, based on natural language instructions.
*   **Machine Learning (BQML):** Features a BQML Agent that leverages BigQuery ML for training and evaluating machine learning models.
*   **RAG-Enhanced Intelligence:** Integrates Retrieval Augmented Generation (RAG) capabilities using pre-configured knowledge corpora to provide contextually relevant responses with domain-specific expertise.
*   **Advanced Search & Retrieval:** Leverages semantic search capabilities to find and retrieve relevant information from business documentation, technical specifications, and BQML best practices.
*   **Code Interpreter Integration:** Supports the use of a Code Interpreter extension in Vertex AI for executing Python code, enabling complex data analysis and manipulation.
*   **ADK Web GUI:** Offers a user-friendly GUI interface for interacting with the agents.
*   **Production Ready:** Includes comprehensive configuration management and security hardening.

### Specialized Sub-Agents:
- **Database Agent**: NL2SQL translation and BigQuery interaction
- **Data Science Agent**: NL2Py analysis and Python code execution  
- **Machine Learning Agent**: BigQuery ML (BQML) model training and evaluation
- **RAG Agent**: Retrieval Augmented Generation for contextual knowledge enhancement using business domain expertise and technical documentation
- **Search Agent**: Advanced semantic search capabilities for finding relevant information across organizational knowledge bases and documentation repositories
- **Code Interpreter**: Complex data analysis and visualization

## Prerequisites

- Google Cloud Account with BigQuery enabled
- Python 3.12+
- Poetry (for dependency management)
- Existing Google Cloud infrastructure:

⚠️ **Important Location Note**: This agent is currently tested and validated for **us-central1** region only. While it may work in other Google Cloud regions, compatibility and functionality in other locations have not been verified. If you need to deploy in a different region, additional testing and configuration adjustments may be required.
  - BigQuery project and dataset
  - RAG corpora for business knowledge and BQML documentation
  - Code Interpreter extension in Vertex AI
  - Cloud Storage bucket for staging

## Initial Setup

### 1. Navigate to the Agent Directory

```bash
cd adk-samples/python/agents/data-analyst
```

### 2. Install Dependencies

```bash
poetry install
```

### 3. Activate Poetry Environment

```bash
poetry env activate
# or alternatively:
source $(poetry env info --path)/bin/activate
```

## Configuration

### 1. Environment Variables Setup

The most critical step is setting up the `.env` file with your existing infrastructure details.

**IMPORTANT**: The agent requires `GOOGLE_GENAI_USE_VERTEXAI=1` to use Google Cloud Vertex AI instead of Google AI Studio API.

Create or update your `.env` file:

```bash
# Required Environment Variables
# Use Vertex AI instead of Google AI Studio API
GOOGLE_GENAI_USE_VERTEXAI=1
GOOGLE_CLOUD_PROJECT=your-existing-project-id
BQ_PROJECT_ID=your-existing-project-id
BQ_DATASET_ID=your-existing-dataset-id

# Model Configuration (using Gemini 2.5 Flash)
ROOT_AGENT_MODEL=gemini-2.5-flash
DATA_ANALYST_AGENT_MODEL=gemini-2.5-flash
BIGQUERY_AGENT_MODEL=gemini-2.5-flash
ANALYTICS_AGENT_MODEL=gemini-2.5-flash
BQML_AGENT_MODEL=gemini-2.5-flash

# RAG Configuration - Use your existing RAG corpora
# General business/domain knowledge RAG corpus
RAG_CORPUS=projects/PROJECT_NUMBER/locations/us-central1/ragCorpora/YOUR_RAG_CORPUS_ID
# BQML-specific documentation and examples RAG corpus  
BQML_RAG_CORPUS_NAME=projects/PROJECT_NUMBER/locations/us-central1/ragCorpora/YOUR_BQML_RAG_CORPUS_ID

# Google Cloud Configuration
GOOGLE_CLOUD_LOCATION=us-central1
GOOGLE_CLOUD_STORAGE_BUCKET=your-existing-storage-bucket

# Code Interpreter Configuration (optional)
CODE_INTERPRETER_EXTENSION_NAME=projects/PROJECT_NUMBER/locations/us-central1/extensions/YOUR_EXTENSION_ID

# SQLGen method 
NL2SQL_METHOD=BASELINE

# Additional model configurations
BASELINE_NL2SQL_MODEL=gemini-2.5-flash
CHASE_NL2SQL_MODEL=gemini-2.5-flash
```

### 2. Key Configuration Issues and Fixes

#### Issue 1: Missing Vertex AI Configuration
**Error**: `Missing key inputs argument! To use the Google AI API, provide ('api_key') arguments. To use the Google Cloud API, provide ('vertexai', 'project' & 'location') arguments.`

**Solution**: Add `GOOGLE_GENAI_USE_VERTEXAI=1` to your `.env` file. This tells the Google AI SDK to use Vertex AI instead of Google AI Studio API.

#### Issue 2: SQL Validation False Positives
**Error**: `Invalid SQL: Contains disallowed DML/DDL operations` for valid SELECT queries.

**Root Cause**: The regex pattern in `run_bigquery_validation()` was too broad:
```python
# Problematic pattern - matches substrings
r"(?i)(update|delete|drop|insert|create|alter|truncate|merge)"
```

**Solution**: Fixed to use word boundaries:
```python
# Fixed pattern - matches only complete words
r"(?i)\b(update|delete|drop|insert|create|alter|truncate|merge)\b"
```

## Building the Agent

### 1. Build the Wheel Package

```bash
poetry build --format=wheel --output=deployment
```

This creates `data_analyst-0.1-py3-none-any.whl` in the `deployment/` directory.

## Deployment to Vertex AI Agent Engine

### 1. Prerequisites for Deployment

Ensure you have the required permissions for Vertex AI Agent Engine:

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

### 2. Deploy the Agent

```bash
cd deployment/
poetry run python deploy.py --create
```

**Expected Output**:
```
Successfully created agent: projects/PROJECT_NUMBER/locations/us-central1/reasoningEngines/RESOURCE_ID
```

**Note**: Save the `RESOURCE_ID` for testing and future reference.

### 3. Delete an Agent (if needed)

```bash
poetry run python deploy.py --delete --resource_id=RESOURCE_ID
```

## Testing the Deployed Agent

### 1. Test with the Deployment Script

```bash
export RESOURCE_ID=your-resource-id
export USER_ID=test_user
poetry run python test_deployment.py --resource_id=$RESOURCE_ID --user_id=$USER_ID
```

### 2. Local Testing

Test the agent locally before deployment:

```bash
poetry run adk run data_analyst
```

### 3. Web UI Testing

Test with the ADK web interface:

```bash
poetry run adk web
```

Select `data_analyst` from the dropdown.

## Example Agent Interactions

Here are examples of how users can interact with the Data Analyst Multi-Agent System:

### Database Queries

> **User:** What data do you have access to?

> **Agent:** I have access to the `your_table_name` table in your BigQuery dataset. This table contains your business data with multiple columns including various identifiers, timestamps, and metrics. The table is partitioned by date fields for optimal performance.


### Data Analysis & Visualization

> **User:** Please generate a plot showing total sales per country.

> **Agent:** Result: A bar plot has been generated showing the total sales per country. The x-axis represents the country, and the y-axis represents the total sales.

> **Explanation:** 
> 1. The database agent was first called to retrieve the total sales per country from the train table.
> 2. The data science agent was then called to generate a bar plot visualizing the results. The plot displays each country on the x-axis and its corresponding total sales on the y-axis.

### Machine Learning

> **User:** What kinds of forecasting models can I train in BQML?

> **Agent:** You can train several types of forecasting models in BQML, including:
> - **ARIMA_PLUS**: Advanced ARIMA models with automatic feature engineering
> - **ARIMA_PLUS_XREG**: ARIMA models with external regressors
> - **Exponential Smoothing**: For trend and seasonal patterns
> - **Temporal Fusion Transformer (TFT)**: Deep learning for complex temporal relationships
> 
> Would you like to proceed with training a forecasting model on your data?

> **User:** Yes

> **Agent:** To proceed, I need to know which model you'd like to use. I also need to know the following:
> *   The name of the column that provides the time points (e.g., 'date').
> *   The name of the column that contains the data to forecast (e.g., 'num_sold').
> *   Do you want to fit and forecast multiple time series using a single query? If so, what are the ID columns?

### Schema Exploration
```
User: Hello
Agent: Hello! I'm a Data Science and Data Analytics Multi Agent System. I can help you with questions about your data.

User: what columns are in the table?
Agent: The table contains the following columns: [lists all available columns from your dataset]
```

### Data Queries
```
User: in the table what is the number of rows with created_at in the last week?
Agent: RESULT: There are X rows in the table with `created_at` in the last week.

User: what is the query?
Agent: The query used was:
```sql
SELECT count(*)
FROM `your-project.your_dataset.your_table`
WHERE created_at >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 7 DAY)
```
```

### Latest Data Analysis
```
User: what is the latest date in created_at?
Agent: RESULT: The latest date in the `created_at` column is YYYY-MM-DD.
```

### RAG-Enhanced Knowledge Queries
```
User: What are the best practices for time series forecasting in BQML?
Agent: Based on the BQML documentation and best practices in our knowledge base, here are the key recommendations for time series forecasting:

1. **Data Preparation**: Ensure your time series data has consistent intervals and handle missing values appropriately
2. **Model Selection**: ARIMA_PLUS models work well for most scenarios, while ARIMA_PLUS_XREG is ideal when you have external regressors
3. **Feature Engineering**: Use holiday effects and seasonal decomposition for better accuracy
4. **Model Evaluation**: Always validate using time-based splits to avoid data leakage

Would you like me to help you implement any of these recommendations with your data?
```

### Search-Powered Business Context
```
User: How should I interpret sales performance metrics for our specific business model?
Agent: Based on the business documentation and domain knowledge available, I can provide context-specific insights about sales performance metrics relevant to your business model. Let me search for the most current guidance and best practices...

[Agent retrieves relevant business context and provides tailored recommendations based on organizational knowledge]
```

### Multi-Modal RAG Assistance
```
User: Can you help me understand the relationship between our customer segments and purchasing patterns?
Agent: I'll combine data analysis with business context from our knowledge base to provide comprehensive insights:

1. First, let me query your data to identify customer segments and their purchasing patterns
2. Then I'll enhance these findings with business context and industry best practices from our documentation
3. Finally, I'll provide actionable recommendations based on both the data and domain expertise

[Agent coordinates between database queries, RAG retrieval, and analytical processing to deliver enhanced insights]
```

## Architecture

The agent uses a multi-agent architecture with:

- **Root Agent**: Orchestrates sub-agents and manages overall workflow
- **Database Agent**: Handles BigQuery operations via NL2SQL
- **Analytics Agent**: Performs data analysis using Python/pandas
- **BQML Agent**: Manages BigQuery ML operations for machine learning
- **RAG Agent**: Provides domain-specific knowledge retrieval and context enhancement
- **Search Agent**: Enables semantic search across organizational knowledge bases

## Troubleshooting

### Common Issues

1. **Environment Variable Missing**: Ensure `GOOGLE_GENAI_USE_VERTEXAI=1` is set
2. **Permissions**: Verify BigQuery and Vertex AI permissions are properly configured
3. **Resource Not Found**: Check that all resource IDs in `.env` point to existing infrastructure
4. **SQL Validation Errors**: The regex fix should resolve false positive DML/DDL errors
5. **500 Internal Server Errors**: If you face 500 errors when running the agent, simply re-run your last command. This is a known intermittent issue.
6. **Code Interpreter Issues**: Review the logs to understand errors. Ensure you're using base-64 encoding for files/images if interacting directly with a code interpreter extension.
7. **SQL Generation Errors**: Include clear descriptions in your tables and columns to boost performance. For large databases, consider setting up a RAG pipeline for schema linking by storing table schema details in a vector store.
8. **Region Compatibility**: This agent is tested for `us-central1` region. If deploying in other regions, additional configuration and testing may be required.

### Debug Steps

1. **Test locally first**: Always test with `poetry run adk run data_analyst` before deploying
2. **Check environment**: Verify all required environment variables are set
3. **Verify infrastructure**: Ensure all referenced Google Cloud resources exist and are accessible
4. **Check logs**: Use Google Cloud Console to view Agent Engine logs for deployed agents
5. **Validate permissions**: Ensure the Reasoning Engine Service Agent has proper BigQuery and Vertex AI permissions
6. **Check table descriptions**: Clear column descriptions improve SQL generation accuracy

### Performance Optimization Tips

*   **Prompt Engineering:** Refine the prompts for `root_agent`, `bqml_agent`, `db_agent`, and `ds_agent` to improve accuracy and guide the agents more effectively. Experiment with different phrasing and levels of detail.
*   **Extension:** Extend the multi-agent system with your own AgentTools or sub_agents. You can add additional tools and sub_agents to the root agent in `data_analyst/agent.py`.
*   **Partial imports:** If you only need certain capabilities, e.g., just the data agent, you can import the data_agent as an AgentTool into your own root agent.
*   **Model Selection:** Try different language models for both the top-level agent and the sub-agents to find the best performance for your data and queries.

## Infrastructure Requirements

The agent is designed to work with your **existing** Google Cloud infrastructure:

- **BigQuery**: Existing project, dataset, and tables
- **RAG Corpora**: Pre-configured corpora for business knowledge and BQML documentation  
- **Code Interpreter**: Existing Vertex AI extension for code execution
- **Storage**: Existing Cloud Storage bucket for staging and artifacts

No new infrastructure is created - the agent leverages what you already have set up.

## Resource IDs Reference

Keep track of your resource IDs for reference:

- **Latest Agent Resource ID**: `projects/YOUR_PROJECT_NUMBER/locations/us-central1/reasoningEngines/YOUR_RESOURCE_ID`
- **Project**: `YOUR_EXISTING_PROJECT_ID`
- **Dataset**: `YOUR_EXISTING_DATASET_ID`
- **Storage Bucket**: `YOUR_EXISTING_STORAGE_BUCKET`

## Success Metrics

✅ **Agent deploys successfully** to Vertex AI Agent Engine  
✅ **SQL queries execute** without validation errors  
✅ **Schema exploration** works correctly  
✅ **Data retrieval** with filters and aggregations  
✅ **Multi-agent coordination** between database, analytics, and BQML agents  
✅ **Session management** for conversational interactions  

## Next Steps

With the agent successfully deployed, you can:

1. **Explore your data** using natural language queries
2. **Perform complex analysis** leveraging the analytics agent
3. **Train ML models** using the BQML agent
4. **Generate visualizations** through the code interpreter integration
5. **Scale analysis** across your existing BigQuery datasets

The agent is now ready for production use with your existing Google Cloud infrastructure!

## Testing Framework (Optional)

For development and validation, the original agent includes comprehensive testing capabilities:

### Running Tests

```bash
# Install development dependencies
poetry install --with=dev

# Run integration tests
poetry run pytest tests

# Run evaluation tests  
poetry run pytest eval
```