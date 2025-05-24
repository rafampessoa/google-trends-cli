"""Unit tests for the TrendingService class."""

import os
from unittest.mock import MagicMock, patch

import pandas as pd
import pytest

from gtrends_core.exceptions.trends_exceptions import TrendsAPIError, ValidationError
from gtrends_core.models.trending import TrendingResult
from gtrends_core.services.trending_service import TrendingService


class TestTrendingService:
    """Test suite for TrendingService class."""

    @pytest.fixture
    def mock_client(self):
        """Create a mock trends client."""
        client = MagicMock()
        # Mock get_current_region
        client.get_current_region.return_value = "US"
        
        # Mock get_trending_searches
        trending_data = {
            "rank": [1, 2, 3, 4, 5],
            "title": ["Topic 1", "Topic 2", "Topic 3", "Topic 4", "Topic 5"],
            "traffic": ["1M+", "500K+", "200K+", "100K+", "50K+"],
        }
        client.get_trending_searches.return_value = pd.DataFrame(trending_data)
        
        # Mock get_trending_searches_with_articles
        news_articles = {
            "Topic 1": [
                {
                    "title": "News about Topic 1",
                    "source": "Example News",
                    "url": "https://example.com/news1",
                    "time_ago": "2 hours ago",
                }
            ]
        }
        client.get_trending_searches_with_articles.return_value = (
            pd.DataFrame(trending_data),
            news_articles,
        )
        return client
    
    @pytest.fixture
    def service(self, mock_client):
        """Create a TrendingService instance with a mock client."""
        return TrendingService(mock_client)
    
    def test_init(self, service, mock_client):
        """Test TrendingService initialization."""
        assert service._client == mock_client
        
    def test_get_trending_searches_default(self, service, mock_client):
        """Test get_trending_searches with default parameters."""
        result = service.get_trending_searches()
        
        assert isinstance(result, TrendingResult)
        assert len(result.data) == 5
        mock_client.get_trending_searches.assert_called_once()
        
    def test_get_trending_searches_with_region(self, service, mock_client):
        """Test get_trending_searches with custom region."""
        result = service.get_trending_searches(region="GB")
        
        assert isinstance(result, TrendingResult)
        mock_client.get_trending_searches.assert_called_once_with(region="GB")
        
    def test_get_trending_searches_with_invalid_region(self, service):
        """Test get_trending_searches with invalid region raises ValidationError."""
        with pytest.raises(ValidationError):
            service.get_trending_searches(region="INVALID")
            
    def test_get_trending_searches_api_error(self, service, mock_client):
        """Test handling of API errors."""
        mock_client.get_trending_searches.side_effect = Exception("API Error")
        
        with pytest.raises(TrendsAPIError):
            service.get_trending_searches()
            
    def test_get_trending_searches_with_articles(self, service, mock_client):
        """Test get_trending_searches_with_articles method."""
        result = service.get_trending_searches_with_articles()
        
        assert isinstance(result, TrendingResult)
        assert hasattr(result, 'articles')
        assert "Topic 1" in result.articles
        mock_client.get_trending_searches_with_articles.assert_called_once()
        
    def test_get_trending_searches_with_articles_and_region(self, service, mock_client):
        """Test get_trending_searches_with_articles with custom region."""
        result = service.get_trending_searches_with_articles(region="CA")
        
        assert isinstance(result, TrendingResult)
        mock_client.get_trending_searches_with_articles.assert_called_once_with(region="CA")
        
    def test_format_trending_searches(self, service):
        """Test _format_trending_searches method."""
        test_data = pd.DataFrame({
            "rank": [1, 2],
            "title": ["Test Topic 1", "Test Topic 2"],
            "traffic": ["100K+", "50K+"]
        })
        
        result = service._format_trending_searches(test_data)
        
        assert isinstance(result, TrendingResult)
        assert len(result.data) == 2
        assert result.data.iloc[0]["title"] == "Test Topic 1"
        
    def test_format_trending_searches_with_articles(self, service):
        """Test _format_trending_searches_with_articles method."""
        test_data = pd.DataFrame({
            "rank": [1, 2],
            "title": ["Test Topic 1", "Test Topic 2"],
            "traffic": ["100K+", "50K+"]
        })
        test_articles = {
            "Test Topic 1": [{"title": "Article 1", "url": "https://example.com"}]
        }
        
        result = service._format_trending_searches_with_articles(test_data, test_articles)
        
        assert isinstance(result, TrendingResult)
        assert hasattr(result, 'articles')
        assert "Test Topic 1" in result.articles
        assert result.articles["Test Topic 1"][0]["title"] == "Article 1" 