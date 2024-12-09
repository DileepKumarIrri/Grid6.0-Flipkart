document.addEventListener('DOMContentLoaded', function() {

    // Get references to the buttons
    const liveFeedButton = document.getElementById('live-feed-btn');
    const uploadButton = document.getElementById('upload-btn');
    
    // Attach click event listeners to the buttons
    liveFeedButton.addEventListener('click', function() {
      window.location.href = '/livefeed';  // Flask route
    });
  
    uploadButton.addEventListener('click', function() {
      window.location.href = '/upload';  // Flask route
    });
  
  });
  