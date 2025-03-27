ETHICS_CHECKLIST = {
    "PART A": {
        "title": "Mandatory components for all submissions",
        "description": "These components are required for all submissions to a Human Research Ethics Committee.",
        "questions": [
            {
                "id": "A1",
                "question": "Cover letter signed by the Principal Investigator",
                "description": "- Brief project description including Phase (if clinical trial)\n- List of all applicable sites\n- List of supporting documentation with version dates/numbers\n- Sponsor details (for commercial research)\n- PI should not be a student",
                "required": True,
                "requires_document": True,
                "document_type": "cover_letter"
            },
            {
                "id": "A2",
                "question": "Human Research Ethics Committee Application Form",
                "description": "Completed application form",
                "required": True,
                "requires_document": True,
                "document_type": "application_form"
            },
            {
                "id": "A3",
                "question": "Study Protocol",
                "description": "Working document with version date/number",
                "required": True,
                "requires_document": True,
                "document_type": "protocol"
            },
            {
                "id": "A4",
                "question": "CV for Principal Investigator",
                "description": "CVs not required for other researchers",
                "required": True,
                "requires_document": True,
                "document_type": "cv"
            },
            {
                "id": "A5",
                "question": "Summary of expertise relevant to this research",
                "description": "As per National Statement Chapter 4.8.7 and 4.8.15",
                "required": True,
                "requires_document": True,
                "document_type": "expertise_summary"
            }
        ]
    },
    "PART B": {
        "title": "Other components that may be required",
        "description": "Requirements depend on the research project",
        "questions": [
            {
                "id": "B1",
                "question": "Master Participant Information Sheet",
                "description": "- Full letterhead with contact details\n- This Is For You To Keep statement\n- Written in plain English\n- Local researcher's details\n- Research description, aims, requirements\n- Confidentiality assurance\n- Complaints procedure",
                "required": True,
                "requires_document": True,
                "document_type": "participant_info"
            }
        ]
    },
    "PART C": {
        "title": "Research using gene technology",
        "questions": [
            {
                "id": "C1",
                "question": "Ionising Radiation Certificate",
                "required": True,
                "requires_document": True,
                "document_type": "radiation_cert"
            }
        ]
    },
    "PART D": {
        "title": "Research using radiological procedures",
        "questions": [
            {
                "id": "D1",
                "question": "Radiation exposure documentation",
                "description": "- PI letter stating radiation is part of normal care\n- Medical Physicist assessment report",
                "required": True,
                "requires_document": True,
                "document_type": "radiation_docs"
            }
        ]
    },
    "PART E": {
        "title": "Aboriginal and Torres Strait Islander Health Research",
        "questions": [
            {
                "id": "E1",
                "question": "Does the research involve Aboriginal and Torres Strait Islander people?",
                "description": "- Section 4.7 of National Statement is adhered to\n- Six core values are addressed",
                "required": True,
                "requires_document": True,
                "document_type": "indigenous_research"
            },
            {
                "id": "E2",
                "question": "Are permits to undertake research and enter remote communities taken?",
                "description": "Attach approval from appropriate land council and community",
                "required": True,
                "requires_document": True,
                "document_type": "community_permits"
            }
        ]
    }
}
