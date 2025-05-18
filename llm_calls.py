from server.config import *
import requests

def call_llm(prompt):
    url = "http://127.0.0.1:1234/v1/chat/completions"
    headers = {"Content-Type": "application/json"}
    payload = {
        "model": "meta-llama-3-8b-instruct",
        "messages": [
            {"role": "system", "content": "You are an assistant that helps with evacuation routing."},
            {"role": "user", "content": prompt}
        ]
    }
    response = requests.post(url, headers=headers, json=payload)
    return response.json()["choices"][0]["message"]["content"]

def classify_input(message):
    response = client.chat.completions.create(
        model=completion_model,
        messages=[
            {
                "role": "system",
                "content": """
                        Your task is to classify if the user message is related to buildings and architecture or not.
                        Output only the classification string.
                        If it is related, output "Related", if not, output "Refuse to answer".

                        # Example #
                        User message: "How do I bake cookies?"
                        Output: "Refuse to answer"

                        User message: "What is the tallest skyscrapper in the world?"
                        Output: "Related"
                        """,
            },
            {
                "role": "user",
                "content": f"""
                        {message}
                        """,
            },
        ],
    )
    return response.choices[0].message.content

def generate_concept(message):
    response = client.chat.completions.create(
        model=completion_model,
        messages=[
            {
                "role": "system",
                "content": """
                        You are a visionary intern at a leading architecture firm.
                        Your task is to craft a short, poetic, and highly imaginative concept for a building design.
                        Weave the initial information naturally into your idea, letting it inspire creative associations and unexpected imagery.
                        Your concept should feel bold, evocative, and memorable — like the opening lines of a story.
                        Keep your response to a maximum of one paragraph.
                        Avoid generic descriptions; instead, focus on mood, atmosphere, and emotional resonance.
                        """,
            },
            {
                "role": "user",
                "content": f"""
                        What is the concept for this building? 
                        Initial information: {message}
                        """,
            },
        ],
    )
    return response.choices[0].message.content

def extract_attributes(message):
    response = client.chat.completions.create(
        model=completion_model,
        messages=[
            {
                "role": "system",
                "content": """

                        # Instructions #
                        You are a keyword extraction assistant.
                        Your task is to read a given text and extract relevant keywords according to three categories: shape, theme, and materials.
                        Only output a JSON object in the following format:
                        {
                            "shape": "keyword1, keyword2",
                            "theme": "keyword3, keyword4",
                            "materials": "keyword5, keyword6"
                        }

                        # Rules #
                        If a category has no relevant keywords, write "None" for that field.
                        Separate multiple keywords in the same field by commas without any additional text.
                        Do not include explanations, introductions, or any extra information—only output the JSON.
                        Focus on concise, meaningful keywords directly related to the given categories.
                        Do not try to format the json output with characters like ```json

                        # Category guidelines #
                        Shape: Words that describe form, geometry, structure (e.g., circle, rectangular, twisting, modular).
                        Theme: Words related to the overall idea, feeling, or concept (e.g., minimalism, nature, industrial, cozy).
                        Materials: Specific physical materials mentioned (e.g., wood, concrete, glass, steel).
                        """,
            },
            {
                "role": "user",
                "content": f"""
                        # GIVEN TEXT # 
                        {message}
                        """,
            },
        ],
    )
    return response.choices[0].message.content

def create_question(message):
    response = client.chat.completions.create(
        model=completion_model,
        messages=[
            {
                "role": "system",
                "content": """
                        # Instruction #
                        You are a thoughtful research assistant specializing in architecture.
                        Your task is to create an open-ended question based on the given text.
                        Your question should invite an answer that points to references to specific brutalist buildings or notable examples.
                        Imagine the question will be answered using a detailed text about brutalist architecture.
                        The question should feel exploratory and intellectually curious.
                        Output only the question, without any extra text.

                        # Examples #
                        - What are some brutalist buildings that embody a strong relationship with the landscape?
                        - Which brutalist structures are known for their monumental scale and raw materiality?
                        - Can you name brutalist buildings that incorporate unexpected geometries or playful spatial compositions?
                        - What are examples of brutalist projects that explore the idea of community or collective living?
                        - Which architects pushed the limits of brutalist design through experimental forms?

                        # Important #
                        Keep the question open-ended, inviting multiple references or examples.
                        The question must be naturally connected to the themes present in the input text.
                        """,
            },
            {
                "role": "user",
                "content": f"""
                        {message}
                        """,
            },
        ],
    )
    return response.choices[0].message.content

def extract_evacuation_info(rag_results, unit_id):
    response = client.chat.completions.create(
        model=completion_model,
        messages=[
            {
                "role": "system",
                "content": """
                You are an evacuation planning assistant.
                Extract the exact distance value and route information for the specified unit from the provided JSON data.
                If the exact unit isn't found, find the closest match.
                
                Return ONLY a valid JSON object with this format:
                {
                    "distance": numeric_value,
                    "route": ["point1", "point2", "point3", ...]
                }
                
                Do not include any explanations or formatting outside the JSON.
                """,
            },
            {
                "role": "user",
                "content": f"""
                Find evacuation information for {unit_id} in this data:
                {rag_results}
                """,
            },
        ],
    )
    return response.choices[0].message.content