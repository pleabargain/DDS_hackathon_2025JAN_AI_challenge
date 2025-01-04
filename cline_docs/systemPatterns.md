# System Patterns

Repository: https://github.com/pleabargain/DDS_hackathon_2025JAN_AI_challenge

## Architecture Overview

### Core Components
1. **Form Processor**
   - Main script (process_form.py)
   - Handles user interaction
   - Manages form flow
   - Coordinates other components

2. **AI Integration**
   - Ollama API client
   - Suggestion generation
   - Model selection
   - Error handling for AI operations

3. **Data Management**
   - JSON file operations
   - Schema validation
   - Progress saving/loading
   - Data structure maintenance

4. **Logging System**
   - Real-time file logging
   - Operation tracking
   - Error monitoring
   - Debug information

## Design Patterns

### 1. Command Pattern
- User input handling through standardized commands
- Command box UI pattern for clear user guidance
- Available commands:
  * SAVE: Save current progress
  * EDIT: Modify previous answers
  * EXIT: Save (with optional save-as) and quit safely
  * RETURN: Accept previous answer and continue
- Command validation and execution
- Consistent command handling across input contexts
- Options display after each previous answer

### 2. UI Patterns
- Previous Answer Display:
  * Bold blue text formatting using ANSI codes
  * Clear visual distinction from new input
  * Consistent formatting across all answer types
- Command Options:
  * Displayed after each previous answer
  * Clear, boxed format for visibility
  * Consistent ordering and spacing
  * Immediate feedback on command execution

### 3. Factory Pattern
- Question generation
- Field extraction
- Response formatting

### 4. Observer Pattern
- Logging system implementation
- Real-time updates
- Progress tracking

### 5. Strategy Pattern
- AI model selection
- Response processing
- Data validation

## Data Flow
1. **Input Processing**
   ```
   User Input -> Validation -> AI Enhancement -> Storage
   ```

2. **Save Operation**
   ```
   Command Detection -> Progress Capture -> [Optional: Save-As Prompt] -> Filename Generation -> JSON Serialization -> File Write
   ```

   Filename Generation:
   ```
   Project Title -> Clean/Sanitize -> Truncate -> Add Timestamp -> {project_title}_{timestamp}.json
   ```

   Exit Save Flow:
   ```
   EXIT Command -> Save-As Prompt -> [Yes: Smart Filename | No: Default File] -> Save Progress -> Exit
   ```

3. **Load Operation**
   ```
   File Read -> JSON Parsing -> Data Validation -> State Restoration -> Display Previous Answers
   ```

4. **Logging Flow**
   ```
   Event Detection -> Log Formatting -> File Write -> Console Output
   ```

## Error Handling
1. **Hierarchical Approach**
   - Top-level exception handling
   - Specific error types
   - Graceful degradation

2. **Recovery Strategies**
   - Auto-save on error
   - Fallback options
   - User notification

3. **Logging Integration**
   - Error context capture
   - Stack trace recording
   - Debug information

## File Structure
```
project/
├── process_form.py    # Main application
├── schema.json        # Data validation
├── test_data.json    # Example data
├── day1form.md       # Form template
├── day1form.json     # User responses
├── logs/             # Generated logs
└── cline_docs/       # Project documentation
    ├── activeContext.md
    ├── productContext.md
    ├── systemPatterns.md
    ├── techContext.md
    └── progress.md
```

## Best Practices
1. **Code Organization**
   - Function-specific modules
   - Clear responsibility separation
   - Consistent naming conventions
   - Command pattern implementation
   - UI pattern consistency

2. **User Interface**
   - Clear command visibility
   - Consistent command behavior
   - Visual feedback for actions
   - Safe exit paths
   - Bold blue text for previous answers
   - Options display after previous answers

3. **Error Management**
   - Comprehensive error handling
   - Detailed logging
   - User-friendly messages

4. **Data Handling**
   - Schema validation
   - Safe file operations
   - Progress preservation
   - Previous answer retention
   - Multiple save file support
   - Save-as functionality during exit
