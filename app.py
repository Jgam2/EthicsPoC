import streamlit as st
import logging
from pathlib import Path
from datetime import datetime
from agents.base_agent import BaseAgent
from agents.document_processor_agent import DocumentProcessorAgent
from utils.ethics_questions import ETHICS_CHECKLIST

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('App')

def initialize_session_state():
    """Initialize session state variables"""
    if 'research_data' not in st.session_state:
        st.session_state.research_data = {}
    if 'checklist_responses' not in st.session_state:
        st.session_state.checklist_responses = {}
    if 'uploaded_documents' not in st.session_state:
        st.session_state.uploaded_documents = {}
    if 'current_page' not in st.session_state:
        st.session_state.current_page = "Research Context"
    if 'document_reviews' not in st.session_state:
        st.session_state.document_reviews = {}
    if 'feedback' not in st.session_state:
        st.session_state.feedback = {}

# Progress calculation functions
def calculate_research_context_progress():
    """Calculate progress for Research Context page"""
    fields = ['title', 'field', 'context', 'description', 'methodology', 'participants', 'timeline']
    total_fields = len(fields)
    filled_fields = sum(1 for field in fields if field in st.session_state.research_data and st.session_state.research_data[field])
    return filled_fields / total_fields if total_fields > 0 else 0

def calculate_ethics_checklist_progress():
    """Calculate progress for Ethics Checklist page"""
    # Get all questions from all parts
    all_questions = []
    for part in ETHICS_CHECKLIST.values():
        all_questions.extend(part["questions"])
    
    # Count total questions
    total_questions = len(all_questions)
    
    # Count answered questions
    answered_questions = sum(1 for q in all_questions 
                        if q['id'] in st.session_state.checklist_responses
                        and 'answer' in st.session_state.checklist_responses[q['id']]
                        and st.session_state.checklist_responses[q['id']]['answer'] in ["YES", "NO", "N/A"])
                        

    # Calculate progress
    if total_questions > 0:
        return answered_questions / total_questions
    else:
        return 0

def calculate_ethics_component_progress(part_key):
    """Calculate progress for a specific ethics checklist component"""
    if part_key not in ETHICS_CHECKLIST:
        return 0
    
    # Get questions for this part
    questions = ETHICS_CHECKLIST[part_key]["questions"]
    total_questions = len(questions)
    
    # Count answered questions for this part
    answered_questions = sum(1 for q in questions if q['id'] in st.session_state.checklist_responses
    and 'answer' in st.session_state.checklist_responses[q['id']]
    and st.session_state.checklist_responses[q['id']]['answer'] in ["YES", "NO", "N/A"])
    
    # Calculate progress
    if total_questions > 0:
        return answered_questions / total_questions
    else:
        return 0

def calculate_review_submit_progress():
    """Calculate progress for Review & Submit page"""
    # For simplicity, we'll consider this page complete if they've reached it
    return 1.0 if st.session_state.current_page == "Review & Submit" else 0.0

def calculate_overall_progress():
    """Calculate overall progress across all pages"""
    # Define weights for each page
    weights = {
        "Research Context": 0.3,
        "Ethics Checklist": 0.6,
        "Review & Submit": 0.1
    }
    
    # Calculate progress for each page
    progress = {
        "Research Context": calculate_research_context_progress(),
        "Ethics Checklist": calculate_ethics_checklist_progress(),
        "Review & Submit": calculate_review_submit_progress()
    }
    
    # Calculate weighted average
    overall = sum(progress[page] * weights[page] for page in weights)
    return overall

