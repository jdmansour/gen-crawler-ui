from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.qa_node import QANode
from ...types import Response


def _get_kwargs(
    source_id: str,
    node_id: str,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/qa/{source_id}/{node_id}/node",
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[QANode, str]]:
    if response.status_code == 404:
        response_404 = cast(str, response.json())
        return response_404
    if response.status_code == 400:
        response_400 = cast(str, response.json())
        return response_400
    if response.status_code == 500:
        response_500 = cast(str, response.json())
        return response_500
    if response.status_code == 200:
        response_200 = QANode.from_dict(response.text)

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[QANode, str]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    source_id: str,
    node_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[Union[QANode, str]]:
    """Get QA Node of a specific sourceId and nodeId

    Args:
        source_id (str):
        node_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[QANode, str]]
    """

    kwargs = _get_kwargs(
        source_id=source_id,
        node_id=node_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    source_id: str,
    node_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[Union[QANode, str]]:
    """Get QA Node of a specific sourceId and nodeId

    Args:
        source_id (str):
        node_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[QANode, str]
    """

    return sync_detailed(
        source_id=source_id,
        node_id=node_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    source_id: str,
    node_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[Union[QANode, str]]:
    """Get QA Node of a specific sourceId and nodeId

    Args:
        source_id (str):
        node_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[QANode, str]]
    """

    kwargs = _get_kwargs(
        source_id=source_id,
        node_id=node_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    source_id: str,
    node_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[Union[QANode, str]]:
    """Get QA Node of a specific sourceId and nodeId

    Args:
        source_id (str):
        node_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[QANode, str]
    """

    return (
        await asyncio_detailed(
            source_id=source_id,
            node_id=node_id,
            client=client,
        )
    ).parsed
