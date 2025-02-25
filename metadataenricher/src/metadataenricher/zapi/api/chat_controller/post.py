from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.assistant_message import AssistantMessage
from ...models.function_message import FunctionMessage
from ...models.system_message import SystemMessage
from ...models.tool_message import ToolMessage
from ...models.user_message import UserMessage
from ...types import Response


def _get_kwargs(
    *,
    body: list[Union["AssistantMessage", "FunctionMessage", "SystemMessage", "ToolMessage", "UserMessage"]],
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/chat",
    }

    _body = []
    for body_item_data in body:
        body_item: dict[str, Any]
        if isinstance(body_item_data, AssistantMessage):
            body_item = body_item_data.to_dict()
        elif isinstance(body_item_data, FunctionMessage):
            body_item = body_item_data.to_dict()
        elif isinstance(body_item_data, SystemMessage):
            body_item = body_item_data.to_dict()
        elif isinstance(body_item_data, ToolMessage):
            body_item = body_item_data.to_dict()
        else:
            body_item = body_item_data.to_dict()

        _body.append(body_item)

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Union["AssistantMessage", "FunctionMessage", "SystemMessage", "ToolMessage", "UserMessage"], str]]:
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

        def _parse_response_200(
            data: object,
        ) -> Union["AssistantMessage", "FunctionMessage", "SystemMessage", "ToolMessage", "UserMessage"]:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                response_200_type_0 = AssistantMessage.from_dict(data)

                return response_200_type_0
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                response_200_type_1 = FunctionMessage.from_dict(data)

                return response_200_type_1
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                response_200_type_2 = SystemMessage.from_dict(data)

                return response_200_type_2
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                response_200_type_3 = ToolMessage.from_dict(data)

                return response_200_type_3
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            response_200_type_4 = UserMessage.from_dict(data)

            return response_200_type_4

        response_200 = _parse_response_200(response.text)

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[Union["AssistantMessage", "FunctionMessage", "SystemMessage", "ToolMessage", "UserMessage"], str]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    body: list[Union["AssistantMessage", "FunctionMessage", "SystemMessage", "ToolMessage", "UserMessage"]],
) -> Response[Union[Union["AssistantMessage", "FunctionMessage", "SystemMessage", "ToolMessage", "UserMessage"], str]]:
    """
    Args:
        body (list[Union['AssistantMessage', 'FunctionMessage', 'SystemMessage', 'ToolMessage',
            'UserMessage']]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Union['AssistantMessage', 'FunctionMessage', 'SystemMessage', 'ToolMessage', 'UserMessage'], str]]
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
    body: list[Union["AssistantMessage", "FunctionMessage", "SystemMessage", "ToolMessage", "UserMessage"]],
) -> Optional[Union[Union["AssistantMessage", "FunctionMessage", "SystemMessage", "ToolMessage", "UserMessage"], str]]:
    """
    Args:
        body (list[Union['AssistantMessage', 'FunctionMessage', 'SystemMessage', 'ToolMessage',
            'UserMessage']]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Union['AssistantMessage', 'FunctionMessage', 'SystemMessage', 'ToolMessage', 'UserMessage'], str]
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    body: list[Union["AssistantMessage", "FunctionMessage", "SystemMessage", "ToolMessage", "UserMessage"]],
) -> Response[Union[Union["AssistantMessage", "FunctionMessage", "SystemMessage", "ToolMessage", "UserMessage"], str]]:
    """
    Args:
        body (list[Union['AssistantMessage', 'FunctionMessage', 'SystemMessage', 'ToolMessage',
            'UserMessage']]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Union['AssistantMessage', 'FunctionMessage', 'SystemMessage', 'ToolMessage', 'UserMessage'], str]]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    body: list[Union["AssistantMessage", "FunctionMessage", "SystemMessage", "ToolMessage", "UserMessage"]],
) -> Optional[Union[Union["AssistantMessage", "FunctionMessage", "SystemMessage", "ToolMessage", "UserMessage"], str]]:
    """
    Args:
        body (list[Union['AssistantMessage', 'FunctionMessage', 'SystemMessage', 'ToolMessage',
            'UserMessage']]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Union['AssistantMessage', 'FunctionMessage', 'SystemMessage', 'ToolMessage', 'UserMessage'], str]
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