def get_question_feedback(agent, question_text, response_answer, document=None):
    """Generate context-specific feedback for a question based on response and document"""
    try:
        # Create a more detailed prompt based on available information
        prompt = f"Question: {question_text}\nResponse: {response_answer}\n"
        
        # Add document information if available
        if document and 'content' in document:
            # Extract text from document if possible
            doc_content = ""
            try:
                # Extract text from document content
                if document.get('name', '').lower().endswith('.pdf'):
                    # For PDF files
                    pdf_file = BytesIO(document['content'])
                    pdf_reader = PyPDF2.PdfReader(pdf_file)
                    for page in pdf_reader.pages:
                        doc_content += page.extract_text() + "\n"
                elif document.get('name', '').lower().endswith(('.doc', '.docx')):
                    # For Word documents
                    doc = docx.Document(BytesIO(document['content']))
                    doc_content = "\n".join([paragraph.text for paragraph in doc.paragraphs])
                else:
                    # For text content
                    doc_content = document['content'].decode('utf-8', errors='ignore')
                
                # Limit content length for the prompt
                doc_content = doc_content[:3000] if len(doc_content) > 3000 else doc_content
                
            except Exception as e:
                logger.error(f"Error extracting document content: {str(e)}")
                doc_content = "Document content could not be extracted"
                
            prompt += f"\nDocument Name: {document.get('name', 'Unknown')}\n"
            prompt += f"Document Type: {document.get('type', 'Unknown')}\n"
            prompt += f"Document Content Preview:\n{doc_content}\n"
            
            # If there's a review, include it
            if 'review' in document:
                review = document['review']
                prompt += f"\nDocument Review Status: {review.get('status', 'Unknown')}\n"
                prompt += f"Document Analysis: {review.get('analysis', 'Not available')}\n"
        
        prompt += "\nPlease provide specific, detailed feedback on this ethics question response."
        if document:
            prompt += " Evaluate if the attached document adequately addresses the requirements related to this specific question. Focus on the content of this particular document and how it relates to the ethics question."
        else:
            prompt += " Since no document was provided, focus on the ethical implications of the response and what documentation might be needed."
        
        prompt += "\nYour feedback should be unique to this specific question and document, not generic."
        
        # Get feedback from the agent with the enhanced context
        feedback_result = agent.get_question_feedback(
            question=question_text,
            response=response_answer,
            document=document,
            prompt=prompt  # Pass the detailed prompt to the agent
        )
        
        # Check if we got an error response
        if isinstance(feedback_result, dict) and feedback_result.get('status') == "ERROR":
            return f"Unable to generate feedback: {feedback_result.get('message', 'AI service error')}"
        
        return feedback_result
    except Exception as e:
        logger.error(f"Error generating feedback: {str(e)}")
        return f"Unable to generate specific feedback: {str(e)}"

def render_sidebar():
    with st.sidebar:
        st.title("Navigation")
        pages = ["Research Context", "Ethics Checklist", "Review & Submit"]
        selected_page = st.radio("Go to", pages)
        st.session_state.current_page = selected_page
        
        # Overall progress
        st.write("---")
        st.subheader("Overall Progress")
        overall_progress = calculate_overall_progress()
        st.progress(overall_progress)
        st.write(f"{int(overall_progress * 100)}% Complete")
        
        # Page-specific progress
        st.write("---")
        st.subheader("Progress by Section")
        
        # Research Context progress
        research_progress = calculate_research_context_progress()
        st.write("Research Context")
        st.progress(research_progress)
        st.write(f"{int(research_progress * 100)}% Complete")
        
        # Ethics Checklist progress
        ethics_progress = calculate_ethics_checklist_progress()
        st.write("Ethics Checklist")
        st.progress(ethics_progress)
        st.write(f"{int(ethics_progress * 100)}% Complete")
        
        # If on Ethics Checklist page, show component progress
        if st.session_state.current_page == "Ethics Checklist":
            st.write("---")
            st.subheader("Ethics Checklist Components")
            
            # Calculate progress for each part of the checklist
            for part_key, part in ETHICS_CHECKLIST.items():
                total_in_part = len(part["questions"])
                answered_in_part = sum(1 for q in part["questions"] 
                    if q['id'] in st.session_state.checklist_responses
                    and 'answer' in st.session_state.checklist_responses[q['id']]
                    and st.session_state.checklist_responses[q['id']]['answer'] in ["YES", "NO", "N/A"])
    
        part_progress = answered_in_part / total_in_part if total_in_part > 0 else 0
        st.write(f"{part['title']}")
        st.progress(part_progress)
        st.write(f"{int(part_progress * 100)}% Complete")

