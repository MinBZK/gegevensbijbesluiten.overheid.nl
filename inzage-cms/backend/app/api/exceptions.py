from fastapi import HTTPException, status


class UserUnauthorizedException(HTTPException):
    """
    HTTP Exception with status code 401 to be thrown when a user's credentials
    cannot be authenticated.
    """

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Inloggegevens konden niet succesvol worden gevalideerd.",
            headers={"WWW-Authenticate": "Bearer"},
        )


class UnprocessableEntity(HTTPException):
    """
    HTTP Exception with status code 422 to be thrown when a unprocessable entity
    was given for processing.
    """

    def __init__(self, detail: str = "Deze waarde bestaat al."):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=detail,
            headers={"WWW-Authenticate": "Bearer"},
        )


class UniqueViolation(HTTPException):
    """
    HTTP Exception with status code 409 to be thrown when a unique key is being duplicated
    """

    def __init__(self, detail: str = "Het object kan niet verwerkt worden."):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail=detail,
            headers={"WWW-Authenticate": "Bearer"},
        )


class ForeignKeyError(HTTPException):
    """
    Violation of foreign key constraints
    """

    def __init__(
        self,
        detail: str = "Bestaande relatie kan niet verwijderd worden ivm afhankelijkheden",
    ):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail=detail,
            headers={"WWW-Authenticate": "Bearer"},
        )


class FileFormatDoesNotMatch(HTTPException):
    """
    Violation of foreign key constraints
    """

    def __init__(
        self,
        detail: str = "Bestandsformaat is geen pdf of word",
    ):
        super().__init__(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail=detail,
            headers={"WWW-Authenticate": "Bearer"},
        )


class MalwareDetected(HTTPException):
    """
    Clamav found malware
    """

    def __init__(
        self,
        detail: str = "Malware gevonden",
    ):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=detail,
            headers={"WWW-Authenticate": "Bearer"},
        )
