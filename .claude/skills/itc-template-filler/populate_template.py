#!/usr/bin/env python3
"""
ITC Template Population Script
Executable tool for populating ITC Project Templates with project data

Usage:
    python populate_template.py --template <path> --output <path> --sources <file1> [file2 ...]

Or import and use programmatically:
    from populate_template import populate_itc_template
    result = populate_itc_template(template_path, output_path, project_data)
"""

import openpyxl
from pathlib import Path
from datetime import datetime
import sys
import argparse

try:
    from .excel_helpers import set_cell_value, validate_template, inspect_template_structure
except ImportError:
    # When running as standalone script
    from excel_helpers import set_cell_value, validate_template, inspect_template_structure


def populate_itc_template(template_path, output_path, project_data, verbose=True):
    """
    Populate ITC template with project data.

    Args:
        template_path: Path to blank ITC template
        output_path: Where to save populated template
        project_data: Dict with extracted project information
        verbose: Print progress messages

    Returns:
        dict: {'success': bool, 'message': str, 'populated_fields': int}
    """
    if verbose:
        print(f"Loading template: {template_path}")

    # Validate template
    success, workbook, error = validate_template(template_path)
    if not success:
        return {'success': False, 'message': error, 'populated_fields': 0}

    populated_count = 0

    # Get main sheet
    try:
        proposal_sheet = workbook['ITC Project Proposal']
    except KeyError:
        available = ', '.join(workbook.sheetnames)
        return {
            'success': False,
            'message': f"Sheet 'ITC Project Proposal' not found. Available: {available}",
            'populated_fields': 0
        }

    if verbose:
        print("Populating Section 1: Problem Statement...")

    # Section 1: Problem Statement
    try:
        if 'project_name' in project_data:
            set_cell_value(proposal_sheet, 'D4', project_data['project_name'])
            populated_count += 1

        if 'submission_date' in project_data:
            set_cell_value(proposal_sheet, 'E5', project_data['submission_date'])
            populated_count += 1
        else:
            set_cell_value(proposal_sheet, 'E5', datetime.now().strftime("%d %B %Y"))
            populated_count += 1

        if 'business_sponsor' in project_data:
            set_cell_value(proposal_sheet, 'E7', project_data['business_sponsor'])
            populated_count += 1

        if 'it_exco_sponsor' in project_data:
            set_cell_value(proposal_sheet, 'E8', project_data['it_exco_sponsor'])
            populated_count += 1

        if 'functional_area' in project_data:
            set_cell_value(proposal_sheet, 'E9', project_data['functional_area'])
            populated_count += 1

        if 'business_unit' in project_data:
            set_cell_value(proposal_sheet, 'E10', project_data['business_unit'])
            populated_count += 1

        if 'problem_statement' in project_data:
            set_cell_value(proposal_sheet, 'E11', project_data['problem_statement'])
            populated_count += 1

        # Key drivers (E13-E17)
        if 'key_drivers' in project_data:
            driver_map = {
                'system_simplification': 'E13',
                'decommissioning': 'E15',
                'regulatory': 'E17'
            }
            for driver, cell in driver_map.items():
                if driver in project_data['key_drivers']:
                    set_cell_value(proposal_sheet, cell, 'X')
                    populated_count += 1

        # Business readiness (E22-E25)
        if 'business_readiness' in project_data:
            readiness_map = {
                'requirements_understood': 'E22',
                'business_case_developed': 'E23',
                'resources_identified': 'E24',
                'funding_secured': 'E25'
            }
            for item, cell in readiness_map.items():
                if project_data['business_readiness'].get(item):
                    set_cell_value(proposal_sheet, cell, 'X')
                    populated_count += 1

    except Exception as e:
        return {
            'success': False,
            'message': f"Error populating Section 1: {e}",
            'populated_fields': populated_count
        }

    if verbose:
        print("Populating Section 2: Benefits/Costs/Duration...")

    # Section 2: Benefits
    try:
        if 'benefits' in project_data:
            for benefit_name, benefit_info in project_data['benefits'].items():
                if 'checkbox' in benefit_info:
                    set_cell_value(proposal_sheet, benefit_info['checkbox'], 'X')
                    populated_count += 1
                if 'description' in benefit_info and 'text' in benefit_info:
                    set_cell_value(proposal_sheet, benefit_info['description'], benefit_info['text'])
                    populated_count += 1

        # Business unit beneficiaries
        if 'beneficiaries' in project_data:
            for unit_name, unit_info in project_data['beneficiaries'].items():
                if 'checkbox' in unit_info:
                    set_cell_value(proposal_sheet, unit_info['checkbox'], 'X')
                    populated_count += 1
                if 'description' in unit_info and 'text' in unit_info:
                    set_cell_value(proposal_sheet, unit_info['description'], unit_info['text'])
                    populated_count += 1

        # Costs and duration
        if 'cost_estimate' in project_data:
            set_cell_value(proposal_sheet, 'E46', project_data['cost_estimate'])
            populated_count += 1

        if 'cost_breakdown' in project_data:
            set_cell_value(proposal_sheet, 'E47', project_data['cost_breakdown'])
            populated_count += 1

        if 'duration' in project_data:
            set_cell_value(proposal_sheet, 'E48', project_data['duration'])
            populated_count += 1

        if 'timeline' in project_data:
            set_cell_value(proposal_sheet, 'E49', project_data['timeline'])
            populated_count += 1

    except Exception as e:
        return {
            'success': False,
            'message': f"Error populating Section 2: {e}",
            'populated_fields': populated_count
        }

    # Scope Elements sheet
    if 'scope_elements' in project_data and verbose:
        print("Populating Scope Elements sheet...")

    try:
        if 'scope_elements' in project_data:
            scope_sheet = workbook['Scope Elements']
            for idx, elem in enumerate(project_data['scope_elements']):
                row = 4 + idx
                if 'description' in elem:
                    scope_sheet[f'A{row}'] = elem['description']
                    populated_count += 1
                if 'understood' in elem:
                    scope_sheet[f'B{row}'] = elem['understood']
                    populated_count += 1
                if 'enhancement' in elem:
                    scope_sheet[f'C{row}'] = elem['enhancement']
                    populated_count += 1
                if 'sponsorship' in elem:
                    scope_sheet[f'E{row}'] = elem['sponsorship']
                    populated_count += 1
                if 'rationale' in elem:
                    scope_sheet[f'F{row}'] = elem['rationale']
                    populated_count += 1
                if 'resources' in elem:
                    scope_sheet[f'H{row}'] = elem['resources']
                    populated_count += 1
    except KeyError:
        if verbose:
            print("Warning: 'Scope Elements' sheet not found, skipping...")
    except Exception as e:
        return {
            'success': False,
            'message': f"Error populating Scope Elements: {e}",
            'populated_fields': populated_count
        }

    # Estimates sheet
    if 'tasks' in project_data and verbose:
        print("Populating Estimates sheet...")

    try:
        if 'tasks' in project_data:
            estimates_sheet = workbook['Estimates']
            for idx, task in enumerate(project_data['tasks']):
                row = 4 + idx
                if 'task' in task:
                    estimates_sheet[f'B{row}'] = task['task']
                    populated_count += 1
                if 'dependency' in task:
                    estimates_sheet[f'C{row}'] = task['dependency']
                    populated_count += 1
                if 'duration' in task:
                    estimates_sheet[f'D{row}'] = task['duration']
                    populated_count += 1
                if 'owner' in task:
                    estimates_sheet[f'G{row}'] = task['owner']
                    populated_count += 1
    except KeyError:
        if verbose:
            print("Warning: 'Estimates' sheet not found, skipping...")
    except Exception as e:
        return {
            'success': False,
            'message': f"Error populating Estimates: {e}",
            'populated_fields': populated_count
        }

    # Save populated template
    if verbose:
        print(f"\nSaving to: {output_path}")

    try:
        workbook.save(output_path)
    except Exception as e:
        return {
            'success': False,
            'message': f"Error saving template: {e}",
            'populated_fields': populated_count
        }

    if verbose:
        print(f"✓ Template populated successfully! ({populated_count} fields)")

    return {
        'success': True,
        'message': f"Successfully populated {populated_count} fields",
        'populated_fields': populated_count
    }


def main():
    """Command-line interface"""
    parser = argparse.ArgumentParser(description='Populate ITC Project Template')
    parser.add_argument('--template', required=True, help='Path to ITC template')
    parser.add_argument('--output', required=True, help='Output path for populated template')
    parser.add_argument('--data', help='Path to JSON file with project data')
    parser.add_argument('--inspect', action='store_true', help='Inspect template structure and exit')
    parser.add_argument('--quiet', action='store_true', help='Suppress progress messages')

    args = parser.parse_args()

    # Inspect mode
    if args.inspect:
        success, workbook, error = validate_template(args.template)
        if not success:
            print(f"Error: {error}", file=sys.stderr)
            return 1

        from excel_helpers import print_inspection_report
        report = inspect_template_structure(workbook)
        print_inspection_report(report)
        return 0

    # Population mode
    if not args.data:
        print("Error: --data required for population (or use --inspect to view structure)", file=sys.stderr)
        return 1

    import json
    with open(args.data) as f:
        project_data = json.load(f)

    result = populate_itc_template(
        args.template,
        args.output,
        project_data,
        verbose=not args.quiet
    )

    if result['success']:
        print(f"\n✓ Success: {result['message']}")
        return 0
    else:
        print(f"\n✗ Failed: {result['message']}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
