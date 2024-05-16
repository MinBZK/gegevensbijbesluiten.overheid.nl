from app.schemas.rules import Importance


class SuperRule:
    __slots__ = ["__code", "__name", "__importance", "__feedback_message", "__explanation"]
    __exception_message = (
        "Deze regel kan niet toegepast worden omdat "
        "besluit structuur niet volledig is. Los eerst de andere regels op die zijn overtreden."
    )

    def __init__(
        self,
        code: int,
        name: str,
        importance: Importance,
        feedback_message: str,
        explanation: str,
    ) -> None:
        self.__code = code
        self.__name = name
        self.__importance = importance
        self.__feedback_message = feedback_message
        self.__explanation = explanation

    @property
    def get_exception_message(self):
        return self.__exception_message

    @property
    def get_code(self):
        return self.__code

    @property
    def get_name(self):
        return self.__name

    @property
    def get_importance(self):
        return self.__importance

    @property
    def get_importance_displayname(self):
        return self.__importance.value

    @property
    def get_feedback_message(self):
        return self.__feedback_message

    @property
    def get_explanation(self):
        return self.__explanation
