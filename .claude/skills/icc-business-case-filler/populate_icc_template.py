#!/usr/bin/env python3
"""
ICC Business Case Template Population
Features interactive clarification mode for missing information
"""

import openpyxl
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple, Optional
import sys

try:
    from .excel_helpers import set_cell_value, validate_template, inspect_template_structure
    from .icc_field_mappings import (
        ICC_FIELD_REGISTRY, ITC_TO_ICC_MAPPING,
        get_clarification_questions, format_clarification_report,
        PRIORITY_CRITICAL, PRIORITY_HIGH
    )
except ImportError:
    # When running as standalone
    from excel_helpers import set_cell_value, validate_template, inspect_template_structure
    from icc_field_mappings import (
        ICC_FIELD_REGISTRY, ITC_TO_ICC_MAPPING,
        get_clarification_questions, format_clarification_report,
        PRIORITY_CRITICAL, PRIORITY_HIGH
    )


def pre_populate_from_itc(icc_workbook, itc_template_path, verbose=True):
    """
    Pre-populate ICC fields from completed ITC template

    Args:
        icc_workbook: ICC template workbook
        itc_template_path: Path to populated ITC template
        verbose: Print progress messages

    Returns:
        tuple: (pre_populated dict, confidence scores)
    """
    if verbose:
        print(f"Pre-populating from ITC template: {itc_template_path}")

    success, itc_wb, error = validate_template(itc_template_path)
    if not success:
        if verbose:
            print(f"Warning: Could not load ITC template: {error}")
        return {}, {}

    pre_populated = {}
    confidence_scores = {}

    try:
        # Get sheets
        icc_summary = icc_workbook['Project Summary']
        itc_proposal = itc_wb['ITC Project Proposal']

        # Project name
        project_name = itc_proposal['D4'].value
        if project_name:
            set_cell_value(icc_summary, 'D1', project_name)
            pre_populated['project_name'] = project_name
            confidence_scores['project_name'] = 1.0
            if verbose:
                print(f"  ✓ Project Name: {project_name}")

        # Sponsor
        sponsor = itc_proposal['E7'].value
        if sponsor:
            set_cell_value(icc_summary, 'C8', sponsor)
            pre_populated['sponsor'] = sponsor
            confidence_scores['sponsor'] = 1.0
            if verbose:
                print(f"  ✓ Sponsor: {sponsor}")

        # IT ExCo Sponsor
        it_sponsor = itc_proposal['E8'].value
        if it_sponsor and it_sponsor != "TBC":
            # Store for potential use in ICC
            pre_populated['it_sponsor'] = it_sponsor
            confidence_scores['it_sponsor'] = 0.9

        # Problem statement (for reference, may need expansion)
        problem_statement = itc_proposal['E11'].value
        if problem_statement:
            pre_populated['problem_statement'] = problem_statement
            confidence_scores['problem_statement'] = 0.7  # Needs expansion for ICC
            if verbose:
                print(f"  ✓ Problem Statement extracted (needs expansion for ICC)")

    except Exception as e:
        if verbose:
            print(f"Warning during ITC pre-population: {e}")

    if verbose:
        print(f"\nPre-populated {len(pre_populated)} fields from ITC template")

    return pre_populated, confidence_scores


def identify_missing_fields(icc_workbook, field_registry=ICC_FIELD_REGISTRY):
    """
    Identify which critical and high priority fields are still missing

    Args:
        icc_workbook: ICC workbook to check
        field_registry: Field definition registry

    Returns:
        tuple: (missing_critical list, missing_high list, missing_medium list)
    """
    missing_critical = []
    missing_high = []
    missing_medium = []

    for sheet_name, fields in field_registry.items():
        try:
            sheet = icc_workbook[sheet_name]
        except KeyError:
            continue

        for field_id, field_def in fields.items():
            try:
                cell_value = sheet[field_def.cell_ref].value
                if not cell_value or str(cell_value).strip() == '':
                    if field_def.priority == PRIORITY_CRITICAL:
                        missing_critical.append(field_id)
                    elif field_def.priority == PRIORITY_HIGH:
                        missing_high.append(field_id)
                    else:
                        missing_medium.append(field_id)
            except:
                # Cell doesn't exist or error accessing
                if field_def.priority == PRIORITY_CRITICAL:
                    missing_critical.append(field_id)
                elif field_def.priority == PRIORITY_HIGH:
                    missing_high.append(field_id)

    return missing_critical, missing_high, missing_medium


