# AI Customer Support System

## Overview
An AI-powered customer support system that automates ticket handling and provides intelligent assistance using Groq's LLM capabilities.

## Features
- Ticket submission and processing
- AI-based ticket classification
- Priority and SLA determination
- Language semantics analysis
- Intent extraction
- Knowledge base integration
- Automated response generation
- Ticket screenshot functionality

## Tech Stack
- Python 3.11
- Streamlit for web interface
- PostgreSQL database
- Groq API for AI processing
- PIL for image processing

## Requirements
- Python 3.11+
- PostgreSQL database
- Groq API key
- Required Python packages (see requirements.txt)

## Setup
1. Clone the repository
2. Set up environment variables:
   - GROQ_API_KEY
   - Database configuration (PGHOST, PGDATABASE, etc.)
3. Install dependencies: `pip install -r requirements.txt`
4. Run the application: `streamlit run main.py`

## Usage
1. Access the web interface
2. Fill in the ticket details (title and description)
3. Submit the ticket
4. View AI analysis results including:
   - Ticket classification
   - Priority and SLA
   - Language analysis
   - Intent extraction
   - Knowledge base matches
   - Generated response
5. Download ticket screenshot if needed

## Architecture
The system uses a modular agent-based architecture:
- Ticket Classification Agent
- Priority Understanding Agent
- Language Semantics Agent
- Knowledge Base Agent
- Content Generation Agent
- Intent Extraction Agent

Each agent is responsible for a specific aspect of ticket processing and uses Groq's LLM for intelligent analysis.
