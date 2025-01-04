import json
import re
import requests
import sys

def read_markdown_file(file_path):
    """Read and return contents of markdown file."""
    try:
        with open(file_path, 'r') as file:
            return file.read()
    except FileNotFoundError:
        print(f"Error: {file_path} not found.")
        sys.exit(1)

def extract_fields(content):
    """Extract fields from markdown content."""
    # Split content into lines
    lines = content.split('\n')
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
    
    return fields

def generate_questions(fields):
    """Generate questions from field names."""
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

def get_ollama_suggestion(answer):
    """Get suggestion from Ollama AI."""
    try:
        response = requests.post('http://localhost:11434/api/generate', 
                               json={
                                   "model": "llama2",
                                   "prompt": f"Based on this answer: '{answer}', suggest an improved or enhanced version that maintains the core idea but adds more detail or clarity."
                               })
        if response.status_code == 200:
            return response.json()['response']
        else:
            print("Error getting suggestion from Ollama")
            return None
    except Exception as e:
        print(f"Error connecting to Ollama: {e}")
        return None

def main():
    # Read markdown file
    content = read_markdown_file('day1form.md')
    
    # Extract fields
    fields = extract_fields(content)
    
    # Generate questions
    questions = generate_questions(fields)
    
    # Initialize results dictionary
    results = {}
    
    # Process each field
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
                
                results[field] = {
                    "question": question,
                    "answer": suggestion
                }
            else:
                results[field] = {
                    "question": question,
                    "answer": user_answer
                }
    
    # Save results to JSON file
    with open('day1form.json', 'w') as f:
        json.dump(results, f, indent=4)
    
    print("\nForm processing complete! Results saved to day1form.json")

if __name__ == "__main__":
    main()
