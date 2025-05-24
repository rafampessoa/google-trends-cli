"""Integration tests for the API endpoints."""

import json
from unittest.mock import MagicMock, patch

import pandas as pd
import pytest
from fastapi.testclient import TestClient

from gtrends_api.main import app
from gtrends_core.models.trending import TrendingResult
from gtrends_core.models.comparison import ComparisonResult
from gtrends_core.models.related import RelatedResult
from gtrends_core.services.trending_service import TrendingService
from gtrends_core.services.comparison_service import ComparisonService
from gtrends_core.services.related_service import RelatedService


@pytest.fixture
def client():
    """Create a test client for the FastAPI app."""
    return TestClient(app)


class TestTrendingAPI:
    """Integration tests for trending endpoints."""
    
    @patch.object(TrendingService, "get_trending_searches")
    def test_get_trending_searches(self, mock_get_trending, client):
        """Test GET /api/v1/trending endpoint."""
        # Mock service response
        mock_data = pd.DataFrame({
            "rank": [1, 2],
            "title": ["Test Topic 1", "Test Topic 2"],
            "traffic": ["100K+", "50K+"]
        })
        mock_result = TrendingResult(data=mock_data)
        mock_get_trending.return_value = mock_result
        
        # Call API
        response = client.get("/api/v1/trending")
        
        # Assertions
        assert response.status_code == 200
        data = response.json()
        assert "data" in data
        assert len(data["data"]) == 2
        assert data["data"][0]["title"] == "Test Topic 1"
        
    @patch.object(TrendingService, "get_trending_searches")
    def test_get_trending_searches_with_region(self, mock_get_trending, client):
        """Test GET /api/v1/trending with region parameter."""
        # Mock service response
        mock_data = pd.DataFrame({
            "rank": [1, 2],
            "title": ["UK Topic 1", "UK Topic 2"],
            "traffic": ["100K+", "50K+"]
        })
        mock_result = TrendingResult(data=mock_data)
        mock_get_trending.return_value = mock_result
        
        # Call API
        response = client.get("/api/v1/trending?region=GB")
        
        # Assertions
        assert response.status_code == 200
        mock_get_trending.assert_called_once_with(region="GB")
        
    @patch.object(TrendingService, "get_trending_searches")
    def test_get_trending_searches_error(self, mock_get_trending, client):
        """Test error handling in trending endpoint."""
        # Mock service error
        mock_get_trending.side_effect = Exception("API Error")
        
        # Call API
        response = client.get("/api/v1/trending")
        
        # Assertions
        assert response.status_code == 500
        data = response.json()
        assert "error" in data
        

class TestComparisonAPI:
    """Integration tests for comparison endpoints."""
    
    @patch.object(ComparisonService, "compare_interests")
    def test_compare_interests(self, mock_compare, client):
        """Test POST /api/v1/comparison endpoint."""
        # Mock service response
        dates = pd.date_range(start="1/1/2023", periods=5, freq="D")
        mock_data = pd.DataFrame({
            "query1": [10, 20, 30, 40, 50],
            "query2": [50, 40, 30, 20, 10]
        }, index=dates)
        mock_result = ComparisonResult(data=mock_data)
        mock_compare.return_value = mock_result
        
        # Call API
        response = client.post(
            "/api/v1/comparison",
            json={"keywords": ["query1", "query2"]}
        )
        
        # Assertions
        assert response.status_code == 200
        data = response.json()
        assert "data" in data
        assert len(data["data"]) == 5
        assert "query1" in data["data"][0]
        assert "query2" in data["data"][0]
        
    @patch.object(ComparisonService, "compare_interests")
    def test_compare_interests_with_params(self, mock_compare, client):
        """Test POST /api/v1/comparison with additional parameters."""
        # Mock service response
        dates = pd.date_range(start="1/1/2023", periods=5, freq="D")
        mock_data = pd.DataFrame({
            "query1": [10, 20, 30, 40, 50],
            "query2": [50, 40, 30, 20, 10]
        }, index=dates)
        mock_result = ComparisonResult(data=mock_data)
        mock_compare.return_value = mock_result
        
        # Call API
        response = client.post(
            "/api/v1/comparison",
            json={
                "keywords": ["query1", "query2"],
                "timeframe": "today 3-m",
                "geo": "US",
                "category": 5
            }
        )
        
        # Assertions
        assert response.status_code == 200
        mock_compare.assert_called_once_with(
            ["query1", "query2"],
            timeframe="today 3-m",
            geo="US",
            category=5
        )
        
    @patch.object(ComparisonService, "compare_interests")
    def test_compare_interests_validation_error(self, mock_compare, client):
        """Test validation error handling in comparison endpoint."""
        # Call API with too many keywords
        response = client.post(
            "/api/v1/comparison",
            json={"keywords": ["q1", "q2", "q3", "q4", "q5", "q6"]}
        )
        
        # Assertions
        assert response.status_code == 422
        data = response.json()
        assert "detail" in data
        

