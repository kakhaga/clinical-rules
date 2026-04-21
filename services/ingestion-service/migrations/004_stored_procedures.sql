-------------------------------------------------------------------------------
-- 1. PATIENTS
CREATE OR REPLACE PROCEDURE core.upsert_patients () LANGUAGE plpgsql AS $$
BEGIN
    INSERT INTO core.patients (
        external_patient_id, 
        first_name, 
        last_name, 
        date_of_birth, 
        gender, 
        phone, 
        language, 
        pcp_provider_id
    )
    SELECT DISTINCT ON (patient_id)
        r.patient_id, 
        r.first_name, 
        r.last_name, 
        CAST(r.date_of_birth AS DATE),
        r.gender, 
        r.phone, 
        r.language, 
        pr.id
    FROM raw.patients r
    LEFT JOIN core.providers pr ON r.pcp_provider_name = pr.provider_name
    ORDER BY patient_id, ingested_at DESC -- 👈 Take the newest one if there are duplicates
    ON CONFLICT (external_patient_id) 
    DO UPDATE SET 
        first_name = EXCLUDED.first_name,
        last_name = EXCLUDED.last_name,
        date_of_birth = EXCLUDED.date_of_birth,
        gender = EXCLUDED.gender,
        phone = EXCLUDED.phone,
        language = EXCLUDED.language,
        pcp_provider_id = EXCLUDED.pcp_provider_id,
        updated_at = NOW();
END;
$$;

-------------------------------------------------------------------------------
-- 2.a DIM ICD
CREATE OR REPLACE PROCEDURE core.upsert_dim_icd () LANGUAGE plpgsql AS $$
BEGIN
    INSERT INTO core.dim_icd (icd_code, icd_family, description)
    SELECT DISTINCT icd_code, LEFT(icd_code, 3), description
    FROM raw.diagnoses
    WHERE icd_code IS NOT NULL
    ON CONFLICT (icd_code) DO UPDATE SET
        icd_family = EXCLUDED.icd_family,
        description = EXCLUDED.description; -- Updates description if the standard changes
END;
$$;

-------------------------------------------------------------------------------
-- 2.b DIAGNOSES
CREATE OR REPLACE PROCEDURE core.upsert_diagnoses () LANGUAGE plpgsql AS $$
BEGIN
    INSERT INTO core.diagnoses (
        patient_id, 
        icd_code_ref, 
        diagnosed_date
    )
    SELECT 
        p.id, 
        i.icd_code,
        CAST(d.diagnosed_date AS DATE)
    FROM raw.diagnoses d
    JOIN core.patients p ON d.patient_id = p.external_patient_id
    JOIN core.dim_icd i ON d.icd_code = i.icd_code
    ON CONFLICT ON CONSTRAINT uniq_normalized_diagnosis
    DO NOTHING; -- Prevents duplicate diagnosis entries for same patient
END;
$$;

-------------------------------------------------------------------------------
-- 3.a DIM LAB TESTS
CREATE OR REPLACE PROCEDURE core.upsert_dim_lab_tests () LANGUAGE plpgsql AS $$
BEGIN
    INSERT INTO core.dim_lab_tests (test_name)
    SELECT DISTINCT test_name
    FROM raw.labs
    WHERE test_name IS NOT NULL
    ON CONFLICT (test_name) DO NOTHING;
END;
$$;

-------------------------------------------------------------------------------
-- 3.b LAB RESULTS
CREATE OR REPLACE PROCEDURE core.upsert_labs () LANGUAGE plpgsql AS $$
BEGIN
    INSERT INTO core.lab_results (patient_id, lab_test_id, result_value, result_date)
    SELECT 
        p.id, 
        lt.id, 
        CAST(r.result_value AS NUMERIC(10,2)), 
        CAST(r.result_date AS DATE)
    FROM raw.labs r
    JOIN core.patients p ON r.patient_id = p.external_patient_id
    JOIN core.dim_lab_tests lt ON r.test_name = lt.test_name
    -- Logic: Don't insert the exact same lab for the same patient on the same day
    ON CONFLICT ON CONSTRAINT uniq_normalized_lab
    DO NOTHING; 
END;
$$;

-------------------------------------------------------------------------------
-- 4.a PROVIDERS
CREATE OR REPLACE PROCEDURE core.upsert_providers () LANGUAGE plpgsql AS $$
BEGIN
    -- Insert distinct providers found in the raw encounter data
    INSERT INTO core.providers (provider_name, specialty)
    SELECT DISTINCT provider_name, specialty
    FROM raw.encounters
    WHERE provider_name IS NOT NULL AND specialty IS NOT NULL
    ON CONFLICT ON CONSTRAINT uniq_provider_spec DO NOTHING;
END;
$$;

-------------------------------------------------------------------------------
-- 4.b ENCOUNTERS
CREATE OR REPLACE PROCEDURE core.upsert_encounters () LANGUAGE plpgsql AS $$
BEGIN
    INSERT INTO core.encounters (
        patient_id, 
        provider_id, 
        encounter_date
    )
    SELECT 
        p.id, 
        pr.id, 
        CAST(e.encounter_date AS DATE)
    FROM raw.encounters e
    JOIN core.patients p 
        ON e.patient_id = p.external_patient_id
    JOIN core.providers pr ON e.provider_name = pr.provider_name 
                           AND e.specialty = pr.specialty
    ON CONFLICT ON CONSTRAINT uniq_normalized_encounter
    DO NOTHING;
END;
$$;

--=============================================================================
-- 1. Full ETL raw -> core
CREATE OR REPLACE PROCEDURE core.run_full_etl () LANGUAGE plpgsql AS $$
BEGIN
    -- 1. Reference Data & Master Dimensions
    -- We process providers first so patients and encounters can link to them
    CALL core.upsert_providers(); 
    CALL core.upsert_dim_icd();         -- Standardize disease codes
    CALL core.upsert_dim_lab_tests();   -- Standardize lab names

    -- 2. Identity Data
    CALL core.upsert_patients(); -- Now links to providers

    -- 3. Transactional Facts
    CALL core.upsert_encounters();
    CALL core.upsert_diagnoses();
    CALL core.upsert_labs();

    -- 4. Clean Staging
    TRUNCATE TABLE raw.patients, raw.diagnoses, raw.labs, raw.encounters;

    -- Step 3: Logging (Optional)
    RAISE NOTICE 'Full ETL cycle for patients, diagnoses, labs, and encounters finished.';
END;
$$;