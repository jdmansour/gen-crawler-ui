from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.disciplines_data import DisciplinesData
from ...models.disciplines_http_validation_error import DisciplinesHTTPValidationError
from ...models.disciplines_result import DisciplinesResult
from ...types import Response


def _get_kwargs(
    *,
    body: DisciplinesData,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/kidra/delete/disciplines",
    }

    _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[DisciplinesHTTPValidationError, DisciplinesResult]]:
    if response.status_code == 200:
        response_200 = DisciplinesResult.from_dict(response.json())

        return response_200
    if response.status_code == 422:
        response_422 = DisciplinesHTTPValidationError.from_dict(response.json())

        return response_422
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[DisciplinesHTTPValidationError, DisciplinesResult]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    body: DisciplinesData,
) -> Response[Union[DisciplinesHTTPValidationError, DisciplinesResult]]:
    """Delete cached data entry for: Predict the OpenEduHub disciplines of the given text

    Args:
        body (DisciplinesData):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[DisciplinesHTTPValidationError, DisciplinesResult]]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    body: DisciplinesData,
) -> Optional[Union[DisciplinesHTTPValidationError, DisciplinesResult]]:
    """Delete cached data entry for: Predict the OpenEduHub disciplines of the given text

    Args:
        body (DisciplinesData):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[DisciplinesHTTPValidationError, DisciplinesResult]
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    body: DisciplinesData,
) -> Response[Union[DisciplinesHTTPValidationError, DisciplinesResult]]:
    """Delete cached data entry for: Predict the OpenEduHub disciplines of the given text

    Args:
        body (DisciplinesData):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[DisciplinesHTTPValidationError, DisciplinesResult]]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    body: DisciplinesData,
) -> Optional[Union[DisciplinesHTTPValidationError, DisciplinesResult]]:
    """Delete cached data entry for: Predict the OpenEduHub disciplines of the given text

    Args:
        body (DisciplinesData):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[DisciplinesHTTPValidationError, DisciplinesResult]
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
