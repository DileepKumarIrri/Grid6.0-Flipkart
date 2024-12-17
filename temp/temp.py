

import requests
import json
import base64
from datetime import datetime

timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
current_date = datetime.now().strftime('%d-%m-%y')



prompt = f"""Task: Detect, identify, and count all distinct grocery items present in the given image.
Instructions:
Count all items: Identify and count every visible grocery item in the image, ensuring the total count is as high as possible, even if item names or expiry dates cannot be identified.
Detect brand names: Recognize and list the brand names of items, if possible. If multiple items of the same brand are present, provide the count for that brand.
Detect expiry dates: For each brand, attempt to recognize the expiry date of the items as dd/mm/yyyy, if visible. If no expiry date can be identified, mark it as "NA".
Timestamp handling: For each detected item, the {timestamp} should be included in the output. If the expiry date is visible and not "NA", calculate the number of days remaining until expiry from the {current_date}.
Determine expiry status: If the current date is past the expiry date, mark "Expired" as "Yes", otherwise "No". Calculate the remaining days before expiry (Expected life span) if the expiry date is valid.
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
    "Timestamp": "{{timestamp}}",
    "Brand": "{{brand_name}}",
    "Expiry date": "{{expiry_date or NA}}",
    "Count": {{count}},
    "Expired": "{{Yes or No or NA}}",
    "Expected life span (Days)": {{remaining_days or NA}}
  }}
]"""


def count_grocery_items(image_path, api_key):
    def encode_image(image_path):
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')

    image_base64 = encode_image(image_path)

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

    response_json = response.json()
  

    # Extract the assistant's message content
    assistant_content = response_json['choices'][0]['message']['content']
    return assistant_content

# ------------------------------------------------------------------------------------

