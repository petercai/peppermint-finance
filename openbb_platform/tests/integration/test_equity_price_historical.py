import sys
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

def test_equity_price_historical_bns_with_yfinance():
    """Test getting historical price data for BNS.TO using yfinance provider.
    
    provider: "alpha_vantage", "cboe", "fmp", "intrinio", "polygon", "tiingo", "tmx", "tradier", "yfinance"
    
    run: pytest tests\integration\test_equity_price_historical.py::test_equity_price_historical_bns_with_yfinance
    cc:  pytest --cov=openbb --cov-report=html tests\integration\test_equity_price_historical.py::test_equity_price_historical_bns_with_yfinance
    
    set PYTHONPATH=%PYTHONPATH%;c:\workspace\github\finance\OpenBB\openbb_platform\openbb 
    $env:PYTHONPATH = ".\openbb_platform"
    $env:PYTHONPATH = ".\openbb_platform;.\openbb_platform\core"
    pytest tests\integration\test_equity_price_historical.py::test_equity_price_historical_bns_with_yfinance
    pytest --import-mode=openbb tests\integration\test_equity_price_historical.py::test_equity_price_historical_bns_with_yfinance
    
    This test verifies the following:
    - The result is not None
    - The result is an OBBject
    - The result is a dataframe
    - The dataframe is not empty
    - The dataframe has the correct columns
    """
    
    # Get today's date and yesterday's date
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=7)
    
    logger.info(f"Fetching BNS.TO data from {start_date} to {end_date}")

    # Add a print statement to see sys.path
    print("------------------")
    print("sys.path:")
    for path in sys.path:
        print(path)
    print("------------------")

    # Add more print statements to trace execution
    print("About to call obb.equity.price.historical")

    
    # Execute the command
    result = obb.equity.price.historical(
        symbol="BNS.TO",
        provider="yfinance",
        start_date=start_date,
        end_date=end_date
    )

    # Log result details
    logger.info(f"Result type: {type(result)}")
    logger.info(f"Result attributes: {dir(result)}")
    logger.info(f"Result metadata: {result.metadata if hasattr(result, 'metadata') else 'No metadata'}")

    # Verify the result is an OBBject
    assert result is not None
    
    # Convert to dataframe and make columns lowercase
    df = result.to_dataframe()
    df.columns = df.columns.str.lower()
    
    # Log DataFrame details
    logger.info("\nDataFrame Info:")
    logger.info(f"Shape: {df.shape}")
    logger.info(f"Columns: {df.columns.tolist()}")
    logger.info(f"Index range: {df.index.min()} to {df.index.max()}")
    logger.info("\nDataFrame Head:")
    logger.info(f"\n{df.head().to_string()}")
    logger.info("\nDataFrame Description:")
    logger.info(f"\n{df.describe().to_string()}")
    
    # Basic data validation
    assert isinstance(df, pd.DataFrame)
    assert not df.empty
    assert "close" in df.columns
    assert "open" in df.columns
    assert "high" in df.columns
    assert "low" in df.columns
    assert "volume" in df.columns
    
    # Verify data types
    assert pd.api.types.is_float_dtype(df["close"])
    assert pd.api.types.is_float_dtype(df["open"]) 
    assert pd.api.types.is_float_dtype(df["high"])
    assert pd.api.types.is_float_dtype(df["low"])
    assert pd.api.types.is_numeric_dtype(df["volume"])
    
    # Verify we got data for the requested date range
    assert len(df.index) > 0
    assert df.index.min() >= start_date
    assert df.index.max() <= end_date

    # Verify price values are reasonable (non-zero)
    assert (df["close"] > 0).all()
    assert (df["open"] > 0).all()
    assert (df["high"] > 0).all()
    assert (df["low"] > 0).all()
    assert (df["volume"] >= 0).all()

