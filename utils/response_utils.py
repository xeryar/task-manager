from typing import Any

from rest_framework import status
from rest_framework.response import Response


def make_success_response(data: dict[str, Any] | list[Any] | dict[int, Any] | None = None, message: str = "") -> Response:
    """
    Make a success response with 200 status code. The message is optional and will be empty by default.
    """
    return Response(
        {
            "status": "success",
            "message": message,
            "data": data,
        },
        status=status.HTTP_200_OK,
    )


def make_created_response(data: dict[str, Any] | list[Any] | dict[int, Any] | None = None, message: str = "") -> Response:
    """
    Make a created response with 201 status code. The message is optional and will be empty by default.
    """
    return Response(
        {
            "status": "created",
            "message": message,
            "data": data,
        },
        status=status.HTTP_201_CREATED,
    )


def make_error_response(data: dict[str, Any] | list[Any] | dict[int, Any] | None = None, message: str = "") -> Response:
    """
    Make a error response with 400 status code. The message is optional and will be empty by default.
    """
    return Response(
        {
            "status": "failed",
            "message": message,
            "data": data,
        },
        status=status.HTTP_400_BAD_REQUEST,
    )


def make_forbidden_response(data: dict[str, Any] | list[Any] | dict[int, Any] | None = None, message: str = "") -> Response:
    """
    Make a forbidden response with 403 status code. The message is optional and will be empty by default.
    """
    return Response(
        {
            "status": "forbidden",
            "message": message,
            "data": data,
        },
        status=status.HTTP_403_FORBIDDEN,
    )
