"""Test the Alpha Vantage fetchers."""

import json
from datetime import date, timedelta

import pytest
from openbb_tmx.models.equity_historical import TmxEquityHistoricalFetcher
from openbb_core.app.service.user_service import UserService
import logging
from logging.handlers import RotatingFileHandler
import os
from openbb_tmx.utils.helpers import get_tmx_tickers
from openbb_tmx import (
    TmxEquityProfileFetcher,
    TmxEquityQuoteFetcher,
    TmxPriceTargetConsensusFetcher,
    TmxCompanyNewsFetcher,
    TmxCompanyFilingsFetcher,
    TmxCalendarEarningsFetcher,
    TmxHistoricalDividendsFetcher,
    TmxGainersFetcher
)
from openbb_tmx.models.equity_profile import TmxEquityProfileData
from openbb_tmx.models.equity_quote import TmxEquityQuoteData
from openbb_tmx.models.price_target_consensus import TmxPriceTargetConsensusData
from openbb_tmx.models.company_news import TmxCompanyNewsData
from openbb_tmx.models.company_filings import TmxCompanyFilingsData
from openbb_tmx.models.calendar_earnings import TmxCalendarEarningsData
from openbb_tmx.models.historical_dividends import TmxHistoricalDividendsData
from openbb_tmx.models.gainers import TmxGainersData

# Create logs directory if it doesn't exist
log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)

# Configure logging with RotatingFileHandler
log_file = os.path.join(log_dir, "price.log")
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


test_credentials = UserService().default_user_settings.credentials.model_dump(
    mode="json"
)


@pytest.mark.asyncio
async def test_tmx_equity_historical_fetcher(credentials=test_credentials):
    end_date = date.today()
    start_date = end_date - timedelta(days=10)
    params = {
        "symbol": "BNS",
        "start_date": start_date,
        "end_date": end_date,
        "interval": "2m",  # Changed to daily for more reliable testing
    }

    fetcher = TmxEquityHistoricalFetcher()
    result = await fetcher.fetch_data(params, credentials)
    assert result
    logger.info(result)
    print(result)


@pytest.mark.asyncio
async def test_tmx_equity_profile_fetcher():
    """Test the TMX Equity Profile fetcher for BNS."""
    params = {
        "symbol": "BNS",
    }

    fetcher = TmxEquityProfileFetcher()
    result = await fetcher.fetch_data(params, credentials=test_credentials)

    assert result
    # assert isinstance(result, TmxEquityProfileData)
    # assert result.symbol == "BNS"
    logger.info(result)


@pytest.mark.asyncio
async def test_tmx_equity_quote_fetcher():
    """Test the TMX Equity Quote fetcher for BNS."""
    params = {
        "symbol": "BNS",
    }

    fetcher = TmxEquityQuoteFetcher()
    result = await fetcher.fetch_data(params, credentials=test_credentials)

    assert result
    assert isinstance(result, list)
    assert len(result) > 0

    first_item = result[0]
    # assert isinstance(first_item, TmxEquityQuoteData)
    # assert first_item.symbol == "BNS"

    logger.info(result)


@pytest.mark.asyncio
async def test_tmx_price_target_consensus_fetcher():
    """Test the TMX Price Target Consensus fetcher for BNS."""
    params = {
        "symbol": "BNS",
    }

    fetcher = TmxPriceTargetConsensusFetcher()
    result = await fetcher.fetch_data(params, credentials=test_credentials)

    assert result
    # assert isinstance(result, TmxPriceTargetConsensusData)
    # assert result.symbol == "BNS"
    logger.info(result)


@pytest.mark.asyncio
async def test_tmx_company_news_fetcher():
    """Test the TMX Company News fetcher for BNS."""
    params = {
        "symbol": "BNS",
    }

    fetcher = TmxCompanyNewsFetcher()
    result = await fetcher.fetch_data(params, credentials=test_credentials)

    assert result
    assert isinstance(result, list)
    assert len(result) > 0

    first_item = result[0]
    # assert isinstance(first_item, TmxCompanyNewsData)
    # assert first_item.symbol == "BNS"
    logger.info(result)


@pytest.mark.asyncio
async def test_tmx_company_filings_fetcher():
    """Test the TMX Company Filings fetcher for BNS."""
    end_date = date.today()
    start_date = end_date - timedelta(days=90)
    params = {
        # "symbol": "BNS",
        "start_date": start_date,
        "end_date": end_date,
    }


    fetcher = TmxCompanyFilingsFetcher()
    result = await fetcher.fetch_data(params, credentials=test_credentials)

    assert result
    # assert isinstance(result, list)
    assert len(result) > 0
    logger.info(json.dumps(result, indent=4))

@pytest.mark.asyncio
async def test_tmx_calendar_earnings_fetcher():
    """Test the TMX Calendar Earnings fetcher for BNS."""
    params = {
        "symbol": "BNS",
    }

    fetcher = TmxCalendarEarningsFetcher()
    result = await fetcher.fetch_data(params, credentials=test_credentials)

    assert result
    # assert isinstance(result, TmxCalendarEarningsData)
    logger.info(result)

@pytest.mark.asyncio
async def test_tmx_historical_dividends_fetcher():
    """Test the TMX Historical Dividends fetcher for BNS."""
    params = {
        "symbol": "BNS",
    }

    fetcher = TmxHistoricalDividendsFetcher()
    result = await fetcher.fetch_data(params, credentials=test_credentials)

    assert result
    # assert isinstance(result, TmxHistoricalDividendsData)
    logger.info(result)

@pytest.mark.asyncio
async def test_tmx_gainers_fetcher():
    """Test the TMX Gainers fetcher."""
    params = {}  # Gainers doesn't require a symbol

    fetcher = TmxGainersFetcher()
    result = await fetcher.fetch_data(params, credentials=test_credentials)

    assert result
    # assert isinstance(result, list)
    assert len(result) > 0
    # assert isinstance(result[0], TmxGainersData)  
    logger.info(result)

