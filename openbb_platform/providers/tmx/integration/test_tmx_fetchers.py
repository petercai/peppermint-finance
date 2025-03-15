"""Test the Alpha Vantage fetchers."""

from datetime import date, timedelta

import pytest
from openbb_tmx.models.equity_historical import TmxEquityHistoricalFetcher
from openbb_core.app.service.user_service import UserService
import logging
from logging.handlers import RotatingFileHandler
import os

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
