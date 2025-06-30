# AI-Powered Web Testing Framework

This framework combines Selenium WebDriver with AI capabilities for robust and intelligent web testing, using natural language descriptions to interact with web elements.

## Features

- AI-powered element location using Google's Gemini API
- Natural language interactions with web elements
- No XPath or CSS selectors needed - AI finds elements automatically
- Rich set of AI-powered actions (click, type, hover, drag & drop, etc.)
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
│   ├── actions.py      # AI-powered UI actions
│   ├── ai_finder.py    # AI-powered element locator
│   └── utils.py        # Utility functions
├── tests/              # Test cases
│   ├── conftest.py     # pytest configurations
│   └── test_*.py       # Test modules
├── config.json         # Main configuration
└── requirements.txt    # Python dependencies
```

## Writing Tests

Example test using AI-powered actions:

```python
def test_login(actions):
    actions.ai_clear_and_type("the username field", "standard_user")
    actions.ai_clear_and_type("the password field", "secret_sauce")
    actions.ai_click("the login button")
    
    assert actions.ai_is_displayed("the inventory page"), "Login failed"
```

Available AI Actions:
- `ai_click(description)` - Click an element
- `ai_clear_and_type(description, text)` - Type into a field
- `ai_hover(description)` - Hover over an element
- `ai_double_click(description)` - Double click an element
- `ai_right_click(description)` - Right click an element
- `ai_drag_and_drop(source_desc, target_desc)` - Drag and drop elements
- `ai_scroll_to(description)` - Scroll to an element
- `ai_wait_until_visible(description)` - Wait for element visibility
- `ai_wait_until_clickable(description)` - Wait for element to be clickable
- `ai_select_option(dropdown_desc, option_desc)` - Select from dropdown
- `ai_get_text(description)` - Get element text
- `ai_is_displayed(description)` - Check if element is visible
- `ai_is_enabled(description)` - Check if element is enabled
- And more...

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

## Key Benefits

1. **Natural Language Testing**: Write tests using human-readable descriptions
2. **Maintenance-Free**: No need to update selectors when UI changes
3. **Self-Healing**: AI adapts to find elements even after UI updates
4. **Readable Tests**: Tests are clear and understandable
5. **Quick Test Development**: No time spent crafting complex selectors

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
