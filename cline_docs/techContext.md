# Technical Context

Repository: https://github.com/pleabargain/DDS_hackathon_2025JAN_AI_challenge

## Development Environment

### Required Software
1. **Python**
   - Version: 3.x
   - Core language for application

2. **Ollama**
   - Local AI model server
   - Required for AI suggestions
   - Installation: https://ollama.ai/download

### Dependencies
```python
# Core Dependencies
json        # JSON handling
re          # Regular expressions
requests    # HTTP client
sys         # System functions
os          # File operations
logging     # Logging system
traceback   # Error tracking
datetime    # Time operations
```

## Configuration

### Logging
- Real-time file logging enabled
- Log files: `form_processor_[timestamp].log`
- Debug level logging
- Both file and console output

### Data Storage
1. **JSON Files**
   - Schema: `schema.json`
   - Example: `test_data.json`
   - User Data: `day1form.json`

2. **Form Template**
   - Format: Markdown
   - File: `day1form.md`

### AI Integration
1. **Ollama API**
   - Endpoint: http://localhost:11434
   - Default Model: llama3.2:latest
   - Configurable model selection

## Technical Constraints

### System Requirements
1. **Hardware**
   - Sufficient RAM for AI model
   - Storage for logs and data

2. **Network**
   - Local network access
   - Ollama API connectivity

### Performance Considerations
1. **Response Time**
   - AI suggestion latency
   - File operation speed
   - Log writing performance

2. **Resource Usage**
   - Memory management
   - Log file growth
   - JSON file size

## Development Guidelines

### Code Style
1. **Python Standards**
   - PEP 8 compliance
   - Clear documentation
   - Type hints (where applicable)

2. **Error Handling**
   - Comprehensive try/except
   - Detailed error messages
   - Proper logging

3. **Documentation**
   - Function docstrings
   - Code comments
   - README updates

### Testing
1. **Manual Testing**
   - Form completion
   - Save/load operations
   - Error scenarios

2. **Data Validation**
   - JSON schema compliance
   - Input validation
   - Output verification

## Security Considerations

### Data Safety
1. **File Operations**
   - Safe file handling
   - Backup considerations
   - Error recovery

2. **Input Validation**
   - User input sanitization
   - Command validation
   - Path verification

### API Security
1. **Ollama Integration**
   - Local-only access
   - Error handling
   - Rate limiting
