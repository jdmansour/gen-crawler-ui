from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.input_data import InputData
from ...models.text_statistics_http_validation_error import TextStatisticsHTTPValidationError
from ...models.text_statistics_result import TextStatisticsResult
from ...types import Response


def _get_kwargs(
    *,
    body: InputData,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/kidra/delete/text-statistics",
    }

    _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[TextStatisticsHTTPValidationError, TextStatisticsResult]]:
    if response.status_code == 200:
        response_200 = TextStatisticsResult.from_dict(response.json())

        return response_200
    if response.status_code == 422:
        response_422 = TextStatisticsHTTPValidationError.from_dict(response.json())

        return response_422
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[TextStatisticsHTTPValidationError, TextStatisticsResult]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    body: InputData,
) -> Response[Union[TextStatisticsHTTPValidationError, TextStatisticsResult]]:
    """Delete cached data entry for: Compute text statistics on the given text

    Args:
        body (InputData):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[TextStatisticsHTTPValidationError, TextStatisticsResult]]
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
    body: InputData,
) -> Optional[Union[TextStatisticsHTTPValidationError, TextStatisticsResult]]:
    """Delete cached data entry for: Compute text statistics on the given text

    Args:
        body (InputData):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[TextStatisticsHTTPValidationError, TextStatisticsResult]
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    body: InputData,
) -> Response[Union[TextStatisticsHTTPValidationError, TextStatisticsResult]]:
    """Delete cached data entry for: Compute text statistics on the given text

    Args:
        body (InputData):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[TextStatisticsHTTPValidationError, TextStatisticsResult]]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    body: InputData,
) -> Optional[Union[TextStatisticsHTTPValidationError, TextStatisticsResult]]:
    """Delete cached data entry for: Compute text statistics on the given text

    Args:
        body (InputData):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[TextStatisticsHTTPValidationError, TextStatisticsResult]
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
