# -*- coding: utf-8 -*-
from typing import Optional

from starlette import status

from fastapi_helper.exceptions.auth_http_exceptions import (
    UnauthorizedException,
    InsufficientRightsException,
    InvalidCredentialsException
)
from fastapi_helper.exceptions.http_exceptions import DefaultHTTPException


class ExamplesGenerate:
    auth_error = (
        UnauthorizedException,
        InvalidCredentialsException,
        InsufficientRightsException
    )

    @staticmethod
    def generate_nested_schema_for_code(responses, error_code):
        responses[error_code] = {}
        responses[error_code]["content"] = {}
        responses[error_code]["content"]["application/json"] = {}

    def get_error_responses(self, *args: Optional[DefaultHTTPException], auth: bool = False) -> dict:
        responses = {}
        if auth:
            args += self.auth_error

        error_codes = {error.status_code for error in args}

        for error_code in error_codes:
            examples = {}

            for error in args:
                instance = error() # noqa
                if instance.status_code == error_code:
                    examples[instance.type] = instance.example()

            self.generate_nested_schema_for_code(responses, error_code)
            responses[error_code]["content"]["application/json"]["examples"] = examples

        self.change_422_validation_schema(responses)

        return responses

    def change_422_validation_schema(self, responses):
        self.generate_nested_schema_for_code(responses, status.HTTP_422_UNPROCESSABLE_ENTITY)
        example = {
            "validation_errors": {
                "summary": "Validation Error",
                "value": [
                    {
                        "code": "validation-error",
                        "type": "string",
                        "message": "string",
                        "field": "string",
                    },
                ],
            },
        }
        responses[status.HTTP_422_UNPROCESSABLE_ENTITY]["content"]["application/json"]["examples"] = example


examples_generate = ExamplesGenerate()
