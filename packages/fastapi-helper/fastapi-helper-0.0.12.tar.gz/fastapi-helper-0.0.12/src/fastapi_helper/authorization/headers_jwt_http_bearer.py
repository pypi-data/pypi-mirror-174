from typing import Optional

from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi.security.utils import get_authorization_scheme_param
from starlette.requests import Request

from fastapi_helper.exceptions.auth_http_exceptions import UnauthorizedException


class JwtHTTPBearer(HTTPBearer):
    async def __call__(
        self,
        request: Request,
    ) -> Optional[HTTPAuthorizationCredentials]:
        authorization: str = request.headers.get("Authorization")
        scheme, credentials = get_authorization_scheme_param(authorization)
        if not (authorization and scheme and credentials):
            if self.auto_error:
                raise UnauthorizedException()
            else:
                return None
        if scheme.lower() != "bearer":
            if self.auto_error:
                raise UnauthorizedException()
            else:
                return None
        return HTTPAuthorizationCredentials(scheme=scheme, credentials=credentials)


jwt_http_bearer = JwtHTTPBearer()
jwt_http_bearer_no_error = JwtHTTPBearer(auto_error=False)