def populate_icc_template(template_path, output_path,
                         itc_template_path=None,
                         business_case_data=None,
                         source_documents=None,
                         interactive_mode=True,
                         verbose=True):
    """
    Main ICC template population function with interactive clarification

    Args:
        template_path: Path to blank ICC template
        output_path: Where to save populated template
        itc_template_path: Optional path to populated ITC template (for pre-population)
        business_case_data: Dict with business case information (optional)
        source_documents: List of file paths to extract information from (optional)
        interactive_mode: If True, generates clarification report for missing fields
        verbose: Print progress messages

    Returns:
        dict: {
            'success': bool,
            'message': str,
            'populated_fields': int,
            'pre_populated_from_itc': int,
            'missing_critical': list,
            'missing_high': list,
            'clarification_report': str (if interactive_mode)
        }
    """
    if verbose:
        print("=" * 80)
        print("ICC BUSINESS CASE TEMPLATE POPULATION")
        print("=" * 80)
        print()

    # Validate ICC template
    success, icc_wb, error = validate_template(template_path)
    if not success:
        return {
            'success': False,
            'message': error,
            'populated_fields': 0
        }

    populated_count = 0
    pre_populated_count = 0
    sources = {}

    # Step 1: Pre-populate from ITC if provided
    if itc_template_path:
        if verbose:
            print("Step 1: Pre-populating from ITC template...")
        pre_populated, confidence = pre_populate_from_itc(icc_wb, itc_template_path, verbose)
        pre_populated_count = len(pre_populated)
        populated_count += pre_populated_count
        sources['ITC'] = pre_populated
        if verbose:
            print()

    # Step 2: Extract from source documents if provided
    if source_documents:
        if verbose:
            print("Step 2: Extracting information from source documents...")
        try:
            from extraction_helpers import extract_information
            for doc_path in source_documents:
                if verbose:
                    print(f"  Reading: {doc_path}")
                # Extract information from document
                # This would integrate with extraction_helpers.py
                # For now, just acknowledge the documents
        except Exception as e:
            if verbose:
                print(f"  Warning: Could not extract from documents: {e}")
        if verbose:
            print()

    # Step 2b: Populate from business case data if provided
    if business_case_data:
        if verbose:
            print("Step 2b: Populating from business case data dict...")
        # Implementation would go here
        # This would use the provided dictionary to populate fields
        if verbose:
            print("  (Business case data dict population not yet implemented)")
            print()

    # Step 3: Identify missing fields
    if verbose:
        print("Step 3: Analyzing gaps and missing information...")

    missing_critical, missing_high, missing_medium = identify_missing_fields(icc_wb)

    if verbose:
        print(f"  Missing CRITICAL fields: {len(missing_critical)}")
        print(f"  Missing HIGH priority fields: {len(missing_high)}")
        print(f"  Missing MEDIUM priority fields: {len(missing_medium)}")
        print()

    # Step 4: Generate clarification report if in interactive mode
    clarification_report = None
    if interactive_mode and (missing_critical or missing_high):
        if verbose:
            print("Step 4: Generating clarification questions...")

        all_missing = missing_critical + missing_high + missing_medium
        questions = get_clarification_questions(all_missing)
        clarification_report = format_clarification_report(questions)

        if verbose:
            print(f"  Generated {sum(len(q) for cat in questions.values() for q in cat.values())} clarification questions")
            print()

    # Step 5: Save template (even if partially populated)
    if verbose:
        print(f"Step 5: Saving template to: {output_path}")

    try:
        # Ensure output path has correct extension
        output_path_obj = Path(output_path)
        if output_path_obj.suffix.lower() not in ['.xlsx', '.xlsm']:
            output_path = str(output_path_obj.with_suffix('.xlsm'))
            if verbose:
                print(f"  Note: Corrected output extension to .xlsm")

        # Save with proper error handling
        icc_wb.save(output_path)

        # Verify file was created
        if not Path(output_path).exists():
            raise Exception("File was not created")

        if verbose:
            print(f"  ✓ Template saved successfully to: {output_path}")
    except Exception as e:
        import traceback
        error_detail = traceback.format_exc()
        if verbose:
            print(f"  ✗ Error saving template: {e}")
            print(f"  Details: {error_detail}")
        return {
            'success': False,
            'message': f"Error saving template: {e}",
            'populated_fields': populated_count,
            'error_detail': error_detail
        }

    # Prepare result
    result = {
        'success': True,
        'message': f'Populated {populated_count} fields ({pre_populated_count} from ITC)',
        'populated_fields': populated_count,
        'pre_populated_from_itc': pre_populated_count,
        'missing_critical': missing_critical,
        'missing_high': missing_high,
        'sources': sources
    }

    if clarification_report:
        result['clarification_report'] = clarification_report

    if verbose:
        print()
        print("=" * 80)
        print("COMPLETION SUMMARY")
        print("=" * 80)
        print(f"✓ Populated fields: {populated_count}")
        if pre_populated_count > 0:
            print(f"  - From ITC template: {pre_populated_count}")
        print(f"⚠  Missing CRITICAL fields: {len(missing_critical)}")
        print(f"⚠  Missing HIGH priority fields: {len(missing_high)}")

        if clarification_report and (missing_critical or missing_high):
            print()
            print("📋 CLARIFICATION REQUIRED")
            print("A detailed clarification report has been generated.")
            print("Please review and provide the requested information.")

        print("=" * 80)

    return result


def main():
    """Command-line interface"""
    import argparse

    parser = argparse.ArgumentParser(description='Populate ICC Business Case Template')
    parser.add_argument('--template', required=True, help='Path to ICC template')
    parser.add_argument('--output', required=True, help='Output path for populated template')
    parser.add_argument('--itc-template', help='Path to populated ITC template (for pre-population)')
    parser.add_argument('--clarification-output', help='Path to save clarification report')
    parser.add_argument('--no-interactive', action='store_true',
                       help='Disable interactive clarification mode')
    parser.add_argument('--quiet', action='store_true', help='Suppress progress messages')

    args = parser.parse_args()

    result = populate_icc_template(
        template_path=args.template,
        output_path=args.output,
        itc_template_path=args.itc_template,
        interactive_mode=not args.no_interactive,
        verbose=not args.quiet
    )

    # Save clarification report if requested
    if 'clarification_report' in result and args.clarification_output:
        with open(args.clarification_output, 'w') as f:
            f.write(result['clarification_report'])
        print(f"\n✓ Clarification report saved to: {args.clarification_output}")

    # Print clarification report to console if generated
    elif 'clarification_report' in result:
        print("\n" + result['clarification_report'])

    if result['success']:
        return 0
    else:
        print(f"\n✗ Failed: {result['message']}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
