"""API schemas for request and response models."""

from gtrends_api.schemas.requests import (
    BatchPeriodEnum,
    CategoryEnum,
    ComparisonRequest,
    InterestByRegionRequest,
    RelatedRequest,
    ResolutionEnum,
    TopicGrowthRequest,
    TrendingRequest,
)
from gtrends_api.schemas.responses import (
    ErrorResponse,
    InterestByRegionResponse,
    InterestOverTimeResponse,
    NewsArticleResponse,
    RegionInterestResponse,
    RelatedQueriesResponse,
    RelatedTopicResponse,
    RelatedTopicsResponse,
    TimePointResponse,
    TrendingSearchResponse,
    TrendingTopicResponse,
)
