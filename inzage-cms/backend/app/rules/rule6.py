import app.config as config
from app.config.resource import TableResource
from app.rules._superrule import SuperRule
from app.schemas.rules import Importance


class Rule6(SuperRule):
    __feedback_message = ""
    __explanation = "Onder een besluit zijn bepaalde velden die verplicht ingevuld moeten worden"
    code = 6
    name = "Verplichte velden zijn niet ingevuld"

    def __init__(self, importance=Importance.ERROR) -> None:
        super().__init__(
            self.code,
            self.name,
            importance,
            self.__feedback_message,
            self.__explanation,
        )

    def matching(self, evtp_structure):
        # mandatory_fields in evtp
        table = TableResource.evtp_version
        results = []

        for mandatory_field in config.resource.EXCEPTIONS_REQUIRED_FIELDS[table]:
            if isinstance(evtp_structure.get(mandatory_field), int):
                continue
            elif evtp_structure.get(mandatory_field).strip():
                continue
            else:
                results.append(
                    {
                        "result": True,
                        "mandatory_field": mandatory_field,
                        "table": table,
                        "gst": None,
                        "gg": None,
                        "feedback_message": f"Het verplichte veld '{mandatory_field}' onder dit besluit is niet ingevuld",
                    }
                )

        # mandatory_fields in oe
        table = TableResource.oe
        for mandatory_field in config.resource.EXCEPTIONS_REQUIRED_FIELDS[table]:
            for gst_object in evtp_structure.get("entities_evtp_gst"):
                if gst_object.get("entity_gst").get("entity_oe_best").get(mandatory_field).strip():
                    continue
                else:
                    results.append(
                        {
                            "result": True,
                            "mandatory_field": mandatory_field,
                            "table": "entity_oe_best",
                            "gst": gst_object.get("entity_gst").get("omschrijving"),
                            "gg": None,
                            "feedback_message": f"Het verplichte veld '{mandatory_field}' onder organisatie {gst_object['entity_gst']['entity_oe_best']['naam_spraakgbr']} is niet ingevuld",
                        }
                    )

        for mandatory_field in config.resource.EXCEPTIONS_REQUIRED_FIELDS[table]:
            for gst_object in evtp_structure.get("entities_evtp_gst"):
                if gst_object.get("entity_gst").get("entity_oe_bron").get(mandatory_field).strip():
                    continue
                else:
                    results.append(
                        {
                            "result": True,
                            "mandatory_field": mandatory_field,
                            "table": "entity_oe_bron",
                            "gst": gst_object.get("entity_gst").get("omschrijving"),
                            "gg": None,
                            "feedback_message": f"Het verplichte veld '{mandatory_field}' onder organisatie {gst_object['entity_gst']['entity_oe_bron']['naam_spraakgbr']} is niet ingevuld",
                        }
                    )

        # mandatory_fields in gg
        table = TableResource.gg
        for mandatory_field in config.resource.EXCEPTIONS_REQUIRED_FIELDS[table]:
            for gst_object in evtp_structure.get("entities_evtp_gst"):
                for gg_object in gst_object.get("entities_gst_gg"):
                    if gg_object.get("entity_gg").get(mandatory_field).strip():
                        continue
                    else:
                        results.append(
                            {
                                "result": True,
                                "mandatory_field": mandatory_field,
                                "table": table,
                                "gst": gst_object.get("entity_gst").get("omschrijving"),
                                "gg": gg_object.get("entity_gg").get("omschrijving"),
                                "feedback_message": f"De verplichte velden '{mandatory_field}' zijn niet \
                                    ingevuld onder gegevensstroom {gst_object.get('entity_gst').get('omschrijving')} \
                                    en gegevensgroep {gg_object.get('entity_gg').get('omschrijving')}",
                            }
                        )

        # mandatory_fields in rge
        table = TableResource.rge
        for mandatory_field in config.resource.EXCEPTIONS_REQUIRED_FIELDS[table]:
            for gst_object in evtp_structure.get("entities_evtp_gst"):
                for rge_object in gst_object.get("entities_gst_rge"):
                    try:
                        rge_object.get("entity_rge").get(mandatory_field).strip()
                    except Exception:
                        results.append(
                            {
                                "result": True,
                                "mandatory_field": mandatory_field,
                                "table": table,
                                "gst": gst_object.get("entity_gst").get("omschrijving"),
                                "rge": rge_object.get("entity_rge").get("titel"),
                                "feedback_message": f"De verplichte velden '{mandatory_field}' zijn niet \
                                    ingevuld onder gegevensstroom {gst_object.get('entity_gst').get('omschrijving')} \
                                    en wettelijke regeling {rge_object.get('entity_rge').get('titel')}",
                            }
                        )

        return results

    def applyRule(self, evtp_structure):
        results = self.matching(evtp_structure)

        if len(results) > 0:
            return results
        else:
            return None
