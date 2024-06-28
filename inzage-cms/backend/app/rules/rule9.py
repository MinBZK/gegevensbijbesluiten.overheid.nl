from app.rules._superrule import SuperRule
from app.schemas.rules import Importance


class Rule9(SuperRule):
    __feedback_message = "De besluitnemende organisatie %s heeft geen koepel organisatie toebedeeld gekregen"
    __explanation = "Voor een besluitnemende organisatie moet er minimaal 1 koepel organisatie aanwezig zijn"
    code = 9
    name = "Geen koepel organisatie toebedeeld aan de besluitnemende organisatie"

    def __init__(self, importance=Importance.ERROR) -> None:
        super().__init__(
            self.code,
            self.name,
            importance,
            self.__feedback_message,
            self.__explanation,
        )

    def applyRule(self, evtp_structure):
        if len(evtp_structure.get("verantwoordelijke_oe").get("parent_entities")) > 0:
            return None
        else:
            return [
                {
                    "result": True,
                    "oe": evtp_structure.get("omschrijving"),
                    "feedback_message": self.get_feedback_message
                    % (evtp_structure.get("verantwoordelijke_oe").get("naam_officieel")),
                }
            ]
