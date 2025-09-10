#!/usr/bin/env python3
"""
ENSDF Tools - Professional Nuclear Data Processing Suite
=========================================================

Unified command-line interface for ENSDF nuclear data processing.
Replaces multiple spaghetti scripts with a single professional tool.

Commands:
  validate    - Validate ENSDF file format and content
  format      - Fix ENSDF formatting issues  
  analyze     - Analyze nuclear data content
  convert     - Convert ENSDF to other formats (PDF, JSON)

Usage:
  python ensdf_tools.py validate "file.ens"
  python ensdf_tools.py format "file.ens" --fix-all
  python ensdf_tools.py analyze "file.ens" --report
  python ensdf_tools.py convert "file.ens" --to-pdf

Author: ENSDF Nuclear Data Team
Version: 1.0.0
"""

import sys
import os
import argparse
import json
from pathlib import Path

# Add modules to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'modules'))

from ensdf_validation import ENSDFValidator
from ensdf_formatting import ENSDFFormatter
from ensdf_analysis import ENSDFAnalyzer

def validate_command(args):
    """Handle validate command."""
    validator = ENSDFValidator()
    
    result = validator.validate_file(
        args.filename,
        check_columns=not args.no_columns,
        check_ordering=not args.no_ordering,
        check_bands=not args.no_bands,
        verbose=args.verbose
    )
    
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        validator.print_results(result)
        
    return 0 if result["success"] else 1

def format_command(args):
    """Handle format command."""
    formatter = ENSDFFormatter()
    
    result = formatter.fix_file(
        args.filename,
        backup=not args.no_backup,
        fix_lengths=args.fix_all or args.fix_lengths,
        fix_ordering=args.fix_all or args.fix_ordering,
        fix_columns=args.fix_all or args.fix_columns,
        dry_run=args.dry_run
    )
    
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        formatter.print_results(result)
        
    return 0 if result["success"] else 1

def analyze_command(args):
    """Handle analyze command."""
    analyzer = ENSDFAnalyzer()
    
    result = analyzer.analyze_file(
        args.filename,
        analyze_levels=not args.no_levels,
        analyze_gammas=not args.no_gammas,
        analyze_lifetimes=not args.no_lifetimes,
        analyze_multipolarities=not args.no_multipolarities
    )
    
    if args.report:
        report_file = args.report if args.report != True else f"{args.filename}.report.txt"
        report_text = analyzer.generate_report(result, report_file)
        print(f"Report written to: {report_file}")
        if not args.quiet:
            print(report_text)
    elif args.json:
        print(json.dumps(result, indent=2, default=str))
    else:
        # Print summary
        print(f"ENSDF ANALYSIS: {result['filename']}")
        print("=" * 60)
        if "levels" in result:
            print(f"Levels: {result['levels']['total_levels']}")
        if "gammas" in result:
            print(f"Gammas: {result['gammas']['total_gammas']}")
        print(f"Analysis performed: {', '.join(result['analysis_performed'])}")
        
    return 0 if result["success"] else 1

def convert_command(args):
    """Handle convert command."""
    if args.to_pdf:
        # Use existing ens2pdf functionality
        try:
            import subprocess
            java_jar = "D:/X/ND/McMaster-MSU-Java-NDS/McMaster_MSU_JAVA_NDS_v3.0_01May2025.jar"
            output_dir = "D:/X/ND/Files/"
            
            base_name = Path(args.filename).stem
            output_file = os.path.join(output_dir, f"{base_name}.pdf")
            
            cmd = ["java", "-jar", java_jar, args.filename, output_file]
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                print(f"PDF generated: {output_file}")
                if args.open:
                    # Try to open in VS Code or system viewer
                    try:
                        subprocess.run(["code", output_file], check=True)
                    except:
                        os.startfile(output_file)
                return 0
            else:
                print(f"PDF conversion failed: {result.stderr}")
                return 1
                
        except Exception as e:
            print(f"Error converting to PDF: {e}")
            return 1
    else:
        print("Only PDF conversion is currently supported")
        return 1

def main():
    """Main command-line interface."""
    parser = argparse.ArgumentParser(
        description='ENSDF Tools - Professional Nuclear Data Processing Suite',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Validate an ENSDF file
  python ensdf_tools.py validate "Si35_adopted.ens"
  
  # Fix formatting issues
  python ensdf_tools.py format "Si35_adopted.ens" --fix-all
  
  # Analyze nuclear data
  python ensdf_tools.py analyze "Si35_adopted.ens" --report
  
  # Convert to PDF
  python ensdf_tools.py convert "Si35_adopted.ens" --to-pdf --open
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Validate command
    validate_parser = subparsers.add_parser('validate', help='Validate ENSDF file')
    validate_parser.add_argument('filename', help='ENSDF file to validate')
    validate_parser.add_argument('--no-columns', action='store_true', help='Skip column validation')
    validate_parser.add_argument('--no-ordering', action='store_true', help='Skip energy ordering check')
    validate_parser.add_argument('--no-bands', action='store_true', help='Skip band flag validation')
    validate_parser.add_argument('--verbose', action='store_true', help='Verbose output')
    validate_parser.add_argument('--json', action='store_true', help='Output as JSON')
    
    # Format command
    format_parser = subparsers.add_parser('format', help='Fix ENSDF formatting')
    format_parser.add_argument('filename', help='ENSDF file to format')
    format_parser.add_argument('--fix-all', action='store_true', help='Apply all fixes')
    format_parser.add_argument('--fix-lengths', action='store_true', help='Fix line lengths only')
    format_parser.add_argument('--fix-ordering', action='store_true', help='Fix energy ordering only') 
    format_parser.add_argument('--fix-columns', action='store_true', help='Fix column positioning only')
    format_parser.add_argument('--no-backup', action='store_true', help='Do not create backup')
    format_parser.add_argument('--dry-run', action='store_true', help='Show changes without applying')
    format_parser.add_argument('--json', action='store_true', help='Output as JSON')
    
    # Analyze command
    analyze_parser = subparsers.add_parser('analyze', help='Analyze nuclear data')
    analyze_parser.add_argument('filename', help='ENSDF file to analyze')
    analyze_parser.add_argument('--no-levels', action='store_true', help='Skip level analysis')
    analyze_parser.add_argument('--no-gammas', action='store_true', help='Skip gamma analysis')
    analyze_parser.add_argument('--no-lifetimes', action='store_true', help='Skip lifetime analysis')
    analyze_parser.add_argument('--no-multipolarities', action='store_true', help='Skip multipolarity analysis')
    analyze_parser.add_argument('--report', nargs='?', const=True, help='Generate detailed report')
    analyze_parser.add_argument('--json', action='store_true', help='Output as JSON')
    analyze_parser.add_argument('--quiet', action='store_true', help='Minimal output')
    
    # Convert command
    convert_parser = subparsers.add_parser('convert', help='Convert ENSDF to other formats')
    convert_parser.add_argument('filename', help='ENSDF file to convert')
    convert_parser.add_argument('--to-pdf', action='store_true', help='Convert to PDF')
    convert_parser.add_argument('--open', action='store_true', help='Open result after conversion')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
        
    # Check if file exists
    if not os.path.exists(args.filename):
        print(f"Error: File '{args.filename}' not found")
        return 1
        
    # Route to appropriate command handler
    if args.command == 'validate':
        return validate_command(args)
    elif args.command == 'format':
        return format_command(args)
    elif args.command == 'analyze':
        return analyze_command(args)
    elif args.command == 'convert':
        return convert_command(args)
    else:
        parser.print_help()
        return 1

if __name__ == '__main__':
    sys.exit(main())
