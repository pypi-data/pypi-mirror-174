# -*- coding: utf-8 -*-
import inspect
from typing import Type

from fastapi import Form, UploadFile, File
from humps.main import camelize
from pydantic import BaseModel
from pydantic.fields import ModelField


def as_form(cls: Type[BaseModel]):
    new_parameters = []

    for field_name, model_field in cls.__fields__.items():
        model_field: ModelField
        new_parameters.append(
            inspect.Parameter(
                model_field.alias,
                inspect.Parameter.POSITIONAL_ONLY,
                default=File(...) if model_field.required else File(model_field.default),
                annotation=model_field.outer_type_,
            )
            if model_field.type_ == UploadFile
            else inspect.Parameter(
                model_field.alias,
                inspect.Parameter.POSITIONAL_ONLY,
                default=Form(...) if model_field.required else Form(model_field.default),
                annotation=model_field.outer_type_,
            ),
        )

    async def as_form_func(**data):
        return cls(**data)

    sig = inspect.signature(as_form_func)
    sig = sig.replace(parameters=new_parameters)
    as_form_func.__signature__ = sig  # type: ignore
    setattr(cls, "as_form", as_form_func)
    return cls


class ApiSchema(BaseModel):
    class Config:
        orm_mode = True
        alias_generator = camelize
        allow_population_by_field_name = True
