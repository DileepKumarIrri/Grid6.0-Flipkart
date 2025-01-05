import requests
import json
from datetime import datetime, timedelta

# Public URL of the endpoint
puburl = "https://ab10-34-16-179-34.ngrok-free.app"
url = puburl + '/webhook1'

# Generate timestamps
current_date = datetime.now()
def process_response(raw_response):
    """Add expiry status and remaining days to the response."""
    processed_data = []
    
    for item in raw_response:
        if "TotalItems" in item:
            # Append the total items directly
            processed_data.append(item)
        else:
            # Add a timestamp dynamically during processing
            current_utc_time = datetime.now()
            ist_time = current_utc_time + timedelta(hours=5, minutes=30)
            item["Timestamp"] = ist_time.strftime('%Y-%m-%d %H:%M:%S')
    return processed_data
def analyze_image(image_path):
    """Send the image to the endpoint and analyze freshness."""
    generic_template = '''
You are a knowledgeable AI assistant. Analyze the uploaded image of one or more eatable items or products for their freshness and provide a customer-friendly report using the following format:

For each item detected in the image, provide the following details:
TotalItems: "give the total eatable items present in the image"
Sl no: "Give the number as you go on detecting elements"
Produce: "Name of the eatable item"
Freshness: "Freshness index (Out of 10)"
Expected life span (Days): "Predicted Shelf Life (e.g., in days)"

If there are multiple eatables in the image, list each item separately using the above format. 
Also remember, do not use any other format like for the response, strictly adhere to the one mentioned above else the world might collapse. 
Do not use any characters like '\' or '*'. Also very important, if the image uploaded is not an eatable item or product, 
then please mention that the analysis of the respective field mentioned above is not possible. Do not leave any field empty.
'''

    try:
        with open(image_path, 'rb') as file:
            response = requests.post(url, files={'file': file}, prompt=generic_template)
            print(response)

        if response.status_code == 200:
            response_json = response.json()
            processed_data = process_response(response_json)
            print("Processed Data:", json.dumps(processed_data, indent=4))
            return processed_data
        else:
            print("Error: Non-JSON Response or Status Code:", response.status_code)
    except Exception as e:
        print("An error occurred:", str(e))

