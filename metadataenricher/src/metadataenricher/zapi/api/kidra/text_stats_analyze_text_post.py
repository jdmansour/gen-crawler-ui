from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.input_data import InputData
from ...models.text_statistics_http_validation_error import TextStatisticsHTTPValidationError
from ...models.text_statistics_result import TextStatisticsResult
from ...types import Response


def _get_kwargs(
    *,
    body: InputData,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/kidra/text-statistics",
    }

    _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[TextStatisticsHTTPValidationError, TextStatisticsResult]]:
    if response.status_code == 200:
        response_200 = TextStatisticsResult.from_dict(response.json())

        return response_200
    if response.status_code == 422:
        response_422 = TextStatisticsHTTPValidationError.from_dict(response.json())

        return response_422
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[TextStatisticsHTTPValidationError, TextStatisticsResult]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    body: InputData,
) -> Response[Union[TextStatisticsHTTPValidationError, TextStatisticsResult]]:
    """Compute text statistics on the given text

     Note: Only German language is supported right now.

        Parameters
        ----------
        text : str
            The text to be analyzed.
        reading_speed : float, optional
            The reading speed in characters per minute to use as a base-line.
            Default: 200
        generate_embeddings : bool, optional
            Whether to also generate a vectorized representation of the text using
            word embeddings.


        Returns
        -------
        flesch_ease : float or null
            The readability score of the text,
            according to the Flesch reading ease.
            null if undefined (i.e. text is empty).
        flesch_classification : str or null
            Interpretation of the Flesch readability score,
            from 'Sehr leicht' to 'Sehr schwer'.
            null if undefined (i.e. text is empty).
        wiener_index : float or null
            The appropriate school grade of the text, based on its readability,
            according to the Wiener index.
            null if undefined (i.e. text is empty).
        reading_time : float or null
            The predicted time to read the text, in seconds.
            This is adjusted for the readability of the text,
            according to the following formula:
            reading_speed / 2 * exp(log(4) * flesch_ease / 121.5).
            Thus, reading speed is doubled at the maximum readability
            (121.5) and halved at readability 0.
            null if undefined (i.e. text is empty).
        embeddings : list[float] or null
            If ``generate_embeddings`` was set to `True`, this will be the
            vectorized representation of the text. Otherwise, `null`.
        version : str
            The version of the text statistics service.

    Args:
        body (InputData):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[TextStatisticsHTTPValidationError, TextStatisticsResult]]
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
    body: InputData,
) -> Optional[Union[TextStatisticsHTTPValidationError, TextStatisticsResult]]:
    """Compute text statistics on the given text

     Note: Only German language is supported right now.

        Parameters
        ----------
        text : str
            The text to be analyzed.
        reading_speed : float, optional
            The reading speed in characters per minute to use as a base-line.
            Default: 200
        generate_embeddings : bool, optional
            Whether to also generate a vectorized representation of the text using
            word embeddings.


        Returns
        -------
        flesch_ease : float or null
            The readability score of the text,
            according to the Flesch reading ease.
            null if undefined (i.e. text is empty).
        flesch_classification : str or null
            Interpretation of the Flesch readability score,
            from 'Sehr leicht' to 'Sehr schwer'.
            null if undefined (i.e. text is empty).
        wiener_index : float or null
            The appropriate school grade of the text, based on its readability,
            according to the Wiener index.
            null if undefined (i.e. text is empty).
        reading_time : float or null
            The predicted time to read the text, in seconds.
            This is adjusted for the readability of the text,
            according to the following formula:
            reading_speed / 2 * exp(log(4) * flesch_ease / 121.5).
            Thus, reading speed is doubled at the maximum readability
            (121.5) and halved at readability 0.
            null if undefined (i.e. text is empty).
        embeddings : list[float] or null
            If ``generate_embeddings`` was set to `True`, this will be the
            vectorized representation of the text. Otherwise, `null`.
        version : str
            The version of the text statistics service.

    Args:
        body (InputData):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[TextStatisticsHTTPValidationError, TextStatisticsResult]
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    body: InputData,
) -> Response[Union[TextStatisticsHTTPValidationError, TextStatisticsResult]]:
    """Compute text statistics on the given text

     Note: Only German language is supported right now.

        Parameters
        ----------
        text : str
            The text to be analyzed.
        reading_speed : float, optional
            The reading speed in characters per minute to use as a base-line.
            Default: 200
        generate_embeddings : bool, optional
            Whether to also generate a vectorized representation of the text using
            word embeddings.


        Returns
        -------
        flesch_ease : float or null
            The readability score of the text,
            according to the Flesch reading ease.
            null if undefined (i.e. text is empty).
        flesch_classification : str or null
            Interpretation of the Flesch readability score,
            from 'Sehr leicht' to 'Sehr schwer'.
            null if undefined (i.e. text is empty).
        wiener_index : float or null
            The appropriate school grade of the text, based on its readability,
            according to the Wiener index.
            null if undefined (i.e. text is empty).
        reading_time : float or null
            The predicted time to read the text, in seconds.
            This is adjusted for the readability of the text,
            according to the following formula:
            reading_speed / 2 * exp(log(4) * flesch_ease / 121.5).
            Thus, reading speed is doubled at the maximum readability
            (121.5) and halved at readability 0.
            null if undefined (i.e. text is empty).
        embeddings : list[float] or null
            If ``generate_embeddings`` was set to `True`, this will be the
            vectorized representation of the text. Otherwise, `null`.
        version : str
            The version of the text statistics service.

    Args:
        body (InputData):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[TextStatisticsHTTPValidationError, TextStatisticsResult]]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    body: InputData,
) -> Optional[Union[TextStatisticsHTTPValidationError, TextStatisticsResult]]:
    """Compute text statistics on the given text

     Note: Only German language is supported right now.

        Parameters
        ----------
        text : str
            The text to be analyzed.
        reading_speed : float, optional
            The reading speed in characters per minute to use as a base-line.
            Default: 200
        generate_embeddings : bool, optional
            Whether to also generate a vectorized representation of the text using
            word embeddings.


        Returns
        -------
        flesch_ease : float or null
            The readability score of the text,
            according to the Flesch reading ease.
            null if undefined (i.e. text is empty).
        flesch_classification : str or null
            Interpretation of the Flesch readability score,
            from 'Sehr leicht' to 'Sehr schwer'.
            null if undefined (i.e. text is empty).
        wiener_index : float or null
            The appropriate school grade of the text, based on its readability,
            according to the Wiener index.
            null if undefined (i.e. text is empty).
        reading_time : float or null
            The predicted time to read the text, in seconds.
            This is adjusted for the readability of the text,
            according to the following formula:
            reading_speed / 2 * exp(log(4) * flesch_ease / 121.5).
            Thus, reading speed is doubled at the maximum readability
            (121.5) and halved at readability 0.
            null if undefined (i.e. text is empty).
        embeddings : list[float] or null
            If ``generate_embeddings`` was set to `True`, this will be the
            vectorized representation of the text. Otherwise, `null`.
        version : str
            The version of the text statistics service.

    Args:
        body (InputData):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[TextStatisticsHTTPValidationError, TextStatisticsResult]
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
