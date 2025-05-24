"""Integration tests for the CLI commands."""

import os
from unittest.mock import MagicMock, patch
import tempfile
import json
import csv
from pathlib import Path

import pandas as pd
import pytest
from click.testing import CliRunner

from gtrends_cli.main import cli
from gtrends_core.models.trending import TrendingResult
from gtrends_core.models.comparison import ComparisonResult
from gtrends_core.models.related import RelatedResult
from gtrends_core.services.trending_service import TrendingService
from gtrends_core.services.comparison_service import ComparisonService
from gtrends_core.services.related_service import RelatedService


@pytest.fixture
def runner():
    """Create a CLI runner for testing commands."""
    return CliRunner()


class TestTrendingCLI:
    """Integration tests for trending CLI commands."""
    
    @patch.object(TrendingService, "get_trending_searches")
    def test_trending_command(self, mock_get_trending, runner):
        """Test 'gtrends trending' command."""
        # Mock service response
        mock_data = pd.DataFrame({
            "rank": [1, 2],
            "title": ["Test Topic 1", "Test Topic 2"],
            "traffic": ["100K+", "50K+"]
        })
        mock_result = TrendingResult(data=mock_data)
        mock_get_trending.return_value = mock_result
        
        # Run command
        result = runner.invoke(cli, ["trending"])
        
        # Assertions
        assert result.exit_code == 0
        assert "Test Topic 1" in result.output
        assert "Test Topic 2" in result.output
        assert "100K+" in result.output
        mock_get_trending.assert_called_once()
        
    @patch.object(TrendingService, "get_trending_searches")
    def test_trending_command_with_region(self, mock_get_trending, runner):
        """Test 'gtrends trending --region' command."""
        # Mock service response
        mock_data = pd.DataFrame({
            "rank": [1, 2],
            "title": ["UK Topic 1", "UK Topic 2"],
            "traffic": ["100K+", "50K+"]
        })
        mock_result = TrendingResult(data=mock_data)
        mock_get_trending.return_value = mock_result
        
        # Run command
        result = runner.invoke(cli, ["trending", "--region", "GB"])
        
        # Assertions
        assert result.exit_code == 0
        assert "UK Topic 1" in result.output
        mock_get_trending.assert_called_once_with(region="GB")
        
    @patch.object(TrendingService, "get_trending_searches")
    def test_trending_command_export_csv(self, mock_get_trending, runner, tmp_path):
        """Test 'gtrends trending --export-format csv' command."""
        # Mock service response
        mock_data = pd.DataFrame({
            "rank": [1, 2],
            "title": ["Test Topic 1", "Test Topic 2"],
            "traffic": ["100K+", "50K+"]
        })
        mock_result = TrendingResult(data=mock_data)
        mock_get_trending.return_value = mock_result
        
        # Create temporary export file
        export_file = tmp_path / "trending_export.csv"
        
        # Run command
        result = runner.invoke(cli, ["trending", "--export-format", "csv", "--export-path", str(export_file)])
        
        # Assertions
        assert result.exit_code == 0
        assert export_file.exists()
        
        # Check CSV content
        with open(export_file, "r") as f:
            reader = csv.reader(f)
            headers = next(reader)
            assert "rank" in headers
            assert "title" in headers
            assert "traffic" in headers
            
            first_row = next(reader)
            assert "Test Topic 1" in first_row
            
    @patch.object(TrendingService, "get_trending_searches_with_articles")
    def test_trending_command_with_articles(self, mock_get_trending_articles, runner):
        """Test 'gtrends trending --with-articles' command."""
        # Mock service response
        mock_data = pd.DataFrame({
            "rank": [1, 2],
            "title": ["Test Topic 1", "Test Topic 2"],
            "traffic": ["100K+", "50K+"]
        })
        mock_articles = {
            "Test Topic 1": [
                {
                    "title": "News about Topic 1",
                    "source": "Example News",
                    "url": "https://example.com/news1",
                    "time_ago": "2 hours ago",
                }
            ]
        }
        mock_result = TrendingResult(data=mock_data, articles=mock_articles)
        mock_get_trending_articles.return_value = mock_result
        
        # Run command
        result = runner.invoke(cli, ["trending", "--with-articles"])
        
        # Assertions
        assert result.exit_code == 0
        assert "Test Topic 1" in result.output
        assert "News about Topic 1" in result.output
        mock_get_trending_articles.assert_called_once()


