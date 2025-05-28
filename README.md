# Research Ethics Proposal Assistant (REPA)

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/streamlit-1.15.0%2B-FF4B4B.svg)](https://streamlit.io/)

REPA is an AI-powered application that guides researchers through the ethics proposal preparation process, providing intelligent feedback, document analysis, and automated report generation to streamline ethics committee submissions.

## 🌟 Features

### Research Context Documentation
- Structured input forms for research details
- Real-time AI feedback on ethical considerations
- Progress tracking for completion status

### Ethics Checklist System
- Comprehensive ethics requirements based on standard frameworks
- Dynamic question presentation based on research context
- Automated validation of responses

### Document Management
- Upload and manage supporting documentation
- AI-powered document analysis and compliance checking
- Automated identification of missing elements and requirements

### AI-Powered Feedback
- Context-specific guidance on ethics questions
- Document review with compliance scoring
- Recommendations for improving ethics applications

### Comprehensive Reporting
- Automated ethics review report generation
- Document compliance summaries
- Downloadable reports for submission

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- Azure AI services account (for AI capabilities)

### Installation

1. Clone this repository
```bash
git clone https://github.com/yourusername/repa.git
cd repa
```

2. Install dependencies
```bash
pip install -r requirements.txt
```
3. Create a .env file with your Azure AI credentials
AZURE_ENDPOINT=https://your-azure-endpoint.com
AZURE_API_KEY=your_api_key_here
AZURE_MODEL=gpt-4-32k

4. Run the application
```bash
streamlit run app.py
```

## 🔧  Project Structure
```bash
research-ethics-assistant/
├── app.py                  # Main Streamlit application
├── config.py               # Configuration settings and environment variables
├── requirements.txt        # Project dependencies
├── agents/
│   ├── base_agent.py       # Core AI agent functionality
│   └── document_processor_agent.py  # Document analysis capabilities
├── utils/
│   ├── azure_ai.py         # Azure AI service wrapper
│   ├── ethics_questions.py # Ethics checklist configuration
│   └── __init__.py
└── .env                    # Environment variables 
```

## 💻  How It Works
Architecture
REPA uses a multi-agent AI system to provide ethics guidance:

Base Agent: Handles general ethics analysis, question feedback, and checklist validation
Document Processor Agent: Specializes in document analysis, extraction, and report generation
Azure AI Wrapper: Provides a unified interface to Azure's AI services
Workflow
Research Context: Users enter details about their research project
Ethics Checklist: The system presents relevant ethics questions based on the research context
Document Upload: Users upload supporting documentation for each requirement
AI Analysis: Documents and responses are analyzed for compliance and completeness
Feedback Generation: The system provides specific feedback and recommendations
Report Generation: A comprehensive ethics review report is generated
Submission: Users can download the report and submit their completed application
## 🔍 Key Components
Ethics Checklist Configuration
The system uses a structured ethics checklist divided into sections:

Part A: Mandatory components for all submissions
Part B: Additional components that may be required
Part C: Requirements for gene technology research
Part D: Requirements for radiological procedures
Part E: Requirements for Aboriginal and Torres Strait Islander health research
Document Analysis
The document processor can analyze various document types:

Consent forms
Research protocols
Ethics committee application forms
CVs/Resumes
Surveys/Questionnaires
For each document, the system:

Determines the document type
Checks relevance to the ethics question
Analyzes for required elements
Provides a compliance score and recommendations
## 🛠️ Customization
### Adding New Ethics Questions
Edit the utils/ethics_questions.py file to add new questions to the checklist:"NEW_PART": 
```bash

{
    "title": "New Ethics Section",
    "description": "Description of this section",
    "questions": [
        {
            "id": "NEW1",
            "question": "Your new ethics question?",
            "description": "Additional guidance for the question",
            "required": True,
            "requires_document": True,
            "document_type": "new_document_type"
        }
    ]
}

```
### Modifying AI Prompts
Edit the config.py file to customize the AI prompts:
```bash
PROMPTS = {
    "new_prompt_type": """
    Your custom prompt template here.
    {placeholder_for_dynamic_content}
    
    Instructions for the AI model.
    """
}
```

## 📊 Progress Tracking
The application tracks progress at multiple levels:

Overall application completion
Section-level completion (Research Context, Ethics Checklist)
Component-level completion for ethics checklist sections
Document compliance status

## 🔒 Security and Privacy
All AI processing is done through Azure AI services
Document content is not stored permanently
User data remains in the session and is not persisted between sessions
No data is used to train AI models

## 📧 Contact
For questions or support, please open an issue on this repository.

