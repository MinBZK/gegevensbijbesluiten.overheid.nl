from app.rules._superrule import SuperRule
from app.schemas.rules import Importance


class Rule8(SuperRule):
    __feedback_message = "De volgende gegevensstroom '%s' heeft geen gegevensstroom type"
    __explanation = "Voor een ieder gst moet er minimaal 1 gegevensstroom type aanwezig zijn"
    code = 8
    name = "Gegevensstroom minimaal 1 type"

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
            if len(gst_object.get("entity_gst").get("entities_gst_gstt")) > 0:
                continue
            else:
                results.append(
                    {
                        "result": True,
                        "gst": gst_object.get("entity_gst").get("omschrijving"),
                        "feedback_message": self.get_feedback_message
                        % (gst_object.get("entity_gst").get("omschrijving"),),
                    }
                )

        if len(results) > 0:
            return results
        else:
            return None
