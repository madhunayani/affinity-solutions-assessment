# In Git Bash
cat > README.md << 'EOF'
# Phase 3: AMFI NAV Data Extraction Shell Script

## Overview
Unix shell script to extract mutual fund NAV (Net Asset Value) data from AMFI India website.

## Data Source
**URL**: https://www.amfiindia.com/spages/NAVAll.txt

## Execution Results
- **Downloaded**: 17,250 lines of raw data
- **Extracted**: 14,058 mutual fund scheme records
- **Output Formats**: TSV and JSON

## Files

### Scripts
- `extract_nav.sh` - Main Bash extraction script

### Output Files
- `nav_output.tsv` - Tab-Separated Values format (14,059 lines including header)
- `nav_output.json` - JSON format (1.6 MB)

### Documentation
- `README.md` - This file

## Requirements
- Bash shell (Git Bash on Windows, native on Linux/Mac)
- `curl` - For downloading data
- `awk` - For text processing

## Usage

### On Windows (Git Bash):
