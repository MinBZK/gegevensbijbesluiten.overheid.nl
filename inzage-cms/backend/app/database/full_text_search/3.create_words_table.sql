-- For evtp_version
CREATE TABLE IF NOT EXISTS words AS 
SELECT word FROM ts_stat('SELECT vector FROM evtp_version');

CREATE OR REPLACE FUNCTION update_words_evtp()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO words (word)
    SELECT word
    FROM ts_stat('SELECT vector FROM evtp_version')
    WHERE word NOT IN (SELECT word FROM words);
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_words_evtp_trigger
AFTER INSERT ON evtp_version
FOR EACH ROW
EXECUTE FUNCTION update_words_evtp();


-- For gg
CREATE OR REPLACE FUNCTION update_words_gg()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO words (word)
    SELECT word
    FROM ts_stat('SELECT vector FROM gg')
    WHERE word NOT IN (SELECT word FROM words);
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_words_gg_trigger
AFTER INSERT ON gg
FOR EACH ROW
EXECUTE FUNCTION update_words_gg();

-- For oe
CREATE OR REPLACE FUNCTION update_words_oe()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO words (word)
    SELECT word
    FROM ts_stat('SELECT vector FROM oe')
    WHERE word NOT IN (SELECT word FROM words);
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_words_oe_trigger
AFTER INSERT ON oe
FOR EACH ROW
EXECUTE FUNCTION update_words_oe();

-- For oe_koepel
CREATE OR REPLACE FUNCTION update_words_oe_koepel()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO words (word)
    SELECT word
    FROM ts_stat('SELECT vector FROM oe_koepel')
    WHERE word NOT IN (SELECT word FROM words);
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_words_oe_koepel_trigger
AFTER INSERT ON oe_koepel
FOR EACH ROW
EXECUTE FUNCTION update_words_oe_koepel();


-- Populate words table with existing data from all tables
INSERT INTO words (word)
SELECT DISTINCT word
FROM (
    SELECT word FROM ts_stat('SELECT vector FROM evtp_version')
    UNION
    SELECT word FROM ts_stat('SELECT vector FROM gg')
    UNION
    SELECT word FROM ts_stat('SELECT vector FROM oe')
    UNION
    SELECT word FROM ts_stat('SELECT vector FROM oe_koepel')
) AS all_words
WHERE word NOT IN (SELECT word FROM words);