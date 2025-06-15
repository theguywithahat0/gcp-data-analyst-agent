#!/usr/bin/env python3
"""
Deployment Verification Script for GCP Data Analyst Agent (ADK Framework)

This script verifies that your deployed agent is working correctly
by running test queries against the deployed agent.
"""

import os
import sys
import json
import logging
import time
from dotenv import load_dotenv
import vertexai
from vertexai import agent_engines

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def print_header():
    """Print verification header."""
    print("🔍 GCP Data Analyst Agent - Deployment Verification")
    print("=" * 80)

def print_status(message, status="info"):
    """Print a status message with color."""
    colors = {
        "info": "\033[94m",  # Blue
        "success": "\033[92m",  # Green
        "error": "\033[91m",  # Red
        "test": "\033[95m",  # Purple
        "response": "\033[96m",  # Cyan
    }
    end_color = "\033[0m"
    print(f"{colors.get(status, colors['info'])}{message}{end_color}")

def format_response(response):
    """Format the agent's response for better readability."""
    try:
        if isinstance(response, str):
            return response
        
        if 'content' in response and 'parts' in response['content']:
            for part in response['content']['parts']:
                if 'text' in part:
                    return part['text']
                elif 'function_response' in part and 'response' in part['function_response']:
                    result = part['function_response']['response'].get('result')
                    if isinstance(result, str) and result.startswith('```json'):
                        try:
                            json_str = result.replace('```json', '').replace('```', '').strip()
                            json_obj = json.loads(json_str)
                            if 'sql_results' in json_obj:
                                return f"SQL Results:\n{json_obj['sql_results']}\n\nNatural Language Results:\n{json_obj['nl_results']}"
                        except:
                            return result
                    return str(result) if result is not None else None
        return str(response)
    except Exception as e:
        logger.error(f"Error formatting response: {e}")
        return str(response)

def verify_agent_deployment():
    """Verify that the agent is deployed and working correctly."""
    try:
        # Load environment variables
        load_dotenv()
        agent_resource_name = os.getenv("AGENT_RESOURCE_NAME")
        if not agent_resource_name:
            raise ValueError("AGENT_RESOURCE_NAME environment variable is not set")

        print_header()
        print_status("Initializing verification...", "info")

        # Get the deployed agent
        print_status("Connecting to deployed agent...", "info")
        agent = agent_engines.get(agent_resource_name)
        print_status("✅ Connected to deployed agent", "success")

        # Log agent details for debugging
        logger.debug(f"Agent details: {agent}")
        logger.debug(f"resource name: {agent.resource_name}")
        
        # Print available methods
        print_status("Available methods on agent:", "info")
        for method in dir(agent):
            if not method.startswith('_'):  # Only show public methods
                print_status(f"- {method}", "info")

        # Create a session
        print_status("Creating session...", "info")
        session = agent.create_session(user_id="verification_user")
        print_status(f"✅ Session created: {session['id']}", "success")
        logger.debug(f"Session details: {session}")

        # Test queries
        test_queries = [
            "What tables are available in the database?",
            "Show me the first 5 rows from the customers table",
            "I want to speak with the BQML agent.",
            "What types of regression models can you help me with? Please explain each type.",
            "I want to speak with the root agent again.",
            "What query would you recommend to find our top customers?"
        ]

        print("\n")
        for i, query in enumerate(test_queries, 1):
            print_status(f"\nTest Query {i}/{len(test_queries)}", "test")
            print_status("-" * 60)
            print_status(f"Query: {query}")

            try:
                logger.debug(f"Sending query to agent: {query}")
                for response in agent.stream_query(
                    user_id="verification_user",
                    session_id=session["id"],
                    message=query
                ):
                    formatted_response = format_response(response)
                    if formatted_response:
                        print_status(formatted_response, "response")
                print_status("✅ Query successful", "success")
            except Exception as e:
                logger.debug(f"Error during query: {str(e)}")
                print_status(f"❌ Query failed: {str(e)}", "error")
                logger.exception("Query error details:")

            print_status("-" * 60)

        print("\n")
        print_status("🎯 Verification Complete!", "success")
        print_status("=" * 40)
        print_status("All queries executed")

    except Exception as e:
        print_status(f"❌ Verification failed: {str(e)}", "error")
        logger.exception("Verification error details:")
        sys.exit(1)

if __name__ == "__main__":
    verify_agent_deployment() 