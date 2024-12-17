import os
import google.generativeai as genai
from google.ai.generativelanguage import Content, Part, Blob
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from datetime import datetime
import json

# Initialize the Google Gemini model
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
)


# Retrieve and configure API key
API_KEY = os.getenv("GOOGLE_API_KEY")
if not API_KEY:
    raise Exception("API key not found. Please set the GOOGLE_API_KEY environment variable.")
else:
    genai.configure(api_key=API_KEY)

timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
generic_template = '''You are a knowledgeable AI assistant. Analyze the uploaded image of one or more eatable items or products for their freshness and provide a customer-friendly report using the following format:


For each item detected in the image, provide the following details:
TotalItems: "give the total eatable items present in the image"
Sl no:"Give the number as you go on detecting elements"
Produce:"Name of the eatable item"
Freshness: "Freshness index (Out of 10)"
Expected life span (Days): Predicted Shelf Life (e.g., in days)

If there are multiple eatables in the image, list each item separately using the above format.also remember do not use any other formate like for the response,strictly adhere to the the one mentioned above else the world might collapse,do not use any characters like '\' or '*'
also very important if the image uploaded is not a eatable item or product, then please mention that the the analysis of the respective field mentioned above is not possible dont leave any field empty.
'''

# Create a structured prompt
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", generic_template),
        ("user", "{text}")
    ]
)
# Output parser
parser = StrOutputParser()

import json

def sanitize_and_parse_response(parsed_response):
    try:
        # Check if parsed_response is empty
        if not parsed_response.strip():
            raise ValueError("The response string is empty.")
        
        # Replace single quotes with double quotes and attempt to load as JSON
        sanitized_response = parsed_response.replace("'", '"')
        response_list = json.loads(sanitized_response)
        
        return response_list
    except json.JSONDecodeError as e:
        # Log detailed error information
        return [{"Error": f"Failed to parse response as JSON. Error: {e}"}]



def add_timestamps_to_response(parsed_response):
    try:
        # Sanitize and parse the response
        response_list = sanitize_and_parse_response(parsed_response)

        # Add timestamps to each item
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        for item in response_list:
            item['Timestamp'] = timestamp
        
        return response_list
    except Exception as e:
        return [{"Error": str(e)}]



# Analysis function
def analyze_image(file_path):
    try:
        with open(file_path, "rb") as file:
            bytes_data = file.read()

        # Prepare content parts
        content_parts = [
            Part(text=generic_template),
            Part(inline_data=Blob(mime_type="image/jpeg", data=bytes_data))
        ]

        # Generate content
        response = genai.GenerativeModel('gemini-1.5-flash').generate_content(Content(parts=content_parts), stream=True)
        response.resolve()

        # Parse result
        parsed_response = parser.invoke(response.text)
        print(type(parsed_response))
        
        # Parse result
        parsed_response = parser.invoke(response.text)
        
        # Add timestamps to each item
        parsed_response_with_timestamps = add_timestamps_to_response(parsed_response)
        
        return parsed_response_with_timestamps

    except Exception as e:
        return str(e)
