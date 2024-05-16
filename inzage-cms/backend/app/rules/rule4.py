from app.rules._superrule import SuperRule
from app.schemas.rules import Importance


class Rule4(SuperRule):
    __feedback_message = (
        "De volgende gegevensstroom '%s' met als verantwoordelijke organisatie '%s' komt niet overeen "
        "met besluitnemende organisatie '%s' uit dit besluit"
    )
    __explanation = (
        "Besluitnemende organisatie uit besluit moet overeenkomen met de verantwoordelijke organisatie in de gst "
        "ofwel afnemende organisatie in gegevensstroom"
    )
    code = 4
    name = "Besluitnemende organisatie komt niet overeen met bestemming organisatie"

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
            if gst_object.get("entity_gst").get("oe_best") != evtp_structure.get("oe_best"):
                results.append(
                    {
                        "result": True,
                        "gst": gst_object.get("entity_gst").get("omschrijving"),
                        "verantwoordelijke_oe": gst_object.get("entity_gst").get("oe_best"),
                        "besluitnemende_oe": evtp_structure.get("oe_best"),
                        "feedback_message": self.get_feedback_message
                        % (
                            gst_object.get("entity_gst").get("omschrijving"),
                            gst_object.get("entity_gst").get("oe_best"),
                            evtp_structure.get("oe_best"),
                        ),
                    }
                )

        if len(results) > 0:
            return results
        else:
            return None
