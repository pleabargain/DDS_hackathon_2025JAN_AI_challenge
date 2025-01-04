# System Patterns

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
- User input handling
- SAVE command implementation
- Command validation and execution

### 2. Factory Pattern
- Question generation
- Field extraction
- Response formatting

### 3. Observer Pattern
- Logging system implementation
- Real-time updates
- Progress tracking

### 4. Strategy Pattern
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
   Command Detection -> Progress Capture -> JSON Serialization -> File Write
   ```

3. **Load Operation**
   ```
   File Read -> JSON Parsing -> Data Validation -> State Restoration
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
└── logs/             # Generated logs
```

## Best Practices
1. **Code Organization**
   - Function-specific modules
   - Clear responsibility separation
   - Consistent naming conventions

2. **Error Management**
   - Comprehensive error handling
   - Detailed logging
   - User-friendly messages

3. **Data Handling**
   - Schema validation
   - Safe file operations
   - Progress preservation
