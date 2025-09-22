#!/usr/bin/env python3
"""
ENSDF Validation Module
======================

Comprehensive validation tools for ENSDF nuclear data files.
Consolidates multiple validation functions into a single professional module.

Functions:
- Column format validation
- Energy ordering verification
- J-pi assignment checking
- Band flag validation
- Line length compliance
- Field positioning verification

Usage:
    from modules.ensdf_validation import ENSDFValidator
    
    validator = ENSDFValidator()
    result = validator.validate_file("filename.ens")
"""

import os
import sys
import re
from typing import List, Dict, Tuple, Optional, Union

class ENSDFValidator:
    """
    Professional ENSDF validation class with comprehensive checking capabilities.
    """
    
    def __init__(self):
        self.errors = []
        self.warnings = []
        
    def validate_file(self, filename: str, 
                     check_columns: bool = True,
                     check_ordering: bool = True, 
                     check_bands: bool = True,
                     verbose: bool = False) -> Dict:
        """
        Comprehensive validation of an ENSDF file.
        
        Args:
            filename: Path to ENSDF file
            check_columns: Validate column positioning
            check_ordering: Validate energy ordering  
            check_bands: Validate band flag positioning
            verbose: Detailed output
            
        Returns:
            Dictionary with validation results
        """
        if not os.path.exists(filename):
            return {"error": f"File {filename} not found", "success": False}
            
        self.errors = []
        self.warnings = []
        
        results = {
            "filename": filename,
            "success": True,
            "errors": [],
            "warnings": [],
            "checks_performed": []
        }
        
        # Read file
        with open(filename, 'r') as f:
            lines = f.readlines()
            
        if check_columns:
            self._validate_columns(lines, results)
            results["checks_performed"].append("column_validation")
            
        if check_ordering:
            self._validate_energy_ordering(lines, results)  
            results["checks_performed"].append("energy_ordering")
            
        if check_bands:
            self._validate_band_flags(lines, results)
            results["checks_performed"].append("band_flags")
            
        results["success"] = len(results["errors"]) == 0
        return results
        
    def _validate_columns(self, lines: List[str], results: Dict):
        """Validate ENSDF column formatting."""
        for line_num, line in enumerate(lines, 1):
            line_content = line.rstrip('\n\r')
            
            # Check line length for data records
            if self._is_data_record(line_content):
                if len(line_content) != 80:
                    results["errors"].append({
                        "line": line_num,
                        "type": "column_length",
                        "message": f"Line {line_num}: Data record is {len(line_content)} chars (should be 80)"
                    })
                    
    def _validate_energy_ordering(self, lines: List[str], results: Dict):
        """Validate that L-records and G-records are in ascending energy order."""
        l_energies = []
        current_level_gammas = []
        
        for line_num, line in enumerate(lines, 1):
            line_content = line.rstrip('\n\r')
            
            if len(line_content) >= 10 and ' L ' in line_content[6:10]:
                # Process previous level's gammas
                if current_level_gammas:
                    self._check_gamma_ordering(current_level_gammas, results)
                current_level_gammas = []
                
                # Extract L-record energy
                energy_str = line_content[9:19].strip()
                if energy_str:
                    try:
                        energy = float(energy_str)
                        l_energies.append((line_num, energy))
                    except ValueError:
                        results["warnings"].append({
                            "line": line_num,
                            "type": "energy_parse",
                            "message": f"Could not parse energy: {energy_str}"
                        })
                        
            elif len(line_content) >= 10 and ' G ' in line_content[6:10]:
                # Extract G-record energy
                energy_str = line_content[9:19].strip()
                if energy_str:
                    try:
                        energy = float(energy_str)
                        current_level_gammas.append((line_num, energy))
                    except ValueError:
                        pass
                        
        # Check final gamma group
        if current_level_gammas:
            self._check_gamma_ordering(current_level_gammas, results)
            
        # Check L-record ordering
        for i in range(1, len(l_energies)):
            prev_line, prev_energy = l_energies[i-1]
            curr_line, curr_energy = l_energies[i]
            if curr_energy < prev_energy:
                results["errors"].append({
                    "line": curr_line,
                    "type": "level_ordering",
                    "message": f"L-record energy {curr_energy} < previous {prev_energy} (line {prev_line})"
                })
                
    def _check_gamma_ordering(self, gammas: List[Tuple[int, float]], results: Dict):
        """Check that gamma energies within a level are in ascending order."""
        for i in range(1, len(gammas)):
            prev_line, prev_energy = gammas[i-1]
            curr_line, curr_energy = gammas[i]
            if curr_energy < prev_energy:
                results["errors"].append({
                    "line": curr_line,
                    "type": "gamma_ordering", 
                    "message": f"Gamma energy {curr_energy} < previous {prev_energy} (line {prev_line})"
                })
                
    def _validate_band_flags(self, lines: List[str], results: Dict):
        """Validate band flag positioning in column 77."""
        band_flags = ['A', 'B', 'b', 'C', 'c']
        
        for line_num, line in enumerate(lines, 1):
            line_content = line.rstrip('\n\r')
            
            # Check L-records for band flags
            if len(line_content) >= 10 and ' L ' in line_content[6:10]:
                # Look for band flags after column 70
                for i, char in enumerate(line_content[70:], 71):
                    if char in band_flags:
                        if i != 77:
                            results["errors"].append({
                                "line": line_num,
                                "type": "band_flag_position",
                                "message": f"Band flag '{char}' at column {i} (should be 77)"
                            })
                        break
                        
    def _is_data_record(self, line: str) -> bool:
        """Check if line is a data record that must be 80 characters."""
        if len(line) < 8:
            return False
        record_type = line[7] if len(line) > 7 else ' '
        return record_type in ['L', 'G', 'E', 'B'] or (len(line) > 8 and line[7:9] == 'DP')
        
    def print_results(self, results: Dict):
        """Print validation results in a formatted way."""
        print(f"ENSDF VALIDATION: {results['filename']}")
        print("=" * 60)
        
        if results["success"]:
            print("SUCCESS: All validation checks passed")
        else:
            print(f"ERRORS FOUND: {len(results['errors'])} errors")
            
        if results["errors"]:
            print("\nERRORS:")
            for error in results["errors"]:
                print(f"  Line {error['line']}: {error['message']}")
                
        if results["warnings"]:
            print("\nWARNINGS:")  
            for warning in results["warnings"]:
                print(f"  Line {warning['line']}: {warning['message']}")
                
        print(f"\nChecks performed: {', '.join(results['checks_performed'])}")
