let currentStream = null; // To keep track of the active video stream
let videoElement = null; // To keep track of the video element
let buttonType = '';

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
    if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
        navigator.mediaDevices.getUserMedia({ video: true })
            .then(function(stream) {
                currentStream = stream;
                videoElement = document.createElement('video');
                videoElement.srcObject = stream;
                videoElement.play();
                const imageContainer = document.getElementById('imageContainer');
                imageContainer.innerHTML = ''; // Clear any previous content
                imageContainer.appendChild(videoElement);
            })
            .catch(function(error) {
                alert("Error accessing camera: " + error.message);
            });
    } else {
        alert("Your browser does not support this feature.");
    }
}

// Capture photo when Capture button is clicked
document.getElementById('captureBtn').addEventListener('click', function() {
    if (videoElement) {
        const canvas = document.getElementById('photoCanvas');
        canvas.width = videoElement.videoWidth;
        canvas.height = videoElement.videoHeight;
        const context = canvas.getContext('2d');
        context.drawImage(videoElement, 0, 0, canvas.width, canvas.height);

        // Stop the video stream
        if (currentStream) {
            currentStream.getTracks().forEach(track => track.stop());
        }

        // Replace video with captured photo
        const imgURL = canvas.toDataURL('image/png');
        const imageContainer = document.getElementById('imageContainer');
        imageContainer.innerHTML = `<img src="${imgURL}" alt="Captured Image" class="captured-image">`;

        // Hide the video element
        videoElement = null; // Reset video element
        // Clear the image container and table when a new image is uploaded
        const tableContainer = document.getElementById('tableContainer');
        tableContainer.innerHTML = ''; // Clear previous table content
        tableContainer.style.display = 'none'; // Hide table container
    } else {
        alert("No video feed available to capture.");
    }
});


// Send captured image to the Flask server
document.querySelector('.details').addEventListener('click', function() {
    const imageElement = document.querySelector('.captured-image');
    if (!imageElement) {
        alert('No image captured or uploaded');
        return;
    }

     // Show the loader when "Get-Details" is clicked
     document.getElementById('loader').classList.remove('hidden');

    // Get the image as a Blob
    fetch(imageElement.src)
        .then(res => res.blob())
        .then(blob => {
            const formData = new FormData();
            formData.append('image', blob, 'captured_image.png'); // Send as captured_image.png
            formData.append('button_type', buttonType); // Pass the button type

            // Send the image to the Flask server using fetch
            fetch('/uploadimage', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json()) // Expect a JSON response from the Flask server
            .then(data => {
                // console.log(data, "data")
                displayTable(data, buttonType); // Call function to display table
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
function displayTable(data, buttonType) {
    const tableContainer = document.getElementById('tableContainer');

    if (!data || data.length === 0) {
        tableContainer.innerHTML = '<p>No data available to display</p>';
        tableContainer.style.display = 'block'; // Show the container with the message
        return;
    }

    tableContainer.innerHTML = ''; // Clear previous data
    tableContainer.style.display = 'block'; // Show the container when data is available

    // Display total items first
    const totalItemsHTML = `<h2 style="margin-top:20px; text-align: left;"><strong>Total Items: ${data.total_items}</strong></h2>`;
    console.log(totalItemsHTML)

    let tableHTML = '';

    if (buttonType === 'grocery') {
        tableHTML = `
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

    } else if (buttonType === 'freshproduce') {
        tableHTML = `
            <table>
                <thead>
                    <tr>
                        <th>Sl no</th>
                        <th>Timestamp</th>
                        <th>Produce</th>
                        <th>Freshness</th>
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
                    <td>${item["Produce"]}</td>
                    <td>${item["Freshness"]}</td>
                    <td>${item["Expected life span (Days)"]}</td>
                </tr>
            `;
        });
    }

    tableHTML += `
        </tbody>
        </table>
    `;

    // Insert total items and table into the page
    tableContainer.innerHTML = totalItemsHTML + tableHTML;
}
