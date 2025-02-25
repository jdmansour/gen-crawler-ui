from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.arge_berufe_net_request import ArgeBerufeNetRequest
from ...types import Response


def _get_kwargs(
    *,
    body: list["ArgeBerufeNetRequest"],
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/data/arge/berufenet",
    }

    _body = []
    for body_item_data in body:
        body_item = body_item_data.to_dict()
        _body.append(body_item)

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[list["ArgeBerufeNetRequest"], str]]:
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
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = ArgeBerufeNetRequest.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[list["ArgeBerufeNetRequest"], str]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    body: list["ArgeBerufeNetRequest"],
) -> Response[Union[list["ArgeBerufeNetRequest"], str]]:
    """Endpoint to add or update data to the Arge Berufenet dataset

    Args:
        body (list['ArgeBerufeNetRequest']):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[list['ArgeBerufeNetRequest'], str]]
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
    body: list["ArgeBerufeNetRequest"],
) -> Optional[Union[list["ArgeBerufeNetRequest"], str]]:
    """Endpoint to add or update data to the Arge Berufenet dataset

    Args:
        body (list['ArgeBerufeNetRequest']):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[list['ArgeBerufeNetRequest'], str]
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    body: list["ArgeBerufeNetRequest"],
) -> Response[Union[list["ArgeBerufeNetRequest"], str]]:
    """Endpoint to add or update data to the Arge Berufenet dataset

    Args:
        body (list['ArgeBerufeNetRequest']):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[list['ArgeBerufeNetRequest'], str]]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    body: list["ArgeBerufeNetRequest"],
) -> Optional[Union[list["ArgeBerufeNetRequest"], str]]:
    """Endpoint to add or update data to the Arge Berufenet dataset

    Args:
        body (list['ArgeBerufeNetRequest']):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[list['ArgeBerufeNetRequest'], str]
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
