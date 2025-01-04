# AI-Enhanced Form Processing System

Repository: https://github.com/pleabargain/DDS_hackathon_2025JAN_AI_challenge

A Python-based form processing system that helps users provide better-quality responses through AI-powered suggestions and real-time feedback.

## Features

- AI-powered response suggestions using Ollama API
- Real-time form validation and feedback
- Save progress at any time by typing 'SAVE'
- Load and continue from previous progress
- Choose JSON file to load from local directory
- Choose custom save location for JSON files
- Project titles automatically formatted (e.g., "Project Title: My Project")
- Previous answers shown in bold blue text when continuing progress
- Detailed logging for system monitoring
- JSON schema validation for form data
- Example test data provided

## Files

- `process_form.py`: Main form processing script
- `generate_docs.py`: Documentation generation script for form responses
- `schema.json`: JSON schema for form data validation
- `test_data.json`: Example form data
- `day1form.md`: Form template in markdown format
- `day1form.json`: Generated form responses
- `form_processor_*.log`: Real-time logging files

## Usage

1. Requirements:
   - Python installed
   - Ollama running
   - Git for version control
2. Run the script:
   ```bash
   python process_form.py
   ```

3. Follow the on-screen instructions:
   - Select a JSON file to load (or use default)
   - Choose to continue progress or start fresh
   - Answer each question thoroughly
   - AI will provide suggestions to enhance your answers

   Available Commands:
   - Type 'SAVE' at any time to save your progress
   - Type 'EDIT' to modify a previous answer
   - Type 'EXIT' to save and quit (with option to save as new file)
   - Type 'RETURN' to accept the previous answer and continue

   Additional Features:
   - Previous answers shown in bold blue text when continuing from saved progress
   - User options displayed after each previous answer
   - Choose where to save your JSON file at completion

4. Your responses will be saved with smart file naming:
   - Default format: `{project_title}_{timestamp}.json` (e.g., `my_project_20240104_120702.json`)
   - Project title is automatically cleaned and truncated for filename compatibility
   - You can also specify a custom filename if desired
   - When exiting, you'll be asked if you want to save as a new file
   - If no, it saves to the default location (`day1form.json`)

## Documentation Generation

To generate documentation from your form responses:
```bash
python generate_docs.py input.json
```
This will create both HTML and Markdown versions of your form responses with proper formatting.

## Logging

The system creates detailed logs in real-time, saved to `form_processor_[timestamp].log`. These logs include:
- System operations
- User interactions
- AI suggestions
- Error tracking
- Progress updates

## Data Files

- `schema.json`: Defines the structure and validation rules for form data
- `test_data.json`: Contains example data showing the expected format
- `day1form.json`: Stores your actual form responses

## Error Handling

The system includes comprehensive error handling for:
- File operations
- API connections
- User interruptions
- Data validation
- Progress saving/loading
