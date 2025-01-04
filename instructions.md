instructions
# Python Developer Instructions

## Task Overview
You are tasked with creating a Python script that will analyze day1form.md and create day1form.json to help users create detailed project plans.

## Core Requirements
1. Analyze day1form.md and create day1form.json
2. Convert form fields to JSON key-value pairs
3. Generate interactive questions from fields
4. Process answers through Ollama AI
5. Store final results in JSON format

## Error Logging Requirements
1. Each function must implement detailed error logging:
   - Log function entry with parameters
   - Log all significant operations
   - Catch and log all potential exceptions
   - Include error context and stack traces
   - Log success/failure of operations

## Data Structure
- Each field becomes a JSON key
- Each key contains:
  - Question string
  - Answer string
Example:
```json
{
  "Project Title": {
    "question": "What is the title of your project?",
    "answer": "User's answer here"
  }
}
```

## Process Flow
1. Read markdown file
2. Extract fields
3. For each field:
   - Present question
   - Get user answer
   - Process through Ollama
   - Get user approval (y/n)
   - Repeat if needed
4. Save to JSON file

## File Locations
- Input: day1form.md (same directory)
- Output: day1form.json (same directory)
