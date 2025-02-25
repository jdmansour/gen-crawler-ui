from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.data import Data
from ...models.http_validation_error import HTTPValidationError
from ...models.result import Result
from ...types import Response


def _get_kwargs(
    *,
    body: Data,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/kidra/link-wikipedia",
    }

    _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[HTTPValidationError, Result]]:
    if response.status_code == 200:
        response_200 = Result.from_dict(response.json())

        return response_200
    if response.status_code == 422:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[HTTPValidationError, Result]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    body: Data,
) -> Response[Union[HTTPValidationError, Result]]:
    """Collect relevant Wikipedia articles for the given text

     Collect relevant Wikipedia articles for the given text

            Parameters
            ----------
            text : str
                The text to be analyzed.

            Returns
            -------
            text : str
                A modified version of the given text,
                where matched phrases are replaced with hyperlinks to their
                corresponding Wikipedia entry.
            entities : list of Entity
                All Wikipedia entries that were matched for the given text.
                Contains the following attributes:

                entity : str
                    The name of the entry.
                start : int
                    The start position of the phrase that was matched to this entity.
                end : int
                    The end position of the phrase that was matched to this entity.
                score : float
                    The score (from 0 to 1) of the match.
                categories : list of str
                    The German Wikipedia categories associated with this entity.
            essentialCategories : list of str
                A list of German Wikipedia categories that are shared between
                multiple associated entities.
            version : str
                The version of the Wikipedia linking service.
                Currently a placeholder.

    Args:
        body (Data):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, Result]]
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
    body: Data,
) -> Optional[Union[HTTPValidationError, Result]]:
    """Collect relevant Wikipedia articles for the given text

     Collect relevant Wikipedia articles for the given text

            Parameters
            ----------
            text : str
                The text to be analyzed.

            Returns
            -------
            text : str
                A modified version of the given text,
                where matched phrases are replaced with hyperlinks to their
                corresponding Wikipedia entry.
            entities : list of Entity
                All Wikipedia entries that were matched for the given text.
                Contains the following attributes:

                entity : str
                    The name of the entry.
                start : int
                    The start position of the phrase that was matched to this entity.
                end : int
                    The end position of the phrase that was matched to this entity.
                score : float
                    The score (from 0 to 1) of the match.
                categories : list of str
                    The German Wikipedia categories associated with this entity.
            essentialCategories : list of str
                A list of German Wikipedia categories that are shared between
                multiple associated entities.
            version : str
                The version of the Wikipedia linking service.
                Currently a placeholder.

    Args:
        body (Data):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, Result]
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    body: Data,
) -> Response[Union[HTTPValidationError, Result]]:
    """Collect relevant Wikipedia articles for the given text

     Collect relevant Wikipedia articles for the given text

            Parameters
            ----------
            text : str
                The text to be analyzed.

            Returns
            -------
            text : str
                A modified version of the given text,
                where matched phrases are replaced with hyperlinks to their
                corresponding Wikipedia entry.
            entities : list of Entity
                All Wikipedia entries that were matched for the given text.
                Contains the following attributes:

                entity : str
                    The name of the entry.
                start : int
                    The start position of the phrase that was matched to this entity.
                end : int
                    The end position of the phrase that was matched to this entity.
                score : float
                    The score (from 0 to 1) of the match.
                categories : list of str
                    The German Wikipedia categories associated with this entity.
            essentialCategories : list of str
                A list of German Wikipedia categories that are shared between
                multiple associated entities.
            version : str
                The version of the Wikipedia linking service.
                Currently a placeholder.

    Args:
        body (Data):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, Result]]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    body: Data,
) -> Optional[Union[HTTPValidationError, Result]]:
    """Collect relevant Wikipedia articles for the given text

     Collect relevant Wikipedia articles for the given text

            Parameters
            ----------
            text : str
                The text to be analyzed.

            Returns
            -------
            text : str
                A modified version of the given text,
                where matched phrases are replaced with hyperlinks to their
                corresponding Wikipedia entry.
            entities : list of Entity
                All Wikipedia entries that were matched for the given text.
                Contains the following attributes:

                entity : str
                    The name of the entry.
                start : int
                    The start position of the phrase that was matched to this entity.
                end : int
                    The end position of the phrase that was matched to this entity.
                score : float
                    The score (from 0 to 1) of the match.
                categories : list of str
                    The German Wikipedia categories associated with this entity.
            essentialCategories : list of str
                A list of German Wikipedia categories that are shared between
                multiple associated entities.
            version : str
                The version of the Wikipedia linking service.
                Currently a placeholder.

    Args:
        body (Data):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, Result]
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
