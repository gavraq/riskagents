#!/usr/bin/env python3
"""
ICC Business Case Template Field Mappings
Defines field locations, priorities, and validation rules for ICC template
"""

from typing import Dict, List, Tuple, Optional

# Field priority levels for gap analysis and clarification
PRIORITY_CRITICAL = "CRITICAL"  # Must have for ICC approval
PRIORITY_HIGH = "HIGH"          # Strongly recommended
PRIORITY_MEDIUM = "MEDIUM"      # Good to have
PRIORITY_LOW = "LOW"            # Optional / nice to have

# Field categories for organized clarification questions
CATEGORY_PROJECT_INFO = "Project Information"
CATEGORY_FINANCIALS = "Financial Details"
CATEGORY_TIMELINE = "Timeline & Milestones"
CATEGORY_BENEFITS = "Benefits & Business Case"
CATEGORY_RISKS = "Risks & Issues"
CATEGORY_RESOURCES = "Resources & Team"
CATEGORY_GOVERNANCE = "Governance & Compliance"


class ICCFieldDefinition:
    """Defines a field in the ICC template with metadata for gap analysis"""

    def __init__(self, cell_ref: str, field_name: str,
                 priority: str, category: str,
                 can_extract_from_itc: bool = False,
                 itc_source: Optional[Tuple[str, str]] = None,
                 clarification_prompt: Optional[str] = None,
                 validation_rule: Optional[str] = None):
        self.cell_ref = cell_ref
        self.field_name = field_name
        self.priority = priority
        self.category = category
        self.can_extract_from_itc = can_extract_from_itc
        self.itc_source = itc_source  # (sheet_name, cell_ref) tuple
        self.clarification_prompt = clarification_prompt
        self.validation_rule = validation_rule


# ICC Field Mapping - Project Summary Sheet
PROJECT_SUMMARY_FIELDS = {
    'project_name': ICCFieldDefinition(
        cell_ref='D1',
        field_name='Project Name',
        priority=PRIORITY_CRITICAL,
        category=CATEGORY_PROJECT_INFO,
        can_extract_from_itc=True,
        itc_source=('ITC Project Proposal', 'D4'),
        clarification_prompt="What is the full project name?",
        validation_rule="required"
    ),

    'icc_date': ICCFieldDefinition(
        cell_ref='C5',
        field_name='Date of ICC',
        priority=PRIORITY_CRITICAL,
        category=CATEGORY_PROJECT_INFO,
        clarification_prompt="What is the planned ICC presentation date? (format: DD/MM/YYYY)",
        validation_rule="date_format"
    ),

    'project_code': ICCFieldDefinition(
        cell_ref='C6',
        field_name='Project Code',
        priority=PRIORITY_HIGH,
        category=CATEGORY_PROJECT_INFO,
        clarification_prompt="What is the project code assigned by PMO?",
        validation_rule="optional"
    ),

    'project_manager': ICCFieldDefinition(
        cell_ref='C7',
        field_name='Project Manager',
        priority=PRIORITY_CRITICAL,
        category=CATEGORY_RESOURCES,
        clarification_prompt="Who is the assigned Project Manager?",
        validation_rule="required"
    ),

    'sponsor': ICCFieldDefinition(
        cell_ref='C8',
        field_name='Sponsor',
        priority=PRIORITY_CRITICAL,
        category=CATEGORY_PROJECT_INFO,
        can_extract_from_itc=True,
        itc_source=('ITC Project Proposal', 'E7'),
        clarification_prompt="Who is the Executive Sponsor?",
        validation_rule="required"
    ),

    'project_start_date': ICCFieldDefinition(
        cell_ref='F6',
        field_name='Expected Project Start Date',
        priority=PRIORITY_CRITICAL,
        category=CATEGORY_TIMELINE,
        clarification_prompt="What is the expected project start date? (format: DD/MM/YYYY)",
        validation_rule="date_format"
    ),

    'project_end_date': ICCFieldDefinition(
        cell_ref='F7',
        field_name='Expected Project End Date',
        priority=PRIORITY_CRITICAL,
        category=CATEGORY_TIMELINE,
        clarification_prompt="What is the expected project completion date? (format: DD/MM/YYYY)",
        validation_rule="date_format"
    ),

    'total_cost_2025': ICCFieldDefinition(
        cell_ref='F8',
        field_name='2025 Cost',
        priority=PRIORITY_CRITICAL,
        category=CATEGORY_FINANCIALS,
        clarification_prompt="What is the total project cost for 2025? (in £'000)",
        validation_rule="numeric_currency"
    ),
}


