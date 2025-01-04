import json
import os
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

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
        return None

def generate_html(data, output_file):
    """Generate HTML file from JSON data."""
    logger.info(f"Generating HTML file: {output_file}")
    try:
        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{data['responses']['Project Title']['answer']}</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            line-height: 1.6;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
        }}
        .section {{
            margin-bottom: 20px;
        }}
        h1 {{
            color: #2c3e50;
            border-bottom: 2px solid #3498db;
            padding-bottom: 10px;
        }}
        h2 {{
            color: #34495e;
        }}
        ul {{
            list-style-type: disc;
            padding-left: 20px;
        }}
        .metadata {{
            color: #7f8c8d;
            font-size: 0.9em;
            margin-bottom: 20px;
        }}
    </style>
</head>
<body>
    <div class="metadata">
        Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        <br>
        Model used: {data['metadata']['model']}
    </div>
"""
        
        for field, content in data['responses'].items():
            html_content += f'    <div class="section">\n        <h2>{field}</h2>\n'
            if isinstance(content['answer'], list):
                html_content += '        <ul>\n'
                for item in content['answer']:
                    html_content += f'            <li>{item}</li>\n'
                html_content += '        </ul>\n'
            else:
                html_content += f'        <p>{content["answer"]}</p>\n'
            html_content += '    </div>\n'

        html_content += """</body>
</html>"""

        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        logger.info(f"Successfully generated HTML file: {output_file}")
        return True
    except Exception as e:
        logger.error(f"Error generating HTML file: {str(e)}")
        return False

def generate_markdown(data, output_file):
    """Generate Markdown file from JSON data."""
    logger.info(f"Generating Markdown file: {output_file}")
    try:
        md_content = f"""# {data['responses']['Project Title']['answer']}

*Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*  
*Model used: {data['metadata']['model']}*

"""
        for field, content in data['responses'].items():
            if field != 'Project Title':  # Skip title since it's already at the top
                md_content += f"## {field}\n\n"
                if isinstance(content['answer'], list):
                    for item in content['answer']:
                        md_content += f"- {item}\n"
                else:
                    md_content += f"{content['answer']}\n"
                md_content += "\n"

        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(md_content)
        logger.info(f"Successfully generated Markdown file: {output_file}")
        return True
    except Exception as e:
        logger.error(f"Error generating Markdown file: {str(e)}")
        return False

def generate_documentation(json_file):
    """Main function to generate documentation from JSON file."""
    # Load JSON data
    data = load_json(json_file)
    if not data:
        print("Failed to load JSON file.")
        return False

    # Extract project title for filename
    try:
        title = data['responses']['Project Title']['answer']
        if title.startswith("Project Title: "):
            title = title[14:]
        safe_title = "".join(c if c.isalnum() else "_" for c in title)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    except KeyError:
        logger.error("JSON file does not contain Project Title")
        print("Error: JSON file must contain a Project Title")
        return False

    # Prompt for output format
    while True:
        format_choice = input("Choose output format (html/md): ").lower().strip()
        if format_choice in ['html', 'md']:
            break
        print("Please enter either 'html' or 'md'")

    # Generate appropriate file
    output_file = f"{safe_title}_{timestamp}.{format_choice}"
    if format_choice == 'html':
        success = generate_html(data, output_file)
    else:
        success = generate_markdown(data, output_file)

    if success:
        print(f"\nSuccessfully generated {format_choice.upper()} file: {output_file}")
        return True
    else:
        print(f"\nFailed to generate {format_choice.upper()} file")
        return False

def print_info():
    """Print information about what the script does."""
    print("\nDocument Generator")
    print("=================")
    print("This script helps you create HTML or Markdown documentation from your JSON files.")
    print("\nWhat it does:")
    print("1. Lists available JSON files in current directory")
    print("2. Lets you select a JSON file to process")
    print("3. Asks whether you want HTML or MD output")
    print("4. Creates a well-structured document containing:")
    print("   - Project title")
    print("   - Generation timestamp")
    print("   - AI model used")
    print("   - All fields from your JSON organized into sections")
    print("\nThe output file will be named using your project title and timestamp.")
    print("\nPress Enter to continue or Ctrl+C to exit...")
    input()

if __name__ == "__main__":
    print_info()
    
    # List JSON files in current directory
    json_files = [f for f in os.listdir('.') if f.endswith('.json')]
    if not json_files:
        print("No JSON files found in current directory")
        exit(1)

    print("\nAvailable JSON files:")
    for i, file in enumerate(json_files, 1):
        print(f"{i}. {file}")

    while True:
        try:
            choice = input("\nSelect a file number: ").strip()
            choice_idx = int(choice) - 1
            if 0 <= choice_idx < len(json_files):
                selected_file = json_files[choice_idx]
                break
            else:
                print("Invalid selection. Please try again.")
        except ValueError:
            print("Please enter a valid number.")

    generate_documentation(selected_file)
