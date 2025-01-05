# Smart Vision Technology 🤖  
## &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; For Instant Quality Check ✨  

---

# 🔍 Try out  
## 💥🚀 [![Click Here](static/images/click.gif)](https://flipmobile.tech/) 💥🚀  
*Click the link and witness the power of Smart Vision Technology in action!*  

**[🌐 https://flipvision.tech/](https://flipmobile.tech/)**

---


---
## 📚 **Application Overview**

Smart Vision Technology is an innovative solution designed to automate the quality check process for grocery items and fresh produce. Leveraging advanced machine learning technologies, it provides real-time insights into the quality, freshness, and other essential attributes of the items. This application offers a seamless, user-friendly experience through an interactive web interface, enabling users to analyze grocery items through live streaming or image uploads in both Mobile and Desktop.

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
   - Users can download detailed reports of grocery and fresh produce items in **CSV** file.

6. 📂 **Data Analysis**
   - Our application features dynamic and interactive visualizations, designed to provide users with a clear and engaging way to explore data insights. This unique capability ensures an intuitive and visually appealing experience for users.
---

## 📷 **Web Application**

Below are some of the interface images showcasing key features of the Smart Vision Technology.

### 🏠 **Home Page**
![Home Page](https://github.com/user-attachments/assets/6b1ed6c7-5470-414e-a87e-927f6e767824)


### 📤 **Upload Page**
![upload](https://github.com/user-attachments/assets/1c63dd09-6b0f-4cdd-b073-315baa6847c0)

### 📷 **Capture Page**
![capture](https://github.com/user-attachments/assets/43ab26c9-6b30-4653-81de-91a024607c50)

### 📄 **Report Download**
![Result](https://github.com/user-attachments/assets/eafff043-cabd-4503-b429-d7fd52fa47df)

### 📄 **Realtime Data Analysis through PowerBI**
![Data Analysis](https://github.com/user-attachments/assets/fd3e8633-32cf-4892-b64b-2cff19f8d9fe)

---

## ⚙️ **Functionality Workflow**
![systemarchitecture](https://github.com/user-attachments/assets/9eb2e7b6-29fa-4d1c-a379-09cb509f23eb)

## ⚙️ **Backend Workflow**
![backendarchitecture](https://github.com/user-attachments/assets/ef440907-e4d4-4a15-8d22-7618a21602a1)

## ⚙️ **Database architecture**
![Database architecture](https://github.com/user-attachments/assets/636786aa-15a0-412b-a2bb-72e7a6053f9b)


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

### **Step 4: Realtime Data Analysis through PowerBI** 💾💾💾
- Users can explore and analyze data insights through interactive visualizations powered by Power BI, seamlessly connected to a relational database.
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
├── models/
|
├── .gitignore        
├── app.py                      # Main application script
├── count.py                    # Script for item counting functionality
├── freshness.py                # Backend script for freshness detection
|___


