# AI-Powered Web Testing Framework

This framework combines Selenium WebDriver with AI capabilities for robust and intelligent web testing.

## Features

- AI-powered element location using Google's Gemini API
- Intelligent test actions with natural language processing
- Page object pattern implementation
- Configurable test environments
- Screenshot capture on test failure
- Support for multiple browsers

## Setup

1. Clone the repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```
3. Configure your environment:
   - Update `config.json` with your Gemini API key
   - Configure browser settings in `browsers.json`

## Project Structure

```
├── framework/           # Core framework components
│   ├── actions.py      # Common UI actions
│   ├── ai_finder.py    # AI-powered element locator
│   ├── handlers/       # Page-specific handlers
│   └── utils.py        # Utility functions
├── tests/              # Test cases
│   ├── conftest.py     # pytest configurations
│   └── test_*.py       # Test modules
├── config.json         # Main configuration
└── requirements.txt    # Python dependencies
```

## Running Tests

Run all tests:
```bash
pytest
```

Run specific test:
```bash
pytest tests/test_login.py
```

## Configuration

### config.json
```json
{
  "gemini": {
    "api_key": "YOUR_API_KEY",
    "model_name": "gemini-2.0-flash-001"
  },
  "webdriver": {
    "browser": "chrome",
    "headless": false,
    "implicit_wait": 10
  }
}
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
