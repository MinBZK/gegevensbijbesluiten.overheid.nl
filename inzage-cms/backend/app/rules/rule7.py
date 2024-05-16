from app.rules._superrule import SuperRule
from app.schemas.rules import Importance


class Rule7(SuperRule):
    __feedback_message = "De volgende gegevensstroom '%s' heeft meerdere hogere gegevensgroep entiteiten"
    __explanation = (
        "Onder één gegevensstroom mogen er geen meerdere gegevensgroepen vallen die verschillende "
        "hogere gegevensgroep entiteiten hebben"
    )
    code = 7
    name = "Meerdere hogere gegevensgroep entiteiten"

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
            gg_cd_sup = []
            for gg_object in gst_object.get("entities_gst_gg"):
                if gg_object.get("entity_gg").get("count_parents") > 0:
                    gg_cd_sup.append(gg_object.get("entity_gg").get("parent_entities")[0].get("gg_cd_sup"))
                else:
                    gg_cd_sup.append(None)

            if gg_cd_sup.count(gg_cd_sup[0]) != len(gg_cd_sup):
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
