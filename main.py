import os
from dotenv import load_dotenv
from nemoguardrails import RailsConfig, LLMRails
import nest_asyncio
import openai
# Load environment variables from .env file
load_dotenv()
nest_asyncio.apply()

openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    raise ValueError("OpenAI API key not found. Please set it in the .env file.")

# Set the OpenAI API key
openai.api_key = openai_api_key

# Define the path to the configuration file
config_path = "./config"
if not os.path.exists(config_path):
    raise ValueError(f"Configuration file does not exist: {config_path}")
try:
    config = RailsConfig.from_path(config_path)
    print("Config loaded successfully.")
except ValueError as e:
    raise ValueError(f"Failed to load configuration: {e}")

# Initialize LLMRails with the loaded configuration
try:
    rails = LLMRails(config)
    print("LLMRails initialized successfully.")
except Exception as e:
    raise ValueError(f"Failed to initialize LLMRails: {e}")


# Function to log and process a user message
def process_message(user_message):
  
    try:
        response =rails.generate(messages=[{"role": "user", "content": user_message}])
        print(f"Model Response: {response['content']}\n")
        # Provide detailed guardrail processing summary
        info = rails.explain()
        info.print_llm_calls_summary()
        print("\n" + "-"*50 + "\n")
    except Exception as e:
        print(f"Error processing message: {e}")

while True:
    user_input = input("Enter your message: ")
    if user_input.lower()in ("quit","exit"):
         break
# Process the user input
    process_message(user_input)
