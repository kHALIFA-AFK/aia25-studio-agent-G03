from server.config import *
from llm_calls import *
from utils.rag_utils import rag_call
import json

user_message = "Can I eat fried rice"

### EXAMPLE 1: Router ###
# Classify the user message to see if we should answer or not
router_output = classify_input(user_message)
if router_output == "Refuse to answer":
    llm_answer = "Sorry, I can only answer questions about the escape route and circulation."

else:
    print(router_output)
    ### EXAMPLE 2: Simple call ###
    # simple call to LLM, try different sys prompt flavours
    brainstorm = generate_concept(user_message)
    print(brainstorm)

    ### EXAMPLE 4: Structured Output ###
    # extract the architecture attributes from the user
    # parse a structured output with regex
    attributes = extract_attributes(brainstorm)
    print(attributes)

    attributes = attributes.strip()
    attributes = json.loads(attributes)
    shape, theme, materials = (attributes[k] for k in ("shape", "theme", "materials"))

    ### EXAMPLE 3: Chaining ###
    brutalist_question = create_question(theme)
    print(brutalist_question)
    # call llm with the output of a previous call

    ### EXAMPLE 5: RAG ####
    # Get a response based on the knowledge found
    rag_result= rag_call(brutalist_question, embeddings = "knowledge/brutalism_embeddings.json", n_results = 10)
    print(rag_result)