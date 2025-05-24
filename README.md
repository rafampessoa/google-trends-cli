# Google Trends CLI Tool

<p align="center">
  <img src="https://raw.githubusercontent.com/Nao-30/google-trends-cli/main/assets/gtrends-logo.png" alt="Google Trends CLI Logo" width="180"/>
</p>

<p align="center">
  <a href="https://pypi.org/project/gtrends/"><img alt="PyPI version" src="https://img.shields.io/pypi/v/gtrends.svg"></a>
  <a href="https://github.com/Nao-30/google-trends-cli/blob/main/LICENSE"><img alt="License" src="https://img.shields.io/github/license/Nao-30/google-trends-cli"></a>
  <a href="https://github.com/Nao-30/google-trends-cli/actions"><img alt="Build status" src="https://github.com/Nao-30/google-trends-cli/workflows/Tests/badge.svg"></a>
  <a href="https://pypi.org/project/gtrends/"><img alt="Python versions" src="https://img.shields.io/pypi/pyversions/gtrends.svg"></a>
</p>

A powerful tool for fetching and analyzing Google Trends data, available as both a command-line tool and an HTTP API. Specially designed for content creators looking to identify what topics are worthy of writing about right now.

> **Note:** For a list of known issues and limitations, see [KNOWN_ISSUES.md](KNOWN_ISSUES.md).

---

## ✨ Features

- 📈 **Real-time Trends**: Access trending searches with a simple command
- 🔍 **Deep Analysis**: Explore related topics and queries for any search term
- 📊 **Comparative Insights**: Compare interest across different topics and timeframes
- ✍️ **Writer Suggestions**: Get data-driven content ideas specifically for writers
- 📱 **Geographic Analysis**: See how trends vary by region, country, or city
- 📉 **Independent Normalization**: Track hundreds of topics with individual trend lines
- 📰 **News Integration**: Find trending topics with associated news articles
- 📁 **Multiple Export Formats**: Save data as CSV, JSON, or Excel files with enhanced JSON structure
- 🖼️ **Visual Reporting**: Generate high-quality trend visualizations with matplotlib
- 🌐 **HTTP API**: Access all functionality via a RESTful API

## 🌐 API Access

All functionality is now available through an HTTP API, making it easy to integrate Google Trends data into your applications:

```bash
# Start the API server
gtrends-api

# By default, the API runs on http://localhost:8000
```

### API Endpoints

| Endpoint | Description |
|----------|-------------|
| `/api/trending` | Get trending searches |
| `/api/related` | Find related topics and queries |
| `/api/compare` | Compare interest across topics |
| `/api/suggestions` | Get content creation suggestions |
| `/api/opportunities` | Find writing opportunities |
| `/api/growth` | Track growth for multiple topics |
| `/api/geo` | Analyze geographic distribution |
| `/api/docs` | Interactive API documentation |

For detailed API documentation, visit the `/api/docs` endpoint when the server is running.

## 🚀 Installation

### Quick Install

```bash
# Basic installation (CLI only)
pip install gtrends-cli

# Installation with API support
pip install "gtrends-cli[api]"
```

### Using the Setup Script

For convenience, you can use the provided setup script:

```bash
# Clone the repository
git clone https://github.com/Nao-30/google-trends-cli.git
cd google-trends-cli

# Make the script executable
chmod +x scripts/setup.sh

# Install CLI only
./scripts/setup.sh

# Install with API support
./scripts/setup.sh --api

# Install with all dependencies (API + development)
./scripts/setup.sh --all

# Install in development mode
./scripts/setup.sh --dev
```

### From Source

```bash
# Clone the repository
git clone https://github.com/Nao-30/google-trends-cli.git
cd google-trends-cli

# CLI only
pip install .

# With API support
pip install ".[api]"

# With development dependencies
pip install ".[dev]"

# With all dependencies
pip install ".[all]"
```

### Docker

```bash
# Pull the image
docker pull nao30/gtrends-api:latest

# Run the API server
docker run -p 8000:8000 nao30/gtrends-api:latest
```

For more detailed installation instructions, see the [Installation Guide](docs/installation.md).

## 💻 Quick Start

```bash
# Show trending searches
gtrends trending

# Get content suggestions for creators
gtrends suggest-topics

# Find writing opportunities
gtrends writing-opportunities
```

## 📖 Usage Examples

### Basic Commands

