from enum import Enum


class ProvinceErrorCode(Enum):
    FORBIDDEN = "forbidden"
    GRAPHQL_ERROR = "graphql_error"
    INVALID = "invalid"
    INVALID_STATUS = "invalid_status"
    INVALID_URL_FORMAT = "invalid_url_format"
    INVALID_MANIFEST_FORMAT = "invalid_manifest_format"
    MANIFEST_URL_CANT_CONNECT = "manifest_url_cant_connect"
    NOT_FOUND = "not_found"
    REQUIRED = "required"
    UNIQUE = "unique"


class CityErrorCode(Enum):
    FORBIDDEN = "forbidden"
    GRAPHQL_ERROR = "graphql_error"
    INVALID = "invalid"
    INVALID_STATUS = "invalid_status"
    INVALID_URL_FORMAT = "invalid_url_format"
    INVALID_MANIFEST_FORMAT = "invalid_manifest_format"
    MANIFEST_URL_CANT_CONNECT = "manifest_url_cant_connect"
    NOT_FOUND = "not_found"
    REQUIRED = "required"
    UNIQUE = "unique"
