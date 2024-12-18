
# ##########################################################################################
#<--------------------------------------Server-Client Model-------------------->>>

# puburl= "https://ab10-34-16-179-34.ngrok-free.app"

# import requests

# # URL of the endpoint
# url = puburl+'/webhook1'

# def count_grocery_items(image_path,api):

# # Send the POST request
#     try:
#         with open(image_path, 'rb') as file:
#             response = requests.post(url, files={'file': file})
#             print(response)

#         # print("Respo  nse Text:", response.text)

#         # Attempt to parse JSON if the response is successful
#         if response.status_code == 200:
#             # print("Response JSON:", response.json())
#             response_json = response.json()
#             return response_json
#         else:
#             print("Non-JSON Response or Error")
#     except Exception as e:
#         print("An error occurred:", str(e))

# image_path=r"C:\Users\darkn\Desktop\images4.jpg"
# print(count_grocery_items(image_path,"api"))

#<----------------------------------API CALL----------------------------------------->>




import requests
import json
import base64
from datetime import datetime
import pytz

ist = pytz.timezone('Asia/Kolkata')
# # Generate timestamps
# current_date = datetime.now()
# current_date_str = current_date.strftime('%Y-%m-%d %H:%M:%S')


def calculate_expiry(expiry_date_str):
    """Calculate expiry status and remaining days."""
    if expiry_date_str == "NA":
        return "NA", "NA"
    
    try:
        expiry_date = datetime.strptime(expiry_date_str, "%d/%m/%Y")
        remaining_days = (expiry_date - current_date).days
        expired = "Yes" if remaining_days < 0 else "No"
        return expired, max(0, remaining_days)
    except ValueError:
        # Invalid expiry date format
        return "NA", "NA"
    
def get_current_timestamp():
    """Get the current timestamp in ISO 8601 format: YYYY-MM-DDTHH:MM:SS±HH:MM."""
    now = datetime.now()
    offset_hours = int(now.utcoffset().total_seconds() / 3600) if now.utcoffset() else 0
    offset_sign = '+' if offset_hours >= 0 else '-'
    offset = f"{offset_sign}{abs(offset_hours):02}:00"
    return now.strftime(f"%Y-%m-%dT%H:%M:%S{offset}")

def process_response(raw_response):
    """Add expiry status and remaining days to the response."""
    processed_data = []
    for item in raw_response:
        if "TotalItems" in item:
            # Append the total items directly
            processed_data.append(item)
        else:
            # Add a timestamp dynamically during processing
            item["Timestamp"] = datetime.now(pytz.utc).astimezone(ist).strftime('%Y-%m-%d %H:%M:%S')
            # Calculate expiry details
            expiry_date = item.get("Expiry date", "NA")
            expired, remaining_days = calculate_expiry(expiry_date)
            # Update the item with calculated fields
            item["Expired"] = expired
            item["Expected life span (Days)"] = remaining_days
            processed_data.append(item)
    return processed_data


def count_grocery_items(image_path, api_key):
    def encode_image(image_path):
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')

    image_base64 = encode_image(image_path)

    # Prompt for the model
    prompt = f"""Task: Detect, identify, and count all distinct grocery items present in the given image.
    Instructions:
    Count all items: Identify and count every visible grocery item in the image, ensuring the total count is as high as possible, even if item names or expiry dates cannot be identified.
    Detect brand names: Recognize and list the brand names of items, if possible. If multiple items of the same brand are present, provide the count for that brand.
    Detect expiry dates: For each brand, attempt to recognize the expiry date of the items as dd/mm/yyyy, if visible. If no expiry date can be identified, mark it as "NA".
    Important Rules for the Output:
    strictly DO NOT include any extra text, explanations, or comments other than the output format.
    If expiry date is "NA", then "Expired" and "Expected life span (Days)" should be "NA". 
    Output format: json
    [
      {{
        "TotalItems":{{total_no_of_items}}
      }},
      {{
        "Sl no": {{serial_number}},
        "Brand": "{{brand_name}}",
        "Expiry date": "{{expiry_date or NA}}",
        "Count": {{count}}
      }}
    ]"""

    url = "https://api.fireworks.ai/inference/v1/chat/completions"
    payload = {
        "model": "accounts/fireworks/models/llama-v3p2-90b-vision-instruct",
        "max_tokens": 4096,
        "top_p": 1,
        "top_k": 40,
        "presence_penalty": 0,
        "frequency_penalty": 0,
        "temperature": 0.6,
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{image_base64}"
                        }
                    },
                    {
                        "type": "text",
                        "text": prompt
                    }
                ]
            }
        ]
    }
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    response = requests.request("POST", url, headers=headers, data=json.dumps(payload))
    print(response)

    raw_response = response.json()['choices'][0]['message']['content']

    # Convert raw response to Python object
    raw_data = json.loads(raw_response)

    # Process the raw data to calculate expiry and add timestamps
    processed_data = process_response(raw_data)

    # Return the updated JSON
    return json.dumps(processed_data, indent=2)


