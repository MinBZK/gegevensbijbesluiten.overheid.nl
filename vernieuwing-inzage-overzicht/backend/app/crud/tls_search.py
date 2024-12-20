import logging
from typing import List

from sqlalchemy import func, select

import app.models as models
from app.core.config import SIMILARITY_THRESHOLD

logger = logging.getLogger(__name__)


def prep_search_for_query(search_query: str) -> str:
    """Prepare search query by replacing ' of ' with ' or '."""
    return search_query.replace(" of ", " or ")


def get_web_search_clause(search_query: str, model):
    """Get basic full-text search clause."""
    return model.vector.op("@@")(func.websearch_to_tsquery("NLD", search_query))


def get_similarity_search_clause(
    search_query: str, model, suggestion_search: bool = False, search_restricted: bool = True
):
    """Full text search query based on word similarity."""
    search_query = prep_search_for_query(search_query)

    # Get similar words query
    similar_words = (
        select(models.words.Words.word)
        .filter(func.similarity(models.words.Words.word, search_query) > SIMILARITY_THRESHOLD)
        .scalar_subquery()
    )

    # Create search vector
    search_vector = func.websearch_to_tsquery(func.array_to_string(func.array(similar_words), " OR "))

    if suggestion_search:
        vector_field = model.vector_suggestion if search_restricted else model.vector
    else:
        vector_field = model.vector

    return vector_field.op("@@")(search_vector)


def build_filters(search_query: str, model) -> List:
    """Build filters based on query parameters."""
    filters = []
    if search_query:
        searchtext = prep_search_for_query(search_query)
        filters.append(get_web_search_clause(searchtext, model))
    return filters


def build_filters_gg(search_query: str, model):
    search_query = prep_search_for_query(search_query)

    filter_ilike = model.omschrijving.ilike(f"%{search_query}%")
    filter_synonyms = get_web_search_clause(search_query, model)
    similarity_score = func.similarity(model.omschrijving, search_query)

    return filter_ilike, filter_synonyms, similarity_score


def build_filters_oe(search_query: str, model):
    filter_ilike = []
    search_query = prep_search_for_query(search_query)

    filter_ilike.append(model.naam_spraakgbr.ilike(f"%{search_query}%"))
    filter_ilike.append(model.naam_officieel.ilike(f"%{search_query}%"))
    filter_ilike.append(model.afko.ilike(f"%{search_query}%"))
    filter_synonyms = get_web_search_clause(search_query, model)
    similarity_score = func.similarity(model.naam_officieel, search_query)

    return filter_ilike, filter_synonyms, similarity_score


def build_filters_oe_koepel(search_query: str, model):
    search_query = prep_search_for_query(search_query)

    filter_ilike = model.titel.ilike(f"%{search_query}%")
    filter_synonyms = get_web_search_clause(search_query, model)
    similarity_score = func.similarity(model.titel, search_query)

    return filter_ilike, filter_synonyms, similarity_score
