from server.config import *
from llm_calls import *
from utils.rag_utils import rag_call
import json
import re
import os

# Get absolute path to file
project_dir = os.path.dirname(os.path.abspath(__file__))
json_path = os.path.join(project_dir, "knowledge", "embedded_sample01.json")

# Define user messages
user_message = "How long does it take to reach the exit from Unit_33?"
user_message_01 = "What is the escape route from Unit_14?"
user_message_02 = "Can you tell me the evacuation distance from Unit_22 to the nearest exit?"

# Function to process a single evacuation query
def process_evacuation_query(message):
    print(f"\n--- Processing Query: '{message}' ---")
    
    # Extract unit ID from user message
    unit_match = re.search(r'Unit_\d+', message)
    unit_id = unit_match.group(0) if unit_match else "Unknown Unit"
    
    router_output = classify_input(message)
    if router_output == "Refuse to answer":
        print("Sorry, I can only answer questions about architecture.")
        return
    
    print(f"Processing evacuation query for {unit_id}")
    
    # Use RAG to get relevant information
    rag_result = rag_call(f"What is the evacuation route and distance for {unit_id}?", 
                        embeddings=json_path,
                        n_results=5)
    
    # Extract structured information using LLM
    structured_info = extract_evacuation_info(rag_result, unit_id)
    
    try:
        info = json.loads(structured_info)
        print(f"\nEvacuation Information for {unit_id}:")
        print(f"• Distance: {info['distance']}")
        print(f"• Route: {', '.join(info['route'])}")
    except json.JSONDecodeError:
        print("Error parsing evacuation information.")

# Process all three queries
print("=== Processing Multiple Evacuation Queries ===")
process_evacuation_query(user_message)
process_evacuation_query(user_message_01)
process_evacuation_query(user_message_02)