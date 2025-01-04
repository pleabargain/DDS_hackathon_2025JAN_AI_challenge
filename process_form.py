import json
import re
import requests
import sys
import os
import logging
import traceback
from datetime import datetime

# Configure logging with real-time file updates
log_file = f'form_processor_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file, mode='a', delay=False),  # immediate writes
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)
logger.info(f"Log file created at: {log_file}")

def load_json(file_path):
    """Load and return contents of a JSON file."""
    logger.info(f"Attempting to load JSON file: {file_path}")
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            logger.debug(f"Successfully loaded JSON from {file_path}")
            return data
    except FileNotFoundError:
        logger.error(f"File not found: {file_path}")
        return None
    except json.JSONDecodeError as e:
        logger.error(f"Error decoding JSON from {file_path}: {str(e)}")
        return None
    except Exception as e:
        logger.error(f"Error reading file {file_path}: {str(e)}")
        logger.error(f"Stack trace: {traceback.format_exc()}")
        return None

def prompt_for_json_file():
    """Prompt user to select a JSON file from local directory."""
    logger.info("Prompting user for JSON file selection")
    print("\nAvailable JSON files in current directory:")
    json_files = [f for f in os.listdir('.') if f.endswith('.json')]
    
    if not json_files:
        logger.warning("No JSON files found in current directory")
        print("No JSON files found in current directory")
        return 'day1form.json'  # default
    
    for i, file in enumerate(json_files, 1):
        print(f"{i}. {file}")
    
    while True:
        try:
            choice = input("\nSelect a file number (or press Enter for default 'day1form.json'): ").strip()
            if not choice:
                logger.info("User selected default file (day1form.json)")
                return 'day1form.json'
            
            choice_idx = int(choice) - 1
            if 0 <= choice_idx < len(json_files):
                selected_file = json_files[choice_idx]
                logger.info(f"User selected file: {selected_file}")
                return selected_file
            else:
                print("Invalid selection. Please try again.")
        except ValueError:
            print("Please enter a valid number.")

def prompt_for_save_location():
    """Prompt user for where to save the JSON file."""
    logger.info("Prompting user for save location")
    while True:
        filename = input("\nEnter filename to save (or press Enter for 'day1form.json'): ").strip()
        if not filename:
            logger.info("User selected default save location (day1form.json)")
            return 'day1form.json'
        
        if not filename.endswith('.json'):
            filename += '.json'
        
        if os.path.exists(filename):
            overwrite = input(f"\n{filename} already exists. Overwrite? (y/n): ").lower()
            if overwrite != 'y':
                continue
        
        logger.info(f"User selected save location: {filename}")
        return filename

def save_progress(results, prompt_save=False):
    """Save current progress to JSON file."""
    logger.info("Saving current progress")
    try:
        filename = prompt_for_save_location() if prompt_save else 'day1form.json'
        with open(filename, 'w') as f:
            json.dump(results, f, indent=4)
        logger.info(f"Successfully saved results to {filename}")
        print(f"\nProgress saved to {filename}")
        return True
    except Exception as e:
        logger.error(f"Error saving progress: {str(e)}")
        logger.error(f"Stack trace: {traceback.format_exc()}")
        print("\nError saving progress!")
        return False

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
        key_features = []
        
        for line in lines:
            # Skip empty lines
            if not line.strip():
                continue
                
            # If line ends with colon, it's a field name
            if line.endswith(':'):
                current_field = line[:-1].strip()
                fields[current_field] = [] if current_field == "Key Features" else ""
                logger.debug(f"Found new field: {current_field}")
            # If line starts with number and dot (like "1."), it's part of Key Features
            elif re.match(r'^\d+\.$', line.strip()):
                if current_field == "Key Features":
                    feature = line.strip()[line.strip().find('.')+1:].strip()
                    if feature:
                        fields[current_field].append(feature)
                        logger.debug(f"Added feature: {feature}")
            # If line is just underscores, skip it
            elif all(c == '_' for c in line.strip()):
                continue
            # If in parentheses, it's a description - skip it
            elif line.strip().startswith('(') and line.strip().endswith(')'):
                continue
            # Otherwise, if we have a current field, add content
            elif current_field and line.strip():
                if current_field != "Key Features":
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
            questions[field] = "What are the main features or functionalities of your application? (Enter one at a time, type 'done' when finished)"
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
    default_model = "llama3.2:latest"
    
    if not models:
        logger.warning(f"No models found, checking if {default_model} is available")
        try:
            response = requests.post(
                'http://localhost:11434/api/generate',
                json={"model": default_model, "prompt": "test"}
            )
            if response.status_code == 200:
                logger.info(f"{default_model} is available")
                return default_model
            else:
                logger.error(f"Failed to use {default_model}. Please ensure it's installed.")
                print(f"\nERROR: {default_model} is not available")
                print(f"Please run: ollama pull {default_model}")
                sys.exit(1)
        except requests.exceptions.ConnectionError:
            logger.error("Could not connect to Ollama API")
            print("\nERROR: Could not connect to Ollama API")
            print("Please ensure Ollama is installed and running")
            print("Installation instructions: https://ollama.ai/download")
            sys.exit(1)
    
    print("\nAvailable models:")
    for i, model in enumerate(models, 1):
        print(f"{i}. {model}")
    
    while True:
        try:
            choice = input(f"\nSelect a model number (or press Enter for default '{default_model}'): ").strip()
            if not choice:
                logger.info(f"User selected default model ({default_model})")
                return default_model
            
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

