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
            })
            .catch(error => {
                console.error('Error:', error);
            });
        });
});

// Function to create and display the table from JSON data
function displayTable(data, buttonType) {
    const tableContainer = document.getElementById('tableContainer');

    if (!data || data.length === 0) {
        tableContainer.innerHTML = '<p>No data available to display</p>';
        return;
    }

    tableContainer.innerHTML = ''; // Clear previous data

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
