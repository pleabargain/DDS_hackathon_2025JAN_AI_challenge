# AI-Assisted Form Processing Tool

# repo
https://github.com/pleabargain/DDS_hackathon_2025JAN_AI_challenge


## Project Overview
This project is part of the DDS Hackathon 2025 January AI Challenge. It consists of a Python script that processes a form template (`day1form.md`) and creates a JSON file with AI-assisted responses using Ollama.

## Purpose
The tool helps users create detailed project plans by:
1. Converting form fields into interactive questions
2. Using Ollama AI to generate suggested responses
3. Allowing users to review and customize AI suggestions
4. Storing the final responses in a structured JSON format

## Technical Requirements
- Python
- Ollama AI engine (with at least one model installed)
- Required Python packages (install via requirements.txt)

## Installation
```bash
# Install Python dependencies
pip install -r requirements.txt

# Install/Update Ollama
pip install -U ollama
```

## Ollama Model Support
The tool now supports multiple Ollama models:
1. Lists all available models on your system
2. Allows selection of preferred model (defaults to llama3.2:latest)
3. Stores model choice in output metadata

## Project Structure
```
.
├── day1form.md          # Template form with project planning fields
├── instructions.md      # Project requirements and specifications
├── process_form.py      # Main script for form processing
├── test_ollama.py      # Ollama setup verification script
├── requirements.txt     # Python package dependencies
├── CHANGELOG.md        # Project changes and roadmap
└── day1form.json       # Output file (generated during execution)
```

## How It Works
1. The script reads the `day1form.md` template
2. Converts each form field into a question-answer pair
3. For each question:
   - Prompts user for input
   - Passes input to Ollama for processing
   - Shows AI-generated suggestion
   - Allows user to accept or reject suggestion
   - Stores final answer in JSON format
4. Creates/updates `day1form.json` with all responses

## Form Fields
- Project Title
- Concept Summary
- Target Audience
- Key Features
- Technical Approach
- Expected Challenges
- Submission Format
- Expected Outcome
- Additional Notes (Optional)

## JSON Structure
```json
{
  "metadata": {
    "model": "selected_model_name",
    "timestamp": "ISO-8601 timestamp"
  },
  "responses": {
    "Project Title": {
      "question": "What is the title of your project?",
      "answer": "[User's approved response]"
    }
    // Additional fields follow the same pattern
  }
}
```

## Usage
1. Ensure Python is installed on your system
2. Install required packages: `pip install requests`
3. Make sure Ollama AI engine is running
4. Run the test script to verify setup: `python test_ollama.py`
5. Run the main script: `python process_form.py`
6. Select your preferred AI model from the list
7. Follow the interactive prompts
8. Review AI suggestions (enter 'y' to accept or 'n' to provide alternative)
9. Check generated `day1form.json` for final output

## Testing Ollama Setup
The included `test_ollama.py` script helps verify your Ollama installation:
- Checks if Ollama API is accessible
- Verifies model availability
- Provides clear error messages and setup instructions

## Development Status
This project is being developed as part of the DDS Hackathon 2025 January AI Challenge, focusing on creating an AI-assisted project planning tool.
