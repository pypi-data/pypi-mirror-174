from cloudyns.base.constants import (
    STATUS_CODE_401_UNAUTHORIZED,
    STATUS_CODE_404_NOT_FOUND,
    STATUS_CODE_429_TO_MANY_REQUESTS,
    STATUS_CODE_500_SERVER_ERROR,
)
from cloudyns.base.exceptions import (
    ApiUnauthorized,
    ApiNotFound,
    ApiRateLimitExceeded,
    ApiInternalServerError,
)


def validate_401(response) -> None:
    if response.status_code == STATUS_CODE_401_UNAUTHORIZED:
        raise ApiUnauthorized


def validate_404(response) -> None:
    if response.status_code == STATUS_CODE_404_NOT_FOUND:
        raise ApiNotFound


def validate_429(response) -> None:
    if response.status_code == STATUS_CODE_429_TO_MANY_REQUESTS:
        raise ApiRateLimitExceeded


def validate_500(response) -> None:
    if response.status_code == STATUS_CODE_500_SERVER_ERROR:
        raise ApiInternalServerError


def validate_basic_status_code_response(response) -> None:
    validate_401(response)
    validate_404(response)
    validate_429(response)
    validate_500(response)