class TestComparisonCLI:
    """Integration tests for comparison CLI commands."""
    
    @patch.object(ComparisonService, "compare_interests")
    def test_compare_command(self, mock_compare, runner):
        """Test 'gtrends compare' command."""
        # Mock service response
        dates = pd.date_range(start="1/1/2023", periods=5, freq="D")
        mock_data = pd.DataFrame({
            "query1": [10, 20, 30, 40, 50],
            "query2": [50, 40, 30, 20, 10]
        }, index=dates)
        mock_result = ComparisonResult(data=mock_data)
        mock_compare.return_value = mock_result
        
        # Run command
        result = runner.invoke(cli, ["compare", "query1", "query2"])
        
        # Assertions
        assert result.exit_code == 0
        assert "query1" in result.output
        assert "query2" in result.output
        mock_compare.assert_called_once_with(
            ["query1", "query2"], 
            timeframe="today 12-m", 
            geo="", 
            category=0
        )
        
    @patch.object(ComparisonService, "compare_interests")
    def test_compare_command_with_params(self, mock_compare, runner):
        """Test 'gtrends compare' command with additional parameters."""
        # Mock service response
        dates = pd.date_range(start="1/1/2023", periods=5, freq="D")
        mock_data = pd.DataFrame({
            "query1": [10, 20, 30, 40, 50],
            "query2": [50, 40, 30, 20, 10]
        }, index=dates)
        mock_result = ComparisonResult(data=mock_data)
        mock_compare.return_value = mock_result
        
        # Run command
        result = runner.invoke(cli, [
            "compare", 
            "query1", 
            "query2", 
            "--timeframe", "today 3-m",
            "--geo", "US",
            "--category", "5"
        ])
        
        # Assertions
        assert result.exit_code == 0
        mock_compare.assert_called_once_with(
            ["query1", "query2"], 
            timeframe="today 3-m", 
            geo="US", 
            category=5
        )
        
    @patch.object(ComparisonService, "compare_interests")
    @patch.object(ComparisonService, "visualize_comparison")
    def test_compare_command_with_visualization(self, mock_visualize, mock_compare, runner, tmp_path):
        """Test 'gtrends compare --visualize' command."""
        # Mock service responses
        dates = pd.date_range(start="1/1/2023", periods=5, freq="D")
        mock_data = pd.DataFrame({
            "query1": [10, 20, 30, 40, 50],
            "query2": [50, 40, 30, 20, 10]
        }, index=dates)
        mock_result = ComparisonResult(data=mock_data)
        mock_compare.return_value = mock_result
        
        # Create temporary visualization file
        viz_file = tmp_path / "comparison.png"
        
        # Run command
        result = runner.invoke(cli, [
            "compare", 
            "query1", 
            "query2", 
            "--visualize",
            "--output", str(viz_file)
        ])
        
        # Assertions
        assert result.exit_code == 0
        mock_visualize.assert_called_once()
        assert mock_visualize.call_args[0][0] == mock_result
        assert mock_visualize.call_args[0][1] == str(viz_file)


class TestRelatedCLI:
    """Integration tests for related CLI commands."""
    
    @patch.object(RelatedService, "get_related_topics")
    def test_related_topics_command(self, mock_get_topics, runner):
        """Test 'gtrends related topics' command."""
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
        
        # Run command
        result = runner.invoke(cli, ["related", "topics", "test query"])
        
        # Assertions
        assert result.exit_code == 0
        assert "Related Topic 1" in result.output
        assert "Rising Topic 1" in result.output
        mock_get_topics.assert_called_once_with(
            "test query",
            geo="",
            timeframe="today 12-m",
            category=0
        )
        
    @patch.object(RelatedService, "get_related_queries")
    def test_related_queries_command(self, mock_get_queries, runner):
        """Test 'gtrends related queries' command."""
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
        
        # Run command
        result = runner.invoke(cli, ["related", "queries", "test query"])
        
        # Assertions
        assert result.exit_code == 0
        assert "Related Query 1" in result.output
        assert "Rising Query 1" in result.output
        mock_get_queries.assert_called_once_with(
            "test query",
            geo="",
            timeframe="today 12-m",
            category=0
        )
        
    @patch.object(RelatedService, "get_related_topics")
    def test_related_topics_command_with_params(self, mock_get_topics, runner):
        """Test 'gtrends related topics' command with additional parameters."""
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
        
        # Run command
        result = runner.invoke(cli, [
            "related", 
            "topics", 
            "test query",
            "--geo", "US",
            "--timeframe", "today 3-m",
            "--category", "5"
        ])
        
        # Assertions
        assert result.exit_code == 0
        mock_get_topics.assert_called_once_with(
            "test query",
            geo="US",
            timeframe="today 3-m",
            category=5
        )
        
    @patch.object(RelatedService, "get_related_topics")
    def test_related_topics_command_export_json(self, mock_get_topics, runner, tmp_path):
        """Test 'gtrends related topics --export-format json' command."""
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
        
        # Create temporary export file
        export_file = tmp_path / "related_export.json"
        
        # Run command
        result = runner.invoke(cli, [
            "related", 
            "topics", 
            "test query",
            "--export-format", "json",
            "--export-path", str(export_file)
        ])
        
        # Assertions
        assert result.exit_code == 0
        assert export_file.exists()
        
        # Check JSON content
        with open(export_file, "r") as f:
            data = json.load(f)
            assert "top" in data
            assert "rising" in data
            assert len(data["top"]) == 2
            assert data["top"][0]["topic_title"] == "Related Topic 1" 