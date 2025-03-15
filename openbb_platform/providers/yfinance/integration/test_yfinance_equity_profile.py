"""Test the Alpha Vantage fetchers."""

from datetime import date, timedelta

import pytest

from openbb_core.app.service.user_service import UserService
from openbb_yfinance import YFinanceEquityProfileFetcher
from openbb_yfinance.models.equity_historical import YFinanceEquityHistoricalFetcher, YFinanceEquityHistoricalData
from openbb_yfinance.models.equity_profile import YFinanceEquityProfileData
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
log_file = os.path.join(log_dir, "profile.log")
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

@pytest.mark.asyncio
async def test_yfinance_equity_profile_fetcher():
    """Test the yfinance Equity Profile fetcher."""
    params = {
        "symbol": "BNS.TO, RY.TO",
    }

    fetcher = YFinanceEquityProfileFetcher()
    result = await fetcher.fetch_data(params, credentials=test_credentials)

    assert result
    # assert isinstance(result, YFinanceEquityProfileData)

    # Validate some expected fields
    # assert isinstance(result.symbol, str)
    # assert isinstance(result.longName, str)
    # assert isinstance(result.sector, str)
    # assert isinstance(result.industry, str)
    # assert isinstance(result.country, str)
    # assert isinstance(result.marketCap, int)

    logger.info(result)




    




