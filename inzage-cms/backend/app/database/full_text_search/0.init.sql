-- Dutch full text search configuration
CREATE TEXT SEARCH DICTIONARY dutch_opentaal_hunspell (
    template = ispell,
    dictfile = nl_nl,
    afffile = nl_nl,
    stopwords = dutch_stopwords_extended
);

CREATE TEXT SEARCH CONFIGURATION NLD (copy = pg_catalog.dutch);

ALTER TEXT SEARCH CONFIGURATION NLD
    ALTER MAPPING FOR asciiword, asciihword, hword_asciipart, word, hword, hword_part
    WITH dutch_opentaal_hunspell, dutch_stem;

CREATE TEXT SEARCH DICTIONARY dutch_syn (
    TEMPLATE = synonym,
    SYNONYMS = dutch_synonyms
);

ALTER TEXT SEARCH CONFIGURATION NLD
    ALTER MAPPING FOR asciiword
    WITH dutch_syn, dutch_stem;

CREATE EXTENSION pg_trgm;
