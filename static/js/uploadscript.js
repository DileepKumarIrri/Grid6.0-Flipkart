let buttonType = '';

// Event listeners for buttons
document.getElementById('groceryBtn').addEventListener('click', function() {
        buttonType = 'grocery';
        uploadImage();
});

document.getElementById('freshproduceBtn').addEventListener('click', function() {
    buttonType = 'freshproduce';
    uploadImage();
});

function uploadImage() {
    const input = document.createElement('input');
    input.type = 'file';
    input.accept = 'image/*';
    input.click();

    // Clear the image container and table when a new image is uploaded
    const imageContainer = document.getElementById('imageContainer');
    const tableContainer = document.getElementById('tableContainer');
    imageContainer.innerHTML = '<p>No image selected</p>'; // Reset image preview
    tableContainer.innerHTML = ''; // Clear previous table content
    tableContainer.style.display = 'none'; // Hide table container

    input.addEventListener('change', function(event) {
        const file = event.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = function(e) {
                const imageContainer = document.getElementById('imageContainer');
                imageContainer.innerHTML = `<img src="${e.target.result}" alt="Uploaded Image" class="uploaded-image">`;
            };
            reader.readAsDataURL(file);
        }
    });
}

document.querySelector('.details').addEventListener('click', function() {
    const imageElement = document.querySelector('.uploaded-image');
    if (!imageElement) {
        alert('No image selected');
        return;
    }

    // Show the loader when "Get-Details" is clicked
    document.getElementById('loader').classList.remove('hidden');

    // Get the image as a Blob
    fetch(imageElement.src)
        .then(res => res.blob())
        .then(blob => {
            const formData = new FormData();
            formData.append('image', blob, 'uploaded_image.png');
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
    const totalItemsHTML = `<h2 style="margin-top:20px; text-align: left; color:black"><strong>Total Items: ${data.total_items}</strong></h2>`;
    // console.log(totalItemsHTML)

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