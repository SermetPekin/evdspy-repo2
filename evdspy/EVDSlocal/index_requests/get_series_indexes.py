from typing import Union, Any, Optional

import pandas as pd

from evdspy.EVDSlocal.config.apikey_class import ApikeyClass
from evdspy.EVDSlocal.index_requests.get_series_indexes_utils import default_start_date_fnc, default_end_date_fnc
from evdspy.EVDSlocal.index_requests.user_requests import ProxyManager, UrlBuilder, UrlSeries, ApiRequester, \
    DataProcessor, RequestConfig


def initial_api_process_when_given(api_key: str = None):
    if api_key:
        if ApikeyClass().get_valid_api_key(check=False) is False:
            from evdspy.EVDSlocal.initial.load_commands_cmds_to_load import save_apikey
            save_apikey(api_key)


def get_series(
        index: Union[str, tuple[Any, ...]],
        start_date: str = default_start_date_fnc(),
        end_date: str = default_end_date_fnc(),
        frequency: Union[str, int, None] = None,
        formulas: Union[str, tuple[str, int, ...]] = None,
        aggregation: Union[str, None] = None,
        cache: bool = False,
        proxy: Optional[str] = None,
        proxies: Optional[dict[str, str]] = None,
        debug: bool = False,
        api_key: Optional[str] = None

) -> Union[pd.DataFrame, str]:
    """
    Retrieves economic data series from the specified API and returns it as a pandas DataFrame.

    Parameters
    ----------
    index : str or tuple of str
        The identifier(s) for the data series to fetch. Can be a single string for one series or a tuple of strings for multiple series.
    start_date : str, optional
        The start date for the data retrieval in 'DD-MM-YYYY' format, by default calls default_start_date_fnc().
    end_date : str, optional
        The end date for the data retrieval in 'DD-MM-YYYY' format, by default calls default_end_date_fnc().
    frequency : str, optional
        The frequency at which data should be retrieved. Examples include 'daily', 'monthly', 'yearly', etc.
    formulas : str or tuple of str, optional
        The computation methods to apply to the data series, such as 'average', 'sum', etc.
    aggregation : str or tuple of str, optional
        The aggregation methods to apply to the data, similar to formulas.
    cache : bool, optional
        If True, uses cached data when available to speed up the data retrieval process, by default False.
    proxy : str, optional
        The URL of the proxy server to use for the requests, by default None.
    proxies : dict, optional
        A dictionary of proxies to use for the request, by default None.
    debug : bool, optional
        If True, runs the function in debug mode, providing additional debug information without making a real API request, by default False.
    api_key : str, optional
        The API key required for accessing the data, by default None.
        When it was given for the first time it will be saved to a file for the subsequent requests.
        alternatively it may be saved by save("APIKEY") function or $ evdspy save [from console]
    Returns
    -------
    pd.DataFrame
        A pandas DataFrame containing the retrieved data series.

    Raises
    ------
    ValueError
        If an invalid API key is provided or required parameters are missing.

    Examples
    --------
    Basic usage:
    >>> template = "TP.ODEMGZS.BDTTOPLAM"
    >>> df = get_series2(template, start_date="01-01-2020", end_date="01-01-2021", frequency="monthly")
    >>> print(df.head())

    Using multiple indexes and cache:
    >>> indexes = ("TP.ODEMGZS.BDTTOPLAM", "TP.ODEMGZS.ABD")
    >>> df = get_series2(indexes, start_date="01-01-2020", frequency="monthly", cache=True)
    >>> print(df.head())

    Applying formulas and aggregation:
    >>> df = get_series2(template, start_date="01-01-2020", formulas="level", aggregation="sum")
    >>> print(df.head())
    """

    """initial_api_process_when_given"""
    initial_api_process_when_given(api_key)

    """RequestConfig"""
    config = RequestConfig(index=index,
                           start_date=start_date,
                           end_date=end_date,
                           frequency=frequency,
                           formulas=formulas,
                           aggregation=aggregation,
                           cache=cache

                           )

    """ProxyManager"""
    proxy_manager = ProxyManager(proxy=proxy, proxies=proxies)
    """UrlBuilder"""
    url_builder = UrlBuilder(config, url_type=UrlSeries())
    """ApiRequester"""
    api_requester = ApiRequester(url_builder, proxy_manager)
    if debug:
        return api_requester.dry_request()
    """DataProcessor"""
    data_processor = DataProcessor(api_requester())
    df = data_processor()
    print(df.head())
    return df


def test_get_series2(capsys):
    with capsys.disabled():
        # setup()
        df = get_series("TP.ODEMGZS.BDTTOPLAM",
                         cache=False)
        assert isinstance(df, pd.DataFrame)


def t_stream():
    import streamlit as st

    df = get_series("TP.ODEMGZS.BDTTOPLAM",
                     cache=True)

    st.write(df)


__all__ = (
    'get_series',
)
