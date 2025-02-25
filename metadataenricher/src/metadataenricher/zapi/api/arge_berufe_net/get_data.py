from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.arge_berufe_net_response_page import ArgeBerufeNetResponsePage
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    page: Union[Unset, Any] = 0,
    size: Union[Unset, Any] = 20,
    sort: Union[Unset, Any] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["page"] = page

    params["size"] = size

    params["sort"] = sort

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/data/arge/berufenet",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[ArgeBerufeNetResponsePage, str]]:
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
        response_200 = ArgeBerufeNetResponsePage.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[ArgeBerufeNetResponsePage, str]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    page: Union[Unset, Any] = 0,
    size: Union[Unset, Any] = 20,
    sort: Union[Unset, Any] = UNSET,
) -> Response[Union[ArgeBerufeNetResponsePage, str]]:
    """Endpoint to retrieve data from the cached Arge Berufenet dataset

    Args:
        page (Union[Unset, Any]):  Default: 0.
        size (Union[Unset, Any]):  Default: 20.
        sort (Union[Unset, Any]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ArgeBerufeNetResponsePage, str]]
    """

    kwargs = _get_kwargs(
        page=page,
        size=size,
        sort=sort,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    page: Union[Unset, Any] = 0,
    size: Union[Unset, Any] = 20,
    sort: Union[Unset, Any] = UNSET,
) -> Optional[Union[ArgeBerufeNetResponsePage, str]]:
    """Endpoint to retrieve data from the cached Arge Berufenet dataset

    Args:
        page (Union[Unset, Any]):  Default: 0.
        size (Union[Unset, Any]):  Default: 20.
        sort (Union[Unset, Any]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ArgeBerufeNetResponsePage, str]
    """

    return sync_detailed(
        client=client,
        page=page,
        size=size,
        sort=sort,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    page: Union[Unset, Any] = 0,
    size: Union[Unset, Any] = 20,
    sort: Union[Unset, Any] = UNSET,
) -> Response[Union[ArgeBerufeNetResponsePage, str]]:
    """Endpoint to retrieve data from the cached Arge Berufenet dataset

    Args:
        page (Union[Unset, Any]):  Default: 0.
        size (Union[Unset, Any]):  Default: 20.
        sort (Union[Unset, Any]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ArgeBerufeNetResponsePage, str]]
    """

    kwargs = _get_kwargs(
        page=page,
        size=size,
        sort=sort,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    page: Union[Unset, Any] = 0,
    size: Union[Unset, Any] = 20,
    sort: Union[Unset, Any] = UNSET,
) -> Optional[Union[ArgeBerufeNetResponsePage, str]]:
    """Endpoint to retrieve data from the cached Arge Berufenet dataset

    Args:
        page (Union[Unset, Any]):  Default: 0.
        size (Union[Unset, Any]):  Default: 20.
        sort (Union[Unset, Any]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ArgeBerufeNetResponsePage, str]
    """

    return (
        await asyncio_detailed(
            client=client,
            page=page,
            size=size,
            sort=sort,
        )
    ).parsed
