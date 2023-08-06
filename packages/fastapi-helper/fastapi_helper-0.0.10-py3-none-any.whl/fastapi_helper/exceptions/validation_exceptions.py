from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette import status
from starlette.requests import Request
from starlette.responses import JSONResponse, Response


def init_validation_handler(app: FastAPI) -> None:
    @app.exception_handler(RequestValidationError)
    async def request_validation_exception_handler(request: Request, exc: RequestValidationError) -> Response:
        errors = []
        for count, error in enumerate(exc.errors()):
            loc, message, types = error["loc"], error["msg"], error['type']
            try:
                field = error["loc"][1]
            except IndexError:
                field = None
            errors.append({
                "code": "validation-error",
                "type": types,
                "message": message,
                "field": None if types == 'value_error.jsondecode' else field
            })
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content=errors
        )
