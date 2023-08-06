from cloudyns.base.constants import (
    DEFAULT_CLOUDYNS_ERROR_CODE,
    DEFAULT_CLOUDYNS_ERROR_MESSAGE,
    DEFAULT_API_CONNECTION_ERROR_CODE,
    DEFAULT_API_CONNECTION_ERROR_MESSAGE,
)


class BaseCloudynsException(Exception):
    code: str = DEFAULT_CLOUDYNS_ERROR_CODE
    message: str = DEFAULT_CLOUDYNS_ERROR_MESSAGE

    def __init__(self, message: str = None, code: str = None):
        if message:
            self.message = message
        if code:
            self.code = code

    def __str__(self):
        return f"{self.code}: {self.message}"


class BaseBuilderProvider(BaseCloudynsException):
    pass


class BuilderProviderMissing(BaseBuilderProvider):
    code = "BUILDER_PROVIDER_MISSION"
    message = "The provider must be included in the CloudynsConf.provider configuration"


class ProviderDoesNotSupport(BaseBuilderProvider):
    code = "PROVIDER_DOES_NOT_SUPPORT"
    message = "There is no support for the provider %(provider)s yet"

    def __init__(self, provider: str, message: str = None, code: str = None):
        super(ProviderDoesNotSupport, self).__init__(message=message, code=code)
        self.provider = provider

    def __str__(self):
        string_error = super(ProviderDoesNotSupport, self).__str__()
        return string_error % {"provider": self.provider}


class BaseProviderManagerException(BaseCloudynsException):
    pass


class ProviderManagerMissingDomain(BaseProviderManagerException):
    code = "PROVIDER_MANAGER_MISSING_DOMAIN"
    message = "%(domain_name)s does not registered!!!"

    def __init__(self, domain_name: str, message: str = None, code: str = None):
        super(ProviderManagerMissingDomain, self).__init__(message=message, code=code)
        self.domain_name = domain_name

    def __str__(self):
        string_error = super(ProviderManagerMissingDomain, self).__str__()
        return string_error % {"domain_name": self.domain_name}


class ProviderTokenAuthenticationMissing(BaseProviderManagerException):
    code = "PROVIDER_TOKEN_AUTH_MISSING"
    message = "The authentication token was not provided!!!"


class BaseRecordException(BaseCloudynsException):
    pass


class RecordNameTypeDoesNotExist(BaseRecordException):
    code = "RECORD_NAME_TYPE_DOES_NOT_EXIST"
    message = "Record name=%(record_name)s and type=%(record_type)s, Does not exist!!!"

    def __init__(
        self, record_name: str, record_type: str, message: str = None, code: str = None
    ):
        super(RecordNameTypeDoesNotExist, self).__init__(message=message, code=code)
        self.record_name = record_name
        self.record_type = record_type

    def __str__(self):
        string_error = super(RecordNameTypeDoesNotExist, self).__str__()
        return string_error % {
            "record_name": self.record_name,
            "record_type": self.record_type,
        }


class MultiplesRecordSameNameType(BaseRecordException):
    code = "MULTIPLES_RECORDS_SAME_NAME_TYPE"
    message = "Exists multiples records with same name=%(record_name)s and record_type=%(record_type)s!!!"

    def __init__(
        self, record_name: str, record_type: str, message: str = None, code: str = None
    ):
        super(MultiplesRecordSameNameType, self).__init__(message=message, code=code)
        self.record_name = record_name
        self.record_type = record_type

    def __str__(self):
        string_error = super(MultiplesRecordSameNameType, self).__str__()
        return string_error % {
            "record_name": self.record_name,
            "record_type": self.record_type,
        }


class ProvidesWrongData(BaseRecordException):
    code = "PROVIDES_WRONG_DATA"
    message = "You don't provide de correct data!!!"


class RecordAlreadyExist(BaseRecordException):
    code = "RECORD_ALREADY_EXIST"
    message = "Already exist this record!!!"


class InvalidRecordType(BaseRecordException):
    code = "INVALID_RECORD_TYPE"
    message = "%(record_type)s is not a valid record type"

    def __init__(self, record_type: str, message: str = None, code: str = None):
        super(InvalidRecordType, self).__init__(message=message, code=code)
        self.record_type = record_type

    def __str__(self):
        string_error = super(InvalidRecordType, self).__str__()
        return string_error % {
            "record_type": self.record_type,
        }


class AttrNameRequiredRecordTypeA(BaseRecordException):
    code = "ATTR_NAME_REQUIRED_RECORD_TYPE_A"
    message = "In A record do you need 'name' value!!!"


class AttrDataRequiredRecordTypeA(BaseRecordException):
    code = "ATTR_DATA_REQUIRED_RECORD_TYPE_A"
    message = "In A record do you need 'data' value!!!"


class BaseAPIConnectionException(BaseCloudynsException):
    code = DEFAULT_API_CONNECTION_ERROR_CODE
    message = DEFAULT_API_CONNECTION_ERROR_MESSAGE


class ApiUnauthorized(BaseAPIConnectionException):
    code = "API_UNAUTHORIZED"
    message = "Not authorized"


class ApiNotFound(BaseAPIConnectionException):
    code = "API_NOT_FOUND"
    message = "Resource Not found"


class AddRecordDomainNotFound(ApiNotFound):
    code = "ADD_RECORD_DOMAIN_NOT_FOUND"
    message = "The domain to which you are trying to add a record does not exist!!!"


class AddRecordUnprocessableEntity(BaseAPIConnectionException):
    code = "UNPROCESSABLE_ENTITY"


class ApiRateLimitExceeded(BaseAPIConnectionException):
    code = "API_RATE_LIMIT_EXCEEDED"
    message = "API Rate limit exceeded!!!"


class ApiInternalServerError(BaseAPIConnectionException):
    code = "API_INTERNAL_SERVER_ERROR"
    message = "Unexpected server-side error!!!"


class ApiUnknownError(BaseAPIConnectionException):
    code = "API_UNKNOWN_ERROR"
    message = "Unknown error!!!"
