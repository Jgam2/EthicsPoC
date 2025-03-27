# test_azure_ai.py
import sys
import os
import json

# Add the parent directory to the path so we can import the modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.azure_ai import AzureAIWrapper

def test_research_context_feedback():
    """Test AI feedback for research context"""
    print("\n=== TESTING RESEARCH CONTEXT FEEDBACK ===\n")
    
    ai_client = AzureAIWrapper()
    
    # Test case 1: Basic research context
    research_data = {
        'title': 'Effects of Social Media on Mental Health in Adolescents',
        'field': 'Psychology',
        'context': 'Increasing social media use among teenagers has raised concerns about mental health impacts.',
        'description': 'This study examines the relationship between social media usage patterns and mental health outcomes in adolescents aged 13-18.',
        'methodology': 'We will use surveys and interviews to collect data from 200 participants about their social media habits and mental health indicators.',
        'participants': 'Adolescents aged 13-18 recruited from local schools with parental consent.',
        'timeline': 'The study will run for 6 months, with data collection in the first 3 months followed by analysis.'
    }
    
    messages = [
        {
            "role": "system",
            "content": "You are an ethics review assistant analyzing research proposals. Provide detailed, specific feedback on the research context with focus on ethical considerations."
        },
        {
            "role": "user",
            "content": f"Please analyze this research context:\n{json.dumps(research_data, indent=2)}"
        }
    ]
    
    result = ai_client.get_completion(messages)
    print("Research Context Feedback:")
    print(result)
    print("\n" + "-"*80 + "\n")
    
    # Test case 2: Research with vulnerable populations
    research_data = {
        'title': 'Impact of Educational Interventions on Children with Learning Disabilities',
        'field': 'Education',
        'context': 'Children with learning disabilities often face challenges in traditional educational settings.',
        'description': 'This study evaluates the effectiveness of specialized educational interventions for children with learning disabilities.',
        'methodology': 'We will implement different educational interventions and measure academic progress over time using standardized tests and teacher assessments.',
        'participants': 'Children aged 8-12 with diagnosed learning disabilities from special education programs.',
        'timeline': 'The study will run for one academic year with assessments at the beginning, middle, and end.'
    }
    
    messages = [
        {
            "role": "system",
            "content": "You are an ethics review assistant analyzing research proposals. Provide detailed, specific feedback on the research context with focus on ethical considerations."
        },
        {
            "role": "user",
            "content": f"Please analyze this research context:\n{json.dumps(research_data, indent=2)}"
        }
    ]
    
    result = ai_client.get_completion(messages)
    print("Research Context Feedback (Vulnerable Populations):")
    print(result)
    print("\n" + "-"*80 + "\n")

def test_ethics_questionnaire_feedback():
    """Test AI feedback for ethics questionnaire responses"""
    print("\n=== TESTING ETHICS QUESTIONNAIRE FEEDBACK ===\n")
    
    ai_client = AzureAIWrapper()
    
    # Test case 1: Human participants question - YES
    messages = [
        {
            "role": "system",
            "content": "You are a research ethics expert providing feedback on ethics checklist responses."
        },
        {
            "role": "user",
            "content": """
            Question: Does your research involve human participants?
            Response: YES
            
            Please provide specific feedback on this ethics question response.
            """
        }
    ]
    
    result = ai_client.get_completion(messages)
    print("Human Participants Question (YES):")
    print(result)
    print("\n" + "-"*80 + "\n")
    
    # Test case 2: Personal data question - NO
    messages = [
        {
            "role": "system",
            "content": "You are a research ethics expert providing feedback on ethics checklist responses."
        },
        {
            "role": "user",
            "content": """
            Question: Will you collect personal data?
            Response: NO
            
            Please provide specific feedback on this ethics question response.
            """
        }
    ]
    
    result = ai_client.get_completion(messages)
    print("Personal Data Question (NO):")
    print(result)
    print("\n" + "-"*80 + "\n")
    
    # Test case 3: Vulnerable populations question with document
    messages = [
        {
            "role": "system",
            "content": "You are a research ethics expert providing feedback on ethics checklist responses."
        },
        {
            "role": "user",
            "content": """
            Question: Does your research involve vulnerable populations?
            Response: YES
            
            Document Name: Vulnerable_Populations_Protocol.docx
            Document Type: Research Protocol
            Document Content Preview: 
            This protocol outlines the procedures for working with vulnerable populations in our research. 
            We will take extra precautions to ensure informed consent is obtained appropriately, considering 
            the specific vulnerabilities of our participants. For children, we will obtain parental consent 
            and child assent. For individuals with cognitive impairments, we will use simplified consent 
            materials and may involve legally authorized representatives. All researchers will receive 
            specialized training on working with vulnerable populations.
            
            Please provide specific feedback on this ethics question response.
            Evaluate if the attached document adequately addresses the requirements.
            """
        }
    ]
    
    result = ai_client.get_completion(messages)
    print("Vulnerable Populations Question with Document:")
    print(result)
    print("\n" + "-"*80 + "\n")

