# 🤖 Smart Vision Technology 🤖
## &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; For Instant Quality Check ✨

---

## 📚 **Application Overview**

Smart Vision Technology is an innovative solution designed to automate the quality check process for grocery items and fresh produce. Leveraging advanced machine learning technologies, it provides real-time insights into the quality, freshness, and other essential attributes of the items. This application offers a seamless, user-friendly experience through an interactive web interface, enabling users to analyze grocery items through live streaming or image uploads in both Mobile and Desktop.

---

## 🔍 Try out

 *Coming Soon*

---

## 📊 **Key Features** 

1. 🌟 **Grocery Item Count**
   - Automatically counts all grocery items present in an image.

2. 📃 **Text Extraction with High Accuracy**
   - Extracts text from images and provides crucial details like:
     - 🏷️ **Brand Name** of the item
     - ⏳ **Expiry Date** of the item

3. 🍎 **Freshness Analysis for Perishables**
   - Calculates the **Freshness Index** of perishable items such as bread, fruits, and vegetables.
   - Predicts the 📅 **Expected Life Span** (in days) for each perishable item.

4. 🎉 **Interactive Web Interface**
   - Provides a sleek, intuitive user interface.
   - Users can upload images from their desktops or use live streaming for real-time analysis.

5. 📂 **Downloadable Reports**
   - Users can download detailed analysis reports of grocery and fresh produce items in **CSV** file.

---

## 📷 **Web Application**

Below are some of the interface images showcasing key features of the Smart Vision Technology.

### 🏠 **Home Page**
![Home_page](https://github.com/user-attachments/assets/d281d6b4-fd38-4c54-a985-9939ff30c3ca)


### 📤 **Image Upload Page**
![upload](https://github.com/user-attachments/assets/4fcea787-6ecc-47f1-b6db-f4c28170c2aa)

### 📷 **Capture Page**
![Livefeed](https://github.com/user-attachments/assets/d6bfff69-4cfc-4f23-94ac-20b2cfa3924f)

### 📄 **Report Download**
![report](https://github.com/user-attachments/assets/c57064fb-8fe3-4064-b721-67bf19ddd1dd)

---

## ⚙️ **Functionality Workflow**
![Workflow](https://github.com/user-attachments/assets/7e73c1e9-11f7-482b-bcce-f98429f6f4a8)


### **Step 1: Input Stage** 📷
- Users can choose between:
  - 📡 **Live Streaming**: External cameras capture video frames, which are preprocessed to enhance image quality.
  - 🖼️ **Image Upload**: Users can browse and upload images from their desktops.

### **Step 2: Processing Stage** 🔄
- For **Grocery Images**:
  - The system routes the image to a finetuned **Llama 3.2 Vision Language Model**.
  - It identifies all grocery items and provides the following information in a table format:
    - 📦 **Total Number of Items**
    - 🏷️ **Brand Name**
    - ⏳ **Expiry Date**
    - 📅 **Expected Life Span** (in days) for each item

- For **Fresh Produce**:
  - The system analyzes the image and provides the following information in a table format:
    - 🍎 **Item Name**
    - 🍃 **Freshness Index**
    - 📅 **Expected Life Span** (in days)

### **Step 3: Download Reports** 💾💾💾
- Users can download the item details in multiple formats, including:
  - 📂 **CSV**

---
<!-- 
## 🛠️ **System Design** 

--- -->

## 💻 **Technologies Used** 

### Frontend: 
- **HTML** 
- **CSS**
- **JAVASCRIPT**  

### Backend:
- **Flask**
- **Python**
- **OpenCV**
- **PyTorch**  

### Machine Learning:
- **Hugging Face Transformer Models** 
 
- **Quantization Tool**: Unsloth module for faster inference  

### Cloud Services: 
- Google Cloud Bucket for model deployment  



## 📦 **Installation & Setup**

1. **Clone the Repository**
   ```bash
   git https://github.com/DileepKumarIrri/Grid6.0-Flipkart.git
   cd smart-vision-technology

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt

3. **Run the Application**
   ```bash
   python app.py

 ### Project Structure 

 ### Smart Vision Technology
```bash
Smart Vision/
│
├── static/                     # Directory for static assets
│   ├── css/                    # Stylesheets
│   ├── images/                 # Image assets
│   ├── js/                     # JavaScript files
│   └── uploads/                # Directory for uploaded files
│
├── templates/                  # HTML templates
│   ├── index.html         
│   ├── live-feed.html        
│   └── upload.html            
│
|
├── .gitignore        
├── app.py                      # Main application script
├── count.py                    # Script for item counting functionality
├── freshness.py                # Backend script for freshness detection
|___


