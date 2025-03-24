# Tibetan Autocomplete

A smart text editor with AI-powered autocomplete support for both Tibetan and English languages. The editor uses Claude AI (Anthropic's API) to provide context-aware sentence completions and detect gibberish text.

## Features

- Real-time sentence completion for Tibetan and English text
- Smart prediction after 1.5 seconds of typing pause
- Gibberish detection for both languages
- UTF-8 support for proper Tibetan text handling
- File operations (Open/Save) with UTF-8 encoding
- Undo/Redo functionality
- Clean and intuitive user interface

## Requirements

- Python 3.x
- Anthropic API key
- Noto Serif Tibetan font (for Tibetan text rendering)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/tibetan_autocomplete.git
cd tibetan_autocomplete
```

2. Install required packages:
```bash
pip install anthropic
```

3. Set up your Anthropic API key:
```bash
export ANTHROPIC_API_KEY='your-api-key-here'
```

## Usage

1. Start the editor:
```bash
python editor.py
```

2. Writing and Autocomplete:
   - Type any text in Tibetan or English
   - After 1.5 seconds of pause in typing, a grey-colored suggestion appears
   - Press the Tab key to accept and insert the suggested completion
   - If you don't want the suggestion, just keep typing and it will disappear

3. File Operations:
   - Save your work using File → Save or File → Save As...
   - Files are saved as .txt format with full UTF-8 support
   - You can write and save any type of text content
   - Open existing .txt files using File → Open
   - Create new documents with File → New

4. Additional Features:
   - Undo/Redo support for all text operations
   - Real-time gibberish detection
   - Clean interface with intuitive controls

## Code Structure

- `editor.py`: Main text editor implementation with GUI
- `predict.py`: AI prediction logic using Claude API
  - `get_tibetan_completion()`: Get completion for Tibetan text
  - `get_english_completion()`: Get completion for English text
  - `is_gibberish()`: Check if input text is gibberish

## Example Usage

```python
# Tibetan text completion
ང་སྐྱིད་པོ་ # (nga skyid po)

# English text completion
The quick brown fox jumps over
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.