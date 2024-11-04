-- Dutch abbreviation configuration
CREATE TEXT SEARCH DICTIONARY dutch_syn_thesaurus (
    TEMPLATE = thesaurus,
		DictFile = nl_synonyms_inzage,
		Dictionary = pg_catalog.dutch_stem
);

ALTER TEXT SEARCH CONFIGURATION NLD
	ALTER MAPPING FOR asciiword, asciihword, hword_asciipart, word, hword, hword_part
	WITH dutch_syn_thesaurus, dutch_stem, dutch_opentaal_hunspell;

-- Drop the existing index
DROP INDEX IF EXISTS gin_idx_evtp;
DROP INDEX IF EXISTS gin_idx_evtp_suggestion;
DROP INDEX IF EXISTS gin_idx_gg;
DROP INDEX IF EXISTS gin_idx_oe;
DROP INDEX IF EXISTS gin_idx_oe_koepel;

-- Recreate the index
CREATE INDEX gin_idx_evtp ON evtp_version USING gin (vector);
CREATE INDEX gin_idx_evtp_suggestion ON evtp_version USING gin (vector_suggestion);
CREATE INDEX gin_idx_gg ON gg USING gin (vector);
CREATE INDEX gin_idx_oe ON oe USING gin (vector);
CREATE INDEX gin_idx_oe_koepel ON oe USING gin (vector);

-- -- Perform tsvector generation on data with thesaurus knowledge of abbreviation
-- evtp_version
UPDATE evtp_version SET vector = to_tsvector('NLD',
    COALESCE(evtp_nm,'') || ' ' || COALESCE(aanleiding,'') || ' ' || COALESCE(omschrijving,'') || ' ' || 
    COALESCE(gebr_dl,''));

UPDATE evtp_version SET vector_suggestion = to_tsvector('NLD',
    COALESCE(evtp_nm,''));

ANALYZE evtp_version;

-- gg
UPDATE gg SET vector = to_tsvector('NLD',
		COALESCE(omschrijving,''));

ANALYZE gg;

-- oe
UPDATE oe SET vector = to_tsvector('NLD',
		COALESCE(naam_spraakgbr,'') || ' ' || COALESCE(naam_officieel,'') || ' ' || COALESCE(afko,''));

ANALYZE oe;

-- oe_koepel
UPDATE oe_koepel SET vector = to_tsvector('NLD',
		COALESCE(titel,'') || ' ' || COALESCE(omschrijving,''));

ANALYZE oe_koepel;