def print_instructions():
    """Print usage instructions."""
    print("\nForm Processing Instructions:")
    print("- Answer each question as thoroughly as possible")
    print("- AI will provide suggestions to enhance your answers")
    print("\nAvailable Commands:")
    print("┌─────────────────────────────────────────────┐")
    print("│ SAVE - Save your progress at any time       │")
    print("│ EDIT - Edit a previous answer              │")
    print("│ EXIT - Exit the program (or press Ctrl+C)  │")
    print("└─────────────────────────────────────────────┘\n")

def edit_answer(results, selected_model):
    """Allow user to edit a specific answer."""
    logger.info("Starting answer editing process")
    
    # Display available fields
    print("\nAvailable fields to edit:")
    fields = list(results["responses"].keys())
    for i, field in enumerate(fields, 1):
        current_answer = results["responses"][field]["answer"]
        if isinstance(current_answer, list):
            print(f"{i}. {field}:")
            for item in current_answer:
                print(f"   - {item}")
        else:
            print(f"{i}. {field}: {current_answer}")
    
    # Get field selection
    while True:
        try:
            choice = input("\nEnter the number of the field to edit (or 0 to cancel): ").strip()
            if choice == '0':
                return
            
            choice_idx = int(choice) - 1
            if 0 <= choice_idx < len(fields):
                field_to_edit = fields[choice_idx]
                break
            else:
                print("Invalid selection. Please try again.")
        except ValueError:
            print("Please enter a valid number.")
    
    # Edit the selected field
    current_data = results["responses"][field_to_edit]
    print(f"\nCurrent answer for '{field_to_edit}':")
    if isinstance(current_data["answer"], list):
        for i, item in enumerate(current_data["answer"], 1):
            print(f"{i}. {item}")
        
        # Handle Key Features editing
        print("\nOptions:")
        print("1. Add new feature")
        print("2. Edit existing feature")
        print("3. Delete feature")
        edit_choice = input("Enter your choice (1-3): ").strip()
        
        if edit_choice == '1':
            feature = input("Enter new feature: ").strip()
            suggestion = get_ollama_suggestion(feature, selected_model)
            if suggestion:
                print(f"\nAI Suggestion: {suggestion}")
                if input("\nUse this suggestion? (y/n): ").lower() == 'y':
                    current_data["answer"].append(suggestion)
                else:
                    current_data["answer"].append(feature)
            else:
                current_data["answer"].append(feature)
        
        elif edit_choice == '2':
            idx = int(input("Enter feature number to edit: ").strip()) - 1
            if 0 <= idx < len(current_data["answer"]):
                new_feature = input("Enter new feature: ").strip()
                suggestion = get_ollama_suggestion(new_feature, selected_model)
                if suggestion:
                    print(f"\nAI Suggestion: {suggestion}")
                    if input("\nUse this suggestion? (y/n): ").lower() == 'y':
                        current_data["answer"][idx] = suggestion
                    else:
                        current_data["answer"][idx] = new_feature
                else:
                    current_data["answer"][idx] = new_feature
        
        elif edit_choice == '3':
            idx = int(input("Enter feature number to delete: ").strip()) - 1
            if 0 <= idx < len(current_data["answer"]):
                del current_data["answer"][idx]
    
    else:
        print(current_data["answer"])
        new_answer = input("\nEnter new answer: ").strip()
        suggestion = get_ollama_suggestion(new_answer, selected_model)
        if suggestion:
            print(f"\nAI Suggestion: {suggestion}")
            if input("\nUse this suggestion? (y/n): ").lower() == 'y':
                current_data["answer"] = suggestion
            else:
                current_data["answer"] = new_answer
        else:
            current_data["answer"] = new_answer
    
    # Save changes
    save_progress(results)
    print(f"\nSuccessfully updated {field_to_edit}")

def format_title_answer(answer):
    """Format the title answer with 'Project Title: ' prefix if not present."""
    if not answer.startswith("Project Title:"):
        return f"Project Title: {answer}"
    return answer

