from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.topic_statistics_http_validation_error import TopicStatisticsHTTPValidationError
from ...models.topic_statistics_input_stats import TopicStatisticsInputStats
from ...models.topic_statistics_output_stats import TopicStatisticsOutputStats
from ...types import Response


def _get_kwargs(
    *,
    body: TopicStatisticsInputStats,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/kidra/delete/topic-statistics",
    }

    _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[TopicStatisticsHTTPValidationError, TopicStatisticsOutputStats]]:
    if response.status_code == 200:
        response_200 = TopicStatisticsOutputStats.from_dict(response.json())

        return response_200
    if response.status_code == 422:
        response_422 = TopicStatisticsHTTPValidationError.from_dict(response.json())

        return response_422
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[TopicStatisticsHTTPValidationError, TopicStatisticsOutputStats]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    body: TopicStatisticsInputStats,
) -> Response[Union[TopicStatisticsHTTPValidationError, TopicStatisticsOutputStats]]:
    """Delete cached data entry for: Counts

    Args:
        body (TopicStatisticsInputStats):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[TopicStatisticsHTTPValidationError, TopicStatisticsOutputStats]]
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
    body: TopicStatisticsInputStats,
) -> Optional[Union[TopicStatisticsHTTPValidationError, TopicStatisticsOutputStats]]:
    """Delete cached data entry for: Counts

    Args:
        body (TopicStatisticsInputStats):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[TopicStatisticsHTTPValidationError, TopicStatisticsOutputStats]
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    body: TopicStatisticsInputStats,
) -> Response[Union[TopicStatisticsHTTPValidationError, TopicStatisticsOutputStats]]:
    """Delete cached data entry for: Counts

    Args:
        body (TopicStatisticsInputStats):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[TopicStatisticsHTTPValidationError, TopicStatisticsOutputStats]]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    body: TopicStatisticsInputStats,
) -> Optional[Union[TopicStatisticsHTTPValidationError, TopicStatisticsOutputStats]]:
    """Delete cached data entry for: Counts

    Args:
        body (TopicStatisticsInputStats):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[TopicStatisticsHTTPValidationError, TopicStatisticsOutputStats]
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
