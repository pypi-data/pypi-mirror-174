# -*- coding: utf-8 -*-
import abc
from abc import abstractproperty, abstractmethod
from fastapi import HTTPException  # noqa
from starlette import status


class ClassABC(type):
    def __init__(cls, name, bases, attrs):
        abstracts = set()

        for base in bases:
            abstracts.update(getattr(base, "__abstractclassmethods__", set()))

        for abstract in abstracts:
            annotation_type = bases[0].__annotations__.get(abstract)
            if annotation_type:
                if not isinstance(getattr(cls, abstract), annotation_type):
                    raise TypeError("Wrong type of {}".format(abstract))

                if getattr(getattr(cls, abstract), "__isabstractmethod__", False):
                    raise TypeError("Your class doesn't define {}".format(abstract))

        for attr in attrs:
            if getattr(attrs[attr], "__isabstractmethod__", False):
                abstracts.add(attr)

        cls.__abstractclassmethods__ = abstracts

        super().__init__(name, bases, attrs)


class BaseHTTPException(HTTPException, metaclass=ClassABC):
    status_code: int = 400

    def __init__(self) -> None:
        super().__init__(status_code=self.status_code)

    @abc.abstractmethod
    def example(self) -> dict:
        pass


class DefaultHTTPException(BaseHTTPException):
    code: str = abstractproperty()
    type: str = abstractproperty()
    message: str = abstractproperty()

    def __init__(self, message: str = None):
        self.message = message if message else self.message
        super(DefaultHTTPException, self).__init__()

    def example(self) -> dict:
        example = {
            "summary": self.type,
            "value":
            [
                {
                    "code": self.code,
                    "type": self.type,
                    "message": self.message
                 },
            ]
        }
        return example

