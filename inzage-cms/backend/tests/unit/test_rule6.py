from datetime import datetime, timezone

import pytest
from app.rules.rule6 import Rule6
from app.schemas.rules import Importance


@pytest.fixture
def evtp_structure():
    return {
        "evtp_cd": 1,
        "versie_nr": 1,
        "evtp_nm": "Sample Event",
        "oe_best": 1,
        "gebr_dl": "Sample Process",
        "aanleiding": "Sample Reason",
        "id_publicatiestatus": 1,
        "huidige_versie": True,
        "omschrijving": "Sample description of the event.",
        "verantwoordelijke_oe": {
            "oe_cd": 1,
            "naam_officieel": "Sample Entity",
            "lidw_sgebr": "the",
            "naam_spraakgbr": "Sample Entity",
            "parent_entities": [
                {
                    "oe_koepel_oe_cd": 1,
                    "oe_koepel_cd": 1,
                    "oe_cd": 1,
                    "notitie": None,
                    "ts_mut": datetime(2024, 1, 1, 0, 0, tzinfo=timezone.utc),
                    "user_nm": "User1",
                    "parent_entity": {"oe_koepel_cd": 1, "titel": "Sample Parent Entity"},
                    "child_entity": {"oe_cd": 1, "naam_officieel": "Sample Entity"},
                }
            ],
            "count_parents": 1,
        },
        "entities_evtp_gst": [
            {
                "evtp_gst_cd": 1,
                "evtp_cd": 1,
                "gst_cd": 1,
                "notitie": None,
                "sort_key": None,
                "entity_gst": {
                    "gst_cd": 1,
                    "oe_bron": 1,
                    "oe_best": 1,
                    "omschrijving": "Sample Data Stream",
                    "conditie": None,
                    "entity_oe_best": {
                        "oe_cd": 1,
                        "naam_officieel": "Sample Entity",
                        "lidw_sgebr": "the",
                        "naam_spraakgbr": "Sample Entity",
                        "parent_entities": [
                            {
                                "oe_koepel_oe_cd": 1,
                                "oe_koepel_cd": 1,
                                "oe_cd": 1,
                                "notitie": None,
                                "ts_mut": datetime(2024, 1, 1, 0, 0, tzinfo=timezone.utc),
                                "user_nm": "User1",
                                "parent_entity": {"oe_koepel_cd": 1, "titel": "Sample Parent Entity"},
                                "child_entity": {"oe_cd": 1, "naam_officieel": "Sample Entity"},
                            }
                        ],
                        "count_parents": 1,
                    },
                    "entity_oe_bron": {
                        "oe_cd": 1,
                        "naam_officieel": "Sample Source Entity",
                        "lidw_sgebr": "the",
                        "naam_spraakgbr": "Sample Source Entity",
                        "parent_entities": [
                            {
                                "oe_koepel_oe_cd": 1,
                                "oe_koepel_cd": 1,
                                "oe_cd": 1,
                                "notitie": None,
                                "ts_mut": datetime(2024, 1, 1, 0, 0, tzinfo=timezone.utc),
                                "user_nm": "User1",
                                "parent_entity": {"oe_koepel_cd": 1, "titel": "Sample Parent Entity"},
                                "child_entity": {"oe_cd": 1, "naam_officieel": "Sample Source Entity"},
                            }
                        ],
                        "count_parents": 1,
                    },
                    "entity_ibron": {
                        "ibron_cd": 1,
                        "titel": "Sample Registration",
                        "afko": "SR",
                        "lidw": "the",
                        "link": "https://sample.link",
                        "oe_cd": 1,
                        "user_nm": "User1",
                        "notitie": None,
                        "ts_mut": datetime(2024, 1, 1, 0, 0, tzinfo=timezone.utc),
                        "entity_oe": {
                            "oe_cd": 1,
                            "naam_officieel": "Sample Source Entity",
                            "lidw_sgebr": "the",
                            "naam_spraakgbr": "Sample Source Entity",
                        },
                    },
                },
                "entities_gst_gstt": [
                    {
                        "gst_cd": 1,
                        "gstt_cd": 1,
                        "gst_gstt_cd": 1,
                        "entity_gst_type": {
                            "gstt_cd": 1,
                            "gstt_naam": "Sample Type",
                            "gstt_oms": "Sample Description",
                            "ts_mut": datetime(2024, 1, 1, 0, 0, tzinfo=timezone.utc),
                            "user_nm": "User1",
                            "gstt_pp": None,
                        },
                    }
                ],
                "entities_gst_gg": [
                    {
                        "gst_gg_cd": 1,
                        "sort_key": 1,
                        "entity_gg": {
                            "gg_cd": 1,
                            "omschrijving": "Sample Personal Data",
                            "notitie": None,
                            "omschrijving_uitgebreid": "Sample detailed description",
                            "count_parents": 1,
                            "count_children": 0,
                            "parent_entities": [
                                {
                                    "gg_struct_cd": 1,
                                    "gg_cd_sub": 1,
                                    "gg_cd_sup": 1,
                                    "notitie": None,
                                    "ts_mut": datetime(2024, 1, 1, 0, 0, tzinfo=timezone.utc),
                                    "user_nm": "User1",
                                    "parent_entity": {
                                        "gg_cd": 1,
                                        "omschrijving": "Sample Parent Data",
                                        "notitie": "Sample Note",
                                        "omschrijving_uitgebreid": "Sample detailed description of parent data.",
                                    },
                                    "child_entity": {
                                        "gg_cd": 1,
                                        "omschrijving": "Sample Personal Data",
                                        "notitie": None,
                                        "omschrijving_uitgebreid": "Sample detailed description",
                                    },
                                }
                            ],
                            "child_entities": [],
                        },
                    },
                    {
                        "gst_gg_cd": 2,
                        "sort_key": 2,
                        "entity_gg": {
                            "gg_cd": 2,
                            "omschrijving": "Sample Address Data",
                            "notitie": "Sample Note",
                            "omschrijving_uitgebreid": "Sample detailed description of address data.",
                            "count_parents": 0,
                            "count_children": 0,
                            "parent_entities": [],
                            "child_entities": [],
                        },
                    },
                ],
                "entities_gst_rge": [
                    {
                        "gst_rge_cd": 1,
                        "sort_key": None,
                        "entity_rge": {
                            "rge_cd": 1,
                            "titel": "Sample Regulation",
                            "re_link": "https://sample.regulation.link",
                        },
                    },
                    {
                        "gst_rge_cd": 2,
                        "sort_key": None,
                        "entity_rge": {"rge_cd": 2, "titel": "Sample Law", "re_link": "https://sample.law.link"},
                    },
                ],
            },
            {
                "evtp_gst_cd": 2,
                "evtp_cd": 1,
                "gst_cd": 2,
                "notitie": None,
                "sort_key": None,
                "entity_gst": {
                    "gst_cd": 2,
                    "oe_bron": 2,
                    "oe_best": 1,
                    "omschrijving": "Sample Data Stream 2",
                    "conditie": None,
                    "entity_oe_best": {
                        "oe_cd": 1,
                        "naam_officieel": "Sample Entity",
                        "lidw_sgebr": "the",
                        "naam_spraakgbr": "Sample Entity",
                        "parent_entities": [
                            {
                                "oe_koepel_oe_cd": 1,
                                "oe_koepel_cd": 1,
                                "oe_cd": 1,
                                "notitie": None,
                                "ts_mut": datetime(2024, 1, 1, 0, 0, tzinfo=timezone.utc),
                                "user_nm": "User1",
                                "parent_entity": {"oe_koepel_cd": 1, "titel": "Sample Parent Entity"},
                                "child_entity": {"oe_cd": 1, "naam_officieel": "Sample Entity"},
                            }
                        ],
                        "count_parents": 1,
                    },
                    "entity_oe_bron": {
                        "oe_cd": 2,
                        "naam_officieel": "Sample Source Entity 2",
                        "lidw_sgebr": "the",
                        "naam_spraakgbr": "Sample Source Entity 2",
                        "parent_entities": [
                            {
                                "oe_koepel_oe_cd": 2,
                                "oe_koepel_cd": 2,
                                "oe_cd": 2,
                                "notitie": None,
                                "ts_mut": datetime(2024, 1, 1, 0, 0, tzinfo=timezone.utc),
                                "user_nm": "User2",
                                "parent_entity": {"oe_koepel_cd": 2, "titel": "Sample Parent Entity 2"},
                                "child_entity": {"oe_cd": 2, "naam_officieel": "Sample Source Entity 2"},
                            }
                        ],
                        "count_parents": 1,
                    },
                    "entity_ibron": None,
                },
                "entities_gst_gstt": [
                    {
                        "gst_cd": 2,
                        "gstt_cd": 2,
                        "gst_gstt_cd": 2,
                        "entity_gst_type": {
                            "gstt_cd": 2,
                            "gstt_naam": "Sample Type 2",
                            "gstt_oms": "Sample Description 2",
                            "ts_mut": datetime(2024, 1, 1, 0, 0, tzinfo=timezone.utc),
                            "user_nm": "User2",
                            "gstt_pp": "push",
                        },
                    }
                ],
                "entities_gst_gg": [
                    {
                        "gst_gg_cd": 2,
                        "sort_key": None,
                        "entity_gg": {
                            "gg_cd": 2,
                            "omschrijving": "Sample Activity Description",
                            "notitie": None,
                            "omschrijving_uitgebreid": "Detailed description of the activity.",
                            "count_parents": 1,
                            "count_children": 0,
                            "parent_entities": [
                                {
                                    "gg_struct_cd": 2,
                                    "gg_cd_sub": 2,
                                    "gg_cd_sup": 2,
                                    "notitie": None,
                                    "ts_mut": datetime(2024, 1, 1, 0, 0, tzinfo=timezone.utc),
                                    "user_nm": "User2",
                                    "parent_entity": {
                                        "gg_cd": 2,
                                        "omschrijving": "Sample Parent Data 2",
                                        "notitie": None,
                                        "omschrijving_uitgebreid": "Detailed description of the parent data.",
                                    },
                                    "child_entity": {
                                        "gg_cd": 2,
                                        "omschrijving": "Sample Activity Description",
                                        "notitie": None,
                                        "omschrijving_uitgebreid": "Detailed description of the activity.",
                                    },
                                }
                            ],
                            "child_entities": [],
                        },
                    }
                ],
                "entities_gst_rge": [
                    {
                        "gst_rge_cd": 2,
                        "sort_key": None,
                        "entity_rge": {"rge_cd": 2, "titel": "Sample Law 2", "re_link": "https://sample.law2.link"},
                    }
                ],
            },
        ],
        "entities_evtp_oe_com_type": [
            {
                "evtp_oe_com_type_cd": 1,
                "oe_com_type_cd": 1,
                "entity_oe_com_type": {"oe_com_type_cd": 1, "omschrijving": "Sample Communication Type"},
            }
        ],
        "entities_evtp_ond": [
            {"evtp_ond_cd": 1, "ond_cd": 1, "evtp_cd": 1, "entity_ond": {"ond_cd": 1, "titel": "Sample Domain"}},
            {"evtp_ond_cd": 2, "ond_cd": 2, "evtp_cd": 1, "entity_ond": {"ond_cd": 2, "titel": "Sample Domain 2"}},
        ],
        "entity_omg": None,
    }


def test_rule6_no_errors(evtp_structure):
    rule = Rule6(importance=Importance.ERROR)
    results = rule.applyRule(evtp_structure)
    assert results is None
