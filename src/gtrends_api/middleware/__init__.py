"""Middleware for the Google Trends API."""

from gtrends_api.middleware.cors import add_cors_middleware
from gtrends_api.middleware.error_handling import add_exception_handlers
from gtrends_api.middleware.rate_limiting import RateLimitMiddleware
