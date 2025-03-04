from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.professions_job_entity import ProfessionsJobEntity
from ...models.update_public_prompt_2_body import UpdatePublicPrompt2Body
from ...types import Response


def _get_kwargs(
    widget_node_id: str,
    context_node_id: str,
    *,
    body: UpdatePublicPrompt2Body,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "put",
        "url": f"/ai/prompt/profession/jobs/public/{widget_node_id}/{context_node_id}",
    }

    _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[ProfessionsJobEntity, str]]:
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
        response_200 = ProfessionsJobEntity.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[ProfessionsJobEntity, str]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    widget_node_id: str,
    context_node_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: UpdatePublicPrompt2Body,
) -> Response[Union[ProfessionsJobEntity, str]]:
    """Forces to prompt the ai service and updates the cached answer

    Args:
        widget_node_id (str):
        context_node_id (str):
        body (UpdatePublicPrompt2Body):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ProfessionsJobEntity, str]]
    """

    kwargs = _get_kwargs(
        widget_node_id=widget_node_id,
        context_node_id=context_node_id,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    widget_node_id: str,
    context_node_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: UpdatePublicPrompt2Body,
) -> Optional[Union[ProfessionsJobEntity, str]]:
    """Forces to prompt the ai service and updates the cached answer

    Args:
        widget_node_id (str):
        context_node_id (str):
        body (UpdatePublicPrompt2Body):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ProfessionsJobEntity, str]
    """

    return sync_detailed(
        widget_node_id=widget_node_id,
        context_node_id=context_node_id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    widget_node_id: str,
    context_node_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: UpdatePublicPrompt2Body,
) -> Response[Union[ProfessionsJobEntity, str]]:
    """Forces to prompt the ai service and updates the cached answer

    Args:
        widget_node_id (str):
        context_node_id (str):
        body (UpdatePublicPrompt2Body):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ProfessionsJobEntity, str]]
    """

    kwargs = _get_kwargs(
        widget_node_id=widget_node_id,
        context_node_id=context_node_id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    widget_node_id: str,
    context_node_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: UpdatePublicPrompt2Body,
) -> Optional[Union[ProfessionsJobEntity, str]]:
    """Forces to prompt the ai service and updates the cached answer

    Args:
        widget_node_id (str):
        context_node_id (str):
        body (UpdatePublicPrompt2Body):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ProfessionsJobEntity, str]
    """

    return (
        await asyncio_detailed(
            widget_node_id=widget_node_id,
            context_node_id=context_node_id,
            client=client,
            body=body,
        )
    ).parsed
