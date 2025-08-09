# Fact Fetch

A Reddit bot that automatically detects and responds to misinformation about plant-based diets and veganism using AI-powered fact-checking.

## Overview

Fact Fetch is an intelligent Reddit bot that monitors vegan-related subreddits and automatically identifies posts containing misinformation. When misinformation is detected, the bot provides evidence-based counterarguments using a curated database of scientific research papers.

## Features

- **Automated Reddit Monitoring**: Continuously monitors specified subreddits for new posts
- **AI-Powered Fact Checking**: Uses OpenAI's GPT-4 to analyze post content for factual accuracy
- **Scientific Evidence Database**: Leverages 15+ peer-reviewed research papers on plant-based diets, sustainability, and animal agriculture
- **Intelligent Response Generation**: Provides evidence-based counterarguments when misinformation is detected
- **Text Normalization**: Cleans and normalizes Reddit text for better AI analysis
- **Comprehensive Logging**: Detailed logging for monitoring and debugging

## Research Database

The bot uses a curated collection of scientific papers covering:

- Environmental impacts of plant-based vs. animal-based diets
- Health benefits and challenges of plant-based nutrition
- Animal welfare and ethical considerations
- Sustainability of alternative protein sources
- Barriers to plant-based diet adoption
- Consumer behavior and attitudes

## Prerequisites

- Python 3.8+
- Reddit API credentials
- OpenAI API key
- Access to OpenAI's file search feature

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd fact_fetch
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
# Create a .env file with your API credentials
REDDIT_CLIENT_ID=your_reddit_client_id
REDDIT_CLIENT_SECRET=your_reddit_client_secret
REDDIT_USER_AGENT=your_user_agent
REDDIT_USERNAME=your_reddit_username
REDDIT_PASSWORD=your_reddit_password
OPENAI_API_KEY=your_openai_api_key
```

## Configuration

### Reddit API Setup

1. Go to https://www.reddit.com/prefs/apps
2. Create a new application (script type)
3. Note your client ID and client secret
4. Set up your Reddit account credentials

### OpenAI Setup

1. Get an OpenAI API key from https://platform.openai.com/
2. Ensure your account has access to the file search feature
3. The bot uses a specific vector store ID for accessing research papers

## Usage

### Running the Bot

```bash
python -m fact_fetch.bot.main
```

The bot will:
1. Monitor the "vegan" subreddit for new posts
2. Analyze posts with more than 100 words
3. Use AI to determine if content contains misinformation
4. Generate evidence-based responses when misinformation is detected
5. Automatically reply to posts with counterarguments

### Testing

You can test the bot's functionality:

```bash
# Test Reddit bot functionality
python -m fact_fetch.bot.reddit_bot

# Test OpenAI query functionality
python -m fact_fetch.bot.openai_query
```

## How It Works

1. **Monitoring**: The bot continuously monitors specified subreddits using Reddit's API
2. **Text Processing**: Reddit posts are cleaned and normalized using the `RedditTextNormalizer`
3. **AI Analysis**: OpenAI's GPT-4 analyzes the text using a custom system prompt and file search tools
4. **Fact Checking**: The AI determines if content is "misinformation", "unverifiable", or "verified"
5. **Response Generation**: If misinformation is detected, the AI generates a counterargument using scientific evidence
6. **Auto-Reply**: The bot automatically posts the counterargument as a reply

## AI Fact-Checking Process

The bot uses a sophisticated AI system that:

- Evaluates factual accuracy against peer-reviewed research
- Provides reasoning for its classification
- Generates persuasive counterarguments when misinformation is found
- Uses only evidence from the curated research database

## Research Papers Included

The bot has access to 15+ peer-reviewed papers covering:

- Plant-based diet sustainability and environmental impacts
- Health benefits and nutritional considerations
- Animal welfare and ethical farming practices
- Consumer behavior and adoption barriers
- Alternative protein sources and their benefits

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## Ethical Considerations

- The bot is designed to provide evidence-based information, not to promote any specific agenda
- All responses are based on peer-reviewed scientific research
- The bot respects Reddit's terms of service and community guidelines

## Limitations

- Requires active internet connection
- Dependent on Reddit and OpenAI API availability
- May not catch all forms of misinformation
- Responses are limited to topics covered in the research database