-------------------------------------------------------------------------------
-- 0. FILE REGISTRY
CREATE TABLE IF NOT EXISTS raw.file_registry (
    filename TEXT PRIMARY KEY,
    last_md5 TEXT NOT NULL,
    processed_at TIMESTAMP DEFAULT NOW()
);

-------------------------------------------------------------------------------
-- 1. PATIENTS
CREATE TABLE IF NOT EXISTS raw.patients (
    patient_id TEXT,
    first_name TEXT,
    last_name TEXT,
    date_of_birth TEXT,
    gender TEXT,
    phone TEXT,
    language TEXT,
    pcp_provider_name TEXT,
    ingested_at TIMESTAMP DEFAULT NOW()
);

-------------------------------------------------------------------------------
-- 2. DIAGNOSES
CREATE TABLE IF NOT EXISTS raw.diagnoses (
    patient_id TEXT,
    icd_code TEXT,
    description TEXT,
    diagnosed_date TEXT,
    ingested_at TIMESTAMP DEFAULT NOW()
);

-------------------------------------------------------------------------------
-- 3. LAB RESULTS
CREATE TABLE IF NOT EXISTS raw.labs (
    patient_id TEXT,
    test_name TEXT,
    result_value TEXT,
    result_date TEXT,
    ingested_at TIMESTAMP DEFAULT NOW()
);

-------------------------------------------------------------------------------
-- 4. ENCOUNTERS
CREATE TABLE IF NOT EXISTS raw.encounters (
    patient_id TEXT,
    specialty TEXT,
    encounter_date TEXT,
    provider_name TEXT,
    ingested_at TIMESTAMP DEFAULT NOW()
);
