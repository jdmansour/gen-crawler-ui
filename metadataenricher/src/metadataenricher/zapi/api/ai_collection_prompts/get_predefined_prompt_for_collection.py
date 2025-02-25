from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.get_predefined_prompt_for_collection_mode import GetPredefinedPromptForCollectionMode
from ...types import UNSET, Response


def _get_kwargs(
    collection_id: str,
    *,
    mode: GetPredefinedPromptForCollectionMode,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    json_mode = mode.value
    params["mode"] = json_mode

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": f"/ai/prompt/collection/public/{collection_id}",
        "params": params,
    }

    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[str]:
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
        response_200 = response.text
        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[str]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    collection_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    mode: GetPredefinedPromptForCollectionMode,
) -> Response[str]:
    """
    Args:
        collection_id (str):
        mode (GetPredefinedPromptForCollectionMode):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[str]
    """

    kwargs = _get_kwargs(
        collection_id=collection_id,
        mode=mode,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    collection_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    mode: GetPredefinedPromptForCollectionMode,
) -> Optional[str]:
    """
    Args:
        collection_id (str):
        mode (GetPredefinedPromptForCollectionMode):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        str
    """

    return sync_detailed(
        collection_id=collection_id,
        client=client,
        mode=mode,
    ).parsed


async def asyncio_detailed(
    collection_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    mode: GetPredefinedPromptForCollectionMode,
) -> Response[str]:
    """
    Args:
        collection_id (str):
        mode (GetPredefinedPromptForCollectionMode):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[str]
    """

    kwargs = _get_kwargs(
        collection_id=collection_id,
        mode=mode,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    collection_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    mode: GetPredefinedPromptForCollectionMode,
) -> Optional[str]:
    """
    Args:
        collection_id (str):
        mode (GetPredefinedPromptForCollectionMode):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        str
    """

    return (
        await asyncio_detailed(
            collection_id=collection_id,
            client=client,
            mode=mode,
        )
    ).parsed