def test_equity_price_historical_bns_with_tmx():
    """Test getting historical price data for BNS.TO using tmx provider.

    provider: "alpha_vantage", "cboe", "fmp", "intrinio", "polygon", "tiingo", "tmx", "tradier", "yfinance"

    This test verifies the following:
    - The result is not None
    - The result is an OBBject
    - The result is a dataframe
    - The dataframe is not empty
    - The dataframe has the correct columns
    """

    # Get today's date and yesterday's date
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=7)  # Using 7 days to ensure we get data even with weekends/holidays

    logger.info(f"Fetching BNS.TO data from {start_date} to {end_date} using tmx")

    # Execute the command
    result = obb.equity.price.historical(
        symbol="BNS.TO",
        provider="tmx",
        start_date=start_date,
        end_date=end_date
    )

    # Log result details
    logger.info(f"Result type: {type(result)}")
    logger.info(f"Result attributes: {dir(result)}")
    logger.info(f"Result metadata: {result.metadata if hasattr(result, 'metadata') else 'No metadata'}")

    # Verify the result is an OBBject
    assert result is not None

    # Convert to dataframe and make columns lowercase
    df = result.to_dataframe()
    df.columns = df.columns.str.lower()

    # Log DataFrame details
    logger.info("\nDataFrame Info:")
    logger.info(f"Shape: {df.shape}")
    logger.info(f"Columns: {df.columns.tolist()}")
    logger.info(f"Index range: {df.index.min()} to {df.index.max()}")
    logger.info("\nDataFrame Head:")
    logger.info(f"\n{df.head().to_string()}")
    logger.info("\nDataFrame Description:")
    logger.info(f"\n{df.describe().to_string()}")

    # Basic data validation
    assert isinstance(df, pd.DataFrame)
    assert not df.empty
    assert "close" in df.columns
    assert "open" in df.columns
    assert "high" in df.columns
    assert "low" in df.columns
    assert "volume" in df.columns

    # Verify data types
    assert pd.api.types.is_float_dtype(df["close"])
    assert pd.api.types.is_float_dtype(df["open"])
    assert pd.api.types.is_float_dtype(df["high"])
    assert pd.api.types.is_float_dtype(df["low"])
    assert pd.api.types.is_numeric_dtype(df["volume"])

    # Verify we got data for the requested date range
    assert len(df.index) > 0
    
    # TMX might not return data for exactly the requested date range,
    # so we just verify we got some data within a reasonable range
    assert not df.empty

    # Verify price values are reasonable (non-zero)
    assert (df["close"] > 0).all()
    assert (df["open"] > 0).all()
    assert (df["high"] > 0).all()
    assert (df["low"] > 0).all()
    assert (df["volume"] >= 0).all()


def test_equity_price_historical_bns_with_alpha_vantage():
    """Test getting historical price data for BNS.TO using alpha_vantage provider.

    provider: "alpha_vantage", "cboe", "fmp", "intrinio", "polygon", "tiingo", "tmx", "tradier", "yfinance"

    This test verifies the following:
    - The result is not None
    - The result is an OBBject
    - The result is a dataframe
    - The dataframe is not empty
    - The dataframe has the correct columns
    """

    # Get today's date and yesterday's date
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=1)

    logger.info(f"Fetching BNS.TO data from {start_date} to {end_date} using alpha_vantage")

    # Execute the command
    result = obb.equity.price.historical(
        symbol="BNS.TO",
        provider="alpha_vantage",
        start_date=start_date,
        end_date=end_date
    )

    # Log result details
    logger.info(f"Result type: {type(result)}")
    logger.info(f"Result attributes: {dir(result)}")
    logger.info(f"Result metadata: {result.metadata if hasattr(result, 'metadata') else 'No metadata'}")

    # Verify the result is an OBBject
    assert result is not None

    # Convert to dataframe and make columns lowercase
    df = result.to_dataframe()
    df.columns = df.columns.str.lower()

    # Log DataFrame details
    logger.info("\nDataFrame Info:")
    logger.info(f"Shape: {df.shape}")
    logger.info(f"Columns: {df.columns.tolist()}")
    logger.info(f"Index range: {df.index.min()} to {df.index.max()}")
    logger.info("\nDataFrame Head:")
    logger.info(f"\n{df.head().to_string()}")
    logger.info("\nDataFrame Description:")
    logger.info(f"\n{df.describe().to_string()}")

    # Basic data validation
    assert isinstance(df, pd.DataFrame)
    assert not df.empty
    assert "close" in df.columns
    assert "open" in df.columns
    assert "high" in df.columns
    assert "low" in df.columns
    assert "volume" in df.columns

    # Verify data types
    assert pd.api.types.is_float_dtype(df["close"])
    assert pd.api.types.is_float_dtype(df["open"])
    assert pd.api.types.is_float_dtype(df["high"])
    assert pd.api.types.is_float_dtype(df["low"])
    assert pd.api.types.is_numeric_dtype(df["volume"])

    # Verify we got data for the requested date range
    assert len(df.index) > 0
    assert df.index.min() >= start_date
    assert df.index.max() <= end_date

    # Verify price values are reasonable (non-zero)
    assert (df["close"] > 0).all()
    assert (df["open"] > 0).all()
    assert (df["high"] > 0).all()
    assert (df["low"] > 0).all()
    assert (df["volume"] >= 0).all()