# Finances Sheet - Key fields (simplified, as there are 1190+ fields)
FINANCES_CRITICAL_FIELDS = {
    'total_capex': ICCFieldDefinition(
        cell_ref='TBD',  # Need to identify exact cell
        field_name='Total Capital Expenditure',
        priority=PRIORITY_CRITICAL,
        category=CATEGORY_FINANCIALS,
        clarification_prompt="What is the total CapEx for this project across all years? (in £'000)",
        validation_rule="numeric_currency"
    ),

    'total_opex': ICCFieldDefinition(
        cell_ref='TBD',
        field_name='Total Operational Expenditure',
        priority=PRIORITY_CRITICAL,
        category=CATEGORY_FINANCIALS,
        clarification_prompt="What is the total OpEx for this project across all years? (in £'000)",
        validation_rule="numeric_currency"
    ),

    'total_fte': ICCFieldDefinition(
        cell_ref='TBD',
        field_name='Total FTE',
        priority=PRIORITY_HIGH,
        category=CATEGORY_RESOURCES,
        clarification_prompt="What is the total FTE requirement for this project?",
        validation_rule="numeric"
    ),
}


# Milestones & Benefits Sheet
MILESTONES_BENEFITS_FIELDS = {
    'key_milestone_1': ICCFieldDefinition(
        cell_ref='C4',  # First milestone row
        field_name='Key Milestone 1',
        priority=PRIORITY_HIGH,
        category=CATEGORY_TIMELINE,
        clarification_prompt="What is the first major project milestone?",
        validation_rule="optional"
    ),

    'milestone_1_date': ICCFieldDefinition(
        cell_ref='H4',
        field_name='Milestone 1 Completion Date',
        priority=PRIORITY_HIGH,
        category=CATEGORY_TIMELINE,
        clarification_prompt="When is the first milestone expected to complete? (format: DD/MM/YYYY)",
        validation_rule="date_format"
    ),

    'regulatory_compliance_benefit': ICCFieldDefinition(
        cell_ref='J4',  # Regulatory benefit column
        field_name='Regulatory Compliance Benefit',
        priority=PRIORITY_MEDIUM,
        category=CATEGORY_BENEFITS,
        can_extract_from_itc=True,
        itc_source=('ITC Project Proposal', 'E31'),
        clarification_prompt="What are the regulatory compliance benefits? Can you quantify penalty/cost avoidance?",
        validation_rule="optional"
    ),
}


# RAIDs Sheet
RAIDS_FIELDS = {
    'key_risk_1': ICCFieldDefinition(
        cell_ref='E5',  # First risk description
        field_name='Key Risk 1 Description',
        priority=PRIORITY_HIGH,
        category=CATEGORY_RISKS,
        clarification_prompt="What is the highest priority risk for this project?",
        validation_rule="optional"
    ),

    'risk_1_impact': ICCFieldDefinition(
        cell_ref='C5',
        field_name='Risk 1 Impact',
        priority=PRIORITY_HIGH,
        category=CATEGORY_RISKS,
        clarification_prompt="What is the impact level of this risk? (High/Medium/Low)",
        validation_rule="enum:High,Medium,Low"
    ),

    'risk_1_likelihood': ICCFieldDefinition(
        cell_ref='D5',
        field_name='Risk 1 Likelihood',
        priority=PRIORITY_HIGH,
        category=CATEGORY_RISKS,
        clarification_prompt="What is the likelihood of this risk? (High/Medium/Low)",
        validation_rule="enum:High,Medium,Low"
    ),

    'risk_1_mitigation': ICCFieldDefinition(
        cell_ref='L5',
        field_name='Risk 1 Mitigation Action',
        priority=PRIORITY_HIGH,
        category=CATEGORY_RISKS,
        clarification_prompt="What is the mitigation action for this risk?",
        validation_rule="optional"
    ),
}


# Business and Asset Class Impact
BUSINESS_IMPACT_FIELDS = {
    'fice_impact': ICCFieldDefinition(
        cell_ref='C8',  # FICE column, first business area row
        field_name='FICE Asset Class Impact',
        priority=PRIORITY_MEDIUM,
        category=CATEGORY_PROJECT_INFO,
        clarification_prompt="What is the impact level on FICE asset class? (High/Medium/Low/None)",
        validation_rule="enum:High,Medium,Low,None"
    ),

    'energy_impact': ICCFieldDefinition(
        cell_ref='I8',
        field_name='Energy Asset Class Impact',
        priority=PRIORITY_MEDIUM,
        category=CATEGORY_PROJECT_INFO,
        clarification_prompt="What is the impact level on Energy asset class? (High/Medium/Low/None)",
        validation_rule="enum:High,Medium,Low,None"
    ),
}


