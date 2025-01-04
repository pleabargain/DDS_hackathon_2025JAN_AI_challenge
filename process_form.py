import json
import re
import requests
import sys
import logging
import traceback
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f'form_processor_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def read_markdown_file(file_path):
    """Read and return contents of markdown file."""
    logger.info(f"Attempting to read markdown file: {file_path}")
    try:
        with open(file_path, 'r') as file:
            content = file.read()
            logger.debug(f"Successfully read {len(content)} characters from {file_path}")
            return content
    except FileNotFoundError:
        logger.error(f"File not found: {file_path}")
        raise
    except Exception as e:
        logger.error(f"Error reading file {file_path}: {str(e)}")
        logger.error(f"Stack trace: {traceback.format_exc()}")
        raise

def extract_fields(content):
    """Extract fields from markdown content."""
    logger.info("Starting field extraction from markdown content")
    try:
        # Split content into lines
        lines = content.split('\n')
        logger.debug(f"Split content into {len(lines)} lines")
        
        fields = {}
        current_field = None
        
        for line in lines:
            # Skip empty lines
            if not line.strip():
                continue
                
            # If line ends with colon, it's a field name
            if line.endswith(':'):
                current_field = line[:-1].strip()
                fields[current_field] = ""
                logger.debug(f"Found new field: {current_field}")
            # If line starts with number and dot (like "1."), it's part of Key Features
            elif re.match(r'^\d+\.$', line.strip()):
                continue
            # If line is just underscores, skip it
            elif all(c == '_' for c in line.strip()):
                continue
            # If in parentheses, it's a description - skip it
            elif line.strip().startswith('(') and line.strip().endswith(')'):
                continue
            # Otherwise, if we have a current field, add content
            elif current_field and line.strip():
                if fields[current_field]:
                    fields[current_field] += " " + line.strip()
                else:
                    fields[current_field] = line.strip()
                logger.debug(f"Added content to {current_field}")
        
        logger.info(f"Successfully extracted {len(fields)} fields")
        return fields
        
    except Exception as e:
        logger.error(f"Error extracting fields: {str(e)}")
        logger.error(f"Stack trace: {traceback.format_exc()}")
        raise
def generate_questions(fields):
    """Generate questions from field names."""
    logger.info("Generating questions from fields")
    logger.debug(f"Processing fields: {list(fields.keys())}")
    questions = {}
    for field in fields:
        if field == "Project Title":
            questions[field] = "What is the title of your project?"
        elif field == "Concept Summary":
            questions[field] = "What is the main concept of your project and what problem does it solve?"
        elif field == "Target Audience":
            questions[field] = "Who is the target audience for your project and what are their needs?"
        elif field == "Key Features":
            questions[field] = "What are the main features or functionalities of your application?"
        elif field == "Technical Approach":
            questions[field] = "How do you plan to implement your project technically?"
        elif field == "Expected Challenges":
            questions[field] = "What challenges do you anticipate and how will you address them?"
        elif field == "Submission Format":
            questions[field] = "How will you present your final submission?"
        elif field == "Expected Outcome":
            questions[field] = "What are your goals for this project?"
        elif field == "Additional Notes":
            questions[field] = "Do you have any additional information to add?"
    return questions

def get_available_models():
    """Get list of available Ollama models."""
    logger.info("Fetching available Ollama models")
    try:
        response = requests.get('http://localhost:11434/api/tags')
        if response.status_code == 200:
            models = [model['name'] for model in response.json()['models']]
            logger.debug(f"Found models: {models}")
            return models
        else:
            logger.error(f"Failed to get models. Status code: {response.status_code}")
            return None
    except Exception as e:
        logger.error(f"Error getting models: {str(e)}")
        return None

