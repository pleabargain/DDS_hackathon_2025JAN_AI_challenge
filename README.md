# AI-Assisted Form Processing Tool

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
- Ollama AI engine
- JSON processing capabilities

## Project Structure
```
.
├── day1form.md          # Template form with project planning fields
├── instructions.md      # Project requirements and specifications
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
  "Project Title": {
    "question": "What is the title of your project?",
    "answer": "[User's approved response]"
  },
  // Additional fields follow the same pattern
}
```

## Usage
1. Ensure Python is installed on your system
2. Make sure Ollama AI engine is running
3. Run the Python script
4. Follow the interactive prompts
5. Review AI suggestions (enter 'y' to accept or 'n' to provide alternative)
6. Check generated `day1form.json` for final output

## Development Status
This project is being developed as part of the DDS Hackathon 2025 January AI Challenge, focusing on creating an AI-assisted project planning tool.
