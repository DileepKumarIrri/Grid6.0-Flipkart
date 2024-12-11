from flask import Flask, render_template, request, redirect, url_for, jsonify
import os
import json
from werkzeug.utils import secure_filename
from datetime import datetime
from dotenv import load_dotenv
from count import count_grocery_items 
from freshness import analyze_image


# Load environment variables
load_dotenv()

app = Flask(__name__)

# Configure upload folder and allowed file extensions
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)



API_KEY = os.getenv("FIREWORKS_API_KEY")
if not API_KEY:
    raise Exception("API key not found. Please set the fireworks_API_KEY environment variable.")
else:
    FIREWORKS_API_KEY = API_KEY




def allowed_file(filename):
    """Check if file extension is allowed."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def home():
    """Render the upload page (upload.html)."""
    return render_template('index.html')


@app.route('/upload')
def upload_page():
    """Render the upload page (upload.html)."""
    return render_template('upload.html')

@app.route('/livefeed')
def capture():
    """Render the upload page (upload.html)."""
    return render_template('live-feed.html')



@app.route('/uploadimage', methods=['POST'])
def upload_image():
    button_type = request.form.get('button_type')  # Identify button clicked
    print(button_type)

    """Handle image upload and save it to the upload folder."""
    if 'image' not in request.files:
        return 'No file part', 400

    file = request.files['image']

    if file.filename == '':
        return 'No selected file', 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)


        # Process the image (extract details, OCR, etc.)
        if button_type == 'freshproduce':
            # Call the image analysis function and get the result
            try:
                result = analyze_image(file_path)

                # Split the result by two newlines to separate items
                items = []
                for item in result.split("\n\n"):
                    item_details = {}
                    # Split each item by single newlines to extract key-value pairs
                    for line in item.split("\n"):
                        if ':' in line:
                            key, value = line.split(":", 1)
                            item_details[key.strip()] = value.strip()

                    items.append(item_details)
                print(items)
                response = {
                    'total_items': len(items),
                    'table_data': items
                }
            except:
                response = {
                    'total_items': 0,
                    'table_data': []
                }

        else:  # Default to Grocery-Items
            try:
                response_data = count_grocery_items(file_path, FIREWORKS_API_KEY)  # Call count.py function
                response_text = json.loads(response_data)  # Attempt to parse the response as JSON
                print(response_text)

                if not response_text or not isinstance(response_text, list):
                    raise ValueError("Invalid response format")

                # Extract total items from the response
                total_items = response_text[0].get('TotalItems', 0) if 'TotalItems' in response_text[0] else 0

                # Extract the rest of the table data
                table_data = response_text[1:] if len(response_text) > 1 else []

                # print(total_items)
                # print(table_data)

                # Send the JSON response
                response = {
                    'total_items': total_items,
                    'table_data': table_data
                }
            except (json.JSONDecodeError, ValueError, KeyError) as e:
                print(f"Error decoding JSON: {e}")
                response = {
                    'total_items': 0,
                    'table_data': []
                }
        return jsonify(response)
    else:
        return 'Invalid file format', 400


if __name__ == '__main__':
    app.run(debug=True)
