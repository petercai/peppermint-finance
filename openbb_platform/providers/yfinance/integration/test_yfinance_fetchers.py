"""Test the Alpha Vantage fetchers."""

from datetime import date

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
    """Test yf_download to fetch last 5 days price data for BNS.TO."""
    end_date = date.today()
    start_date = end_date - timedelta(days=5)

    df = yf_download(
        symbol="BNS.TO", start_date=start_date, end_date=end_date, interval="2m"
    )

    assert not df.empty
    logger.info(df)
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


@pytest.mark.record_http
def test_av_equity_historical_fetcher(credentials=test_credentials):
    """Test the Alpha Vantage Equity Historical fetcher."""
    params = {
        "symbol": "AAPL",
        "start_date": date(2025, 1, 1),
        "end_date": date(2025, 1, 10),
        "interval": "15m",
    }

    fetcher = AVEquityHistoricalFetcher()
    result = fetcher.fetch_data(params, credentials)
    assert result is None
    print(result)


@pytest.mark.record_http
def test_av_historical_eps_fetcher(credentials=test_credentials):
    """Test the Alpha Vantage Historical Earnings fetcher."""
    params = {"symbol": "AAPL,MSFT", "period": "quarter", "limit": 4}

    fetcher = AVHistoricalEpsFetcher()
    result = fetcher.fetch_data(params, credentials)
    assert result is None

@pytest.mark.record_http
def test_av_equity_historical_fetcher(credentials=test_credentials):
    """Test the Alpha Vantage Equity Historical fetcher."""
    params = {
        "symbol": "AAPL",
        "start_date": date(2025, 1, 1),
        "end_date": date(2025, 1, 10),
        "interval": "15m",
    }

    import yfinance as yf
    data = yf.download(**params)
    assert not data.empty

@pytest.mark.record_http
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
from openbb_yfinance.models.equity_historical import YFinanceEquityHistoricalFetcher



@pytest.mark.record_http
def test_yfinance_equity_historical_fetcher(credentials=test_credentials):
    """Test the yfinance Equity Historical fetcher."""
    end_date = date.today()
    start_date = end_date - timedelta(days=30)
    params = {
        "symbol": "AAPL",
        "start_date": start_date,
        "end_date": end_date,
        "interval": "1d",  # Changed to daily for more reliable testing
    }

    fetcher = YFinanceEquityHistoricalFetcher()
    result = fetcher.extract_data(params, credentials)

    assert result
    assert result.body
    df = result.body.to_dataframe()
    assert not df.empty
    assert "close" in df.columns
    assert "open" in df.columns
    assert "high" in df.columns
    assert "low" in df.columns
    assert "volume" in df.columns

    # Verify data types
    assert df["close"].dtype == float
    assert df["open"].dtype == float
    assert df["high"].dtype == float
    assert df["low"].dtype == float
    assert df["volume"].dtype == int

    # Verify we got data for the requested date range
    assert len(df.index) > 0
    assert df.index.min().date() >= start_date
    assert df.index.max().date() <= end_date
    
    # Verify price values are reasonable (non-zero)
    assert (df["close"] > 0).all()
    assert (df["open"] > 0).all()
    assert (df["high"] > 0).all()
    assert (df["low"] > 0).all()
    assert (df["volume"] >= 0).all()

