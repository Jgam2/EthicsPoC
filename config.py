# config.py
import os
from dotenv import load_dotenv
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('Config')

# Load environment variables
env_path = Path('.env').resolve()
load_dotenv(dotenv_path=env_path)

# Validate environment variables
def validate_env_variables():
    required_vars = {
        'AZURE_ENDPOINT': os.getenv('AZURE_ENDPOINT'),
        'AZURE_API_KEY': os.getenv('AZURE_API_KEY')
    }
    
    missing_vars = [var for var, value in required_vars.items() if not value]
    
    if missing_vars:
        logger.warning(f"Missing environment variables: {', '.join(missing_vars)}.")
        # Set default values if environment variables are missing
        if 'AZURE_ENDPOINT' not in os.environ:
            os.environ['AZURE_ENDPOINT'] = 'https://jasg-m8ieejvv-francecentral.services.ai.azure.com/models'
            logger.info(f"Using default endpoint: {os.environ['AZURE_ENDPOINT']}")
        if 'AZURE_API_KEY' not in os.environ:
            os.environ['AZURE_API_KEY'] = ''
            logger.warning("API key not provided. Authentication will fail.")
        if 'AZURE_MODEL' not in os.environ:
            os.environ['AZURE_MODEL'] = 'gpt-4-32k'
            logger.info(f"Using default model: {os.environ['AZURE_MODEL']}")
        return False
    
    logger.info("All required environment variables are present")
    return True

# Azure AI Configuration
AZURE_AI_CONFIG = {
    "endpoint": os.getenv('AZURE_ENDPOINT'),
    "api_key": os.getenv('AZURE_API_KEY'),
    "model": os.getenv('AZURE_MODEL', 'gpt-4-32k')
}

# API Configuration
API_CONFIG = {
    "max_retries": 3,
    "timeout": 30,
    "backoff_factor": 0.5,
    "max_tokens": 4000,
    "temperature": 0.7
}

# Prompts Configuration
PROMPTS = {
    "ethics_review": """
    Analyze the following research context from an ethics perspective:
    {context}
    
    Provide a structured analysis including:
    1. Ethical considerations
    2. Potential risks
    3. Recommended safeguards
    4. Compliance requirements
    """,
    
    "checklist_validation": """
    Review the following ethics checklist responses:
    {responses}
    
    Evaluate:
    1. Completeness
    2. Consistency
    3. Areas requiring attention
    4. Additional documentation needs
    """,
    
    "document_review": """
    Review this document in relation to the following ethics question:
    
    Question: {question}
    
    Document Name: {filename}
    
    Provide a structured analysis including:
    1. Compliance with ethical standards
    2. Clarity and completeness
    3. Recommendations for improvement
    """,
    
    "question_feedback": """
    Review this ethics question and response:
    
    Question: {question}
    Response: {response}
    
    Provide specific feedback on:
    1. Appropriateness of the response
    2. Ethical considerations
    3. Potential issues or concerns
    4. Suggestions for improvement or clarification
    """
}

# Validate environment variables
validate_env_variables()