# Complete field registry organized by sheet
ICC_FIELD_REGISTRY = {
    'Project Summary': PROJECT_SUMMARY_FIELDS,
    'Finances': FINANCES_CRITICAL_FIELDS,
    'Milestones & Benefits': MILESTONES_BENEFITS_FIELDS,
    'RAIDs': RAIDS_FIELDS,
    'Business and Asset Class': BUSINESS_IMPACT_FIELDS,
}


# Pre-population mapping from ITC to ICC
ITC_TO_ICC_MAPPING = {
    # Project basics
    ('ITC Project Proposal', 'D4'): [('Project Summary', 'D1')],  # Project name
    ('ITC Project Proposal', 'E7'): [('Project Summary', 'C8')],  # Sponsor
    ('ITC Project Proposal', 'E11'): [('Project Summary', 'problem_statement_field')],  # Problem statement

    # Benefits (ITC identifies themes, ICC needs quantification)
    ('ITC Project Proposal', 'E31'): [('Milestones & Benefits', 'regulatory_benefit_ref')],  # Regulatory
    ('ITC Project Proposal', 'H31'): [('Milestones & Benefits', 'regulatory_description_ref')],

    # Scope elements → Milestones
    ('Scope Elements', 'A*'): [('Milestones & Benefits', 'C*')],  # Requirements → Milestones
}


def get_clarification_questions(missing_fields: List[str],
                               field_registry: Dict = ICC_FIELD_REGISTRY) -> Dict[str, List[Dict]]:
    """
    Generate organized clarification questions grouped by category and priority

    Args:
        missing_fields: List of field identifiers that are missing
        field_registry: Registry of field definitions

    Returns:
        Dict organized by category with questions
    """
    questions_by_category = {}

    for sheet_name, fields in field_registry.items():
        for field_id, field_def in fields.items():
            if field_id in missing_fields and field_def.clarification_prompt:
                category = field_def.category

                if category not in questions_by_category:
                    questions_by_category[category] = {
                        PRIORITY_CRITICAL: [],
                        PRIORITY_HIGH: [],
                        PRIORITY_MEDIUM: [],
                        PRIORITY_LOW: []
                    }

                questions_by_category[category][field_def.priority].append({
                    'field_id': field_id,
                    'field_name': field_def.field_name,
                    'sheet': sheet_name,
                    'cell': field_def.cell_ref,
                    'prompt': field_def.clarification_prompt,
                    'validation': field_def.validation_rule
                })

    return questions_by_category


def format_clarification_report(questions_by_category: Dict) -> str:
    """
    Format clarification questions as markdown report

    Returns:
        Markdown-formatted report ready for presentation to user
    """
    report = "# ICC Business Case - Information Required\n\n"
    report += "The following information is needed to complete the ICC business case template.\n"
    report += "Questions are organized by category and priority.\n\n"

    priority_emoji = {
        PRIORITY_CRITICAL: "🔴 CRITICAL",
        PRIORITY_HIGH: "🟡 HIGH",
        PRIORITY_MEDIUM: "🟢 MEDIUM",
        PRIORITY_LOW: "⚪ LOW"
    }

    for category, priority_groups in questions_by_category.items():
        # Check if category has any questions
        has_questions = any(len(questions) > 0 for questions in priority_groups.values())
        if not has_questions:
            continue

        report += f"## {category}\n\n"

        for priority in [PRIORITY_CRITICAL, PRIORITY_HIGH, PRIORITY_MEDIUM, PRIORITY_LOW]:
            questions = priority_groups[priority]
            if not questions:
                continue

            report += f"### {priority_emoji[priority]}\n\n"

            for q in questions:
                report += f"**{q['field_name']}** (Sheet: {q['sheet']}, Cell: {q['cell']})\n"
                report += f"- {q['prompt']}\n"
                if q['validation'] and q['validation'] != 'optional':
                    report += f"- *Validation: {q['validation']}*\n"
                report += "\n"

    report += "---\n\n"
    report += "## Next Steps\n\n"
    report += "1. Review the critical (🔴) questions first - these are required for ICC approval\n"
    report += "2. Provide answers for high priority (🟡) questions to strengthen the business case\n"
    report += "3. Medium (🟢) and low (⚪) priority questions can be addressed later if needed\n\n"
    report += "Once you provide this information, I can complete the ICC template.\n"

    return report
