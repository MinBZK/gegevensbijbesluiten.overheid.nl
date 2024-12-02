from app.rules.rule8 import Rule8
from app.schemas.rules import Importance


def test_rule8_with_valid_data():
    rule = Rule8(importance=Importance.ERROR)
    evtp_structure = {
        "entities_evtp_gst": [
            {"entities_gst_gstt": ["type1"], "omschrijving": "Gegevensstroom 1"},
            {"entities_gst_gstt": ["type2"], "omschrijving": "Gegevensstroom 2"},
        ]
    }
    result = rule.applyRule(evtp_structure)
    assert result is None


def test_rule8_with_invalid_data():
    rule = Rule8(importance=Importance.ERROR)
    evtp_structure = {
        "entities_evtp_gst": [
            {"entities_gst_gstt": [], "omschrijving": "Gegevensstroom 1"},
            {"entities_gst_gstt": ["type2"], "omschrijving": "Gegevensstroom 2"},
            {"entities_gst_gstt": [], "omschrijving": "Gegevensstroom 3"},
        ]
    }
    result = rule.applyRule(evtp_structure)
    assert result is not None
    assert len(result) == 2
    assert result[0]["gst"] == "Gegevensstroom 1"
    assert result[1]["gst"] == "Gegevensstroom 3"
    assert (
        result[0]["feedback_message"] == "De volgende gegevensstroom 'Gegevensstroom 1' heeft geen gegevensstroom type"
    )
    assert (
        result[1]["feedback_message"] == "De volgende gegevensstroom 'Gegevensstroom 3' heeft geen gegevensstroom type"
    )


def test_rule8_with_empty_data():
    rule = Rule8(importance=Importance.ERROR)
    evtp_structure = {"entities_evtp_gst": []}
    result = rule.applyRule(evtp_structure)
    assert result is None
