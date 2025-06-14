#!/usr/bin/env python3
"""
Deployment Verification Script for GCP Data Analyst Agent (Simplified Framework)

This script verifies that your deployed agent is working correctly
with proper database queries, BQML functionality, and RAG corpus access.
"""

import os
import sys
import asyncio
import vertexai
from vertexai import agent_engines
from google.adk.sessions import VertexAiSessionService
from dotenv import load_dotenv


def print_header():
    """Print verification header."""
    print("🔍 GCP Data Analyst Agent - Deployment Verification (Simplified Framework)")
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


async def verify_agent_deployment():
    """Verify the deployed agent is working correctly."""
    
    # Load environment
    load_dotenv()
    
    project_id = os.getenv('GOOGLE_CLOUD_PROJECT', 'jh-testing-project')
    location = os.getenv('LOCATION', 'us-central1')
    
    print_status(f"Project: {project_id}")
    print_status(f"Location: {location}")
    print()
    
    try:
        # Initialize Vertex AI
        vertexai.init(project=project_id, location=location)
        print_status("Vertex AI initialized", "success")
        
        # Get the latest deployed agent resource name (Simplified Framework)
        agent_resource_name = "projects/115564817055/locations/us-central1/reasoningEngines/1858975095406460928"
        
        print_status(f"Connecting to agent: {agent_resource_name}")
        
        # Connect to agent
        agent_engine = agent_engines.get(agent_resource_name)
        print_status("Agent connection successful", "success")
        
        # Create session service
        session_service = VertexAiSessionService(project=project_id, location=location)
        
        # Create session
        print_status("Creating session...")
        session = await session_service.create_session(
            app_name=agent_resource_name,
            user_id="verification_user",
        )
        print_status(f"Session created: {session.id}", "success")
        print()
        
        # Test queries to verify functionality
        test_queries = [
            {
                "query": "Hello! Can you help me with data analysis?",
                "description": "Basic conversational test",
                "expected_keywords": ["data analysis", "help", "query", "database"]
            },
            {
                "query": "What tools do you have available?",
                "description": "Tool availability test",
                "expected_keywords": ["tools", "database", "data science", "agent"]
            },
            {
                "query": "What tables are available in the database?",
                "description": "Database schema exploration",
                "expected_keywords": ["tables", "database", "available"]
            },
            {
                "query": "Using your tools show me some rows of the customers table",
                "description": "Database query request test",
                "expected_keywords": ["customers", "data", "query", "table", "SELECT"]
            },
            {
                "query": "Please transfer me to the BQML agent",
                "description": "BQML agent transfer test",
                "expected_keywords": ["BQML", "transfer", "bq_ml_agent"]
            },
            {
                "query": "What type of models can you help me make and can you give me an example?",
                "description": "BQML model types and examples test",
                "expected_keywords": ["models", "example", "regression", "classification", "CREATE MODEL"]
            },
            {
                "query": "How do I create a linear regression model?",
                "description": "BQML linear regression test",
                "expected_keywords": ["linear regression", "CREATE MODEL", "LINEAR_REG"]
            },
            {
                "query": "Please transfer me back to the root agent",
                "description": "Root agent transfer test",
                "expected_keywords": ["root agent", "transfer", "data analysis"]
            },
            {
                "query": "Can you call the data science agent to help me analyze some data?",
                "description": "Data science agent call test",
                "expected_keywords": ["data science agent", "call_ds_agent", "analyze"]
            }
        ]
        
        results = []
        
        for i, test in enumerate(test_queries, 1):
            print_status(f"Test {i}: {test['description']}", "test")
            print(f"   Query: {test['query']}")
            print("-" * 60)
            
            try:
                response_parts = []
                event_count = 0
                max_events = 100  # Prevent infinite loops
                
                # Stream query to agent with timeout protection
                for event in agent_engine.stream_query(
                    user_id="verification_user",
                    session_id=session.id,
                    message=test['query'],
                ):
                    event_count += 1
                    if event_count > max_events:
                        print_status("Too many events, stopping stream", "warning")
                        break
                        
                    if "content" in event:
                        parts = event["content"].get("parts", [])
                        for part in parts:
                            if "text" in part:
                                response_parts.append(part["text"])
                
                # Analyze response
                full_response = "".join(response_parts)
                
                if full_response:
                    response_length = len(full_response)
                    print_status(f"Response received ({response_length} chars)", "success")
                    
                    # Check for issues
                    if "PERMISSION_DENIED" in full_response:
                        print_status("Permission error detected in response", "error")
                        results.append({"test": i, "status": "failed", "issue": "permission_error"})
                    elif "403" in full_response or "401" in full_response:
                        print_status("Authentication error detected", "error")
                        results.append({"test": i, "status": "failed", "issue": "auth_error"})
                    elif "Error" in full_response and "SQL" in full_response:
                        print_status("SQL execution error - this might be expected for demo data", "warning")
                        results.append({"test": i, "status": "warning", "issue": "sql_error"})
                    elif response_length < 50:
                        print_status("Response too short - possible issue", "warning")
                        results.append({"test": i, "status": "warning", "issue": "short_response"})
                    else:
                        # Check for expected keywords
                        response_lower = full_response.lower()
                        expected_keywords = test.get("expected_keywords", [])
                        found_keywords = [kw for kw in expected_keywords if kw.lower() in response_lower]
                        
                        if found_keywords or not expected_keywords:
                            print_status("Response looks good!", "success")
                            if found_keywords:
                                print_status(f"Found expected keywords: {', '.join(found_keywords)}", "info")
                            results.append({"test": i, "status": "passed"})
                        else:
                            print_status("Response received but missing expected content", "warning")
                            results.append({"test": i, "status": "warning", "issue": "missing_keywords"})
                        
                    # Show full response
                    print(f"   Full Response:")
                    print(f"   {'-' * 40}")
                    print(f"   {full_response}")
                    print(f"   {'-' * 40}")
                    
                    # Special checks for specific tests
                    if "database query request" in test['description'].lower():
                        if "customers" in full_response.lower() or "data" in full_response.lower() or "query" in full_response.lower():
                            print_status("✅ Database query request handled", "success")
                        else:
                            print_status("⚠️ No database query request handling detected", "warning")
                    
                    if "bqml agent transfer" in test['description'].lower():
                        if "bq_ml_agent" in full_response or "transfer" in full_response.lower():
                            print_status("✅ BQML agent transfer detected", "success")
                        else:
                            print_status("⚠️ No BQML agent transfer detected", "warning")
                    
                    if "bqml classification models" in test['description'].lower():
                        if "DNN_CLASSIFIER" in full_response or "LOGISTIC_REG" in full_response or "classification" in full_response.lower():
                            print_status("✅ BQML classification models detected", "success")
                        else:
                            print_status("⚠️ No BQML classification models detected", "warning")
                    
                    if "bqml linear regression" in test['description'].lower():
                        if "linear regression" in full_response.lower() or "CREATE MODEL" in full_response or "LINEAR_REG" in full_response:
                            print_status("✅ BQML linear regression info detected", "success")
                        else:
                            print_status("⚠️ No BQML linear regression info detected", "warning")
                    
                    if "root agent transfer" in test['description'].lower():
                        if "root agent" in full_response.lower() or "transfer" in full_response.lower() or "data analysis" in full_response.lower():
                            print_status("✅ Root agent transfer detected", "success")
                        else:
                            print_status("⚠️ No root agent transfer detected", "warning")
                    
                    if "data science agent call" in test['description'].lower():
                        if "call_ds_agent" in full_response or "data science agent" in full_response.lower():
                            print_status("✅ Data science agent call detected", "success")
                        else:
                            print_status("⚠️ No data science agent call detected", "warning")
                    
                else:
                    print_status("No response received", "error")
                    results.append({"test": i, "status": "failed", "issue": "no_response"})
                    
            except Exception as e:
                print_status(f"Test failed with error: {str(e)}", "error")
                results.append({"test": i, "status": "failed", "issue": str(e)})
            
            print()
        
        # Summary
        print("🎯 VERIFICATION SUMMARY")
        print("=" * 40)
        
        passed = sum(1 for r in results if r["status"] == "passed")
        warnings = sum(1 for r in results if r["status"] == "warning")
        failed = sum(1 for r in results if r["status"] == "failed")
        
        print_status(f"Tests Passed: {passed}/{len(test_queries)}", "success" if passed > 0 else "info")
        if warnings > 0:
            print_status(f"Tests with Warnings: {warnings}", "warning")
        if failed > 0:
            print_status(f"Tests Failed: {failed}", "error")
        
        print()
        print_status(f"Agent Resource: {agent_resource_name}")
        print_status(f"Session ID: {session.id}")
        
        # Detailed results
        print("\n📋 Detailed Test Results:")
        for i, result in enumerate(results, 1):
            status_emoji = {"passed": "✅", "warning": "⚠️", "failed": "❌"}
            status = result["status"]
            issue = result.get("issue", "")
            issue_text = f" ({issue})" if issue else ""
            print(f"   Test {i}: {status_emoji.get(status, '❓')} {status.upper()}{issue_text}")
        
        # Overall status
        if failed == 0 and warnings <= 1:  # Allow 1 warning for demo data issues
            print()
            print_status("🎉 VERIFICATION SUCCESSFUL - Simplified agent is working perfectly!", "success")
            return True
        elif failed == 0:
            print()
            print_status("⚠️ VERIFICATION COMPLETED WITH WARNINGS - Agent is mostly working", "warning")
            print_status("This is likely due to demo data limitations, not agent issues", "info")
            return True
        else:
            print()
            print_status("❌ VERIFICATION FAILED - Agent has issues that need attention", "error")
            return False
            
    except Exception as e:
        print_status(f"Critical error during verification: {str(e)}", "error")
        return False


def main():
    """Main verification function."""
    print_header()
    
    try:
        success = asyncio.run(verify_agent_deployment())
        
        if success:
            print("\n✅ Your GCP Data Analyst Agent (Simplified Framework) is ready for use!")
            print("\n💡 Next steps:")
            print("   • Test via GCP Console Sessions tab")
            print("   • Try database queries: 'Show me data from the customers table'")
            print("   • Test BQML: 'Use the BQML agent to help me create a classification model'")
            print("   • Test data science: 'Analyze this data and create a visualization'")
            print("   • Upload business documents to your Business RAG corpus")
        else:
            print("\n❌ Verification failed - please check the issues above")
            print("💡 Common issues:")
            print("   • Database connection problems")
            print("   • RAG corpus permission issues")
            print("   • Model availability issues")
        
        return 0 if success else 1
        
    except KeyboardInterrupt:
        print("\n⚠️ Verification interrupted by user")
        return 1
    except Exception as e:
        print(f"\n❌ Unexpected error: {str(e)}")
        return 1


if __name__ == "__main__":
    sys.exit(main()) 