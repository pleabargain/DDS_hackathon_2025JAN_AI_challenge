import requests
import sys
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_ollama_connection():
    """Test if Ollama API is accessible."""
    try:
        logger.info("Testing Ollama API connection...")
        response = requests.get('http://localhost:11434/api/version')
        if response.status_code == 200:
            logger.info("Successfully connected to Ollama API")
            return True
        else:
            logger.error(f"Failed to connect to Ollama API. Status code: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        logger.error("Could not connect to Ollama API. Is Ollama running?")
        return False

def test_llama2_model():
    """Test if llama2 model is available."""
    try:
        logger.info("Testing llama2 model availability...")
        response = requests.post(
            'http://localhost:11434/api/generate',
            json={
                "model": "llama2",
                "prompt": "test"
            }
        )
        if response.status_code == 200:
            logger.info("llama2 model is available and responding")
            return True
        else:
            logger.error(f"llama2 model test failed. Status code: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        logger.error("Could not connect to Ollama API while testing llama2 model")
        return False

def main():
    """Run Ollama connectivity tests."""
    print("Testing Ollama setup...")
    
    if not test_ollama_connection():
        print("\nERROR: Could not connect to Ollama API")
        print("Please ensure Ollama is installed and running")
        print("Installation instructions: https://ollama.ai/download")
        sys.exit(1)
    
    if not test_llama2_model():
        print("\nERROR: llama2 model is not available")
        print("Please run: ollama pull llama2")
        sys.exit(1)
    
    print("\nSUCCESS: Ollama is properly configured and ready to use")

if __name__ == "__main__":
    main()
