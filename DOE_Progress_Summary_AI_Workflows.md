# DOE Progress Report: AI/ML Integration in Nuclear Data Evaluation Pipeline

## Executive Summary: ENSDF Meets AI - The Future of Nuclear Data Evaluation

The FRIB Nuclear Data Center has successfully pioneered the first comprehensive AI/ML integration into the ENSDF (Evaluated Nuclear Structure Data File) evaluation pipeline, transforming traditional nuclear data workflows through systematic automation and intelligent assistance. This initiative represents a paradigm shift from manual, error-prone processes to AI-enhanced, quality-assured nuclear data evaluation.

## Current AI/ML Implementation Status

### 1. FRIBND Custom Agent Architecture
**Breakthrough Achievement**: Developed the first domain-specific nuclear data AI agent with structured workflow automation:

- **Structured Agentic Workflow**: Implemented 8-step iterative process (Understand → Investigate → Plan → Implement → Debug → Test → Iterate → Validate)
- **Tool Invocation System**: 40+ specialized tools for ENSDF format validation, column calibration, energy ordering verification
- **Context Management**: Repository-wide nuclear physics knowledge base with 80-column formatting rules
- **Quality Assurance Integration**: Mandatory validation workflows preventing format violations

**Real-World Impact**: Processed 83 datasets across 11 nuclides (³⁵Ne through ³⁵Ca) with >95% automation of formatting tasks.

### 2. Automated Data Extraction Pipeline
**Innovation**: Vision-enabled AI for scientific literature digitization:

- **Publication Data Mining**: Automated extraction from nuclear physics papers, level schemes, and experimental tables
- **Image Processing**: Direct conversion of published figures to ENSDF-compliant data structures
- **Cross-Validation**: AI-assisted comparison between multiple experimental sources
- **Quality Control**: Systematic verification against nuclear systematics and selection rules

**Demonstrated Success**: Successfully extracted and validated data from 1984CA14 (81 resonance entries), 2025LiAA (115Sb compilation), and multiple PRC papers.

### 3. Format Compliance Automation
**Technical Achievement**: Zero-tolerance ENSDF formatting system:

- **Column Calibration**: Real-time 80-column validation with character-level precision
- **Energy Ordering**: Automated verification of ascending energy sequences for levels and transitions
- **Nuclear Notation**: Intelligent conversion of text to proper ENSDF symbols (superscripts, Greek letters, mathematical operators)
- **Error Prevention**: Pre-emptive detection and correction of common formatting mistakes

**Quantified Results**: Reduced formatting errors from ~30% (manual) to <1% (AI-assisted) across 83 evaluated datasets.

## Strategic AI/ML Expansion Opportunities - Where the Biggest Gains Await

### 1. HIGHEST IMPACT: Intelligent Data Evaluation and Cross-Validation
**Current Gap**: Manual comparison of experimental results requires expert knowledge and is time-intensive.

**AI/ML Solution**:
- **Automated Discrepancy Detection**: ML models trained on nuclear systematics to flag inconsistent experimental values
- **Weighted Average Calculations**: AI-optimized statistical treatment of conflicting measurements
- **Systematic Uncertainty Assessment**: Machine learning analysis of experimental method reliability
- **Real-time Literature Monitoring**: Automated scanning of new publications for relevant nuclear data

**Expected Impact**: 50-70% reduction in evaluation time while improving data consistency and reliability.

### 2. HIGH IMPACT: Predictive Nuclear Structure Models
**Current Process**: Evaluators manually estimate missing nuclear properties using neighboring nuclei.

**AI/ML Enhancement**:
- **Deep Learning Structure Prediction**: Neural networks trained on existing ENSDF database to predict missing levels, transitions, and decay properties
- **Uncertainty Quantification**: Bayesian approaches for reliable uncertainty estimates on predicted values
- **Experimental Design Optimization**: AI recommendations for measurements that would most improve nuclear structure knowledge
- **Mass Chain Consistency**: ML models ensuring systematic behavior across isotopic and isotonic chains

