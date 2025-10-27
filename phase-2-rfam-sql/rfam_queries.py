"""
Rfam Database Exploration
Author: Madhu
Date: October 27, 2025

Script to connect to Rfam public database and explore schema
"""

import mysql.connector
from mysql.connector import Error

# Connection configuration
CONFIG = {
    'host': 'mysql-rfam-public.ebi.ac.uk',
    'user': 'rfamro',
    'password': '',  # No password required
    'port': 4497,
    'database': 'Rfam'
}

def connect_to_rfam():
    """Establish connection to Rfam database"""
    try:
        connection = mysql.connector.connect(**CONFIG)
        if connection.is_connected():
            db_info = connection.get_server_info()
            print(f"✓ Connected to Rfam MySQL Server version {db_info}")
            return connection
    except Error as e:
        print(f"❌ Error connecting to MySQL: {e}")
        return None

def execute_query(connection, query, description="Query"):
    """Execute SQL query and display results"""
    try:
        cursor = connection.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        
        print(f"\n{'='*80}")
        print(f"{description}")
        print(f"{'='*80}")
        print(f"Columns: {', '.join(columns)}")
        print(f"Results: {len(results)} rows\n")
        
        for row in results[:10]:  # Show first 10 rows
            print(row)
        
        if len(results) > 10:
            print(f"\n... and {len(results) - 10} more rows")
        
        cursor.close()
        return results
        
    except Error as e:
        print(f"❌ Error executing query: {e}")
        return None

def explore_schema(connection):
    """Explore database schema"""
    
    # Show all tables
    query = "SHOW TABLES"
    execute_query(connection, query, "Available Tables in Rfam Database")
    
    # Describe taxonomy table
    query = "DESCRIBE taxonomy"
    execute_query(connection, query, "Taxonomy Table Structure")
    
    # Describe rfamseq table
    query = "DESCRIBE rfamseq"
    execute_query(connection, query, "Rfamseq Table Structure")
    
    # Describe family table
    query = "DESCRIBE family"
    execute_query(connection, query, "Family Table Structure")

if __name__ == "__main__":
    print("="*80)
    print("RFAM DATABASE EXPLORER")
    print("="*80)
    
    conn = connect_to_rfam()
    
    if conn:
        explore_schema(conn)
        conn.close()
        print("\n✓ Connection closed")
