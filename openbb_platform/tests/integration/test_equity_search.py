import pytest
from datetime import datetime, timedelta
import pandas as pd
from openbb import obb
import logging
from logging.handlers import RotatingFileHandler
import os

# Create logs directory if it doesn't exist
log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)

# Configure logging with RotatingFileHandler
log_file = os.path.join(log_dir, "search.log")
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

def test_equity_search_tmx():
    
    """Test equity search functionality for TMX provider with query 'bns'.

    This test performs an equity search using the TMX provider for the query 'bns'.
    It logs each result returned by the search to ensure that the function is 
    correctly retrieving and handling the expected data.
    
    run: pytest tests\integration\test_equity_search.py::test_equity_search_tmx
    """

    results = obb.equity.search(provider="tmx", query="bns")
    for result in results:
        logger.info(result)


def test_equity_search_nasdaq(query='AAPL', provider='nasdaq'):
    """Test equity search functionality for NASDAQ provider with a given query.

    This test performs an equity search using the NASDAQ provider for the specified query.
    It logs each result returned by the search to ensure that the function is
    correctly retrieving and handling the expected data.

    Args:
        query (str): The query string to search for. Defaults to 'AAPL'.
        provider (str): The provider to use for the search. Defaults to 'nasdaq'.

    run: pytest tests\integration\test_equity_search.py::test_equity_search_nasdaq
    """

    try:
        results = obb.equity.search(query=query, is_symbol=False, use_cache=True, provider=provider)
        for result in results:
            logger.info(result)
    except Exception as e:
        logger.error(f"An error occurred during equity search: {e}")
        raise



def test_equity_search_all():
    # Test equity search using TMX provider
    """
    Test equity search using TMX provider with no query parameter
    run: pytest tests\integration\test_equity_search.py::test_equity_search_all
    """
    results = obb.equity.search(provider="tmx")
    for result in results:
        logger.info(result)
