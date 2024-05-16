from app.rules._superrule import SuperRule
from app.schemas.rules import Importance


class Rule0(SuperRule):
    __feedback_message = "Het besluit heeft %s aan gekoppeld"
    __explanation = "Dit besluit is niet volledig"
    code = 0
    name = "Besluit structuur incompleet"

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
        if not evtp_structure.get("entities_evtp_gst") or not evtp_structure.get("entities_evtp_ond"):
            results.append(
                {
                    "result": True,
                    "gst": "",
                    "gg": "",
                    "feedback_message": self.get_feedback_message % (" geen gegevensstroom of onderwerp"),
                }
            )

        for gst_object in evtp_structure.get("entities_evtp_gst"):
            if not gst_object.get("entities_gst_gg") or not gst_object.get("entities_gst_rge"):
                results.append(
                    {
                        "result": True,
                        "gst": gst_object.get("entity_gst").get("omschrijving"),
                        "gg": "",
                        "feedback_message": self.get_feedback_message
                        % (
                            f' geen gegevensgroep/regelingelement aan gegevensstroom {gst_object.get("entity_gst").get("omschrijving")}'
                        ),
                    }
                )

        if len(results) > 0:
            return results
        else:
            return None
