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

# Create logs directory if it doesn't exist
log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)

# Configure logging with RotatingFileHandler
log_file = os.path.join(log_dir, "helper.log")
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
async def test_get_tmx_tickers():
    """Test the get_tmx_tickers function."""
    result = await get_tmx_tickers()

    assert result
    # assert isinstance(result, list)
    assert len(result) > 0
    
    logger.info(
        json.dumps(result, indent=4)
    )
