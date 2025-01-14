from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.topic_assistant_embeddings_data import TopicAssistantEmbeddingsData
from ...models.topic_assistant_embeddings_http_validation_error import TopicAssistantEmbeddingsHTTPValidationError
from ...models.topic_assistant_embeddings_result import TopicAssistantEmbeddingsResult
from ...types import Response


def _get_kwargs(
    *,
    body: TopicAssistantEmbeddingsData,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/kidra/topic-assistant-embeddings",
    }

    _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[TopicAssistantEmbeddingsHTTPValidationError, TopicAssistantEmbeddingsResult]]:
    if response.status_code == 200:
        response_200 = TopicAssistantEmbeddingsResult.from_dict(response.json())

        return response_200
    if response.status_code == 422:
        response_422 = TopicAssistantEmbeddingsHTTPValidationError.from_dict(response.json())

        return response_422
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[TopicAssistantEmbeddingsHTTPValidationError, TopicAssistantEmbeddingsResult]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    body: TopicAssistantEmbeddingsData,
) -> Response[Union[TopicAssistantEmbeddingsHTTPValidationError, TopicAssistantEmbeddingsResult]]:
    """Predict topics from the OpenEduHub topic tree, using text embeddings

     Predict topics from the OpenEduHub topic tree, using text embeddings

            Parameters
            ----------
            text : str
                The text to be analyzed.

            Returns
            -------
            topics : list of Topic
                The predicted topics from the topic tree.
                Contains the following attributes:

                weight : int
                    The weight attributed to the sub tree.
                uri : str
                    The URI of the topic.
                label : str, optional
                    The label of the topic.
                match : null
                    Irrelevant for this function.
            version : str
                The version of the topic prediction tool.

    Args:
        body (TopicAssistantEmbeddingsData):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[TopicAssistantEmbeddingsHTTPValidationError, TopicAssistantEmbeddingsResult]]
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
    body: TopicAssistantEmbeddingsData,
) -> Optional[Union[TopicAssistantEmbeddingsHTTPValidationError, TopicAssistantEmbeddingsResult]]:
    """Predict topics from the OpenEduHub topic tree, using text embeddings

     Predict topics from the OpenEduHub topic tree, using text embeddings

            Parameters
            ----------
            text : str
                The text to be analyzed.

            Returns
            -------
            topics : list of Topic
                The predicted topics from the topic tree.
                Contains the following attributes:

                weight : int
                    The weight attributed to the sub tree.
                uri : str
                    The URI of the topic.
                label : str, optional
                    The label of the topic.
                match : null
                    Irrelevant for this function.
            version : str
                The version of the topic prediction tool.

    Args:
        body (TopicAssistantEmbeddingsData):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[TopicAssistantEmbeddingsHTTPValidationError, TopicAssistantEmbeddingsResult]
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    body: TopicAssistantEmbeddingsData,
) -> Response[Union[TopicAssistantEmbeddingsHTTPValidationError, TopicAssistantEmbeddingsResult]]:
    """Predict topics from the OpenEduHub topic tree, using text embeddings

     Predict topics from the OpenEduHub topic tree, using text embeddings

            Parameters
            ----------
            text : str
                The text to be analyzed.

            Returns
            -------
            topics : list of Topic
                The predicted topics from the topic tree.
                Contains the following attributes:

                weight : int
                    The weight attributed to the sub tree.
                uri : str
                    The URI of the topic.
                label : str, optional
                    The label of the topic.
                match : null
                    Irrelevant for this function.
            version : str
                The version of the topic prediction tool.

    Args:
        body (TopicAssistantEmbeddingsData):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[TopicAssistantEmbeddingsHTTPValidationError, TopicAssistantEmbeddingsResult]]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    body: TopicAssistantEmbeddingsData,
) -> Optional[Union[TopicAssistantEmbeddingsHTTPValidationError, TopicAssistantEmbeddingsResult]]:
    """Predict topics from the OpenEduHub topic tree, using text embeddings

     Predict topics from the OpenEduHub topic tree, using text embeddings

            Parameters
            ----------
            text : str
                The text to be analyzed.

            Returns
            -------
            topics : list of Topic
                The predicted topics from the topic tree.
                Contains the following attributes:

                weight : int
                    The weight attributed to the sub tree.
                uri : str
                    The URI of the topic.
                label : str, optional
                    The label of the topic.
                match : null
                    Irrelevant for this function.
            version : str
                The version of the topic prediction tool.

    Args:
        body (TopicAssistantEmbeddingsData):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[TopicAssistantEmbeddingsHTTPValidationError, TopicAssistantEmbeddingsResult]
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
