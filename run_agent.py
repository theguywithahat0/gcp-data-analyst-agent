#!/usr/bin/env python3
"""
Script to run the GCP Data Analyst Agent locally using the ADK.
"""

import os
from dotenv import load_dotenv
from data_analyst.agent import root_agent
from google_adk.run_agent import run_agent

def main():
    # Load environment variables
    load_dotenv()
    
    # Run the agent
    run_agent(root_agent)

if __name__ == "__main__":
    main() 