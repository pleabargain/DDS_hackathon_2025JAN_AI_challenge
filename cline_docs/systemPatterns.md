# System Patterns

## Architecture
- Single Python script architecture
- File-based input/output system
- Interactive command-line interface
- AI integration via Ollama

## Key Technical Decisions
1. Using markdown for input form (easy to read/parse)
2. JSON for output (structured, easy to process)
3. Interactive CLI for user input
4. Ollama AI for response suggestions
5. Question-answer pair structure in JSON

## Design Patterns
- Input/Output Processing Pattern
  - Read markdown
  - Process fields
  - Generate JSON
- Interactive Pattern
  - User input
  - AI processing
  - User verification
- Data Storage Pattern
  - Structured JSON
  - Key-value pairs
  - Question-answer format
