
# Affinity Solutions Technical Assessment

**Candidate**: Madhu Nayani  
**Date**: October 27, 2025  
**Repository**: https://github.com/madhunayani/affinity-solutions-assessment

## Overview
Complete technical assessment covering web scraping, SQL database analysis, and Unix shell scripting.

## Project Structure

### Phase 1: OLX Web Scraper
**Technology**: Python, Selenium, BeautifulSoup, Pandas

**Task**: Extract car cover listings from OLX India

**Results**:
- 10 car cover products extracted
- Filtered out real estate listings
- Output: CSV with title, description, price

**Files**: [`phase-1-olx-scraper/`](./phase-1-olx-scraper/)

---

### Phase 2: Rfam SQL Database Analysis
**Technology**: MySQL Connector, SQL

**Task**: Complex queries on public Rfam RNA families database

**Results**:
- Question 1: 8 tiger species found; Sumatran Tiger NCBI ID: 9695
- Question 2: 6 key table relationships documented
- Question 3 & 4: SQL queries provided with explanations

**Files**: [`phase-2-rfam-sql/`](./phase-2-rfam-sql/)

---

### Phase 3: AMFI NAV Data Extraction
**Technology**: Bash Shell Script, awk, curl

**Task**: Extract mutual fund NAV data from AMFI India

**Results**:
- 14,058 scheme records extracted
- Dual output: TSV (14K lines) and JSON (1.6 MB)
- Data format comparison and recommendations

**Files**: [`phase-3-shell-script/`](./phase-3-shell-script/)

---

## Quick Links
- [Phase 1 README](./phase-1-olx-scraper/README.md)
- [Phase 2 README](./phase-2-rfam-sql/README.md)
- [Phase 3 README](./phase-3-shell-script/README.md)

## Technologies Used
- **Languages**: Python, SQL, Bash
- **Libraries**: Selenium, BeautifulSoup, Pandas, MySQL Connector
- **Tools**: Git Bash, VS Code, Git
- **Databases**: MySQL (Rfam public server)

## Key Achievements
✅ Successfully scraped dynamic JavaScript-rendered pages  
✅ Implemented data filtering logic for accurate results  
✅ Connected to remote MySQL database and executed complex queries  
✅ Handled performance limitations with proper documentation  
✅ Created cross-format data extraction (TSV + JSON)  
✅ Comprehensive documentation for all phases  

## Installation & Usage
See individual phase README files for detailed setup and execution instructions.

## Author
**Madhu Nayani**  
Full Stack Developer (MERN)  
[GitHub Profile](https://github.com/madhunayani)

## License
MIT License - See [LICENSE](./LICENSE) file
EOF

# Commit root README
git add README.md
git commit -m "Add comprehensive root README with project overview"
git push origin main