def select_model():
    """Prompt user to select an Ollama model."""
    logger.info("Starting model selection process")
    models = get_available_models()
    
    if not models:
        logger.warning("No models found, defaulting to llama3.2:latest")
        return "llama3.2:latest"
    
    print("\nAvailable models:")
    for i, model in enumerate(models, 1):
        print(f"{i}. {model}")
    
    while True:
        try:
            choice = input("\nSelect a model number (or press Enter for default 'llama3.2:latest'): ").strip()
            if not choice:
                logger.info("User selected default model (llama3.2:latest)")
                return "llama3.2:latest"
            
            choice_idx = int(choice) - 1
            if 0 <= choice_idx < len(models):
                selected_model = models[choice_idx]
                logger.info(f"User selected model: {selected_model}")
                return selected_model
            else:
                print("Invalid selection. Please try again.")
        except ValueError:
            print("Please enter a valid number.")

def get_ollama_suggestion(answer, model):
    """Get suggestion from Ollama AI."""
    logger.info(f"Requesting suggestion from Ollama AI using model: {model}")
    logger.debug(f"Input answer: {answer}")
    
    try:
        logger.debug("Sending POST request to Ollama API")
        response = requests.post(
            'http://localhost:11434/api/generate', 
            json={
                "model": model,
                "prompt": f"Based on this answer: '{answer}', suggest an improved or enhanced version that maintains the core idea but adds more detail or clarity."
            }
        )
        
        if response.status_code == 200:
            suggestion = response.json()['response']
            logger.debug(f"Received suggestion from Ollama: {suggestion}")
            return suggestion
        else:
            logger.error(f"Ollama API error - Status code: {response.status_code}")
            logger.error(f"Response content: {response.text}")
            return None
            
    except requests.exceptions.ConnectionError:
        logger.error("Connection error - Unable to connect to Ollama API")
        logger.error(f"Stack trace: {traceback.format_exc()}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error while getting Ollama suggestion: {str(e)}")
        logger.error(f"Stack trace: {traceback.format_exc()}")
        return None

def main():
    logger.info("Starting form processing")
    try:
        # Select AI model
        logger.info("Selecting AI model")
        selected_model = select_model()
        
        # Read markdown file
        logger.info("Reading markdown file")
        content = read_markdown_file('day1form.md')
        
        # Extract fields
        logger.info("Extracting fields from content")
        fields = extract_fields(content)
        
        # Generate questions
        logger.info("Generating questions")
        questions = generate_questions(fields)
        
        # Initialize results dictionary with metadata
        results = {
            "metadata": {
                "model": selected_model,
                "timestamp": datetime.now().isoformat()
            },
            "responses": {}
        }
        
        # Process each field
        logger.info("Processing fields and getting user input")
        for field, question in questions.items():
            print(f"\n{question}")
            user_answer = input("Your answer: ").strip()
            
            if user_answer:
                # Get AI suggestion
                print("\nGetting AI suggestion...")
                suggestion = get_ollama_suggestion(user_answer)
                
                if suggestion:
                    print(f"\nAI Suggestion: {suggestion}")
                    satisfied = input("\nAre you satisfied with this suggestion? (y/n): ").lower()
                    
                    while satisfied != 'y':
                        user_answer = input("\nPlease provide a new answer: ").strip()
                        print("\nGetting new AI suggestion...")
                        suggestion = get_ollama_suggestion(user_answer)
                        if suggestion:
                            print(f"\nAI Suggestion: {suggestion}")
                            satisfied = input("\nAre you satisfied with this suggestion? (y/n): ").lower()
                        else:
                            print("Using your original answer due to AI service error.")
                            suggestion = user_answer
                            satisfied = 'y'
                    
                results["responses"][field] = {
                    "question": question,
                    "answer": suggestion
                }
            else:
                results["responses"][field] = {
                    "question": question,
                    "answer": user_answer
                }
        
        # Save results to JSON file
        logger.info("Saving results to JSON file")
        with open('day1form.json', 'w') as f:
            json.dump(results, f, indent=4)
        logger.info("Successfully saved results to day1form.json")
        print("\nForm processing complete! Results saved to day1form.json")
        
    except KeyboardInterrupt:
        logger.warning("Process interrupted by user")
        print("\nProcess interrupted by user")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Error in main process: {str(e)}")
        logger.error(f"Stack trace: {traceback.format_exc()}")
        print(f"\nAn error occurred: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
