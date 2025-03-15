"""Test the Alpha Vantage fetchers."""

from datetime import date, timedelta

from openbb_core.app.service.user_service import UserService
from openbb_yfinance.models.equity_historical import YFinanceEquityHistoricalFetcher, YFinanceEquityHistoricalData
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






    




