#!/usr/bin/env python3
"""
Deployment Verification Script for GCP Data Analyst Agent

This script verifies that your deployed agent is working correctly
with proper RAG corpus access and conversational responses.
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
    print("🔍 GCP Data Analyst Agent - Deployment Verification")
    print("=" * 60)


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
        
        # Get the latest deployed agent resource name
        # You should update this with your actual deployed agent resource name
        agent_resource_name = "projects/115564817055/locations/us-central1/reasoningEngines/8125171026939084800"
        
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
                "description": "Basic conversational test"
            },
            {
                "query": "What BigQuery ML models are available for classification?",
                "description": "BQML RAG corpus test"
            },
            {
                "query": "How do I optimize a linear regression model in BQML?",
                "description": "Advanced BQML documentation test"
            }
        ]
        
        results = []
        
        for i, test in enumerate(test_queries, 1):
            print_status(f"Test {i}: {test['description']}", "test")
            print(f"   Query: {test['query']}")
            print("-" * 50)
            
            try:
                response_parts = []
                
                # Stream query to agent
                for event in agent_engine.stream_query(
                    user_id="verification_user",
                    session_id=session.id,
                    message=test['query'],
                ):
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
                    elif "403" in full_response:
                        print_status("Authentication error detected", "error")
                        results.append({"test": i, "status": "failed", "issue": "auth_error"})
                    elif response_length < 50:
                        print_status("Response too short - possible issue", "warning")
                        results.append({"test": i, "status": "warning", "issue": "short_response"})
                    else:
                        print_status("Response looks good!", "success")
                        results.append({"test": i, "status": "passed"})
                        
                    # Show preview of response
                    preview = full_response[:200] + "..." if len(full_response) > 200 else full_response
                    print(f"   Preview: {preview}")
                    
                else:
                    print_status("No response received", "error")
                    results.append({"test": i, "status": "failed", "issue": "no_response"})
                    
            except Exception as e:
                print_status(f"Test failed with error: {str(e)}", "error")
                results.append({"test": i, "status": "failed", "issue": str(e)})
            
            print()
        
        # Summary
        print("🎯 VERIFICATION SUMMARY")
        print("=" * 30)
        
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
        
        # Overall status
        if failed == 0 and warnings == 0:
            print()
            print_status("🎉 VERIFICATION SUCCESSFUL - Agent is working perfectly!", "success")
            return True
        elif failed == 0:
            print()
            print_status("⚠️ VERIFICATION COMPLETED WITH WARNINGS - Agent is mostly working", "warning")
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
            print("\n✅ Your GCP Data Analyst Agent is ready for use!")
            print("\n💡 Next steps:")
            print("   • Test via GCP Console Sessions tab")
            print("   • Try the example queries from the README")
            print("   • Upload business documents to your Business RAG corpus")
        else:
            print("\n❌ Verification failed - please check the issues above")
            print("\n🔧 Troubleshooting:")
            print("   • Check GCP authentication: gcloud auth application-default login")
            print("   • Verify agent resource name in this script")
            print("   • Review GCP Console logs for detailed errors")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n\n⏹️ Verification cancelled by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Unexpected error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main() 