```bash
# Show trending searches
gtrends trending

# Show trending searches with news articles
gtrends trending --with-news

# Show topics and queries related to a term
gtrends related "book publishing"

# Compare interest in multiple topics
gtrends compare "fiction books" "non-fiction books" "poetry"

# Get content suggestions for writers
gtrends suggest-topics --category=books

# Find writing opportunities
gtrends writing-opportunities "science fiction" "fantasy"

# Analyze growth patterns for topics (up to 500+ topics)
gtrends topic-growth "science fiction" "fantasy" "romance" "mystery" --period=24h

# Show geographic interest distribution
gtrends geo-interest "literature" --resolution=COUNTRY

# Search for category IDs
gtrends categories --find=book

# Search for location codes
gtrends geo "middle east"

# Show supported timeframe formats
gtrends help-timeframe
```

### For Content Creators

Commands specially designed for content creators looking to identify trending topics:

```bash
# Get topic suggestions in the books category
gtrends suggest-topics --category=books --region=US

# Find specific writing opportunities based on rising trends
gtrends writing-opportunities "book publishing" "fiction" --count=10

# Compare interest in publishing trends over time with visualization
gtrends compare "self-publishing" "traditional publishing" --visualize

# Monitor rapid growth patterns for genres (independently normalized)
gtrends topic-growth "mystery" "thriller" "romance" "sci-fi" "fantasy" --period=7d 
```

### Export Options

```bash
# Export trending searches to CSV (default)
gtrends trending --export

# Export to a specific location and format
gtrends suggest-topics --export --export-path="~/my-projects" --format=json

# Generate visualization and export data
gtrends compare "poetry" "prose" "fiction" --export --visualize

# Export comparison data with enhanced JSON structure
gtrends compare "fiction" "non-fiction" --export --format=json
```

## 📋 Available Commands

| Command | Description |
|---------|-------------|
| `trending` | Show current trending searches |
| `related` | Find related topics and queries |
| `suggest-topics` | Get content creation suggestions |
| `compare` | Compare interest across topics |
| `writing-opportunities` | Find specific writing opportunities |
| `topic-growth` | Track growth for multiple topics |
| `geo-interest` | Analyze geographic distribution |
| `categories` | List available content categories |
| `geo` | Search for location codes |
| `help-timeframe` | Show timeframe format help |

## ⚙️ Common Options

| Option | Description |
|--------|-------------|
| `--region`, `-r` | Region code (e.g., US, GB, AE) |
| `--count`, `-n` | Number of results to display |
| `--timeframe`, `-t` | Time range (e.g., 'now 1-d', 'today 3-m') |
| `--export`, `-e` | Export results to file |
| `--export-path` | Directory to save exported data |
| `--format`, `-f` | Export format (csv, json, xlsx) |
| `--visualize`, `-v` | Generate visualization |

## 🕒 Timeframe Formats

```
Standard formats:    'now 1-H', 'today 3-m', 'today 12-m'
Custom intervals:    'now 123-H', 'today 45-d', 'today 18-m'
Date-based:          '2024-02-01 10-d', '2024-01-01 2024-12-31'
Hourly precision:    '2024-03-25T12 2024-03-25T15'
All available data:  'all'
```

## 📊 Example Outputs







## 📑 Full Documentation

For complete documentation on all commands and options:

```bash
# General help
gtrends --help

# Command-specific help
gtrends [COMMAND] --help
```

## 🛠️ Requirements

### Core Requirements
- Python 3.8+
- trendspy
- click
- pandas
- rich
- python-dateutil
- matplotlib (optional, for visualizations)

### API Requirements (optional)
- fastapi
- uvicorn
- starlette

### Development Requirements
- pytest (for testing)
- pytest-cov (for test coverage)
- black (for code formatting)
- isort (for import sorting)
- flake8 (for linting)

## 🧪 Development

To set up the development environment:

```bash
# Clone the repository
git clone https://github.com/Nao-30/google-trends-cli
cd google-trends-cli

# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Check test coverage
pytest --cov=src tests/
```

Our test suite covers CLI commands, API functionality, content suggestions, formatting utilities, and helper functions. We welcome contributions to expand test coverage.

## 🤝 Contributing

Contributions are welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## ⚖️ License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 💖 Acknowledgements

- [TrendsPy](https://github.com/sdil87/trendspy) for Google Trends data access
- [Click](https://click.palletsprojects.com/) for the command-line interface
- [Rich](https://github.com/Textualize/rich) for beautiful terminal output
- [NSL](https://blog.mohammed-al-kebsi.space) for project sponsorship