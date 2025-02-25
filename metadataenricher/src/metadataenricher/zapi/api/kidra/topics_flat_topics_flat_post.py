from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.topic_assistant_keywords_data import TopicAssistantKeywordsData
from ...models.topic_assistant_keywords_http_validation_error import TopicAssistantKeywordsHTTPValidationError
from ...models.topic_assistant_keywords_result import TopicAssistantKeywordsResult
from ...types import Response


def _get_kwargs(
    *,
    body: TopicAssistantKeywordsData,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/kidra/topic-assistant-keywords",
    }

    _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[TopicAssistantKeywordsHTTPValidationError, TopicAssistantKeywordsResult]]:
    if response.status_code == 200:
        response_200 = TopicAssistantKeywordsResult.from_dict(response.json())

        return response_200
    if response.status_code == 422:
        response_422 = TopicAssistantKeywordsHTTPValidationError.from_dict(response.json())

        return response_422
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[TopicAssistantKeywordsHTTPValidationError, TopicAssistantKeywordsResult]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    body: TopicAssistantKeywordsData,
) -> Response[Union[TopicAssistantKeywordsHTTPValidationError, TopicAssistantKeywordsResult]]:
    """Predict topics from the OpenEduHub topic tree, using keywords

     Predict topics from the OpenEduHub topic tree, using keywords

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
                    The number of matches in the sub tree.
                uri : str
                    The URI of the topic.
                label : str, optional
                    The label of the topic.
                match : str, optional
                    The keyword in the text that was associated with the topic.
                    If there are multiple, comma separated.
            version : str
                The version of the topic prediction tool.

    Args:
        body (TopicAssistantKeywordsData):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[TopicAssistantKeywordsHTTPValidationError, TopicAssistantKeywordsResult]]
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
    body: TopicAssistantKeywordsData,
) -> Optional[Union[TopicAssistantKeywordsHTTPValidationError, TopicAssistantKeywordsResult]]:
    """Predict topics from the OpenEduHub topic tree, using keywords

     Predict topics from the OpenEduHub topic tree, using keywords

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
                    The number of matches in the sub tree.
                uri : str
                    The URI of the topic.
                label : str, optional
                    The label of the topic.
                match : str, optional
                    The keyword in the text that was associated with the topic.
                    If there are multiple, comma separated.
            version : str
                The version of the topic prediction tool.

    Args:
        body (TopicAssistantKeywordsData):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[TopicAssistantKeywordsHTTPValidationError, TopicAssistantKeywordsResult]
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    body: TopicAssistantKeywordsData,
) -> Response[Union[TopicAssistantKeywordsHTTPValidationError, TopicAssistantKeywordsResult]]:
    """Predict topics from the OpenEduHub topic tree, using keywords

     Predict topics from the OpenEduHub topic tree, using keywords

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
                    The number of matches in the sub tree.
                uri : str
                    The URI of the topic.
                label : str, optional
                    The label of the topic.
                match : str, optional
                    The keyword in the text that was associated with the topic.
                    If there are multiple, comma separated.
            version : str
                The version of the topic prediction tool.

    Args:
        body (TopicAssistantKeywordsData):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[TopicAssistantKeywordsHTTPValidationError, TopicAssistantKeywordsResult]]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    body: TopicAssistantKeywordsData,
) -> Optional[Union[TopicAssistantKeywordsHTTPValidationError, TopicAssistantKeywordsResult]]:
    """Predict topics from the OpenEduHub topic tree, using keywords

     Predict topics from the OpenEduHub topic tree, using keywords

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
                    The number of matches in the sub tree.
                uri : str
                    The URI of the topic.
                label : str, optional
                    The label of the topic.
                match : str, optional
                    The keyword in the text that was associated with the topic.
                    If there are multiple, comma separated.
            version : str
                The version of the topic prediction tool.

    Args:
        body (TopicAssistantKeywordsData):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[TopicAssistantKeywordsHTTPValidationError, TopicAssistantKeywordsResult]
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
