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
chmod +x extract_nav.sh
./extract_nav.sh


### On Linux/Mac:
chmod +x extract_nav.sh
./extract_nav.sh


## Output Format

### TSV (nav_output.tsv):
Scheme Name Net Asset Value
Aditya Birla Sun Life Banking & PSU Debt Fund - DIRECT - IDCW 109.5673
Aditya Birla Sun Life Banking & PSU Debt Fund - DIRECT - MONTHLY IDCW 117.9433
...


### JSON (nav_output.json):
[
{
"scheme_name": "Aditya Birla Sun Life Banking & PSU Debt Fund - DIRECT - IDCW",
"nav": "109.5673"
},
{
"scheme_name": "Aditya Birla Sun Life Banking & PSU Debt Fund - DIRECT - MONTHLY IDCW",
"nav": "117.9433"
}
]


## Script Features
1. Downloads latest NAV data from AMFI India
2. Parses semicolon-delimited format
3. Extracts only Scheme Name and NAV fields
4. Filters out headers and category dividers
5. Outputs data in both TSV and JSON formats
6. Displays summary statistics and sample data

## Data Processing Logic

### Input Format (from AMFI)
Scheme Code;ISIN1;ISIN2;Scheme Name;NAV;Date


### Extraction Process
1. Split by semicolon (`;`) delimiter
2. Extract field 4 (Scheme Name) and field 5 (NAV)
3. Remove whitespace and special characters
4. Filter out header rows and category labels
5. Export to TSV and JSON

## Why JSON Over TSV?

### Advantages of JSON:
- **Structured**: Hierarchical data representation
- **Type-safe**: Can specify data types (string, number, boolean)
- **Extensible**: Easy to add nested objects or arrays
- **API-friendly**: Standard format for web APIs
- **Language support**: Native parsing in JavaScript, Python, etc.
- **Self-documenting**: Field names included with data

### When TSV is Better:
- **Simplicity**: Easy to view in text editors
- **Spreadsheet compatibility**: Direct import to Excel/Google Sheets
- **File size**: Smaller than JSON for simple tabular data
- **Performance**: Faster to parse for very large datasets
- **Human readable**: Simple columnar format

### Recommendation
- Use **JSON** for applications, APIs, and web services
- Use **TSV** for data analysis, Excel import, and manual review

## Sample Schemes Extracted
- Aditya Birla Sun Life Banking & PSU Debt Fund (multiple plans)
- HDFC Equity Funds
- ICICI Prudential Schemes
- SBI Mutual Funds
- And 14,000+ more schemes

## Technical Details

### Bash Script Components:
- `curl -L -s -A "Mozilla/5.0"` - Download with user agent and follow redirects
- `awk -F';'` - Process semicolon-delimited data
- `gsub()` - Remove whitespace and special characters
- `column -t` - Format sample output display

### Error Handling:
- Checks if download succeeded
- Validates file existence
- Displays line counts and file sizes
- Cleans up temporary files

## Challenges & Solutions

### Challenge 1: Initial Download Failure
**Problem**: `curl` only downloaded 1 line initially
**Solution**: Added `-L` flag to follow redirects and `-A` flag for user agent

### Challenge 2: Data Format Parsing
**Problem**: AWK field positions needed adjustment
**Solution**: Analyzed AMFI file format, identified correct field indices (4 and 5)

### Challenge 3: Header/Category Filtering
**Problem**: Raw data includes category headers and dividers
**Solution**: Added regex filters to exclude non-scheme rows

## Execution Time
- Download: ~2 seconds
- Processing: ~1 second
- Total: ~3 seconds

## Author
Madhu - October 27, 2025

## Assignment Context
This script was developed as part of the Affinity Solutions technical assessment (Phase 3), demonstrating proficiency in:
- Unix shell scripting
- Data extraction and transformation
- Text processing with awk
- Multiple output format generation
EOF

# Verify README created
cat README.md

Final Git Push for Phase 3

# In Git Bash
cd /d/MERN\ Stack\ Projects/affinity-assignment

# Add Phase 3 files
git add phase-3-shell-script/

# Commit
git commit -m "Complete Phase 3: AMFI NAV data extraction shell script

- Bash script to download and parse AMFI mutual fund NAV data
- Successfully extracted 14,058 scheme records
- Dual output format: TSV (14K lines) and JSON (1.6 MB)
- Comprehensive documentation and format comparison
- Execution time: ~3 seconds"

# Push
git push origin main
