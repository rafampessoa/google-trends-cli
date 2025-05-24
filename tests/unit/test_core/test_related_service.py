"""Unit tests for the RelatedService class."""

from unittest.mock import MagicMock, patch

import pandas as pd
import pytest

from gtrends_core.exceptions.trends_exceptions import TrendsAPIError, ValidationError
from gtrends_core.models.related import RelatedResult
from gtrends_core.services.related_service import RelatedService


class TestRelatedService:
    """Test suite for RelatedService class."""

    @pytest.fixture
    def mock_client(self):
        """Create a mock trends client."""
        client = MagicMock()
        
        # Mock get_related_topics
        top_topics_data = {"topic_title": ["Related Topic 1", "Related Topic 2"], "value": [100, 90]}
        rising_topics_data = {"topic_title": ["Rising Topic 1", "Rising Topic 2"], "value": [120, 150]}

        related_topics = {
            "top": pd.DataFrame(top_topics_data),
            "rising": pd.DataFrame(rising_topics_data),
        }
        client.get_related_topics.return_value = related_topics
        
        # Mock get_related_queries
        top_queries_data = {"query": ["Related Query 1", "Related Query 2"], "value": [100, 90]}
        rising_queries_data = {"query": ["Rising Query 1", "Rising Query 2"], "value": [120, 150]}

        related_queries = {
            "top": pd.DataFrame(top_queries_data),
            "rising": pd.DataFrame(rising_queries_data),
        }
        client.get_related_queries.return_value = related_queries
        
        return client
    
    @pytest.fixture
    def service(self, mock_client):
        """Create a RelatedService instance with a mock client."""
        return RelatedService(mock_client)
    
    def test_init(self, service, mock_client):
        """Test RelatedService initialization."""
        assert service._client == mock_client
        
    def test_get_related_topics_default(self, service, mock_client):
        """Test get_related_topics with default parameters."""
        result = service.get_related_topics("test query")
        
        assert isinstance(result, RelatedResult)
        assert hasattr(result, "top")
        assert hasattr(result, "rising")
        assert len(result.top) == 2
        assert len(result.rising) == 2
        mock_client.get_related_topics.assert_called_once()
        
    def test_get_related_topics_with_params(self, service, mock_client):
        """Test get_related_topics with custom parameters."""
        result = service.get_related_topics(
            "test query", 
            geo="US", 
            timeframe="today 3-m", 
            category=5
        )
        
        assert isinstance(result, RelatedResult)
        mock_client.get_related_topics.assert_called_once_with(
            keyword="test query",
            geo="US",
            timeframe="today 3-m",
            category=5
        )
        
    def test_get_related_topics_api_error(self, service, mock_client):
        """Test handling of API errors."""
        mock_client.get_related_topics.side_effect = Exception("API Error")
        
        with pytest.raises(TrendsAPIError):
            service.get_related_topics("test query")
            
    def test_get_related_topics_invalid_timeframe(self, service):
        """Test get_related_topics with invalid timeframe raises ValidationError."""
        with pytest.raises(ValidationError):
            service.get_related_topics("test query", timeframe="invalid")
            
    def test_get_related_queries_default(self, service, mock_client):
        """Test get_related_queries with default parameters."""
        result = service.get_related_queries("test query")
        
        assert isinstance(result, RelatedResult)
        assert hasattr(result, "top")
        assert hasattr(result, "rising")
        assert len(result.top) == 2
        assert len(result.rising) == 2
        mock_client.get_related_queries.assert_called_once()
        
    def test_get_related_queries_with_params(self, service, mock_client):
        """Test get_related_queries with custom parameters."""
        result = service.get_related_queries(
            "test query", 
            geo="US", 
            timeframe="today 3-m", 
            category=5
        )
        
        assert isinstance(result, RelatedResult)
        mock_client.get_related_queries.assert_called_once_with(
            keyword="test query",
            geo="US",
            timeframe="today 3-m",
            category=5
        )
        
    def test_get_related_queries_api_error(self, service, mock_client):
        """Test handling of API errors."""
        mock_client.get_related_queries.side_effect = Exception("API Error")
        
        with pytest.raises(TrendsAPIError):
            service.get_related_queries("test query")
            
    def test_get_related_queries_invalid_timeframe(self, service):
        """Test get_related_queries with invalid timeframe raises ValidationError."""
        with pytest.raises(ValidationError):
            service.get_related_queries("test query", timeframe="invalid")
            
    def test_format_related_result(self, service):
        """Test _format_related_result method."""
        top_data = pd.DataFrame({
            "topic_title": ["Test Topic 1", "Test Topic 2"],
            "value": [100, 90]
        })
        rising_data = pd.DataFrame({
            "topic_title": ["Rising Topic 1", "Rising Topic 2"],
            "value": [120, 150]
        })
        
        result = service._format_related_result({
            "top": top_data,
            "rising": rising_data
        })
        
        assert isinstance(result, RelatedResult)
        assert hasattr(result, "top")
        assert hasattr(result, "rising")
        assert len(result.top) == 2
        assert len(result.rising) == 2
        assert result.top.iloc[0]["topic_title"] == "Test Topic 1"
        assert result.rising.iloc[0]["topic_title"] == "Rising Topic 1"
        
    def test_format_related_queries_result(self, service):
        """Test _format_related_queries_result method."""
        top_data = pd.DataFrame({
            "query": ["Test Query 1", "Test Query 2"],
            "value": [100, 90]
        })
        rising_data = pd.DataFrame({
            "query": ["Rising Query 1", "Rising Query 2"],
            "value": [120, 150]
        })
        
        result = service._format_related_queries_result({
            "top": top_data,
            "rising": rising_data
        })
        
        assert isinstance(result, RelatedResult)
        assert hasattr(result, "top")
        assert hasattr(result, "rising")
        assert len(result.top) == 2
        assert len(result.rising) == 2
        assert result.top.iloc[0]["query"] == "Test Query 1"
        assert result.rising.iloc[0]["query"] == "Rising Query 1"
        
    def test_filter_results(self, service):
        """Test filter_results method."""
        related_result = RelatedResult(
            top=pd.DataFrame({
                "topic_title": ["Test Topic 1", "Test Topic 2", "Test Topic 3"],
                "value": [100, 90, 80]
            }),
            rising=pd.DataFrame({
                "topic_title": ["Rising Topic 1", "Rising Topic 2", "Rising Topic 3"],
                "value": [120, 150, 130]
            })
        )
        
        filtered_result = service.filter_results(related_result, limit=2)
        
        assert isinstance(filtered_result, RelatedResult)
        assert len(filtered_result.top) == 2
        assert len(filtered_result.rising) == 2
        assert filtered_result.top.iloc[0]["topic_title"] == "Test Topic 1"
        assert filtered_result.rising.iloc[0]["topic_title"] == "Rising Topic 1" 