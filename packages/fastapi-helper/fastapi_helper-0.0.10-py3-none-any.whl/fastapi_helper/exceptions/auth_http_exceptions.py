# -*- coding: utf-8 -*-
from starlette import status

from fastapi_helper import DefaultHTTPException


class UnauthorizedException(DefaultHTTPException):
    code = "bearer-001"
    type = "UNAUTHORIZED"
    message = "Credentials were not provided."
    status_code = status.HTTP_403_FORBIDDEN


class InvalidCredentialsException(DefaultHTTPException):
    code = "bearer-002"
    type = "LOGIN_BAD_CREDENTIALS"
    message = "Invalid credentials."
    status_code = status.HTTP_401_UNAUTHORIZED


class InsufficientRightsException(DefaultHTTPException):
    code = "auth-003"
    type = "INSUFFICIENT_RIGHTS"
    message = "Insufficient rights to perform this action."
    status_code = status.HTTP_403_FORBIDDEN