**Expected Benefit**: Dramatically improved adopted datasets with fewer "unknown" values and better-constrained nuclear properties.

### 3. MEDIUM-HIGH IMPACT: Automated Quality Assurance and Validation
**Current Challenge**: Manual checking of nuclear data against physical constraints and selection rules.

**AI/ML Advancement**:
- **Physics Constraint Validation**: Automated verification against conservation laws, selection rules, and nuclear models
- **Statistical Consistency Checks**: ML detection of outliers and statistically improbable values
- **Cross-Reference Validation**: AI comparison with complementary nuclear databases (RIPL, XUNDL, NSR)
- **Trend Analysis**: Machine learning identification of systematic errors in experimental techniques

**Projected Outcome**: Near-elimination of physics violations and statistical inconsistencies in evaluated data.

### 4. EMERGING OPPORTUNITY: Intelligent Experimental Data Integration
**Vision**: Real-time AI processing of FRIB experimental results for immediate ENSDF integration.

**AI/ML Framework**:
- **Live Data Stream Processing**: AI analysis of FRIB experiments as data is collected
- **Automated Preliminary Evaluation**: Real-time generation of preliminary nuclear structure assignments
- **Experiment-Theory Comparison**: AI-assisted comparison with shell model and ab initio predictions
- **Dynamic Database Updates**: Continuous integration of new experimental results into working evaluations

**Transformative Potential**: Reduction from years to months for new experimental data to appear in official evaluations.

## Technical Innovation Metrics and Community Impact

### Development Timeline
- **June 2025**: Initial GitHub Copilot integration for ENSDF formatting
- **July 2025**: FRIBND agent architecture deployment
- **August 2025**: Vision-enabled data extraction implementation
- **Present**: Full workflow automation for A=35 evaluation (83 datasets)

### Community Adoption
- **Open Source Platform**: All tools available via GitHub with comprehensive documentation
- **USNDP Integration**: Tools being evaluated for adoption across U.S. Nuclear Data Program centers
- **International Interest**: NSDD evaluators worldwide expressing interest in AI-assisted workflows
- **Training Materials**: LECM2025 presentation and tutorials prepared for community distribution

### Scientific Publications and Recognition
- **Methodology Paper**: In preparation for submission to Nuclear Data Sheets
- **Conference Presentations**: LECM2025 invited talk on AI-assisted nuclear data evaluation
- **Community Engagement**: Active collaboration with Berkeley (BEApR), ORNL (HFIR), and international evaluators

## Future Vision: Fully AI-Integrated Nuclear Data Ecosystem

The ultimate goal is a comprehensive AI/ML nuclear data ecosystem where:
1. **Experimental results** are automatically processed and preliminarily evaluated in real-time
2. **Literature mining** continuously updates nuclear databases with new published data
3. **Predictive models** fill gaps in nuclear knowledge with quantified uncertainties
4. **Quality assurance** is automated through physics-informed machine learning
5. **Community collaboration** is enhanced through shared AI tools and methodologies

This represents not just incremental improvement, but a fundamental transformation of how nuclear data evaluation is conducted in the 21st century, positioning DOE's nuclear data infrastructure as the global leader in AI-enhanced scientific databases.

## Resource Requirements for Full Implementation

### Near-term (1-2 years): $200K-300K
- Enhanced computational infrastructure for ML model training
- Specialized AI/ML personnel (1-2 postdocs/staff)
- Advanced software licensing and cloud computing resources

### Long-term (3-5 years): $500K-750K annually
- Dedicated AI/ML research group (3-4 personnel)
- High-performance computing resources for large-scale model training
- Community outreach and training program development
- Integration with national nuclear data infrastructure

**Return on Investment**: Conservative estimates suggest 3-5x improvement in evaluation efficiency and data quality, positioning U.S. nuclear data capabilities as the global standard.