# Custom CSS to match the design
def apply_custom_css():
    st.markdown("""
        <style>
        /* Increase overall font size */
        html, body, [class*="css"] {
            font-size: 16px !important;
        }
        
        /* Increase header sizes */
        h1 {
            font-size: 2.2rem !important;
            color: #1E88E5 !important; /* Blue color for main title */
        }
        
        h2 {
            font-size: 1.8rem !important;
        }
        
        h3 {
            font-size: 1.5rem !important;
        }
        
        h4 {
            font-size: 1.3rem !important;
        }
        
        /* Increase paragraph and list text */
        p, li, label, .stRadio > label {
            font-size: 1.1rem !important;
        }
        
        /* Increase button text */
        .stButton button {
            font-size: 1.1rem !important;
        }
        
        /* Increase expander text */
        .streamlit-expanderHeader {
            font-size: 1.1rem !important;
        }
        
        /* Modern progress bar styling */
        .stProgress > div > div {
            background-color: #4CAF50 !important; /* Green progress bar */
            background-image: none !important;
        }
        
        .stProgress {
            height: 10px !important;
            border-radius: 5px !important;
            background-color: #f0f0f0 !important;
        }
        
        /* Other styling */
        .stTextArea textarea {
            background-color: #f8f9fa;
            border: 1px solid #dee2e6;
            border-radius: 4px;
            padding: 10px;
            font-size: 1.1rem !important;
        }
        
        .stMarkdown h4 {
            margin-top: 20px;
            margin-bottom: 10px;
            color: #2C3E50;
        }
        
        .stButton button {
            background-color: #1E88E5;
            color: white;
            border-radius: 4px;
            padding: 10px 24px;
            margin-top: 20px;
            transition: all 0.3s ease;
        }
        
        .stButton button:hover {
            background-color: #1565C0;
            box-shadow: 0 2px 5px rgba(0,0,0,0.2);
        }
        
        /* Main title styling */
        .main-title {
            color: #1E88E5;
            font-weight: 600;
            margin-bottom: 30px;
        }
        
        /* Sidebar styling */
        .css-1d391kg, .css-1lcbmhc {
            background-color: #f8f9fa;
        }
        
        /* Progress labels */
        .progress-label {
            font-size: 0.9rem !important;
            color: #555;
            margin-top: 5px;
            margin-bottom: 15px;
        }
        
       /* NEW: Centered title styling */
        .centered-title {
            text-align: center !important;
            font-size: 2.5rem !important;
            font-weight: 700 !important;
            color: #1E88E5 !important;
            margin-bottom: 30px !important;
            padding-top: 20px !important;
            width: 100% !important;
        }
        
        /* NEW: Container for centered content */
        .center-container {
            display: flex !important;
            justify-content: center !important;
            width: 100% !important;
        }
        </style>
    """, unsafe_allow_html=True)
    
    
def save_and_continue_ethics(uploaded_documents=None, responses_complete=None):
    """Handle the save and continue logic for the ethics checklist page"""
    if uploaded_documents is None:
        uploaded_documents = st.session_state.get('uploaded_documents', {})
    
    # Get all questions from all parts
    all_questions = []
    for part in ETHICS_CHECKLIST.values():
        all_questions.extend(part["questions"])
    
    # Check if all questions have been answered
    if responses_complete is None:
        responses_complete = all(q['id'] in st.session_state.checklist_responses 
                            and 'answer' in st.session_state.checklist_responses[q['id']]
                            and st.session_state.checklist_responses[q['id']]['answer'] in ["YES", "NO", "N/A"]
                            for q in all_questions)
    
    if responses_complete:
        # Store documents in session state
        st.session_state.uploaded_documents.update(uploaded_documents)
        
        try:
            # Validate responses using BaseAgent
            agent = BaseAgent()
            validation = agent.validate_checklist(
                st.session_state.checklist_responses,
                st.session_state.uploaded_documents
            )
            
            st.success("Ethics checklist completed successfully!")
            st.info("AI Review: " + validation)
            
            # Display document summary
            if st.session_state.uploaded_documents:
                st.subheader("Uploaded Documents Summary")
                for doc_id, doc_info in st.session_state.uploaded_documents.items():
                    st.write(f"📎 {doc_info.get('type', 'Document')}: {doc_info.get('name', 'Unknown')}")
            
            st.session_state.current_page = "Review & Submit"
            st.rerun()
        except Exception as e:
            logger.error(f"Error validating checklist: {str(e)}")
            st.warning("Unable to perform AI validation. Your responses have been saved and you can proceed.")
            
            # Still allow proceeding to the next page
            st.session_state.current_page = "Review & Submit"
            st.rerun()
    else:
        st.error("Please answer all questions before proceeding.")

