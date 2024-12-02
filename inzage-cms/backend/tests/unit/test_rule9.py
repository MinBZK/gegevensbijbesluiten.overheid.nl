from app.rules.rule9 import Rule9
from app.schemas.rules import Importance


def test_rule9_with_parent_entities():
    evtp_structure = {
        "verantwoordelijke_oe": {"parent_entities": ["entity1"], "naam_officieel": "Test Organization"},
        "omschrijving": "Test Description",
    }
    rule = Rule9()
    result = rule.applyRule(evtp_structure)
    assert result is None


def test_rule9_without_parent_entities():
    evtp_structure = {
        "verantwoordelijke_oe": {"parent_entities": [], "naam_officieel": "Test Organization"},
        "omschrijving": "Test Description",
    }
    rule = Rule9()
    result = rule.applyRule(evtp_structure)
    assert result is not None
    assert len(result) == 1
    assert result[0]["result"] is True
    assert result[0]["oe"] == "Test Description"
    assert result[0]["feedback_message"] == (
        "De besluitnemende organisatie Test Organization heeft geen koepel organisatie toebedeeld gekregen"
    )


def test_rule9_custom_importance():
    evtp_structure = {
        "verantwoordelijke_oe": {"parent_entities": [], "naam_officieel": "Test Organization"},
        "omschrijving": "Test Description",
    }
    rule = Rule9(importance=Importance.WARNING)
    result = rule.applyRule(evtp_structure)
    assert result is not None
    assert len(result) == 1
    assert result[0]["result"] is True
    assert result[0]["oe"] == "Test Description"
    assert result[0]["feedback_message"] == (
        "De besluitnemende organisatie Test Organization heeft geen koepel organisatie toebedeeld gekregen"
    )
