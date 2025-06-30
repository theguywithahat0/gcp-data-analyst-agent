# Data Analyst Agent - Setup Notes

## Overview

This `data_analyst` agent is a modified copy of the original `data-science` agent with the key difference being that it uses your **existing infrastructure** instead of creating new infrastructure components.

## Key Differences from Original Data-Science Agent

### 1. **No Infrastructure Creation**
- **Original**: Creates new BigQuery datasets, RAG corpora, Code Interpreter extensions, and Cloud Storage buckets
- **Data Analyst**: Uses your existing infrastructure components specified in the `.env` file

### 2. **Simplified Deployment**
- **Original**: Includes bucket setup and infrastructure provisioning
- **Data Analyst**: Deploys directly to existing infrastructure without setup steps

### 3. **Pre-configured Environment**
- Your existing `.env` file has been copied to this directory with the following infrastructure already configured:
  - `GOOGLE_CLOUD_PROJECT=kp-dev-data-warehouse`
  - `BQ_DATASET_ID=kp_dev_agent_test`
  - `RAG_CORPUS=projects/51666693838/locations/us-central1/ragCorpora/4899916394579099648`
  - `BQML_RAG_CORPUS_NAME=projects/51666693838/locations/us-central1/ragCorpora/4035225266123964416`
  - `CODE_INTERPRETER_EXTENSION_NAME=projects/51666693838/locations/us-central1/extensions/9154739421537370112`
  - `GOOGLE_CLOUD_STORAGE_BUCKET=kp-dev-data-warehouse-agent-staging`

## Quick Start

1. **Install dependencies:**
   ```bash
   cd python/agents/data-analyst
   poetry install
   ```

2. **Verify environment:**
   ```bash
   # Your .env file is already configured with existing infrastructure
   cat .env
   ```

3. **Run the agent:**
   ```bash
   poetry run adk run data_analyst
   ```

4. **Deploy to existing infrastructure:**
   ```bash
   # First build the wheel
   poetry build --format=wheel --output=deployment
   
   # Then deploy using existing infrastructure
   cd deployment
   python deploy.py --create
   ```

## What Was Changed

### File Structure
- Renamed `data_science/` package to `data_analyst/`
- Updated all import statements and references
- Modified `pyproject.toml` package name from "data-science" to "data-analyst"

### Deployment Changes
- Removed `setup_staging_bucket()` function
- Modified `deploy.py` to use existing bucket instead of creating new one
- Added support for existing RAG corpus environment variable
- Simplified environment variable handling with fallbacks

### Environment Variables
- Added `RAG_CORPUS` support (your existing general RAG corpus)
- Maintained compatibility with existing variable names
- Added fallbacks for legacy variable names (e.g., `BQ_PROJECT_ID` falls back to `GOOGLE_CLOUD_PROJECT`)

## Benefits

1. **No Infrastructure Overhead**: Uses your existing, tested infrastructure
2. **Faster Setup**: No need to create and configure new resources
3. **Cost Efficient**: Leverages existing resources instead of duplicating them
4. **Consistent Environment**: Uses the same infrastructure as your other projects

## Files Modified

- `deployment/deploy.py` - Removed infrastructure creation, uses existing resources
- All Python files - Updated import statements from `data_science` to `data_analyst`
- `pyproject.toml` - Updated package name and description
- `.env.example` - Updated to reflect existing infrastructure usage
- `README.md` - Updated setup instructions for existing infrastructure 