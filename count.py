
# ##########################################################################################
#<--------------------------------------Server-Client Model-------------------->>>

puburl= "https://ef41-52-55-2-14.ngrok-free.app"

import requests

# URL of the endpoint
url = puburl+'/webhook1'
import requests
import json
import base64
from datetime import datetime,timedelta
from insert_data import insert_packaged_goods
# # Generate timestamps
current_date = datetime.now()
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
            current_utc_time = datetime.now()
            ist_time = current_utc_time + timedelta(hours=5, minutes=30)
            item["Timestamp"] = ist_time.strftime('%Y-%m-%d %H:%M:%S')
            # Calculate expiry details
            expiry_date = item.get("Expiry date", "NA")
            expired, remaining_days = calculate_expiry(expiry_date)
            # Update the item with calculated fields
            item["Expired"] = expired
            item["Expected life span (Days)"] = remaining_days
            processed_data.append(item)
    return processed_data

def count_grocery_items(image_path):

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

# Send the POST request
    try:
        with open(image_path, 'rb') as file:
            response = requests.post(url, files={'file': file}, prompt=prompt)
            print(response)


            response= process_response(response)  #process the response

        # print("Respo  nse Text:", response.text)

        # Attempt to parse JSON if the response is successful
        if response.status_code == 200:
            # print("Response JSON:", response.json())
            insert_packaged_goods(response)
            response_json = response.json()
            return response_json
        else:
            print("Non-JSON Response or Error")
    except Exception as e:
        print("An error occurred:", str(e))



#<----------------------------------API CALL----------------------------------------->>

