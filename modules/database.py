import sqlite3
import pandas as pd
from datetime import datetime

DB_FILE = "threat_registry.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # Create the unified threats table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS threat_registry (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            threat_type TEXT NOT NULL,
            indicator TEXT NOT NULL,
            risk_level TEXT NOT NULL,
            details TEXT,
            evidence_hash TEXT NOT NULL
        )
    """)
    
    # Create the dashboard stats table (to be updated dynamically by n8n agents)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS dashboard_stats (
            key TEXT PRIMARY KEY,
            value TEXT NOT NULL
        )
    """)
    
    # Insert some high-fidelity mock records if table is brand new/empty
    cursor.execute("SELECT COUNT(*) FROM threat_registry")
    if cursor.fetchone()[0] == 0:
        mock_records = [
            (
                datetime(2026, 7, 5, 10, 15).strftime("%Y-%m-%d %H:%M:%S"),
                "Digital Arrest",
                "+91 91234-56789",
                "RED",
                "CBI Impersonation claiming drugs in courier package",
                "a1b2c3d4e5f67890abcdef1234567890abcdef1234567890abcdef12345678"
            ),
            (
                datetime(2026, 7, 6, 14, 20).strftime("%Y-%m-%d %H:%M:%S"),
                "Phishing Email",
                "refund-verify@incometax-gov-in.info",
                "RED",
                "Tax refund scam proposing credential validation link",
                "f6e5d4c3b2a10987abcdefabcdefabcdefabcdefabcdefabcdefabcdefabcd"
            ),
            (
                datetime(2026, 7, 6, 16, 45).strftime("%Y-%m-%d %H:%M:%S"),
                "Counterfeit Currency",
                "Rs 500 Note Signature #9942",
                "RED",
                "Fake note detected by Pos/Scanner (GLCM variance fail)",
                "9876543210abcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcd"
            ),
            (
                datetime(2026, 7, 7, 9, 30).strftime("%Y-%m-%d %H:%M:%S"),
                "SIEM Intrusion",
                "196.22.45.109",
                "AMBER",
                "SSH Brute Force attempts matched in firewall log correlation",
                "bc1234567890abcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefab"
            )
        ]
        cursor.executemany("""
            INSERT INTO threat_registry (timestamp, threat_type, indicator, risk_level, details, evidence_hash)
            VALUES (?, ?, ?, ?, ?, ?)
        """, mock_records)
        
    # Seed dashboard stats if empty
    cursor.execute("SELECT COUNT(*) FROM dashboard_stats")
    if cursor.fetchone()[0] == 0:
        default_stats = [
            ("active_scams", "1550000"),
            ("scam_source", "MHA / I4C Portal Reports"),
            ("seized_notes", "225769"),
            ("notes_source", "RBI Annual Report 2022-23"),
            ("mule_accounts", "340000"),
            ("mule_source", "MHA / I4C Bulletins"),
            ("intercepted_voip", "17000000"),
            ("voip_source", "DoT / Sanchar Saathi"),
            ("last_updated", "2024")
        ]
        cursor.executemany("""
            INSERT OR REPLACE INTO dashboard_stats (key, value)
            VALUES (?, ?)
        """, default_stats)
        
    conn.commit()
    conn.close()

def log_threat_to_db(threat_type, indicator, risk_level, details, evidence_hash):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    cursor.execute("""
        INSERT INTO threat_registry (timestamp, threat_type, indicator, risk_level, details, evidence_hash)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (timestamp, threat_type, indicator, risk_level, details, evidence_hash))
    
    conn.commit()
    conn.close()

def get_logged_threats():
    conn = sqlite3.connect(DB_FILE)
    df = pd.read_sql_query("SELECT * FROM threat_registry ORDER BY id DESC", conn)
    conn.close()
    return df

def search_threats(query_str):
    conn = sqlite3.connect(DB_FILE)
    # Using SQL Parameter binding for security
    query = f"%{query_str}%"
    df = pd.read_sql_query("""
        SELECT * FROM threat_registry 
        WHERE indicator LIKE ? OR threat_type LIKE ? OR details LIKE ? 
        ORDER BY id DESC
    """, conn, params=(query, query, query))
    conn.close()
    return df

def get_dashboard_stats():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT key, value FROM dashboard_stats")
    rows = cursor.fetchall()
    conn.close()
    
    # Convert list of tuples to key-value dict
    stats_dict = {}
    for r in rows:
        # Convert numeric strings to actual numbers if possible
        val = r[1]
        if val.isdigit():
            stats_dict[r[0]] = int(val)
        else:
            stats_dict[r[0]] = val
    return stats_dict

def update_dashboard_stat(key, value):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT OR REPLACE INTO dashboard_stats (key, value)
        VALUES (?, ?)
    """, (key, str(value)))
    conn.commit()
    conn.close()
