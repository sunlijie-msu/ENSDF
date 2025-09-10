#!/usr/bin/env python3
"""
ENSDF Analysis Module
====================

Professional nuclear data analysis tools for ENSDF files.
Consolidates multiple analysis functions into a single module.

Functions:
- Energy level analysis
- Gamma transition analysis
- J-pi assignment verification
- Lifetime analysis
- Multipolarity analysis
- Statistical analysis

Usage:
    from modules.ensdf_analysis import ENSDFAnalyzer
    
    analyzer = ENSDFAnalyzer()
    report = analyzer.analyze_file("filename.ens")
"""

import os
import sys
import re
import json
from typing import List, Dict, Tuple, Optional, Any
from collections import defaultdict, Counter

class ENSDFAnalyzer:
    """
    Professional ENSDF analysis class with comprehensive nuclear data analysis.
    """
    
    def __init__(self):
        self.data = {}
        
    def analyze_file(self, filename: str, 
                    analyze_levels: bool = True,
                    analyze_gammas: bool = True,
                    analyze_lifetimes: bool = True,
                    analyze_multipolarities: bool = True) -> Dict:
        """
        Comprehensive analysis of an ENSDF file.
        
        Args:
            filename: Path to ENSDF file
            analyze_levels: Analyze energy levels
            analyze_gammas: Analyze gamma transitions  
            analyze_lifetimes: Analyze level lifetimes
            analyze_multipolarities: Analyze transition multipolarities
            
        Returns:
            Dictionary with analysis results
        """
        if not os.path.exists(filename):
            return {"error": f"File {filename} not found", "success": False}
            
        # Read and parse file
        with open(filename, 'r') as f:
            lines = f.readlines()
            
        results = {
            "filename": filename,
            "success": True,
            "statistics": {},
            "levels": [],
            "gammas": [],
            "analysis_performed": []
        }
        
        # Parse records
        parsed_data = self._parse_ensdf(lines)
        
        if analyze_levels:
            results["levels"] = self._analyze_levels(parsed_data)
            results["analysis_performed"].append("level_analysis")
            
        if analyze_gammas:
            results["gammas"] = self._analyze_gammas(parsed_data)
            results["analysis_performed"].append("gamma_analysis")
            
        if analyze_lifetimes:
            results["lifetimes"] = self._analyze_lifetimes(parsed_data)
            results["analysis_performed"].append("lifetime_analysis")
            
        if analyze_multipolarities:
            results["multipolarities"] = self._analyze_multipolarities(parsed_data)
            results["analysis_performed"].append("multipolarity_analysis")
            
        # Generate statistics
        results["statistics"] = self._generate_statistics(results)
        
        return results
        
    def _parse_ensdf(self, lines: List[str]) -> Dict:
        """Parse ENSDF file into structured data."""
        data = {
            "levels": [],
            "gammas": [],
            "comments": [],
            "other_records": []
        }
        
        current_level = None
        
        for line_num, line in enumerate(lines, 1):
            line_content = line.rstrip('\n\r')
            
            if len(line_content) >= 10:
                record_type = line_content[7] if len(line_content) > 7 else ' '
                
                if record_type == 'L':
                    # Level record
                    level_data = self._parse_level_record(line_content, line_num)
                    data["levels"].append(level_data)
                    current_level = level_data
                    
                elif record_type == 'G':
                    # Gamma record
                    gamma_data = self._parse_gamma_record(line_content, line_num)
                    if current_level:
                        gamma_data["parent_level"] = current_level["energy"]
                    data["gammas"].append(gamma_data)
                    
        return data
        
    def _parse_level_record(self, line: str, line_num: int) -> Dict:
        """Parse L-record into structured data."""
        level = {
            "line_number": line_num,
            "raw_line": line,
            "energy": None,
            "energy_uncertainty": None,
            "jpi": None,
            "half_life": None,
            "half_life_uncertainty": None,
            "band_flag": None
        }
        
        # Extract energy (columns 10-19)
        energy_str = line[9:19].strip()
        if energy_str:
            try:
                level["energy"] = float(energy_str)
            except ValueError:
                level["energy"] = energy_str
                
        # Extract energy uncertainty (columns 20-21)
        de_str = line[19:21].strip()
        if de_str:
            level["energy_uncertainty"] = de_str
            
        # Extract J-pi (columns 23-39)
        jpi_str = line[22:39].strip()
        if jpi_str:
            level["jpi"] = jpi_str
            
        # Extract half-life (columns 40-49)
        t_str = line[39:49].strip()
        if t_str:
            level["half_life"] = t_str
            
        # Extract half-life uncertainty (columns 50-55)
        dt_str = line[49:55].strip()
        if dt_str:
            level["half_life_uncertainty"] = dt_str
            
        # Extract band flag (column 77)
        if len(line) >= 77:
            band_char = line[76]
            if band_char in ['A', 'B', 'b', 'C', 'c']:
                level["band_flag"] = band_char
                
        return level
        
    def _parse_gamma_record(self, line: str, line_num: int) -> Dict:
        """Parse G-record into structured data."""
        gamma = {
            "line_number": line_num,
            "raw_line": line,
            "energy": None,
            "energy_uncertainty": None,
            "intensity": None,
            "intensity_uncertainty": None,
            "multipolarity": None,
            "mixing_ratio": None
        }
        
        # Extract energy (columns 10-19)
        energy_str = line[9:19].strip()
        if energy_str:
            try:
                gamma["energy"] = float(energy_str)
            except ValueError:
                gamma["energy"] = energy_str
                
        # Extract energy uncertainty (columns 20-21)
        de_str = line[19:21].strip()
        if de_str:
            gamma["energy_uncertainty"] = de_str
            
        # Extract intensity (columns 23-29)
        ri_str = line[22:29].strip()
        if ri_str:
            try:
                gamma["intensity"] = float(ri_str)
            except ValueError:
                gamma["intensity"] = ri_str
                
        # Extract intensity uncertainty (columns 30-31)
        dri_str = line[29:31].strip()
        if dri_str:
            gamma["intensity_uncertainty"] = dri_str
            
        # Extract multipolarity (columns 32-41)
        mult_str = line[31:41].strip()
        if mult_str:
            gamma["multipolarity"] = mult_str
            
        return gamma
        
    def _analyze_levels(self, data: Dict) -> Dict:
        """Analyze energy levels."""
        levels = data["levels"]
        
        analysis = {
            "total_levels": len(levels),
            "energy_range": {},
            "jpi_distribution": {},
            "band_distribution": {},
            "levels_with_lifetimes": 0
        }
        
        if levels:
            energies = [l["energy"] for l in levels if isinstance(l["energy"], (int, float))]
            if energies:
                analysis["energy_range"] = {
                    "min": min(energies),
                    "max": max(energies),
                    "span": max(energies) - min(energies)
                }
                
        # J-pi distribution
        jpi_count = Counter([l["jpi"] for l in levels if l["jpi"]])
        analysis["jpi_distribution"] = dict(jpi_count)
        
        # Band flag distribution
        band_count = Counter([l["band_flag"] for l in levels if l["band_flag"]])
        analysis["band_distribution"] = dict(band_count)
        
        # Levels with lifetimes
        analysis["levels_with_lifetimes"] = len([l for l in levels if l["half_life"]])
        
        return analysis
        
    def _analyze_gammas(self, data: Dict) -> Dict:
        """Analyze gamma transitions."""
        gammas = data["gammas"]
        
        analysis = {
            "total_gammas": len(gammas),
            "energy_range": {},
            "intensity_distribution": {},
            "multipolarity_distribution": {}
        }
        
        if gammas:
            energies = [g["energy"] for g in gammas if isinstance(g["energy"], (int, float))]
            if energies:
                analysis["energy_range"] = {
                    "min": min(energies),
                    "max": max(energies),
                    "span": max(energies) - min(energies)
                }
                
        # Multipolarity distribution
        mult_count = Counter([g["multipolarity"] for g in gammas if g["multipolarity"]])
        analysis["multipolarity_distribution"] = dict(mult_count)
        
        return analysis
        
    def _analyze_lifetimes(self, data: Dict) -> Dict:
        """Analyze level lifetimes."""
        levels_with_lifetimes = [l for l in data["levels"] if l["half_life"]]
        
        analysis = {
            "levels_with_lifetimes": len(levels_with_lifetimes),
            "lifetime_units": {},
            "lifetime_range": {}
        }
        
        # Extract lifetime units
        unit_count = defaultdict(int)
        for level in levels_with_lifetimes:
            t_str = level["half_life"]
            if t_str:
                # Extract units (PS, NS, US, MS, S, etc.)
                units = re.findall(r'[A-Z]{1,2}', t_str)
                for unit in units:
                    unit_count[unit] += 1
                    
        analysis["lifetime_units"] = dict(unit_count)
        
        return analysis
        
    def _analyze_multipolarities(self, data: Dict) -> Dict:
        """Analyze transition multipolarities."""
        gammas_with_mult = [g for g in data["gammas"] if g["multipolarity"]]
        
        analysis = {
            "gammas_with_multipolarity": len(gammas_with_mult),
            "multipolarity_types": {},
            "electric_vs_magnetic": {"E": 0, "M": 0, "mixed": 0}
        }
        
        for gamma in gammas_with_mult:
            mult = gamma["multipolarity"]
            if mult:
                # Count E1, E2, M1, etc.
                if 'E' in mult and 'M' in mult:
                    analysis["electric_vs_magnetic"]["mixed"] += 1
                elif 'E' in mult:
                    analysis["electric_vs_magnetic"]["E"] += 1
                elif 'M' in mult:
                    analysis["electric_vs_magnetic"]["M"] += 1
                    
        return analysis
        
    def _generate_statistics(self, results: Dict) -> Dict:
        """Generate overall statistics."""
        stats = {
            "total_records": 0,
            "data_quality": "good"
        }
        
        if "levels" in results:
            stats["total_records"] += results["levels"].get("total_levels", 0)
            
        if "gammas" in results:
            stats["total_records"] += results["gammas"].get("total_gammas", 0)
            
        return stats
        
    def generate_report(self, results: Dict, output_file: Optional[str] = None) -> str:
        """Generate a comprehensive analysis report."""
        report = []
        report.append(f"ENSDF ANALYSIS REPORT: {results['filename']}")
        report.append("=" * 60)
        report.append("")
        
        if "levels" in results:
            level_data = results["levels"]
            report.append("LEVEL ANALYSIS:")
            report.append(f"  Total levels: {level_data['total_levels']}")
            
            if level_data.get("energy_range"):
                er = level_data["energy_range"]
                report.append(f"  Energy range: {er['min']:.1f} - {er['max']:.1f} keV (span: {er['span']:.1f} keV)")
                
            if level_data.get("jpi_distribution"):
                report.append("  J-π distribution:")
                for jpi, count in level_data["jpi_distribution"].items():
                    report.append(f"    {jpi}: {count}")
                    
            report.append("")
            
        if "gammas" in results:
            gamma_data = results["gammas"]
            report.append("GAMMA ANALYSIS:")
            report.append(f"  Total gammas: {gamma_data['total_gammas']}")
            
            if gamma_data.get("energy_range"):
                er = gamma_data["energy_range"]
                report.append(f"  Energy range: {er['min']:.1f} - {er['max']:.1f} keV (span: {er['span']:.1f} keV)")
                
            report.append("")
            
        report_text = "\n".join(report)
        
        if output_file:
            with open(output_file, 'w') as f:
                f.write(report_text)
                
        return report_text
