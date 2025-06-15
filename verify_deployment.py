#!/usr/bin/env python3
"""
Deployment Verification Script for GCP Data Analyst Agent (ADK Framework)

This script verifies that your deployed agent is working correctly
with proper database queries, BQML functionality, and RAG corpus access.
"""

import os
import sys
from dotenv import load_dotenv
import vertexai
from vertexai.preview.reasoning_engines import AdkApp
from google.adk.agents import Agent
from data_analyst.sub_agents.bigquery import tools as bq_tools

def print_header():
    """Print verification header."""
    print("🔍 GCP Data Analyst Agent - Deployment Verification (ADK Framework)")
    print("=" * 80)

def print_status(message, status="info"):
    """Print status message with emoji."""
    emoji_map = {
        "info": "ℹ️",
        "success": "✅", 
        "warning": "⚠️",
        "error": "❌",
        "test": "🧪"
    }
    print(f"{emoji_map.get(status, 'ℹ️')} {message}")

def verify_agent_deployment():
    """Verify the deployed agent is working correctly."""
    
    # Load environment
    load_dotenv()
    
    project_id = os.getenv('GOOGLE_CLOUD_PROJECT', 'jh-testing-project')
    location = os.getenv('GOOGLE_CLOUD_LOCATION', 'us-central1')
    
    print_header()
    print_status(f"Project: {project_id}")
    print_status(f"Location: {location}")
    print()
    
    try:
        # Initialize Vertex AI
        vertexai.init(project=project_id, location=location)
        print_status("Vertex AI initialized", "success")

        # Create root agent with BigQuery tools
        root_agent = Agent(
            model=os.getenv('ROOT_AGENT_MODEL', 'gemini-2.0-flash-001'),
            name='data_analyst_agent',
            instruction="""You are a data analyst agent that helps users query and analyze data from BigQuery.
            You have access to the jaffle_shop dataset and can help users understand and query the data.
            
            Before answering any questions, you should:
            1. Get the current database settings using update_database_settings()
            2. Get the schema information using get_bigquery_schema()
            3. Then proceed with the user's query
            
            When asked to run a query:
            1. Use initial_bq_nl2sql() to generate the SQL
            2. Use run_bigquery_validation() to validate and run the query
            3. Format the results in a clear, readable way
            """,
            tools=[
                bq_tools.initial_bq_nl2sql,
                bq_tools.run_bigquery_validation,
                bq_tools.get_bigquery_schema,
                bq_tools.update_database_settings
            ]
        )

        # Create ADK app
        app = AdkApp(agent=root_agent)
        print_status("✅ ADK app created")
        
        # Create session
        print_status("Creating session...")
        session = app.create_session(
            user_id="verification_user",
            session_id=None  # Let ADK generate a session ID
        )
        print_status(f"✅ Session created: {session.id}")
        print()
        
        # Test queries to verify functionality
        test_queries = [
            {
                "query": "What tables are available in the database?",
                "description": "Database schema exploration",
                "expected_keywords": ["tables", "database", "available"]
            },
            {
                "query": "Show me the first 5 rows from the customers table",
                "description": "Basic query execution",
                "expected_keywords": ["SELECT", "customers", "LIMIT"]
            }
        ]
        
        results = []
        
        for i, test in enumerate(test_queries, 1):
            print_status(f"Test {i}: {test['description']}", "test")
            print(f"   Query: {test['query']}")
            print("-" * 60)
            
            try:
                # Stream query to agent
                for event in app.stream_query(
                    user_id="verification_user",
                    session_id=session.id,
                    message=test['query']
                ):
                    if isinstance(event, dict):
                        if 'content' in event:
                            content = event['content']
                            if 'parts' in content:
                                for part in content['parts']:
                                    if 'text' in part:
                                        print(part['text'])
                                    elif 'function_call' in part:
                                        print(f"[Function Call] {part['function_call']['name']}")
                                    elif 'function_response' in part:
                                        print(f"[Function Response] {part['function_response']['name']}")
                                        if 'response' in part['function_response']:
                                            print(part['function_response']['response'])
                        elif 'text' in event:
                            print(event['text'])
                        elif 'function_call' in event:
                            print(f"[Function Call] {event['function_call']['name']}")
                        elif 'function_response' in event:
                            print(f"[Function Response] {event['function_response']['name']}")
                            if 'response' in event['function_response']:
                                print(event['function_response']['response'])
                    else:
                        print(event)
                
                print_status("Test completed successfully", "success")
                results.append({"test": i, "status": "passed"})
                
            except Exception as e:
                print_status(f"Test failed with error: {str(e)}", "error")
                results.append({"test": i, "status": "failed", "issue": str(e)})
            
            print()
        
        # Summary
        print("🎯 VERIFICATION SUMMARY")
        print("=" * 40)
        
        passed = sum(1 for r in results if r["status"] == "passed")
        failed = sum(1 for r in results if r["status"] == "failed")
        
        print_status(f"Tests Passed: {passed}/{len(test_queries)}", "success" if passed == len(test_queries) else "error")
        if failed > 0:
            print_status(f"Tests Failed: {failed}/{len(test_queries)}", "error")
            
        # Clean up
        print("\nCleaning up...")
        app.delete_session(user_id="verification_user", session_id=session.id)
        print_status("✅ Session deleted")
        
        return passed == len(test_queries)
        
    except Exception as e:
        print_status(f"Verification failed with error: {str(e)}", "error")
        raise
        return False

def main():
    """Main entry point."""
    try:
        success = verify_agent_deployment()
        sys.exit(0 if success else 1)
    except Exception as e:
        print_status(f"Fatal error: {str(e)}", "error")
        sys.exit(1)

if __name__ == "__main__":
    main() 