def test_document_review():
    """Test AI document review"""
    print("\n=== TESTING DOCUMENT REVIEW ===\n")
    
    ai_client = AzureAIWrapper()
    
    # Test case 1: Consent form review
    messages = [
        {
            "role": "system",
            "content": "You are a document review assistant specializing in research ethics documentation."
        },
        {
            "role": "user",
            "content": """
            Ethics Question: Does your research involve human participants?
            
            Document Name: Informed_Consent_Form.docx
            Document Type: Consent Form
            
            Document Content Preview:
            INFORMED CONSENT FORM
            
            Research Project: Effects of Social Media on Mental Health in Adolescents
            
            Purpose of the Research:
            This study aims to understand how social media use affects the mental health of teenagers aged 13-18.
            
            What You Will Be Asked to Do:
            If you agree to participate, you will be asked to:
            1. Complete a survey about your social media usage (approximately 20 minutes)
            2. Participate in a one-hour interview about your experiences with social media
            3. Allow researchers to analyze your social media activity for a period of two weeks
            
            Risks and Benefits:
            There are minimal risks associated with this study. Some questions may make you think about negative experiences on social media, which could cause mild discomfort. If you experience distress, we can provide resources for support.
            
            Benefits include contributing to important research on teen mental health and social media use. You may also gain insights into your own social media habits.
            
            Confidentiality:
            All information collected will be kept strictly confidential. Your name will be replaced with a code, and only the research team will have access to the key linking your name to the code. All data will be stored on encrypted servers.
            
            Voluntary Participation:
            Your participation is completely voluntary. You can withdraw at any time without penalty by contacting the research team.
            
            Please analyze this document and provide:
            1. An assessment of whether it adequately addresses the ethics question
            2. Identification of any missing or incomplete elements
            3. Specific recommendations for improvement
            4. A status determination (APPROVED, ANALYZING, or NEEDS_REVISION)
            """
        }
    ]
    
    result = ai_client.get_completion(messages)
    print("Consent Form Review:")
    print(json.dumps(result, indent=2))
    print("\n" + "-"*80 + "\n")
    
    # Test case 2: Research protocol review
    messages = [
        {
            "role": "system",
            "content": "You are a document review assistant specializing in research ethics documentation."
        },
        {
            "role": "user",
            "content": """
            Ethics Question: Please upload your research protocol.
            
            Document Name: Research_Protocol.docx
            Document Type: Research Protocol
            
            Document Content Preview:
            RESEARCH PROTOCOL
            
            Project Title: Effects of Social Media on Mental Health in Adolescents
            
            1. Background and Rationale
            Social media use has increased dramatically among adolescents in recent years. Previous studies have suggested links between social media use and mental health outcomes, but the relationship remains poorly understood.
            
            2. Research Objectives
            - To examine the relationship between social media usage patterns and mental health indicators in adolescents
            - To identify specific social media behaviors associated with positive and negative mental health outcomes
            - To explore adolescents' perceptions of how social media affects their wellbeing
            
            3. Methodology
            This is a mixed-methods study combining surveys, interviews, and social media data analysis.
            
            4. Participant Recruitment
            200 adolescents aged 13-18 will be recruited from local schools. Information sessions will be held at schools, and interested students will receive information packets to take home to their parents/guardians.
            
            5. Data Collection Procedures
            - Online survey measuring social media use and mental health indicators
            - Semi-structured interviews with a subset of 30 participants
            - Analysis of social media activity for participants who consent to this component
            
            6. Data Analysis
            Statistical analysis will be performed on survey data, while thematic analysis will be used for interview data.
            
            Please analyze this document and provide:
            1. An assessment of whether it adequately addresses the ethics question
            2. Identification of any missing or incomplete elements
            3. Specific recommendations for improvement
            4. A status determination (APPROVED, ANALYZING, or NEEDS_REVISION)
            """
        }
    ]
    
    result = ai_client.get_completion(messages)
    print("Research Protocol Review:")
    print(json.dumps(result, indent=2))
    print("\n" + "-"*80 + "\n")

def test_review_report_generation():
    """Test review report generation"""
    print("\n=== TESTING REVIEW REPORT GENERATION ===\n")
    
    ai_client = AzureAIWrapper()
    
    # Create mock reviews
    reviews = {
        "doc1": {
            "status": "APPROVED",
            "analysis": "The consent form meets all requirements.",
            "missing_elements": [],
            "recommendations": ["Add contact information for the ethics committee"],
            "compliance_score": 95
        },
        "doc2": {
            "status": "NEEDS_REVISION",
            "analysis": "The protocol lacks sufficient detail on data security.",
            "missing_elements": ["Data security procedures", "Risk mitigation strategies"],
            "recommendations": ["Add data security details", "Include risk mitigation plan"],
            "compliance_score": 70
        }
    }
    
    messages = [
        {
            "role": "system",
            "content": "You are a review report generator for ethics applications."
        },
        {
            "role": "user",
            "content": f"Please generate a review report based on these document reviews:\n{json.dumps(reviews, indent=2)}"
        }
    ]
    
    result = ai_client.get_completion(messages)
    print("Review Report:")
    if isinstance(result, dict):
        print(json.dumps(result, indent=2))
    else:
        print(result)
    print("\n" + "-"*80 + "\n")

if __name__ == "__main__":
    print("Testing AzureAIWrapper...")
    
    test_research_context_feedback()
    test_ethics_questionnaire_feedback()
    test_document_review()
    test_review_report_generation()
    
    print("\nAll tests completed!")