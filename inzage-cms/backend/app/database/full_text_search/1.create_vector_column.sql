-- For evtp_version table
ALTER TABLE IF EXISTS evtp_version
ADD COLUMN IF NOT EXISTS vector tsvector;

ALTER TABLE IF EXISTS evtp_version
ADD COLUMN IF NOT EXISTS vector_suggestion tsvector;

UPDATE evtp_version SET vector = to_tsvector('NLD',
    COALESCE(evtp_nm,'') || ' ' || COALESCE(aanleiding,'') || ' ' || COALESCE(omschrijving,'') || ' ' ||
    COALESCE(gebr_dl,''));

UPDATE evtp_version SET vector_suggestion = to_tsvector('NLD',
    COALESCE(evtp_nm,''));

CREATE INDEX IF NOT EXISTS gin_idx_evtp ON evtp_version USING gin (vector);

CREATE INDEX IF NOT EXISTS gin_idx_evtp_suggestion ON evtp_version USING gin (vector_suggestion);

CREATE OR REPLACE FUNCTION update_evtp_vector() RETURNS TRIGGER AS $$
BEGIN
  NEW.vector :=
    to_tsvector('NLD', COALESCE(NEW.evtp_nm,'') || ' ' || COALESCE(NEW.aanleiding,'') || ' ' || COALESCE(NEW.omschrijving,'') || ' ' ||
    COALESCE(NEW.gebr_dl,''));
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER evtp_vector_trigger 
BEFORE INSERT OR UPDATE ON evtp_version 
FOR EACH ROW EXECUTE FUNCTION update_evtp_vector();

CREATE OR REPLACE FUNCTION update_evtp_vector_suggestion() RETURNS TRIGGER AS $$
BEGIN
  NEW.vector_suggestion :=
    to_tsvector('NLD', COALESCE(NEW.evtp_nm,''));
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER evtp_vector_suggestion_trigger 
BEFORE INSERT OR UPDATE ON evtp_version 
FOR EACH ROW EXECUTE FUNCTION update_evtp_vector_suggestion();

-- For gg table
ALTER TABLE IF EXISTS gg
ADD COLUMN IF NOT EXISTS vector tsvector;

UPDATE gg SET vector = to_tsvector('NLD',
    COALESCE(omschrijving,''));

CREATE INDEX IF NOT EXISTS gin_idx_gg ON gg USING gin (vector);

CREATE OR REPLACE FUNCTION update_gg_vector() RETURNS TRIGGER AS $$
BEGIN
  NEW.vector :=
    to_tsvector('NLD', COALESCE(NEW.omschrijving,''));
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER gg_vector_trigger 
BEFORE INSERT OR UPDATE ON gg 
FOR EACH ROW EXECUTE FUNCTION update_gg_vector();

-- For oe table
ALTER TABLE IF EXISTS oe
ADD COLUMN IF NOT EXISTS vector tsvector;

UPDATE oe SET vector = to_tsvector('NLD',
    COALESCE(naam_spraakgbr,'') || ' ' || COALESCE(naam_officieel,'') || ' ' || COALESCE(afko,''));

CREATE INDEX IF NOT EXISTS gin_idx_oe ON oe USING gin (vector);

CREATE OR REPLACE FUNCTION update_oe_vector() RETURNS TRIGGER AS $$
BEGIN
  NEW.vector :=
    to_tsvector('NLD', COALESCE(NEW.naam_spraakgbr,'') || ' ' || COALESCE(NEW.naam_officieel,'') || ' ' || COALESCE(NEW.afko,''));
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER oe_vector_trigger 
BEFORE INSERT OR UPDATE ON oe
FOR EACH ROW EXECUTE FUNCTION update_oe_vector();

-- For oe_koepel table
ALTER TABLE IF EXISTS oe_koepel
ADD COLUMN IF NOT EXISTS vector tsvector;

UPDATE oe_koepel SET vector = to_tsvector('NLD',
    COALESCE(titel,'') || ' ' || COALESCE(omschrijving,''));

CREATE INDEX IF NOT EXISTS gin_idx_oe_koepel ON oe_koepel USING gin (vector);

CREATE OR REPLACE FUNCTION update_oe_koepel_vector() RETURNS TRIGGER AS $$
BEGIN
  NEW.vector :=
    to_tsvector('NLD', COALESCE(NEW.titel,'') || ' ' || COALESCE(NEW.omschrijving,''));
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER oe_koepel_vector_trigger 
BEFORE INSERT OR UPDATE ON oe_koepel
FOR EACH ROW EXECUTE FUNCTION update_oe_koepel_vector();