def render_research_context():
    st.header("Research Context")
    
    # Get current values from session state or use empty strings
    current_data = st.session_state.research_data
    title = current_data.get('title', '')
    field = current_data.get('field', '')
    context = current_data.get('context', '')
    description = current_data.get('description', '')
    methodology = current_data.get('methodology', '')
    participants = current_data.get('participants', '')
    timeline = current_data.get('timeline', '')
    
    with st.form("research_context_form"):
        # 1. Research Title
        st.markdown("#### 1. Research Title")
        title = st.text_area(
            label="Research Title",
            key="research_title",
            value=title,
            height=100,
            placeholder="Enter the title of your research project"
        )
        
        # 2. Research Field and 3. Research Context in columns
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 2. Research Field")
            field = st.text_area(
                label="Research Field",
                key="research_field",
                value=field,
                height=150,
                placeholder="Enter your research field(s)"
            )
        
        with col2:
            st.markdown("#### 3. Research Context")
            context = st.text_area(
                label="Research Context",
                key="research_context",
                value=context,
                height=150,
                placeholder="Describe the context of your research"
            )
        
        # 4. Research Description
        st.markdown("#### 4. Research Description")
        description = st.text_area(
            label="Research Description",
            key="research_description",
            value=description,
            height=150,
            placeholder="Provide a detailed description of your research"
        )
        
        # 5. Research Methodology
        st.markdown("#### 5. Research Methodology")
        methodology = st.text_area(
            label="Research Methodology",
            key="research_methodology",
            value=methodology,
            height=150,
            placeholder="Describe your research methodology"
        )
        
        # 6. Target Participants and 7. Expected Timeline in columns
        col3, col4 = st.columns(2)
        
        with col3:
            st.markdown("#### 6. Target Participants")
            participants = st.text_area(
                label="Target Participants",
                key="target_participants",
                value=participants,
                height=150,
                placeholder="Describe your target participants"
            )
        with col4:
            st.markdown("#### 7. Expected Timeline")
            timeline = st.text_area(
                label="Expected Timeline",
                key="expected_timeline",
                value=timeline,
                height=150,
                placeholder="Outline your expected research timeline"
            )
        
        # Form buttons
        col_buttons = st.columns([1, 1])
        
        with col_buttons[0]:
            generate_feedback = st.form_submit_button("Generate AI Feedback")
        
        with col_buttons[1]:
            save_continue = st.form_submit_button("Save and Continue")
        
        # Update session state with current values
        current_data = {
            'title': title,
            'field': field,
            'context': context,
            'description': description,
            'methodology': methodology,
            'participants': participants,
            'timeline': timeline
        }
        st.session_state.research_data = current_data
        
        # Handle form submission
        if generate_feedback:
            # Check if there's any content to provide feedback on
            if any(current_data.values()):
                try:
                    # Generate feedback using BaseAgent
                    agent = BaseAgent()
                    feedback = agent.analyze_research_context(current_data)
                    
                    # Store feedback in session state
                    st.session_state.research_feedback = feedback
                    st.session_state.show_research_feedback = True
                except Exception as e:
                    st.error(f"Unable to generate feedback: {str(e)}")
                    logger.error(f"Error generating research context feedback: {str(e)}")
            else:
                st.warning("Please fill in some information before requesting feedback.")
        
        if save_continue:
            # Validate if all fields are filled
            if all(current_data.values()):
                st.success("Research context saved successfully!")
                st.session_state.current_page = "Ethics Checklist"
                st.rerun()
            else:
                st.error("Please fill in all fields before proceeding.")
    
    # Display feedback outside the form if available
    if 'show_research_feedback' in st.session_state and st.session_state.show_research_feedback:
        with st.expander("AI Feedback on Research Context", expanded=True):
            st.markdown(f"**Overall Guidance:**\n{st.session_state.get('research_feedback', 'No feedback available')}")

