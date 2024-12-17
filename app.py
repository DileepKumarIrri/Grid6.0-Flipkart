
from flask import Flask, render_template, request, redirect, url_for, jsonify
import os
import json
from werkzeug.utils import secure_filename
from datetime import datetime

from dotenv import load_dotenv
from count import count_grocery_items
from freshness import analyze_image
current_date_str= datetime.now().strftime('%Y-%m-%d %H:%M:%S')

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

# Load API key
try:
    API_KEY = os.getenv("FIREWORKS_API_KEY")
    if not API_KEY:
        raise EnvironmentError("API key not found. Please set the FIREWORKS_API_KEY environment variable.")
    else:
        FIREWORKS_API_KEY = API_KEY
except EnvironmentError as e:
    print(f"Critical Error: {e}")
    exit(1)


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
    """Render the live feed page."""
    return render_template('live-feed.html')


@app.route('/uploadimage', methods=['POST'])
def upload_image():
    """Handle image upload and save it to the upload folder."""
    try:
        button_type = request.form.get('button_type')  # Identify button clicked
        print(button_type)

        if 'image' not in request.files:
            return jsonify({'error': 'No file part provided'}), 400

        file = request.files['image']

        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

            try:
                file.save(file_path)
            except Exception as e:
                return jsonify({'error': f'Failed to save the file: {str(e)}'}), 500

            # Process the image (extract details, OCR, etc.)
            if button_type == 'freshproduce':
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
                            item_details["Timestamp"] = current_date_str

                        items.append(item_details)


                    print(items)
                    response = {
                        'total_items': len(items),
                        'table_data': items
                    }

                except Exception as e:
                    print(f"Error processing image with analyze_image: {e}")
                    response = {
                        'total_items': 0,
                        'table_data': [],
                        'error': 'Failed to process image for freshness analysis.'
                    }

            else:  # Default to Grocery-Items
                try:
                    response_data = count_grocery_items(file_path, FIREWORKS_API_KEY)
                    response_text = json.loads(response_data)  # Attempt to parse the response as JSON
                    print(response_text)

                    if not response_text or not isinstance(response_text, list):
                        raise ValueError("Invalid response format")

                    # Extract total items from the response
                    total_items = response_text[0].get('TotalItems', 0) if 'TotalItems' in response_text[0] else 0

                    # Extract the rest of the table data
                    table_data = response_text[1:] if len(response_text) > 1 else []

                    response = {
                        'total_items': total_items,
                        'table_data': table_data
                    }

                except (json.JSONDecodeError, ValueError, KeyError) as e:
                    print(f"Error decoding JSON from count_grocery_items: {e}")
                    response = {
                        'total_items': 0,
                        'table_data': [],
                        'error': 'Invalid data returned from the grocery counting service.'
                    }

            return jsonify(response)

        else:
            return jsonify({'error': 'Invalid file format. Allowed formats: png, jpg, jpeg, gif'}), 400

    except Exception as e:
        print(f"Unexpected error: {e}")
        return jsonify({'error': 'An unexpected error occurred while processing your request'}), 500


if __name__ == '__main__':
    try:
        app.run(debug=True)
    except Exception as e:
        print(f"Error starting Flask application: {e}")
