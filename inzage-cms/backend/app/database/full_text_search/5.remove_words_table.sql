-- Drop the words table and related functions/triggers
DROP TABLE IF EXISTS words;
DROP FUNCTION IF EXISTS update_words_evtp();
DROP FUNCTION IF EXISTS update_words_gg();
DROP FUNCTION IF EXISTS update_words_oe();
DROP FUNCTION IF EXISTS update_words_oe_koepel();