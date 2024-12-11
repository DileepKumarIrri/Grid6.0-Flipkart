let currentStream = null;
let videoElement = null;
let currentStream = null;
let videoElement = null;
let buttonType = '';

// Populate available cameras
navigator.mediaDevices.enumerateDevices().then(devices => {
    const videoDevices = devices.filter(device => device.kind === 'videoinput');
    const cameraSelect = document.getElementById('cameraSelect');
    videoDevices.forEach((device, index) => {
        const option = document.createElement('option');
        option.value = device.deviceId;
        option.text = device.label || `Camera ${index + 1}`;
        cameraSelect.appendChild(option);
    });
});

// Populate available cameras
navigator.mediaDevices.enumerateDevices().then(devices => {
    const videoDevices = devices.filter(device => device.kind === 'videoinput');
    const cameraSelect = document.getElementById('cameraSelect');
    videoDevices.forEach((device, index) => {
        const option = document.createElement('option');
        option.value = device.deviceId;
        option.text = device.label || `Camera ${index + 1}`;
        cameraSelect.appendChild(option);
    });
});

// Start the camera for Grocery Items
document.getElementById('groceryBtn').addEventListener('click', function() {
    buttonType = 'grocery';
    startCamera();
});

// Start the camera for Fresh Produce
document.getElementById('freshproduceBtn').addEventListener('click', function() {
    buttonType = 'freshproduce';
    startCamera();
});

// Start camera function
function startCamera() {
    const selectedCameraId = document.getElementById('cameraSelect').value;
    const selectedCameraId = document.getElementById('cameraSelect').value;
    if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
        const constraints = {
            video: { 
                deviceId: selectedCameraId ? { exact: selectedCameraId } : undefined 
            }
        };
        navigator.mediaDevices.getUserMedia(constraints)
        const constraints = {
            video: { 
                deviceId: selectedCameraId ? { exact: selectedCameraId } : undefined 
            }
        };
        navigator.mediaDevices.getUserMedia(constraints)
            .then(function(stream) {
                currentStream = stream;
                if (videoElement) {
                    videoElement.srcObject = null; // Clear the existing video stream
                }
                if (videoElement) {
                    videoElement.srcObject = null; // Clear the existing video stream
                }
                videoElement = document.createElement('video');
                videoElement.srcObject = stream;
                videoElement.play();
                const imageContainer = document.getElementById('imageContainer');
                imageContainer.innerHTML = ''; // Clear previous content
                imageContainer.innerHTML = ''; // Clear previous content
                imageContainer.appendChild(videoElement);
            })
            .catch(function(error) {
                alert("Error accessing camera: " + error.message);
            });
    } else {
        alert("Your browser does not support this feature.");
    }
}

// Capture photo
// Capture photo
document.getElementById('captureBtn').addEventListener('click', function() {
    if (videoElement) {
        const canvas = document.getElementById('photoCanvas');
        canvas.width = videoElement.videoWidth;
        canvas.height = videoElement.videoHeight;
        const context = canvas.getContext('2d');
        context.drawImage(videoElement, 0, 0, canvas.width, canvas.height);

        if (currentStream) {
            currentStream.getTracks().forEach(track => track.stop());
        }

        const imgURL = canvas.toDataURL('image/png');
        const imageContainer = document.getElementById('imageContainer');
        imageContainer.innerHTML = `<img src="${imgURL}" alt="Captured Image" class="captured-image">`;
        videoElement = null;
        videoElement = null;
        const tableContainer = document.getElementById('tableContainer');
        tableContainer.innerHTML = ''; 
        tableContainer.style.display = 'none'; 
        tableContainer.innerHTML = ''; 
        tableContainer.style.display = 'none'; 
    } else {
        alert("No video feed available to capture.");
    }
});

// Send image to server
// Send image to server
document.querySelector('.details').addEventListener('click', function() {
    const imageElement = document.querySelector('.captured-image');
    if (!imageElement) {
        alert('No image captured or uploaded');
        return;
    }

    document.getElementById('loader').classList.remove('hidden');
    document.getElementById('loader').classList.remove('hidden');

    fetch(imageElement.src)
        .then(res => res.blob())
        .then(blob => {
            const formData = new FormData();
            formData.append('image', blob, 'captured_image.png'); 
            formData.append('button_type', buttonType);
            formData.append('image', blob, 'captured_image.png'); 
            formData.append('button_type', buttonType);

            fetch('/uploadimage', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json()) 
            .then(response => response.json()) 
            .then(data => {
                displayTable(data, buttonType);
                showDownloadButton();
            })
            .catch(error => {
                console.error('Error:', error);
            })
            .finally(() => {
                document.getElementById('loader').classList.add('hidden');
            });
        });
});

// Display Table
// Display Table
function displayTable(data, buttonType) {
    const tableContainer = document.getElementById('tableContainer');
    if (!data || data.length === 0) {
        tableContainer.innerHTML = '<p>No data available to display</p>';
        tableContainer.style.display = 'block'; 
        tableContainer.style.display = 'block'; 
        return;
    }
    tableContainer.innerHTML = ''; 
    tableContainer.style.display = 'block'; 

    const totalItemsHTML = `<h2 style="margin-top:20px; text-align: left; color:black"><strong>Total Items: ${data.total_items}</strong></h2>`;
    console.log(totalItemsHTML)

    let tableHTML = `
        <table>
            <thead>
                <tr>
                    <th>Sl no</th>
                    <th>Timestamp</th>
                    <th>Brand</th>
                    <th>Expiry date</th>
                    <th>Count</th>
                    <th>Expired</th>
                    <th>Expected life span (Days)</th>
                </tr>
            </thead>
            <tbody>
    `;

    data.table_data.forEach(item => {
        tableHTML += `
            <tr>
                <td>${item["Sl no"]}</td>
                <td>${item["Timestamp"]}</td>
                <td>${item["Brand"]}</td>
                <td>${item["Expiry date"]}</td>
                <td>${item["Count"]}</td>
                <td>${item["Expired"]}</td>
                <td>${item["Expected life span (Days)"]}</td>
            </tr>
        `;
    });
    data.table_data.forEach(item => {
        tableHTML += `
            <tr>
                <td>${item["Sl no"]}</td>
                <td>${item["Timestamp"]}</td>
                <td>${item["Brand"]}</td>
                <td>${item["Expiry date"]}</td>
                <td>${item["Count"]}</td>
                <td>${item["Expired"]}</td>
                <td>${item["Expected life span (Days)"]}</td>
            </tr>
        `;
    });

    tableHTML += `</tbody></table>`;
    tableContainer.innerHTML = tableHTML;
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

document.getElementById('download-btn').addEventListener('click', downloadCSV);