def render_ethics_checklist():
    st.header("Research Ethics Application Checklist")
    
    # Add a Save and Continue button at the top for better accessibility
    col_top = st.columns([3, 1])
    with col_top[1]:
        if st.button("Save and Continue", key="top_save_continue"):
            save_and_continue_ethics()
    
    # Initialize variables to track responses and documents
    responses_complete = True
    uploaded_documents = {}
    
    # Process each part of the checklist
    for part_key, part in ETHICS_CHECKLIST.items():
        st.subheader(part["title"])
        if "description" in part:
            st.write(part["description"])
        
        # Process each question in this part
        for q in part["questions"]:
            st.write("---")
            st.write(f"**{q['question']}**")
            if "description" in q:
                st.caption(q["description"])
            
            # Create columns for response and document upload
            col1, col2 = st.columns([2, 1])
            
            # Response selection - CHANGE HERE: Add an empty option as default
            with col1:
                # Get current answer if it exists
                current_answer = None
                if q['id'] in st.session_state.checklist_responses and 'answer' in st.session_state.checklist_responses[q['id']]:
                    current_answer = st.session_state.checklist_responses[q['id']]['answer']
                
                # Add empty option as first choice
                options = ["", "YES", "NO", "N/A"]
                index = 0
                if current_answer in options:
                    index = options.index(current_answer)
                
                response = st.radio(
                    f"Response for {q['id']}",
                    options,
                    index=index,
                    key=f"response_{q['id']}",
                    horizontal=True,
                    label_visibility="collapsed"
                )

                # Store response only if a non-empty option is selected
                if response:
                    st.session_state.checklist_responses[q['id']] = {
                        'question': q['question'],
                        'answer': response
                    }
                else:
                    # If empty option is selected, remove any existing answer
                    if q['id'] in st.session_state.checklist_responses and 'answer' in st.session_state.checklist_responses[q['id']]:
                        del st.session_state.checklist_responses[q['id']]['answer']
                    responses_complete = False
            
            # Document upload if required
            if q.get('requires_document', False):
                with col2:
                    uploaded_file = st.file_uploader(
                        f"Upload document for {q['id']}",
                        key=f"doc_{q['id']}",
                        type=['pdf', 'doc', 'docx'],
                        label_visibility="collapsed"
                    )
                    if uploaded_file:
                        try:
                            # Initialize document processor
                            processor = DocumentProcessorAgent()
                            # Process document content
                            content = uploaded_file.read()
                            
                            # Try to review document
                            review_result = processor.review_document(
                                content,
                                uploaded_file.name,
                                q['question']
                            )
                            
                            # Check if we got an error response
                            if review_result.get('status') == "ERROR":
                                st.error(review_result.get('message', "Error processing document"))
                                # Store document without review
                                uploaded_documents[q['id']] = {
                                    'name': uploaded_file.name,
                                    'type': q.get('document_type', 'Document'),
                                    'content': content
                                }
                            else:
                                # Store document and review
                                uploaded_documents[q['id']] = {
                                    'name': uploaded_file.name,
                                    'type': q.get('document_type', 'Document'),
                                    'content': content,
                                    'review': review_result
                                }
                            
                                # Show review status with appropriate color
                                status = review_result.get('status', 'ANALYZING')
                                if status == "APPROVED":
                                    status_color = "green"
                                elif status == "NEEDS_REVISION":
                                    status_color = "red"
                                else:  # ANALYZING or any other status
                                    status_color = "orange"
                                    
                                st.markdown(f"Status: <span style='color:{status_color}'>{status}</span>", 
                                    unsafe_allow_html=True)
                                
                                # If we have a review result, show details
                                with st.expander("View Document Analysis"):
                                    st.write("Analysis:", review_result.get('analysis', 'No analysis available'))
                                    if review_result.get('recommendations'):
                                        st.write("Recommendations:")
                                        for rec in review_result.get('recommendations', []):
                                            st.write(f"- {rec}")
                                    if review_result.get('compliance_score'):
                                        st.write(f"Compliance Score: {review_result.get('compliance_score')}/100")
                        except Exception as e:
                            st.error(f"Error processing document: {str(e)}")
                            logger.error(f"Document processing error: {str(e)}")
            
            # Generate AI Feedback button for each question
            feedback_key = f"feedback_{q['id']}"
            if st.button("Generate AI Feedback", key=feedback_key):
                # Store that we're generating feedback for this question
                st.session_state[f"generating_feedback_{q['id']}"] = True
                st.rerun()
            
            
            # Handle feedback generation in a separate block to avoid freezing
            if f"generating_feedback_{q['id']}" in st.session_state and st.session_state[f"generating_feedback_{q['id']}"]:
                with st.spinner("Generating AI feedback..."):
                    try:
                        # Get the response for this question
                        question_id = q['id']
                        question_text = q['question']
                        response_data = st.session_state.checklist_responses.get(question_id, {})
                        response_answer = response_data.get('answer', 'Not answered')
                        
                        # Initialize BaseAgent to get feedback
                        agent = BaseAgent()
                        
                        # get document if available
                        document = uploaded_documents.get(question_id, None)
                        
                        # Use the helper function to get context-specific feedback
                        feedback = get_question_feedback(
                            agent=agent,
                            question_text=question_text,
                            response_answer=response_answer,
                            document=document
                        )
                        
                        # Store feedback in session state to persist it
                        if 'feedback' not in st.session_state:
                            st.session_state.feedback = {}
                        st.session_state.feedback[question_id] = feedback
                        
                        # Clear the generating flag
                        del st.session_state[f"generating_feedback_{q['id']}"]
                    except Exception as e:
                        logger.error(f"Error generating feedback: {str(e)}")
                        
                        # Create a fallback feedback message
                        if 'feedback' not in st.session_state:
                            st.session_state.feedback = {}
                        
                        st.session_state.feedback[question_id] = f"AI feedback service encountered an error: {str(e)}. Please try again later or proceed with your application."
                        
                        # Clear the generating flag
                        del st.session_state[f"generating_feedback_{q['id']}"]
                    
                    st.rerun()
            
            # Display feedback if it exists for this question
            if 'feedback' in st.session_state and q['id'] in st.session_state.feedback:
                with st.expander("AI Feedback", expanded=True):
                    st.markdown(f"**AI Feedback:**\n{st.session_state.feedback[q['id']]}")
    
    # Bottom Save and Continue button
    if st.button("Save and Continue", key="bottom_save_continue"):
        save_and_continue_ethics(uploaded_documents, responses_complete)

