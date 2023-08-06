from typing import Optional

from fastapi.security import OAuth2
from fastapi.security.utils import get_authorization_scheme_param
from fastapi_helper.exceptions.auth_http_exceptions import UnauthorizedException
from starlette.requests import Request


class OAuth2PasswordBearerCookie(OAuth2):
    async def __call__(self, request: Request) -> Optional[str]:
        cookie_authorization: str = request.cookies.get("Authorization")
        cookie_scheme, cookie_param = get_authorization_scheme_param(
            cookie_authorization,
        )
        if not cookie_authorization or cookie_scheme.lower() != "bearer":
            if self.auto_error:
                raise UnauthorizedException()
            else:
                return None
        return cookie_param


auth_bearer = OAuth2PasswordBearerCookie()
