"""Unit tests for the ComparisonService class."""

import os
from unittest.mock import MagicMock, patch
from datetime import datetime, timedelta

import pandas as pd
import pytest
import matplotlib.pyplot as plt
import numpy as np

from gtrends_core.exceptions.trends_exceptions import TrendsAPIError, ValidationError
from gtrends_core.models.comparison import ComparisonResult
from gtrends_core.services.comparison_service import ComparisonService


class TestComparisonService:
    """Test suite for ComparisonService class."""

    @pytest.fixture
    def mock_client(self):
        """Create a mock trends client."""
        client = MagicMock()
        
        # Mock get_interest_over_time
        dates = pd.date_range(start="1/1/2023", periods=10, freq="D")
        interest_data = {
            "date": dates,
            "query1": [10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
            "query2": [100, 90, 80, 70, 60, 50, 40, 30, 20, 10],
        }
        client.get_interest_over_time.return_value = pd.DataFrame(interest_data).set_index("date")
        
        return client
    
    @pytest.fixture
    def service(self, mock_client):
        """Create a ComparisonService instance with a mock client."""
        return ComparisonService(mock_client)
    
    def test_init(self, service, mock_client):
        """Test ComparisonService initialization."""
        assert service._client == mock_client
        
    def test_compare_interests_default(self, service, mock_client):
        """Test compare_interests with default parameters."""
        result = service.compare_interests(["query1", "query2"])
        
        assert isinstance(result, ComparisonResult)
        assert "query1" in result.data.columns
        assert "query2" in result.data.columns
        mock_client.get_interest_over_time.assert_called_once()
        
    def test_compare_interests_with_timeframe(self, service, mock_client):
        """Test compare_interests with custom timeframe."""
        result = service.compare_interests(["query1", "query2"], timeframe="today 3-m")
        
        assert isinstance(result, ComparisonResult)
        mock_client.get_interest_over_time.assert_called_once_with(
            keywords=["query1", "query2"], 
            timeframe="today 3-m", 
            geo="", 
            category=0
        )
        
    def test_compare_interests_with_geo(self, service, mock_client):
        """Test compare_interests with custom geo region."""
        result = service.compare_interests(["query1", "query2"], geo="US")
        
        assert isinstance(result, ComparisonResult)
        mock_client.get_interest_over_time.assert_called_once_with(
            keywords=["query1", "query2"], 
            timeframe="today 12-m", 
            geo="US", 
            category=0
        )
        
    def test_compare_interests_too_many_keywords(self, service):
        """Test compare_interests with too many keywords raises ValidationError."""
        with pytest.raises(ValidationError):
            service.compare_interests(["query1", "query2", "query3", "query4", "query5", "query6"])
            
    def test_compare_interests_invalid_timeframe(self, service):
        """Test compare_interests with invalid timeframe raises ValidationError."""
        with pytest.raises(ValidationError):
            service.compare_interests(["query1", "query2"], timeframe="invalid")
            
    def test_compare_interests_api_error(self, service, mock_client):
        """Test handling of API errors."""
        mock_client.get_interest_over_time.side_effect = Exception("API Error")
        
        with pytest.raises(TrendsAPIError):
            service.compare_interests(["query1", "query2"])
            
    def test_format_comparison_result(self, service):
        """Test _format_comparison_result method."""
        dates = pd.date_range(start="1/1/2023", periods=5, freq="D")
        test_data = pd.DataFrame({
            "query1": [10, 20, 30, 40, 50],
            "query2": [50, 40, 30, 20, 10]
        }, index=dates)
        
        result = service._format_comparison_result(test_data)
        
        assert isinstance(result, ComparisonResult)
        assert result.data.shape == (5, 2)
        assert result.data.index.name == "date"
        assert list(result.data.columns) == ["query1", "query2"]
        
    @patch("matplotlib.pyplot.savefig")
    def test_visualize_comparison(self, mock_savefig, service, tmp_path):
        """Test visualize_comparison method."""
        # Create test data
        dates = pd.date_range(start="1/1/2023", periods=10, freq="D")
        test_data = pd.DataFrame({
            "query1": [10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
            "query2": [100, 90, 80, 70, 60, 50, 40, 30, 20, 10],
        }, index=dates)
        comparison_result = ComparisonResult(data=test_data)
        
        # Create a temporary file path
        output_path = os.path.join(tmp_path, "comparison.png")
        
        # Test visualization function
        service.visualize_comparison(comparison_result, output_path)
        
        # Verify savefig was called with the right path
        mock_savefig.assert_called_once_with(output_path, bbox_inches='tight', dpi=300)
        
    def test_get_avg_interest(self, service):
        """Test get_avg_interest method."""
        dates = pd.date_range(start="1/1/2023", periods=5, freq="D")
        test_data = pd.DataFrame({
            "query1": [10, 20, 30, 40, 50],
            "query2": [50, 40, 30, 20, 10]
        }, index=dates)
        comparison_result = ComparisonResult(data=test_data)
        
        averages = service.get_avg_interest(comparison_result)
        
        assert isinstance(averages, dict)
        assert "query1" in averages
        assert "query2" in averages
        assert averages["query1"] == 30.0
        assert averages["query2"] == 30.0
        
    def test_get_peak_interest(self, service):
        """Test get_peak_interest method."""
        dates = pd.date_range(start="1/1/2023", periods=5, freq="D")
        test_data = pd.DataFrame({
            "query1": [10, 20, 30, 40, 50],
            "query2": [50, 40, 30, 20, 10]
        }, index=dates)
        comparison_result = ComparisonResult(data=test_data)
        
        peaks = service.get_peak_interest(comparison_result)
        
        assert isinstance(peaks, dict)
        assert "query1" in peaks
        assert "query2" in peaks
        assert peaks["query1"] == 50
        assert peaks["query2"] == 50
        
    def test_get_growth_rate(self, service):
        """Test get_growth_rate method."""
        dates = pd.date_range(start="1/1/2023", periods=5, freq="D")
        test_data = pd.DataFrame({
            "query1": [10, 20, 30, 40, 50],  # Growing
            "query2": [50, 40, 30, 20, 10]   # Declining
        }, index=dates)
        comparison_result = ComparisonResult(data=test_data)
        
        growth_rates = service.get_growth_rate(comparison_result)
        
        assert isinstance(growth_rates, dict)
        assert "query1" in growth_rates
        assert "query2" in growth_rates
        assert growth_rates["query1"] > 0  # Should be positive growth
        assert growth_rates["query2"] < 0  # Should be negative growth 