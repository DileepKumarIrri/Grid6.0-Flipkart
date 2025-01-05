const menuToggle = document.getElementById('menuToggle');
const menu = document.getElementById('menu');
const uploadRadio = document.getElementById("uploadImage");
const liveCaptureRadio = document.getElementById("liveCapture");
const uploadButton = document.getElementById("uploadbutton");
const getDetailsButton = document.getElementById("get-det-button");
const getcapDetailsButton = document.getElementById("get-cap-det-button");
const imageContainer = document.getElementById("imageContainer");
const tableContainer = document.getElementById("tableContainer");
const captureOptions = document.getElementById("captureOptions");
const captureButton = document.getElementById("capturebutton");
const capturedCanvas = document.getElementById("capturedCanvas");
const retakeButton = document.getElementById("retakebutton");

let currentStream = null;
let videoElement = null;


document.getElementById('freshness').style.color = "white";
document.getElementById('freshness').style.backgroundColor = "#0552FF";

menuToggle.addEventListener('click', () => {
    menu.classList.toggle('active');
});

document.addEventListener("DOMContentLoaded", function () {
    const uploadSection = document.querySelector(".upload");
    const captureSection = document.querySelector(".capture");

    function updateSectionVisibility() {
        if (uploadRadio.checked) {
            uploadSection.style.display = "block";
            captureSection.style.display = "none";
        } else if (liveCaptureRadio.checked) {
            uploadSection.style.display = "none";
            captureSection.style.display = "block";
        }
    }

    updateSectionVisibility();

    // Event listeners for radio buttons
    uploadRadio.addEventListener("change", function () {
        if (this.checked) {
            uploadSection.style.display = "block";
            captureSection.style.display = "none";
            tableContainer.innerHTML = '<p>upload image...</p>'; 
            downloadButton.style.display = "none";
        }
    });

    liveCaptureRadio.addEventListener("change", function () {
        if (this.checked) {
            uploadSection.style.display = "none";
            captureSection.style.display = "block";
            tableContainer.innerHTML = '<p>capture image...</p>'; 
            downloadButton.style.display = "none";
        }
    });

    captureButton.addEventListener('click', function () {
        captureImage();
    });

    retakeButton.addEventListener('click', function () {
        startCamera();
    });
    
});

document.getElementById('grocery').addEventListener('click', function () {
    window.location.href = "/grocerydetection";
});

document.getElementById('data_anaylysis').addEventListener('click', function () {
    window.location.href = "/dataanalysis";
});


// Function to handle image capturing   
// Populate camera options
navigator.mediaDevices.enumerateDevices().then(devices => {
    const videoDevices = devices.filter(device => device.kind === 'videoinput');
    if (videoDevices.length === 0) {
        alert("No camera devices found.");
    }
    videoDevices.forEach((device, index) => {
        const option = document.createElement('option');
        option.value = device.deviceId;
        option.text = device.label || `Camera ${index + 1}`;
        captureOptions.appendChild(option);
    });
});

// Monitor changes in camera selection and store the selected device ID
let selectedCameraId = null;

// Listen for camera option change
captureOptions.addEventListener("change", function () {
    selectedCameraId = this.value; // Update the selected camera ID
    console.log("Selected Camera ID:", selectedCameraId); // Log for verification
    startCamera(); // Start the camera with the selected device ID
});



// Start camera function
async function startCamera() {
    const selectedCameraId = captureOptions.value;
    tableContainer.innerHTML = '<p>capture image...</p>'; 
    if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
        const constraints = {
            video: {
                deviceId: selectedCameraId ? { exact: selectedCameraId } : undefined
            }
        };
        try {
            const stream = await navigator.mediaDevices.getUserMedia(constraints);
            if (currentStream) {
                // Stop any existing stream
                currentStream.getTracks().forEach(track => track.stop());
            }
            currentStream = stream;

            // Create a video element if it doesn't already exist
            if (!videoElement) {
                videoElement = document.createElement('video');
                videoElement.autoplay = true;
            }
            videoElement.srcObject = stream;

            // Clear and append the video element to the image container
            const imageContainer = document.getElementById('captureContainer');
            imageContainer.innerHTML = ''; // Clear previous content
            imageContainer.appendChild(videoElement);

            videoElement.play();
        } catch (error) {
            alert("Error accessing camera: " + error.message);
        }
    } else {
        alert("Your browser does not support this feature.");
    }
}


// Capture image from the video stream
function captureImage() {
    if (!videoElement || !currentStream) {
        alert("No video stream available");
        return;
    }

    // Create a canvas to capture the frame from the video
    const canvas = capturedCanvas;
    const context = canvas.getContext('2d');
    canvas.width = videoElement.videoWidth;
    canvas.height = videoElement.videoHeight;

    // Draw the current frame from the video onto the canvas
    context.drawImage(videoElement, 0, 0, canvas.width, canvas.height);

    if (currentStream) {
        currentStream.getTracks().forEach(track => track.stop());
    }


    const imgURL = canvas.toDataURL('image/png');
    const imageContainer = document.getElementById('captureContainer');
    imageContainer.innerHTML = `<img src="${imgURL}" alt="Captured Image" class="captured-image">`;
    videoElement = null;
    const tableContainer = document.getElementById('tableContainer');
    tableContainer.innerHTML = '<p>Image captured successfully...</p>'; 
    
    // Optionally, stop the camera stream after capturing the image
    stopCamera();


    // Function to handle "Get Details" button
getcapDetailsButton.addEventListener("click", () => {
    const imageElement = document.querySelector('.captured-image');
    if (!imageElement) {
        alert('Please Capture image To go');
        return;
    }

    document.getElementById('loader').classList.remove('hidden');
    fetch(imageElement.src)
        .then(res => res.blob())
        .then(blob => {
            const formData = new FormData();
            formData.append('image', blob, 'captured_image.png');

            // Send the image to the Flask server using fetch
            fetch('/freshproduce', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json()) // Expect a JSON response from the Flask server
            .then(data => {
                console.log(data, "data")
                displayTable(data); // Call function to display table
                showDownloadButton();
            })
            .catch(error => {
                console.error('Error:', error);
            })
            .finally(() => {
                // Hide the loader once data is processed
                document.getElementById('loader').classList.add('hidden');
            });
        });
});
    
}

