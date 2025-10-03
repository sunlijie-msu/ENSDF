#!/usr/bin/env python3
"""
ENSDF Spaghetti Code Cleanup Script
==================================

This script organizes the chaotic .github folder by:
1. Moving redundant scripts to a legacy/ folder
2. Preserving only essential tools
3. Documenting the reorganization

**CRITICAL**: This is a ONE-TIME cleanup to address the spaghetti code crisis.
After cleanup, use ensdf_tools.py unified interface for all operations.
"""

import os
import shutil
from pathlib import Path
from typing import Dict, List

def categorize_scripts() -> Dict[str, List[str]]:
    """Categorize scripts by function to identify redundancy."""
    
    # Essential tools to keep
    essential_scripts = {
        'ensdf_tools.py',           # New unified interface
        'column_calibrate.py',      # Legacy validation tool
        'check_gamma_ordering.py',  # Legacy ordering tool
        'ens2pdf.py',              # PDF conversion tool
        'cleanup_spaghetti_scripts.py'  # This cleanup script
    }
    
    # Categorize redundant scripts
    redundant_categories = {
        'verify_scripts': [],
        'check_scripts': [],
        'analyze_scripts': [],
        'compare_scripts': [],
        'fix_scripts': [],
        'extract_scripts': [],
        'debug_scripts': [],
        'test_scripts': [],
        'final_scripts': [],
        'other_redundant': []
    }
    
    # Scan .github directory
    github_dir = Path(__file__).parent
    
    for script_file in github_dir.glob("*.py"):
        script_name = script_file.name
        
        # Skip essential scripts
        if script_name in essential_scripts:
            continue
            
        # Categorize redundant scripts
        if script_name.startswith('verify_'):
            redundant_categories['verify_scripts'].append(script_name)
        elif script_name.startswith('check_'):
            redundant_categories['check_scripts'].append(script_name)
        elif script_name.startswith('analyze_'):
            redundant_categories['analyze_scripts'].append(script_name)
        elif script_name.startswith('compare_'):
            redundant_categories['compare_scripts'].append(script_name)
        elif script_name.startswith('fix_'):
            redundant_categories['fix_scripts'].append(script_name)
        elif script_name.startswith('extract_'):
            redundant_categories['extract_scripts'].append(script_name)
        elif script_name.startswith('debug_'):
            redundant_categories['debug_scripts'].append(script_name)
        elif script_name.startswith('test_') or script_name.startswith('simple_'):
            redundant_categories['test_scripts'].append(script_name)
        elif script_name.startswith('final_') or script_name.startswith('ultimate_'):
            redundant_categories['final_scripts'].append(script_name)
        else:
            redundant_categories['other_redundant'].append(script_name)
    
    return essential_scripts, redundant_categories

def create_reorganization_report(essential: set, redundant: Dict[str, List[str]]) -> str:
    """Generate comprehensive reorganization report."""
    
    report_lines = [
        "ENSDF Spaghetti Code Cleanup Report",
        "=" * 50,
        "",
        "## PROBLEM IDENTIFIED:",
        f"Found {sum(len(scripts) for scripts in redundant.values())} redundant scripts",
        "causing massive code duplication and maintenance nightmares.",
        "",
        "## ESSENTIAL TOOLS PRESERVED:",
    ]
    
    for script in sorted(essential):
        if script == 'ensdf_tools.py':
            report_lines.append(f"  ✓ {script} - NEW unified interface (replaces most legacy scripts)")
        elif script == 'column_calibrate.py':
            report_lines.append(f"  ✓ {script} - Legacy validation (use: ensdf_tools.py validate)")
        elif script == 'check_gamma_ordering.py':
            report_lines.append(f"  ✓ {script} - Legacy ordering (use: ensdf_tools.py validate)")
        elif script == 'ens2pdf.py':
            report_lines.append(f"  ✓ {script} - PDF conversion (use: ensdf_tools.py convert)")
        else:
            report_lines.append(f"  ✓ {script}")
    
    report_lines.extend([
        "",
        "## REDUNDANT SCRIPTS MOVED TO legacy/:",
        ""
    ])
    
    total_redundant = 0
    for category, scripts in redundant.items():
        if scripts:
            report_lines.append(f"### {category.replace('_', ' ').title()}:")
            for script in sorted(scripts):
                report_lines.append(f"  ❌ {script}")
                total_redundant += 1
            report_lines.append("")
    
    report_lines.extend([
        f"## SUMMARY:",
        f"  - Preserved: {len(essential)} essential scripts",
        f"  - Moved to legacy: {total_redundant} redundant scripts",
        f"  - Reorganization: Professional module structure in modules/",
        f"  - New interface: ensdf_tools.py replaces {total_redundant} scattered scripts",
        "",
        "## FUTURE WORKFLOW:",
        "  All operations should use: python ensdf_tools.py [validate|format|analyze|convert]",
        "  Legacy scripts preserved for reference but discouraged for daily use.",
        "",
        "## ANTI-SPAGHETTI RULES NOW ENFORCED:",
        "  - NO new verify_*, check_*, analyze_*, compare_* scripts",
        "  - ALL functionality goes into modules/ with unified interface",
        "  - Professional code organization with separation of concerns",
        ""
    ])
    
    return "\n".join(report_lines)

def perform_cleanup():
    """Execute the cleanup process."""
    
    github_dir = Path(__file__).parent
    legacy_dir = github_dir / "legacy"
    
    print("🧹 Starting ENSDF Spaghetti Code Cleanup...")
    
    # Categorize scripts
    essential_scripts, redundant_categories = categorize_scripts()
    
    # Create legacy directory
    legacy_dir.mkdir(exist_ok=True)
    print(f"📁 Created legacy directory: {legacy_dir}")
    
    # Move redundant scripts
    moved_count = 0
    for category, scripts in redundant_categories.items():
        if scripts:
            category_dir = legacy_dir / category
            category_dir.mkdir(exist_ok=True)
            
            for script in scripts:
                source = github_dir / script
                destination = category_dir / script
                
                if source.exists():
                    shutil.move(str(source), str(destination))
                    moved_count += 1
                    print(f"  📦 Moved {script} → legacy/{category}/")
    
    # Generate report
    report_content = create_reorganization_report(essential_scripts, redundant_categories)
    
    # Save report
    report_file = github_dir / "spaghetti_cleanup_report.md"
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(report_content)
    
    print(f"📊 Generated cleanup report: {report_file}")
    print(f"✅ Cleanup complete! Moved {moved_count} redundant scripts to legacy/")
    print()
    print("🎯 NEXT STEPS:")
    print("  1. Use: python ensdf_tools.py [command] for all operations")
    print("  2. Legacy scripts available in legacy/ folder for reference")
    print("  3. Follow anti-spaghetti rules in copilot-instructions.md")
    print()
    print("💡 Professional nuclear data processing now available via unified interface!")

if __name__ == "__main__":
    perform_cleanup()
