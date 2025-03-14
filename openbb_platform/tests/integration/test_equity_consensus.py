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
log_file = os.path.join(log_dir, "consensus.log")
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


# @pytest.mark.parametrize("provider", obb.equity.estimates.consensus.provider_choices)
def test_get_all_equity_consensus_providers(provider):
    """
    Tests the equity consensus endpoint for all available providers.

    This test is parametrized to run once for each provider in the
    `available_providers` list. It asserts that the result is a
    non-empty pandas DataFrame.
    
    run: pytest tests\integration\test_equity_consensus.py::test_get_all_equity_consensus_providers


    Parameters
    ----------
    provider : str
        The provider to use for the test.

    """
    result = obb.equity.consensus.get(provider=provider)
    assert isinstance(result, pd.DataFrame), f"Expected DataFrame, got {type(result)}"
    assert not result.empty, "Result should not be empty"
    result = obb.equity.consensus.get(provider=provider)
    assert isinstance(result, pd.DataFrame), f"Expected DataFrame, got {type(result)}"
    assert not result.empty, "Result should not be empty"