def render_review_submit():
    st.header("Review & Submit")
    
    # Research Context Review
    st.subheader("Research Context")
    for key, value in st.session_state.research_data.items():
        st.write(f"**{key.replace('_', ' ').title()}:** {value}")
    
    # Ethics Checklist Review
    st.subheader("Ethics Checklist Responses")
    for q_id, response in st.session_state.checklist_responses.items():
        st.write(f"**{response['question']}**")
        st.write(f"Answer: {response['answer']}")
        
        # Show document review if available
        if q_id in st.session_state.uploaded_documents:
            doc = st.session_state.uploaded_documents[q_id]
            st.write(f"📎 Document: {doc['name']}")
            if 'review' in doc:
                review = doc['review']
                status = review.get('status', 'ANALYZING')
                if status == "APPROVED":
                    status_color = "green"
                elif status == "NEEDS_REVISION":
                    status_color = "red"
                else:  # ANALYZING or any other status
                    status_color = "orange"
                st.markdown(f"Status: <span style='color:{status_color}'>{status}</span>", 
                        unsafe_allow_html=True)
    
    # Generate and download review report
    if st.session_state.uploaded_documents:
        try:
            processor = DocumentProcessorAgent()
            report_result = processor.generate_review_report(
                {k: v.get('review', {}) for k, v in st.session_state.uploaded_documents.items() if 'review' in v}
            )
            
            # Check if we got an error response
            if report_result.get('status') == "ERROR":
                st.error(report_result.get('message', "Error generating review report"))
            else:
                st.subheader("Document Review Report")
                report = report_result.get('report', '')
                
                st.download_button(
                    label="Download Review Report",
                    data=report,
                    file_name=f"ethics_review_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                    mime="text/plain"
                )
                
                # Display the report in the UI
                with st.expander("View Report", expanded=True):
                    st.markdown(report)
        except Exception as e:
            logger.error(f"Error generating review report: {str(e)}")
            st.error("Unable to generate review report. Please try again later.")
    
    if st.button("Submit Application"):
        # Here you would typically integrate with your BaseAgent for final review
        st.success("Application submitted successfully!")
        st.balloons()

