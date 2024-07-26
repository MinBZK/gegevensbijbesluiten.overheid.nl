from fastapi import HTTPException, status


class UserDoesNotExistException(HTTPException):
    """
    HTTP Exception with status code 404 to be thrown when a user can not be found.
    """

    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Geen gebruiker gevonden met dit mailadres",
        )


class InvalidTOTPException(HTTPException):
    """
    HTTP Exception with status code 401 to be thrown when an incorrect TOTP has been given.
    """

    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Ongeldige authenticator code.",
        )


class UserAlreadyExistsException(HTTPException):
    """
    HTTP Exception with status code 400 to be thrown when a user is being created
    with an email for which there already exists a user.
    """

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Er bestaat al een gebruiker met dit emailadres in het systeem.",
        )


class PasswordNotProvidedException(HTTPException):
    """
    HTTP Exception with status code 400 to be thrown when a password is being updated
    an no password is provided.
    """

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Geen wachtwoord gegeven om mee te updaten.",
        )


class NoRelationFound(HTTPException):
    """
    HTTP Exception with status code 400 to be thrown when a password is being updated
    an no password is provided.
    """

    def __init__(self, primary_key: int):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Geen relatie gevonden voor id={primary_key}.",
        )


class UserForbiddenException(HTTPException):
    """
    HTTP Exception with status code 403 to be thrown when a user is attempting
    to perform an operation for which they are not authorized.
    """

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Deze gebruiker heeft niet genoeg rechten om deze operatie uit te voeren.",
        )


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


class ExpiredToken(HTTPException):
    """
    HTTP Exception with status code 403 to be thrown when a unprocessable entity
    was given for processing.
    """

    def __init__(self, detail: str = "FastAPI Token is verlopen"):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
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


class NoRowFound(HTTPException):
    """
    Violation of foreign key constraints
    """

    def __init__(
        self,
        detail: str = "Er is geen record gevonden in de database",
    ):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=detail,
            headers={"WWW-Authenticate": "Bearer"},
        )


class FileAlreadyExists(HTTPException):
    """
    Violation of foreign key constraints
    """

    def __init__(
        self,
        detail: str = "Bestand bestaat al",
    ):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
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
