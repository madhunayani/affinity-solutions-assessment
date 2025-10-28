#!/bin/bash

###############################################################################
# AMFI NAV Data Extractor - FIXED VERSION
# Author: Madhu
# Date: October 27, 2025
###############################################################################

# Configuration
URL="https://www.amfiindia.com/spages/NAVAll.txt"
OUTPUT_TSV="nav_output.tsv"
OUTPUT_JSON="nav_output.json"

echo "=========================================="
echo "AMFI NAV Data Extraction Script"
echo "=========================================="
echo ""

# Step 1: Download with proper headers
echo "[1/4] Downloading NAV data from AMFI..."
curl -L -s -A "Mozilla/5.0" "$URL" -o nav_raw.txt

if [ ! -f nav_raw.txt ]; then
    echo "❌ Error: Failed to download data"
    exit 1
fi

echo "✓ Download complete ($(wc -l < nav_raw.txt) lines)"

# Step 2: Extract Scheme Name and NAV
echo ""
echo "[2/4] Extracting Scheme Name and Net Asset Value..."

# Create TSV header
echo -e "Scheme Name\tNet Asset Value" > "$OUTPUT_TSV"

# Process the file
# Format in file: Scheme Code;ISIN1;ISIN2;Scheme Name;NAV;Date
awk -F';' '
    NF >= 5 && $4 != "" && $4 != "Scheme Name" && $5 != "" && $5 != "Net Asset Value" {
        # Field 4: Scheme Name
        # Field 5: NAV
        scheme_name = $4
        nav_value = $5
        
        # Remove leading/trailing whitespace
        gsub(/^[ \t\r\n]+|[ \t\r\n]+$/, "", scheme_name)
        gsub(/^[ \t\r\n]+|[ \t\r\n]+$/, "", nav_value)
        
        # Skip empty or header lines
        if (scheme_name != "" && nav_value != "" && scheme_name !~ /^Open Ended/ && scheme_name !~ /Mutual Fund$/) {
            # Print as TSV
            print scheme_name "\t" nav_value
        }
    }
' nav_raw.txt >> "$OUTPUT_TSV"

line_count=$(wc -l < "$OUTPUT_TSV")
echo "✓ Extracted $((line_count - 1)) scheme records"

# Step 3: Create JSON output
echo ""
echo "[3/4] Converting to JSON format..."

# Create JSON structure
echo "[" > "$OUTPUT_JSON"

first_line=1
awk -F'\t' '
    NR > 1 {  # Skip header
        if (first_line == 0) print ","  # Add comma for previous entry
        first_line = 0
        
        scheme = $1
        nav = $2
        
        # Escape special characters in JSON
        gsub(/"/, "\\\"", scheme)
        gsub(/\\/, "\\\\", scheme)
        
        printf "  {\n"
        printf "    \"scheme_name\": \"%s\",\n", scheme
        printf "    \"nav\": \"%s\"\n", nav
        printf "  }"
    }
' first_line=1 "$OUTPUT_TSV" >> "$OUTPUT_JSON"

echo "" >> "$OUTPUT_JSON"
echo "]" >> "$OUTPUT_JSON"

echo "✓ JSON conversion complete"

# Step 4: Display summary
echo ""
echo "[4/4] Summary"
echo "=========================================="
echo "Files created:"
echo "  - $OUTPUT_TSV ($(wc -l < "$OUTPUT_TSV") lines)"
echo "  - $OUTPUT_JSON ($(wc -c < "$OUTPUT_JSON") bytes)"
echo ""
echo "Sample data (first 10 schemes):"
head -n 11 "$OUTPUT_TSV" | column -t -s $'\t'

echo ""
echo "✓ Extraction complete!"
echo "=========================================="

# Cleanup
rm -f nav_raw.txt