def main():
    try:
        # Page config
        st.set_page_config(
            page_title="Research Ethics Proposal Assistant",
            page_icon="📝",
            layout="wide"
        )
        
        # Initialize session state
        initialize_session_state()
        
        # Apply custom CSS
        apply_custom_css()
        
        # Display centered title
        st.markdown("<div class='center-container'><h1 class='centered-title'>Research Ethics Proposal Assistant (REPA)</h1></div>", unsafe_allow_html=True)
        
        # Sidebar navigation with progress indicators
        with st.sidebar:
            st.title("Navigation")
            pages = ["Research Context", "Ethics Checklist", "Review & Submit"]
            selected_page = st.radio("Go to", pages)
            st.session_state.current_page = selected_page
            
            # Overall progress
            st.write("---")
            st.subheader("Overall Progress")
            overall_progress = calculate_overall_progress()
            st.progress(overall_progress)
            st.write(f"{int(overall_progress * 100)}% Complete")
            
            # Page-specific progress
            st.write("---")
            st.subheader("Progress by Section")
            
            # Research Context progress
            research_progress = calculate_research_context_progress()
            st.write("Research Context")
            st.progress(research_progress)
            st.write(f"{int(research_progress * 100)}% Complete")
            
            # Ethics Checklist progress
            ethics_progress = calculate_ethics_checklist_progress()
            st.write("Ethics Checklist")
            st.progress(ethics_progress)
            st.write(f"{int(ethics_progress * 100)}% Complete")
            
            # If on Ethics Checklist page, show component progress
            if st.session_state.current_page == "Ethics Checklist":
                st.write("---")
                st.subheader("Ethics Checklist Components")
                
                # Calculate progress for each part of the checklist
                for part_key, part in ETHICS_CHECKLIST.items():
                    total_in_part = len(part["questions"])
                    answered_in_part = sum(1 for q in part["questions"] 
                                    if q['id'] in st.session_state.checklist_responses
                                    and 'answer' in st.session_state.checklist_responses[q['id']]
                                    and st.session_state.checklist_responses[q['id']]['answer'] in ["YES", "NO", "N/A"])
                    
                    part_progress = answered_in_part / total_in_part if total_in_part > 0 else 0
                    st.write(f"{part['title']}")
                    st.progress(part_progress)
                    st.write(f"{int(part_progress * 100)}% Complete")
        
        # Render appropriate page
        if st.session_state.current_page == "Research Context":
            render_research_context()
        elif st.session_state.current_page == "Ethics Checklist":
            render_ethics_checklist()
        elif st.session_state.current_page == "Review & Submit":
            render_review_submit()

    except Exception as e:
        logger.error(f"Application error: {str(e)}")
        st.error("An error occurred in the application. Please check the logs.")

if __name__ == "__main__":
    main()