def main():
    logger.info("Starting form processing")
    try:
        print_instructions()
        
        # Handle command line argument for edit mode
        if len(sys.argv) > 1 and sys.argv[1].lower() == '--edit':
            json_file = prompt_for_json_file()
            existing_data = load_json(json_file)
            if existing_data:
                selected_model = select_model()
                existing_data["metadata"]["model"] = selected_model
                edit_answer(existing_data, selected_model)
                sys.exit(0)
            else:
                print("No existing data found to edit.")
                sys.exit(1)
        
        # Prompt for JSON file to load
        json_file = prompt_for_json_file()
        existing_data = load_json(json_file)
        if existing_data:
            print("\nFound existing progress. Would you like to:")
            print("1. Continue from where you left off")
            print("2. Start fresh")
            choice = input("\nEnter your choice (1/2): ").strip()
            if choice == '1':
                results = existing_data
                print("\nLoading previous progress...")
                logger.info("Continuing with existing progress")
            else:
                results = {
                    "metadata": {
                        "model": None,
                        "timestamp": datetime.now().isoformat()
                    },
                    "responses": {}
                }
                logger.info("Starting fresh despite existing progress")
        else:
            results = {
                "metadata": {
                    "model": None,
                    "timestamp": datetime.now().isoformat()
                },
                "responses": {}
            }
            logger.info("Starting fresh - no existing progress found")

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
        
        # Update metadata if starting fresh
        if not existing_data:
            results = {
                "metadata": {
                    "model": selected_model,
                    "timestamp": datetime.now().isoformat()
                },
                "responses": {}
            }
        else:
            # Update only the model in existing data
            results["metadata"]["model"] = selected_model
        
        # Process each field
        logger.info("Processing fields and getting user input")
        for field, question in questions.items():
            # Display previous answer if it exists
            if existing_data and field in existing_data["responses"]:
                prev_answer = existing_data["responses"][field]["answer"]
                if isinstance(prev_answer, list):
                    print(f"\n{question}")
                    print("\033[1;34mPrevious answer:")
                    for item in prev_answer:
                        print(f"- {item}")
                    print("\033[0m")
                else:
                    print(f"\n{question}")
                    print(f"\033[1;34mPrevious answer: {prev_answer}\033[0m")
            else:
                print(f"\n{question}")
            
            if field == "Key Features":
                features = []
                while True:
                    feature = input("Enter feature (or 'done' to finish): ").strip()
                    if feature.lower() == 'done':
                        break
                    if feature.upper() == 'SAVE':
                        save_progress(results)
                        continue
                    if feature.upper() == 'EXIT':
                        print("\nSaving progress before exit...")
                        save_progress(results)
                        print("Goodbye!")
                        sys.exit(0)
                    if feature:
                        # Get AI suggestion for each feature
                        print("\nGetting AI suggestion...")
                        suggestion = get_ollama_suggestion(feature, selected_model)
                        
                        if suggestion:
                            print(f"\nAI Suggestion: {suggestion}")
                            satisfied = input("\nAre you satisfied with this suggestion? (y/n): ").lower()
                            
                            while satisfied != 'y':
                                feature = input("\nPlease provide a new feature: ").strip()
                                print("\nGetting new AI suggestion...")
                                suggestion = get_ollama_suggestion(feature, selected_model)
                                if suggestion:
                                    print(f"\nAI Suggestion: {suggestion}")
                                    satisfied = input("\nAre you satisfied with this suggestion? (y/n): ").lower()
                                else:
                                    print("Using your original feature due to AI service error.")
                                    suggestion = feature
                                    satisfied = 'y'
                            
                            features.append(suggestion)
                        else:
                            features.append(feature)
                
                results["responses"][field] = {
                    "question": question,
                    "answer": features
                }
            else:
                user_answer = input("Your answer: ").strip()
                
                if user_answer.upper() == 'SAVE':
                    save_progress(results)
                    continue
                elif user_answer.upper() == 'EDIT':
                    edit_answer(results, selected_model)
                    continue
                elif user_answer.upper() == 'EXIT':
                    print("\nSaving progress before exit...")
                    save_progress(results)
                    print("Goodbye!")
                    sys.exit(0)
                elif user_answer:
                    # Get AI suggestion
                    print("\nGetting AI suggestion...")
                    suggestion = get_ollama_suggestion(user_answer, selected_model)
                    
                    if suggestion:
                        print(f"\nAI Suggestion: {suggestion}")
                        satisfied = input("\nAre you satisfied with this suggestion? (y/n): ").lower()
                        
                        while satisfied != 'y':
                            user_answer = input("\nPlease provide a new answer: ").strip()
                            print("\nGetting new AI suggestion...")
                            suggestion = get_ollama_suggestion(user_answer, selected_model)
                            if suggestion:
                                print(f"\nAI Suggestion: {suggestion}")
                                satisfied = input("\nAre you satisfied with this suggestion? (y/n): ").lower()
                            else:
                                print("Using your original answer due to AI service error.")
                                suggestion = user_answer
                                satisfied = 'y'
                        
                    final_answer = suggestion if suggestion else user_answer
                    if field == "Project Title":
                        final_answer = format_title_answer(final_answer)
                    
                    results["responses"][field] = {
                        "question": question,
                        "answer": final_answer
                    }
                else:
                    results["responses"][field] = {
                        "question": question,
                        "answer": user_answer
                    }
        
        # Final save with prompt
        logger.info("Form processing complete - prompting for save location")
        save_progress(results, prompt_save=True)
        print("\nForm processing complete!")
        
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
