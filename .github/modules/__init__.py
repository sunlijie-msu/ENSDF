"""
ENSDF Modules Package
====================

Professional nuclear data processing modules for ENSDF files.

Modules:
- ensdf_validation: Comprehensive validation tools
- ensdf_formatting: Professional formatting utilities  
- ensdf_analysis: Nuclear data analysis tools

Example usage:
    from modules.ensdf_validation import ENSDFValidator
    from modules.ensdf_formatting import ENSDFFormatter
    from modules.ensdf_analysis import ENSDFAnalyzer
    
    # Validate file
    validator = ENSDFValidator()
    result = validator.validate_file("file.ens")
    
    # Format file
    formatter = ENSDFFormatter()
    formatter.fix_file("file.ens", backup=True)
    
    # Analyze file
    analyzer = ENSDFAnalyzer()
    report = analyzer.analyze_file("file.ens")
"""

__version__ = "1.0.0"
__author__ = "ENSDF Nuclear Data Team"

from .ensdf_validation import ENSDFValidator
from .ensdf_formatting import ENSDFFormatter  
from .ensdf_analysis import ENSDFAnalyzer

__all__ = [
    "ENSDFValidator",
    "ENSDFFormatter", 
    "ENSDFAnalyzer"
]
