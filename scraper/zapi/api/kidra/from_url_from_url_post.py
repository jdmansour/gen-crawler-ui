from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.text_extraction_data import TextExtractionData
from ...models.text_extraction_http_validation_error import TextExtractionHTTPValidationError
from ...models.text_extraction_result import TextExtractionResult
from ...types import Response


def _get_kwargs(
    *,
    body: TextExtractionData,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/kidra/text-extraction",
    }

    _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[TextExtractionHTTPValidationError, TextExtractionResult]]:
    if response.status_code == 200:
        response_200 = TextExtractionResult.from_dict(response.json())

        return response_200
    if response.status_code == 422:
        response_422 = TextExtractionHTTPValidationError.from_dict(response.json())

        return response_422
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[TextExtractionHTTPValidationError, TextExtractionResult]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    body: TextExtractionData,
) -> Response[Union[TextExtractionHTTPValidationError, TextExtractionResult]]:
    r"""Extract text from a given URL

     Extract text from a given URL

        Parameters
        ---------
        url : str
            The URL from which to extract text.
        lang : str, optional
            The ISO 639-1 code for the language of the text.
            If set to 'auto', try to detect it instead.
            Default: 'auto'.
        preference : str, optional
            Whether to prioritize precision, recall, or neither
            when extracting the text.
            Default: 'none'
        method : \"simple\" or \"browser\"
            Whether to get the content of the website naively, or to use a headless
            browser in order to e.g. deal with JavaScript-heavy pages.

        Returns
        -------
        text : str
            The extracted text.
        lang : str
            If lang was set to 'auto', the detected language.
            Otherwise, whatever lang was set to.
        version : str
            The version of the text extractor.

    Args:
        body (TextExtractionData):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[TextExtractionHTTPValidationError, TextExtractionResult]]
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
    body: TextExtractionData,
) -> Optional[Union[TextExtractionHTTPValidationError, TextExtractionResult]]:
    r"""Extract text from a given URL

     Extract text from a given URL

        Parameters
        ---------
        url : str
            The URL from which to extract text.
        lang : str, optional
            The ISO 639-1 code for the language of the text.
            If set to 'auto', try to detect it instead.
            Default: 'auto'.
        preference : str, optional
            Whether to prioritize precision, recall, or neither
            when extracting the text.
            Default: 'none'
        method : \"simple\" or \"browser\"
            Whether to get the content of the website naively, or to use a headless
            browser in order to e.g. deal with JavaScript-heavy pages.

        Returns
        -------
        text : str
            The extracted text.
        lang : str
            If lang was set to 'auto', the detected language.
            Otherwise, whatever lang was set to.
        version : str
            The version of the text extractor.

    Args:
        body (TextExtractionData):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[TextExtractionHTTPValidationError, TextExtractionResult]
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    body: TextExtractionData,
) -> Response[Union[TextExtractionHTTPValidationError, TextExtractionResult]]:
    r"""Extract text from a given URL

     Extract text from a given URL

        Parameters
        ---------
        url : str
            The URL from which to extract text.
        lang : str, optional
            The ISO 639-1 code for the language of the text.
            If set to 'auto', try to detect it instead.
            Default: 'auto'.
        preference : str, optional
            Whether to prioritize precision, recall, or neither
            when extracting the text.
            Default: 'none'
        method : \"simple\" or \"browser\"
            Whether to get the content of the website naively, or to use a headless
            browser in order to e.g. deal with JavaScript-heavy pages.

        Returns
        -------
        text : str
            The extracted text.
        lang : str
            If lang was set to 'auto', the detected language.
            Otherwise, whatever lang was set to.
        version : str
            The version of the text extractor.

    Args:
        body (TextExtractionData):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[TextExtractionHTTPValidationError, TextExtractionResult]]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    body: TextExtractionData,
) -> Optional[Union[TextExtractionHTTPValidationError, TextExtractionResult]]:
    r"""Extract text from a given URL

     Extract text from a given URL

        Parameters
        ---------
        url : str
            The URL from which to extract text.
        lang : str, optional
            The ISO 639-1 code for the language of the text.
            If set to 'auto', try to detect it instead.
            Default: 'auto'.
        preference : str, optional
            Whether to prioritize precision, recall, or neither
            when extracting the text.
            Default: 'none'
        method : \"simple\" or \"browser\"
            Whether to get the content of the website naively, or to use a headless
            browser in order to e.g. deal with JavaScript-heavy pages.

        Returns
        -------
        text : str
            The extracted text.
        lang : str
            If lang was set to 'auto', the detected language.
            Otherwise, whatever lang was set to.
        version : str
            The version of the text extractor.

    Args:
        body (TextExtractionData):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[TextExtractionHTTPValidationError, TextExtractionResult]
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
