-- For evtp_version
ALTER TABLE IF EXISTS evtp_version DROP COLUMN IF EXISTS vector;
DROP INDEX IF EXISTS gin_idx_evtp;
ALTER TABLE IF EXISTS evtp_version DROP COLUMN IF EXISTS vector_suggestion;
DROP INDEX IF EXISTS gin_idx_evtp_suggestion;
DROP TRIGGER IF EXISTS evtp_vector_trigger ON evtp_version;
DROP FUNCTION IF EXISTS update_evtp_vector();
DROP TRIGGER IF EXISTS evtp_vector_suggestion_trigger ON evtp_version;
DROP FUNCTION IF EXISTS update_evtp_vector_suggestion();

-- For gg
ALTER TABLE IF EXISTS gg DROP COLUMN IF EXISTS vector;
DROP INDEX IF EXISTS gin_idx_gg;
DROP TRIGGER IF EXISTS gg_vector_trigger ON gg;
DROP FUNCTION IF EXISTS update_gg_vector();

-- For oe
ALTER TABLE IF EXISTS oe DROP COLUMN IF EXISTS vector;
DROP INDEX IF EXISTS gin_idx_oe;
DROP TRIGGER IF EXISTS oe_vector_trigger ON oe;
DROP FUNCTION IF EXISTS update_oe_vector();

-- For oe_koepel
ALTER TABLE IF EXISTS oe_koepel DROP COLUMN IF EXISTS vector;
DROP INDEX IF EXISTS gin_idx_oe_koepel;
DROP TRIGGER IF EXISTS oe_koepel_vector_trigger ON oe;
DROP FUNCTION IF EXISTS update_oe_koepel_vector();