// Stop the camera stream
function stopCamera() {
    if (currentStream) {
        const tracks = currentStream.getTracks();
        tracks.forEach(track => track.stop()); // Stop each track (video)
        currentStream = null;
    }
}



// Function to handle image upload
uploadButton.addEventListener("click", () => {
    imageContainer.innerHTML = '<div><img src="static/assets/upload.svg" alt="Upload Image"></div><div><p>Upload Image</p></div>'; // Reset image preview
    uploadImage();
});


function uploadImage() {
    const input = document.createElement('input');
    input.type = 'file';
    input.accept = 'image/*';
    input.click();

    tableContainer.innerHTML = ''; // Clear previous table content

    input.addEventListener('change', function(event) {
        const file = event.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = function(e) {
                const imageContainer = document.getElementById('imageContainer');
                imageContainer.innerHTML = `<img src="${e.target.result}" alt="Uploaded Image" class="uploaded-image">`;
                tableContainer.innerHTML = '<p>Image  uploaded successfully...</p>';
            };
            reader.readAsDataURL(file);
        }
    });
}


// Function to handle "Get Details" button
getDetailsButton.addEventListener("click", () => {
    
    const imageElement = document.querySelector('.uploaded-image');
    if (!imageElement) {
        alert('Please Upload image To go');
        return;
    }

    document.getElementById('loader').classList.remove('hidden'); // Show loader while data is processed
    fetch(imageElement.src)
        .then(res => res.blob())
        .then(blob => {
            const formData = new FormData();
            formData.append('image', blob, 'uploaded_image.png');

            // Send the image to the Flask server using fetch
            fetch('/freshproduce', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json()) // Expect a JSON response from the Flask server
            .then(data => {
                console.log(data, "data")
                displayTable(data); // Call function to display table
                showDownloadButton();
            })
            .catch(error => {
                console.error('Error:', error);
            })
            .finally(() => {
                // Hide the loader once data is processed
                document.getElementById('loader').classList.add('hidden');
            });
        });
});


// Function to create and display the table from JSON data
function displayTable(data) {
    const tableContainer = document.getElementById('tableContainer');

    if (!data || data.length === 0) {
        tableContainer.innerHTML = '<p>No data available to display</p>';
        tableContainer.style.display = 'block'; // Show the container with the message
        return;
    }

    tableContainer.innerHTML = ''; // Clear previous data
    tableContainer.style.display = 'block'; // Show the container when data is available


    // Display total items first
    const totalItemsHTML = `<h2><strong>Total Items: ${data.total_items}</strong></h2>`;
    // console.log(totalItemsHTML)

    let tableHTML = '';
    tableHTML = `
        <table>
            <thead>
                <tr>
                    <th>Sl no</th>
                    <th>Timestamp</th>
                    <th>Produce</th>
                    <th>Freshness</th>
                    <th>Shelf life (Days)</th>
                </tr>
            </thead>
            <tbody>
    `;

    data.table_data.forEach(item => {
        tableHTML += `
            <tr>
                <td>${item["Sl no"]}</td>
                <td>${item["Timestamp"]}</td>
                <td>${item["Produce"]}</td>
                <td>${item["Freshness"]}</td>
                <td>${item["Expected life span (Days)"]}</td>
            </tr>
        `;
    });

    tableHTML += `
        </tbody>
        </table>
    `;

    // Insert total items and table into the page
    tableContainer.innerHTML = totalItemsHTML + tableHTML;
}



function showDownloadButton() {
    const downloadButton = document.getElementById("download-btn");
    downloadButton.style.display = "block";
    downloadButton.addEventListener("click", downloadCSV);
}


// CSV download logic
function downloadCSV() {
    const tableContainer = document.getElementById('tableContainer');
    const table = tableContainer.querySelector('table'); 
    if (!table) {
        alert('No table available for download');
        return;
    }

    let csv = [];
    const rows = table.querySelectorAll('tr');

    for (let i = 0; i < rows.length; i++) {
        const row = [];
        const cols = rows[i].querySelectorAll('td, th');

        for (let j = 0; j < cols.length; j++) {
            row.push(cols[j].innerText.replace(/,/g, '')); 
        }
        csv.push(row.join(','));
    }

    const csvFile = new Blob([csv.join('\n')], { type: 'text/csv' });
    const downloadLink = document.createElement('a');
    downloadLink.download = 'table_data.csv';
    downloadLink.href = window.URL.createObjectURL(csvFile);
    downloadLink.style.display = 'none';

    document.body.appendChild(downloadLink);
    downloadLink.click();
    document.body.removeChild(downloadLink);
}



