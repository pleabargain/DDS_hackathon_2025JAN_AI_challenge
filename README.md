# Form Processing System

Project Statistics:
- Total Lines of Code: 705 (Python: 365, JSON: 340)
- Total Lines of Documentation: 430 (README, instructions, forms, and other docs)

A Python-based system designed for efficient form management and structured documentation. The system helps users provide comprehensive and organized responses when filling out project documentation forms.

## Features

### Core Functionality
- Structured question-answer format for organized documentation
- Real-time form validation and feedback
- Progress management with save/load capabilities
- Custom file naming with automatic datestamp
- Previous answers displayed in bold blue text
- Comprehensive logging system
- JSON schema validation

### Command System
- `SAVE`: Save current progress at any time
- `EDIT`: Modify previous answers
- `EXIT`: Save and quit safely
- `RETURN`: Accept previous answer and continue

### Data Management
- Structured JSON data storage
- Schema-based validation
- Custom file naming: `{user_input}_{timestamp}.json`
- Multiple save file support
- Progress preservation

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/pleabargain/DDS_hackathon_2025JAN_AI_challenge.git
   cd DDS_hackathon_2025JAN_AI_challenge
   ```

2. Install Python 3.x if not already installed

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Project Structure

```
project/
├── process_form.py    # Main application
├── generate_docs.py   # Documentation generator
├── md_to_pdf.py      # PDF conversion utility
├── schema.json       # Data validation schema
├── test_data.json    # Example data
├── day1form.md       # Form template
├── md_to_pdf.log     # PDF conversion logs
└── form_processor.log # System logs
```

## Usage

### Form Processing

1. Start the form processor:
   ```bash
   python process_form.py
   ```

2. Follow the interactive prompts:
   - Choose to load existing progress or start fresh
   - Answer questions in sequence
   - Use commands (SAVE, EDIT, EXIT, RETURN) as needed
   - Previous answers will be shown in bold blue text

3. Save your progress:
   - Type 'SAVE' at any prompt
   - Enter a custom filename prefix
   - File will be saved as `{your_prefix}_{timestamp}.json`

### Documentation Generation

1. Generate formatted documentation from form responses:
   ```bash
   python generate_docs.py input.json
   ```
   This creates both HTML and Markdown versions of your form responses.

2. Convert markdown to PDF:
   ```bash
   python md_to_pdf.py input.md
   ```
   This converts markdown files to PDF format with proper formatting.

## System Features

### Progress Management
- Save/load functionality with custom naming
- Automatic datestamp for version control
- Multiple save file support
- Interrupt-safe operations
- Real-time progress tracking

### Data Validation
- JSON schema compliance checking
- Input validation
- Consistent data formatting
- Example data provided

### Logging System
- Real-time operation logging
- Detailed error tracking
- System operation auditing
- Debug information capture

## Error Handling

The system includes comprehensive error handling for:
- File operations (read/write)
- User input validation
- Data structure verification
- Progress preservation
- Safe exit procedures

## Best Practices

### File Naming
- Use descriptive prefixes for save files
- Automatic timestamp addition
- Format: `{user_input}_{timestamp}.json`
- Example: `project_20240104_120702.json`

### Form Completion
- Answer questions thoroughly
- Save progress regularly
- Review previous answers when continuing
- Use EDIT command for corrections
- Exit safely using EXIT command

## Support Files

- `schema.json`: Defines form data structure and validation rules
- `test_data.json`: Provides example data in expected format
- `day1form.md`: Contains form template
- `form_processor.log`: Records system operations and errors
- `md_to_pdf.log`: Logs PDF conversion operations

## Recent Changes

- Enhanced file saving mechanism with custom naming
- Added markdown to PDF conversion functionality
- Improved user input handling
- Updated documentation
- Enhanced error handling
- Simplified form processing workflow

## Version Control

After making changes to the project:

1. Stage your changes:
   ```bash
   git add .
   ```

2. Commit with a descriptive message:
   ```bash
   git commit -m "Description of changes made"
   ```

3. Push to the repository:
   ```bash
   git push origin main
   ```

## Planned Improvements

- Input validation for filenames
- Enhanced error messages
- Improved progress tracking
- File backup system
