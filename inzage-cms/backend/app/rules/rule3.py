from app.rules._superrule import SuperRule
from app.schemas.rules import Importance


class Rule3(SuperRule):
    __feedback_message = "De volgende gegevensstroom '%s' met gegevensgroep '%s' heeft een hogere gegevensgroep entiteit als enige gegevensgroep"
    __explanation = "Onder één gegevensstroom mag een gegevensgroep geen hogere gegevensgroep entiteit zijn"
    code = 3
    name = "Alleen hogere gegevensgroep aanwezig"

    def __init__(self, importance=Importance.ERROR) -> None:
        super().__init__(
            self.code,
            self.name,
            importance,
            self.__feedback_message,
            self.__explanation,
        )

    def applyRule(self, evtp_structure):
        results = []
        for gst_object in evtp_structure.get("entities_evtp_gst"):
            for gg_object in gst_object.get("entities_gst_gg"):
                if (
                    gg_object.get("entity_gg").get("count_parents") == 0
                    and gg_object.get("entity_gg").get("count_children") > 0
                ):
                    results.append(
                        {
                            "result": True,
                            "gst": gst_object.get("entity_gst").get("omschrijving"),
                            "gg": gg_object.get("entity_gg").get("omschrijving"),
                            "feedback_message": self.get_feedback_message
                            % (
                                gst_object.get("entity_gst").get("omschrijving"),
                                gg_object.get("entity_gg").get("omschrijving"),
                            ),
                        }
                    )

        if len(results) > 0:
            return results
        else:
            return None
