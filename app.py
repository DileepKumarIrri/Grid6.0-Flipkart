from flask import Flask, render_template, request, redirect, url_for, jsonify
import json
import os
from werkzeug.utils import secure_filename
from count import count_grocery_items
from dotenv import load_dotenv
from freshness import analyze_image
from insert_data import insert_fresh_produce
from datetime import datetime,timedelta, timezone
import pytz


# Load environment variables
load_dotenv()

app = Flask(__name__)

# Configuration
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER



# Ensure the upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)



def allowed_file(filename):
    """Check if a file has an allowed extension."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_current_timestamp():
    """Get current timestamp in format: YYYY-MM-DD HH:MM:SS"""
    ist = pytz.timezone('Asia/Kolkata')
    now_utc = datetime.now(timezone.utc)
    now_ist = now_utc.astimezone(ist)
    return now_ist.strftime("%Y-%m-%d %H:%M:%S")

@app.route("/")
def home():
    """Render the home page (index.html)."""
    return render_template("index.html")

@app.route("/grocerydetection")
def grocery():
    return render_template("grocery.html")


@app.route("/freshnessdetection")
def freshness_detection():
    return render_template("freshness.html")

@app.route("/dataanalysis")
def data_analysis():
    return render_template("analysis.html")

@app.route('/aboutus')
def about_us():
    """Render the about us page (aboutus.html)."""
    return render_template('aboutus.html')

@app.route('/architectures')
def architectures():
    """Render the architectures page (architectures.html)."""
    return render_template('architectures.html')

@app.route("/groceryitems", methods=["POST"])
def grocery_detection():
    """Handle image upload and save it to the upload folder."""
    print("grocey")
    try:
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
            
            try:
                response_data = count_grocery_items(file_path)
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


@app.route("/freshproduce", methods=["POST"])
def fresh_detection():
    """Handle image upload and save it to the upload folder."""
    print("Freshness")
    try:
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
            
            # current_utc_time = datetime.now()
            # ist_time = current_utc_time + timedelta(hours=5, minutes=30)
            try:
                result = analyze_image(file_path)
                ts=get_current_timestamp()
                # Split the result by two newlines to separate items
                items = []
                for item in result.split("\n\n"):
                    item_details = {}
                    # Split each item by single newlines to extract key-value pairs
                    for line in item.split("\n"):
                        if ':' in line:
                            key, value = line.split(":", 1)
                            item_details[key.strip()] = value.strip()
                        
                    if item_details:
                        item_details["Timestamp"] = ts
                        items.append(item_details)

                print(items)
                insert_fresh_produce(items)
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
            return jsonify(response)
        
        else:
            return jsonify({'error': 'Invalid file format. Allowed formats: png, jpg, jpeg, gif'}), 400

    except Exception as e:
        print(f"Unexpected error: {e}")
        return jsonify({'error': 'An unexpected error occurred while processing your request'}), 500        
    





if __name__ == "__main__":
    app.run(debug=True)
