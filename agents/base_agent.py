from utils.azure_ai import AzureAIWrapper
from config import PROMPTS
from typing import Dict, Any, Optional
import logging
import json

logger = logging.getLogger(__name__)

class BaseAgent:
    def __init__(self):
        self.ai_client = AzureAIWrapper()
        
    def validate_checklist(self, responses: Dict[str, Any], documents: Optional[Dict] = None) -> str:
        """Validate ethics checklist responses and documents"""
        try:
            # Prepare messages for validation
            messages = [
                {
                    "role": "system",
                    "content": """You are an ethics review assistant validating research ethics applications. 
                    Your role is to ensure all mandatory components are properly addressed and documented."""
                },
                {
                    "role": "user",
                    "content": f"""
                    Review these ethics checklist responses and documents:
                    
                    Responses:
                    {str(responses)}
                    
                    Documents Submitted:
                    {str(documents.keys()) if documents else 'No documents uploaded'}
                    
                    Provide a structured analysis including:
                    1. Completeness of responses
                    2. Required documentation status
                    3. Potential issues or concerns
                    4. Recommendations for improvement
                    
                    Focus on:
                    - Mandatory components (Part A)
                    - Required documentation
                    - Consistency of responses
                    - Compliance with ethics guidelines
                    """
                }
            ]
            
            result = self.ai_client.get_completion(messages)
            
            # If no result or error, return error status
            if not result or result == "AI service encountered an error.":
                return {
                    "status": "ERROR",
                    "message": "Unable to validate checklist due to AI service error."
                }
            
            return result
        except Exception as e:
            logger.error(f"Error validating checklist: {str(e)}")
            return {
                "status": "ERROR",
                "message": f"Error validating checklist: {str(e)}"
            }
    
    def analyze_research_context(self, context: Dict[str, Any], custom_prompt=None) -> str:
        """Analyze research context for ethical considerations"""
        try:
            # Use custom prompt if provided
            if custom_prompt:
                user_content = custom_prompt
            else:
                user_content = PROMPTS["ethics_review"].format(context=str(context))
                
            messages = [
                {
                    "role": "system",
                    "content": "You are an ethics review assistant analyzing research proposals. Provide detailed, specific feedback on the research context with focus on ethical considerations."
                },
                {
                    "role": "user",
                    "content": user_content
                }
            ]
            
            result = self.ai_client.get_completion(messages)
            
            # If no result or error, return error status
            if not result or result == "AI service encountered an error.":
                return {
                    "status": "ERROR",
                    "message": "Unable to analyze research context due to AI service error."
                }
            
            return result
        except Exception as e:
            logger.error(f"Error analyzing research context: {str(e)}")
            return {
                "status": "ERROR",
                "message": f"Error analyzing research context: {str(e)}"
            }
    
    def get_research_context_feedback(self, context: Dict[str, Any], field_name: str) -> str:
        """Generate feedback for a specific research context field"""
        try:
            field_descriptions = {
                'title': "research title",
                'field': "research field",
                'context': "research context",
                'description': "research description",
                'methodology': "research methodology",
                'participants': "target participants",
                'timeline': "expected timeline"
            }
            
            field_desc = field_descriptions.get(field_name, field_name)
            field_value = context.get(field_name, "")
            
            if not field_value:
                return {
                    "status": "ERROR",
                    "message": f"Please provide information about your {field_desc}."
                }
            
            messages = [
                {
                    "role": "system",
                    "content": f"""You are an ethics review assistant providing feedback on a research proposal's {field_desc}.
                    Provide constructive feedback focusing on ethical considerations, clarity, and completeness."""
                },
                {
                    "role": "user",
                    "content": f"""
                    Review this {field_desc} for a research proposal:
                    
                    {field_value}
                    
                    Provide specific feedback on:
                    1. Clarity and completeness
                    2. Ethical considerations
                    3. Potential issues or concerns
                    4. Suggestions for improvement
                    
                    Keep your feedback concise, constructive, and focused on helping the researcher improve their proposal.
                    """
                }
            ]
            
            result = self.ai_client.get_completion(messages)
            
            # If no result or error, return error status
            if not result or result == "AI service encountered an error.":
                return {
                    "status": "ERROR",
                    "message": f"Unable to generate feedback for {field_desc} due to AI service error."
                }
            
            return result
        except Exception as e:
            logger.error(f"Error generating research context feedback: {str(e)}")
            return {
                "status": "ERROR",
                "message": f"Error generating feedback for {field_name}: {str(e)}"
            }
    
    def get_question_feedback(self, question, response, document=None, prompt=None):
        """
        Generate specific feedback for an ethics question based on the response and document
        
        Args:
            question: The ethics question text
            response: The user's response (YES/NO/N/A)
            document: Optional document information
            prompt: Optional pre-formatted prompt to use
            
        Returns:
            String containing detailed feedback on the response
        """
        try:
            # Use the provided prompt if available, otherwise build one
            if not prompt:
                system_content = """You are a research ethics expert providing feedback on ethics checklist responses.
                Analyze the response and any attached document to provide specific, helpful feedback."""
                
                user_content = f"""Question: {question}
                Response: {response}
                """
                
                if document:
                    user_content += f"\nDocument provided: {document.get('name', 'Unknown')}\n"
                    
                    # Try to extract document content if available
                    if 'content' in document:
                        try:
                            # Extract a preview of the document content
                            doc_content = document['content'].decode('utf-8', errors='ignore')[:1000]
                            user_content += f"Document content preview: {doc_content}\n"
                        except Exception as e:
                            logger.error(f"Error extracting document content: {str(e)}")
                            user_content += "Document content could not be extracted.\n"
                    
                    if 'review' in document:
                        review = document['review']
                        user_content += f"Document review status: {review.get('status', 'Unknown')}\n"
                        user_content += f"Document analysis: {review.get('analysis', 'Not available')}\n"
                        
                        # Include additional review information if available
                        if 'missing_elements' in review and review['missing_elements']:
                            user_content += "Missing elements:\n"
                            for element in review['missing_elements']:
                                user_content += f"- {element}\n"
                        
                        if 'recommendations' in review and review['recommendations']:
                            user_content += "Recommendations:\n"
                            for rec in review['recommendations']:
                                user_content += f"- {rec}\n"
                
                user_content += """
                Please provide specific feedback on this ethics question response.
                If a document is attached, evaluate if it adequately addresses the requirements.
                
                Structure your feedback as follows:
                1. Assessment of the response
                2. Ethical considerations
                3. Potential issues or concerns
                4. Specific recommendations
                
                Be detailed and specific in your analysis, focusing on how the response and document (if provided)
                address the ethical requirements implied by the question.
                """
            else:
                # Use the provided custom prompt
                system_content = """You are a research ethics expert providing feedback on ethics checklist responses."""
                user_content = prompt
            
            # Prepare messages for the AI service
            messages = [
                {
                    "role": "system",
                    "content": system_content
                },
                {
                    "role": "user",
                    "content": user_content
                }
            ]
            
            # Call the Azure AI service
            result = self.ai_client.get_completion(messages)
            
            # If no result or error, return error status
            if not result or result == "AI service encountered an error.":
                return {
                    "status": "ERROR",
                    "message": "Unable to generate question feedback due to AI service error."
                }
            
            return result
        except Exception as e:
            logger.error(f"Error in get_question_feedback: {str(e)}")
            return {
                "status": "ERROR",
                "message": f"Error generating question feedback: {str(e)}"
            }