import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "jalrakshak.db")

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.executescript("""
    CREATE TABLE IF NOT EXISTS assets (
        id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        asset_type TEXT NOT NULL,
        location TEXT NOT NULL,
        baseline_vib_rms REAL DEFAULT 1.0,
        baseline_current_rms REAL DEFAULT 4.2,
        baseline_temp REAL DEFAULT 42.0,
        baseline_flow REAL DEFAULT 85.0,
        status TEXT DEFAULT 'HEALTHY',
        last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE IF NOT EXISTS sensor_readings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        asset_id TEXT NOT NULL,
        vibration_rms REAL,
        crest_factor REAL,
        motor_current REAL,
        temperature REAL,
        flow_rate REAL,
        tank_level REAL,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(asset_id) REFERENCES assets(id)
    );

    CREATE TABLE IF NOT EXISTS health_assessments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        asset_id TEXT NOT NULL,
        health_score REAL,
        predicted_state TEXT,
        anomaly_score REAL,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(asset_id) REFERENCES assets(id)
    );

    CREATE TABLE IF NOT EXISTS water_reliability_snapshots (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        asset_id TEXT NOT NULL,
        pump_health REAL,
        flow_efficiency REAL,
        tank_recovery_factor REAL,
        water_reliability_score REAL,
        risk_level TEXT,
        maintenance_priority TEXT,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(asset_id) REFERENCES assets(id)
    );

    CREATE TABLE IF NOT EXISTS maintenance_recommendations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        asset_id TEXT NOT NULL,
        risk_level TEXT,
        urgency TEXT,
        reason TEXT,
        recommended_action TEXT,
        est_window_hours_min INTEGER,
        est_window_hours_max INTEGER,
        status TEXT DEFAULT 'PENDING',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(asset_id) REFERENCES assets(id)
    );

    CREATE TABLE IF NOT EXISTS mesh_nodes (
        node_id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        node_type TEXT NOT NULL,
        health_score INTEGER,
        status TEXT,
        last_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        hops INTEGER DEFAULT 1,
        rssi INTEGER DEFAULT -65
    );

    CREATE TABLE IF NOT EXISTS events (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        asset_id TEXT,
        event_type TEXT,
        severity TEXT,
        message TEXT,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    # Seed initial assets if empty
    cursor.execute("SELECT COUNT(*) as cnt FROM assets")
    if cursor.fetchone()["cnt"] == 0:
        cursor.executescript("""
        INSERT INTO assets (id, name, asset_type, location, status) VALUES
        ('PUMP-01', 'Primary Borewell Pump A', 'PUMP', 'North Wellfield, Sector 1', 'HEALTHY'),
        ('PUMP-02', 'Solar Submersible Pump B', 'PUMP', 'East Agricultural Line', 'MONITOR'),
        ('PUMP-03', 'Centrifugal Booster Pump C', 'PUMP', 'Central Distribution Hub', 'DEGRADING'),
        ('PUMP-04', 'High-Pressure Booster D', 'PUMP', 'Hilltop Reservoir Feed', 'CRITICAL'),
        ('TANK-01', 'Community Overhead Tank 1', 'TANK', 'Main Village Square', 'HEALTHY');

        INSERT INTO mesh_nodes (node_id, name, node_type, health_score, status, hops, rssi) VALUES
        ('NODE-P01', 'Pump-01 (nRF54LM20)', 'PUMP', 95, 'CONNECTED', 1, -58),
        ('NODE-P02', 'Pump-02 (nRF54LM20)', 'PUMP', 82, 'CONNECTED', 2, -72),
        ('NODE-P03', 'Pump-03 (nRF54LM20)', 'PUMP', 54, 'CONNECTED', 1, -64),
        ('NODE-P04', 'Pump-04 (nRF54LM20)', 'PUMP', 31, 'WARNING', 3, -84),
        ('NODE-T01', 'Tank-01 Telemetry Node', 'TANK', 92, 'CONNECTED', 1, -60),
        ('GW-TECH01', 'Technician Handheld Gateway', 'GATEWAY', 100, 'ONLINE', 0, -45);

        INSERT INTO events (asset_id, event_type, severity, message) VALUES
        ('PUMP-03', 'ANOMALY_DETECTED', 'WARNING', 'Vibration RMS increased +28% above baseline.'),
        ('PUMP-04', 'CRITICAL_ALARM', 'CRITICAL', 'Motor temperature exceeded 68°C. Immediate inspection needed.');
        """)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    print("[Database] SQLite database initialized successfully.")