class TestRelatedAPI:
    """Integration tests for related endpoints."""
    
    @patch.object(RelatedService, "get_related_topics")
    def test_get_related_topics(self, mock_get_topics, client):
        """Test GET /api/v1/related/topics endpoint."""
        # Mock service response
        top_data = pd.DataFrame({
            "topic_title": ["Related Topic 1", "Related Topic 2"],
            "value": [100, 90]
        })
        rising_data = pd.DataFrame({
            "topic_title": ["Rising Topic 1", "Rising Topic 2"],
            "value": [120, 150]
        })
        mock_result = RelatedResult(top=top_data, rising=rising_data)
        mock_get_topics.return_value = mock_result
        
        # Call API
        response = client.get("/api/v1/related/topics?keyword=test")
        
        # Assertions
        assert response.status_code == 200
        data = response.json()
        assert "top" in data
        assert "rising" in data
        assert len(data["top"]) == 2
        assert len(data["rising"]) == 2
        assert data["top"][0]["topic_title"] == "Related Topic 1"
        assert data["rising"][0]["topic_title"] == "Rising Topic 1"
        
    @patch.object(RelatedService, "get_related_queries")
    def test_get_related_queries(self, mock_get_queries, client):
        """Test GET /api/v1/related/queries endpoint."""
        # Mock service response
        top_data = pd.DataFrame({
            "query": ["Related Query 1", "Related Query 2"],
            "value": [100, 90]
        })
        rising_data = pd.DataFrame({
            "query": ["Rising Query 1", "Rising Query 2"],
            "value": [120, 150]
        })
        mock_result = RelatedResult(top=top_data, rising=rising_data)
        mock_get_queries.return_value = mock_result
        
        # Call API
        response = client.get("/api/v1/related/queries?keyword=test")
        
        # Assertions
        assert response.status_code == 200
        data = response.json()
        assert "top" in data
        assert "rising" in data
        assert len(data["top"]) == 2
        assert len(data["rising"]) == 2
        assert data["top"][0]["query"] == "Related Query 1"
        assert data["rising"][0]["query"] == "Rising Query 1"
        
    @patch.object(RelatedService, "get_related_topics")
    def test_get_related_topics_with_params(self, mock_get_topics, client):
        """Test GET /api/v1/related/topics with additional parameters."""
        # Mock service response
        top_data = pd.DataFrame({
            "topic_title": ["Related Topic 1", "Related Topic 2"],
            "value": [100, 90]
        })
        rising_data = pd.DataFrame({
            "topic_title": ["Rising Topic 1", "Rising Topic 2"],
            "value": [120, 150]
        })
        mock_result = RelatedResult(top=top_data, rising=rising_data)
        mock_get_topics.return_value = mock_result
        
        # Call API
        response = client.get(
            "/api/v1/related/topics?keyword=test&geo=US&timeframe=today+3-m&category=5"
        )
        
        # Assertions
        assert response.status_code == 200
        mock_get_topics.assert_called_once_with(
            "test",
            geo="US",
            timeframe="today 3-m",
            category=5
        )
        
    @patch.object(RelatedService, "get_related_topics")
    def test_get_related_topics_error(self, mock_get_topics, client):
        """Test error handling in related topics endpoint."""
        # Mock service error
        mock_get_topics.side_effect = Exception("API Error")
        
        # Call API
        response = client.get("/api/v1/related/topics?keyword=test")
        
        # Assertions
        assert response.status_code == 500
        data = response.json()
        assert "error" in data 