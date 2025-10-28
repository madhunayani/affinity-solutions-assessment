-- ==============================================================================
-- AFFINITY SOLUTIONS ASSIGNMENT - SQL QUERIES
-- Rfam Database Analysis
-- Author: Madhu Nayani
-- Date: October 27-28, 2025
-- ==============================================================================

-- ==============================================================================
-- QUESTION 1a: How many types of tigers in taxonomy table?
-- ==============================================================================

SELECT COUNT(*) as tiger_count
FROM taxonomy
WHERE species LIKE '%Panthera tigris%';

-- RESULT: 8 tiger types found


-- ==============================================================================
-- QUESTION 1b: What is the ncbi_id of the Sumatran Tiger?
-- ==============================================================================

SELECT ncbi_id, species, tax_string
FROM taxonomy
WHERE species LIKE '%Panthera tigris sumatrae%'
   OR species = 'Panthera tigris sumatrae';

-- RESULT: 
-- ncbi_id: 9695
-- species: Panthera tigris sumatrae (Sumatran tiger)


-- ==============================================================================
-- QUESTION 2: Find all columns that connect tables (Foreign Keys)
-- ==============================================================================

-- Key relationships identified in Rfam database:

-- 1. taxonomy.ncbi_id (PRIMARY KEY)
--    Referenced by: rfamseq.ncbi_id, genseq.ncbi_id

-- 2. rfamseq.rfamseq_acc (PRIMARY KEY)
--    Referenced by: full_region.rfamseq_acc, seed_region.rfamseq_acc

-- 3. family.rfam_acc (PRIMARY KEY)
--    Referenced by: full_region.rfam_acc, seed_region.rfam_acc, family_ncbi.rfam_acc

-- Query to find common columns across tables:
SELECT 
    t1.TABLE_NAME as table_name,
    t1.COLUMN_NAME as column_name,
    GROUP_CONCAT(DISTINCT t2.TABLE_NAME SEPARATOR ', ') as connected_to_tables,
    COUNT(DISTINCT t2.TABLE_NAME) as connection_count
FROM 
    INFORMATION_SCHEMA.COLUMNS t1
JOIN 
    INFORMATION_SCHEMA.COLUMNS t2 
    ON t1.COLUMN_NAME = t2.COLUMN_NAME 
    AND t1.TABLE_NAME != t2.TABLE_NAME
WHERE 
    t1.TABLE_SCHEMA = 'Rfam' 
    AND t2.TABLE_SCHEMA = 'Rfam'
GROUP BY 
    t1.TABLE_NAME, t1.COLUMN_NAME
HAVING 
    connection_count >= 1
ORDER BY 
    connection_count DESC, t1.TABLE_NAME
LIMIT 30;


-- ==============================================================================
-- QUESTION 3: Which type of rice has the longest DNA sequence?
-- ==============================================================================

SELECT 
    t.species,
    t.ncbi_id,
    MAX(r.length) as max_sequence_length,
    r.description
FROM 
    taxonomy t
JOIN 
    rfamseq r ON t.ncbi_id = r.ncbi_id
WHERE 
    t.species LIKE '%Oryza sativa%'
    OR t.species LIKE '%Oryza%'
GROUP BY
    t.species, t.ncbi_id, r.description
ORDER BY 
    max_sequence_length DESC
LIMIT 1;

-- NOTE: This query may timeout on the public Rfam server due to large table size


-- ==============================================================================
-- QUESTION 4: Paginated query - Page 9 (15 results per page)
-- ==============================================================================

-- Requirements:
-- - Families with DNA sequence length > 1,000,000
-- - Order by length descending
-- - Page 9 with 15 results per page
-- - Show: family accession ID, family name, max length

-- Pagination calculation:
-- Page 9, 15 results per page
-- OFFSET = (9 - 1) × 15 = 120
-- LIMIT = 15

SELECT 
    f.rfam_acc AS family_accession_id,
    f.rfam_id AS family_name,
    MAX(r.length) AS max_length
FROM 
    family f
JOIN 
    full_region fr ON f.rfam_acc = fr.rfam_acc
JOIN 
    rfamseq r ON fr.rfamseq_acc = r.rfamseq_acc
GROUP BY 
    f.rfam_acc, f.rfam_id
HAVING 
    MAX(r.length) > 1000000
ORDER BY 
    max_length DESC
LIMIT 15 OFFSET 120;

-- ==============================================================================
-- END OF QUERIES
-- ==============================================================================
