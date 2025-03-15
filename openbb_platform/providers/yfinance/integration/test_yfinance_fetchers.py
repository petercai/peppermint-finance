"""Test the Alpha Vantage fetchers."""

from datetime import date, datetime

import pytest

from openbb_core.app.service.user_service import UserService
from openbb_yfinance.utils.helpers import yf_download

test_credentials = UserService().default_user_settings.credentials.model_dump(
    mode="json"
)
import logging
from logging.handlers import RotatingFileHandler
import os

# Create logs directory if it doesn't exist
log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)

# Configure logging with RotatingFileHandler
log_file = os.path.join(log_dir, "yfinance.log")
handler = RotatingFileHandler(
    log_file,
    maxBytes=1_000_000,  # 1MB
    backupCount=3,  # Keep 3 backup files
    encoding='utf-8'
)
handler.setFormatter(
    logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
)

# Get logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(handler)


def test_yfinance_yf_download_bns_last_5_days(credentials=test_credentials):
    """
    $env:PYTHONPATH = ".\;.\core;.\extensions;.\providers;.\obbject_extensions\charting;providers\yfinance"
    pytest providers\yfinance\integration\test_yfinance_fetchers.py::test_yfinance_yf_download_bns_last_5_days
    pytest --cov=openbb --cov-report=html providers\yfinance\integration\test_yfinance_fetchers.py::test_yfinance_yf_download_bns_last_5_days
    
    """
    end_date = date.today()
    start_date = end_date - timedelta(days=30)

    df = yf_download(
        symbol="BNS.TO", start_date=start_date, end_date=end_date, interval="2m"
    )

    assert not df.empty
    logger.info(df)
    print(df)
    assert "close" in df.columns
    assert "open" in df.columns
    assert "high" in df.columns
    assert "low" in df.columns
    assert "volume" in df.columns
    assert "date" in df.columns

    # Verify data types
    assert df["close"].dtype == float
    assert df["open"].dtype == float
    assert df["high"].dtype == float
    assert df["low"].dtype == float
    assert df["volume"].dtype == int

    # Verify we got data for the requested date range
    # assert len(df) > 0
    # assert df["date"].min() >= start_date.strftime("%Y-%m-%d")
    # assert df["date"].max() <= end_date.strftime("%Y-%m-%d")

    # Verify price values are reasonable (non-zero)
    assert (df["close"] > 0).all()
    assert (df["open"] > 0).all()
    assert (df["high"] > 0).all()
    assert (df["low"] > 0).all()
    assert (df["volume"] >= 0).all()


def test_yfinance_equity_historical_fetcher(credentials=test_credentials):
    """
        run: pytest tests\integration\test_equity_price_historical.py::test_equity_price_historical_bns_with_yfinance
        cc:  pytest --cov=openbb --cov-report=html tests\integration\test_equity_price_historical.py::test_equity_price_historical_bns_with_yfinance
        
        $env:PYTHONPATH = ".\;.\core;.\extensions;.\providers;.\obbject_extensions\charting;providers\yfinance"
        pytest -s providers\yfinance\integration\test_yfinance_fetchers.py::test_yfinance_equity_historical_fetcher
        
    """
    end_date = date.today()
    start_date = end_date - timedelta(days=30)
    params = {
        "symbol": "AAPL",
        "start_date": start_date,
        "end_date": end_date,
        "interval": "2m",  # Changed to daily for more reliable testing
    }

    fetcher = YFinanceEquityHistoricalFetcher()
    result = fetcher.retrieve_data(params, credentials)
    assert result
    print(result)



def test_av_historical_eps_fetcher(credentials=test_credentials):
    """Test the Alpha Vantage Historical Earnings fetcher."""
    params = {"symbol": "AAPL", "period": "quarter"}

    import yfinance as yf
    ticker = yf.Ticker(params["symbol"])
    data = ticker.earnings
    assert data is not None
    
    
"""Test the yfinance fetchers."""

from datetime import date, timedelta

import pytest
from openbb_core.app.service.user_service import UserService
from openbb_yfinance.models.equity_historical import YFinanceEquityHistoricalFetcher, YFinanceEquityHistoricalData


def test_yfinance_equity_historical_fetcher2(credentials=test_credentials):
    """Test the yfinance Equity Historical fetcher."""
    end_date = date.today()
    start_date = end_date - timedelta(days=30)
    params = {
        "symbol": "AAPL",
        "start_date": start_date,
        "end_date": end_date,
        "interval": "2m",  # Changed to daily for more reliable testing
    }

    fetcher = YFinanceEquityHistoricalFetcher()
    query = fetcher.transform_query(params=params)
    if query is None:
        raise ValueError("Query must not be None.")
    # data = await maybe_coroutine(
    #     cls.extract_data, query=query, credentials=credentials, **kwargs
    # )
    data = fetcher.extract_data(query=query, credentials=credentials)
    if data is None:
        raise ValueError("Data must not be None.")
    result = fetcher.transform_data(query=query, data=data)

    assert result
    assert isinstance(result, list)
    assert len(result) > 0
    logger.info(result)
    for data_point in result:
        assert isinstance(data_point, YFinanceEquityHistoricalData)
        # assert isinstance(data_point.date, datetime.date)
        assert isinstance(data_point.open, float)
        assert isinstance(data_point.high, float)
        assert isinstance(data_point.low, float)
        assert isinstance(data_point.close, float)
        assert isinstance(data_point.volume, int)
        assert isinstance(data_point.split_ratio, (float, type(None)))
        assert isinstance(data_point.dividend, (float, type(None)))

        # Verify price values are reasonable (non-zero)
        assert data_point.close > 0
        assert data_point.open > 0
        assert data_point.high > 0
        assert data_point.low > 0
        assert data_point.volume >= 0

        # Verify split_ratio and dividend are either float or None
        if data_point.split_ratio is not None:
            assert data_point.split_ratio > 0
        if data_point.dividend is not None:
            assert data_point.dividend >= 0

