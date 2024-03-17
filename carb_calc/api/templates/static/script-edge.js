// Get the modal
var modal = document.getElementById("popupModal");
// Get the <span> element that closes the modal
var span = document.getElementsByClassName("close")[0];
// Define a boolean flag to control sending and listening
var socketActive = true;
var canvas = document.getElementById("canvas");
var context = canvas.getContext("2d");
const video = document.querySelector("#videoElement");
var classification = document.getElementById("classification");
var bboxes = document.getElementById("bboxes");
var autoModalCheckbox = document.getElementById("autoModalCheckbox");
var multipleObjectsCheckbox = document.getElementById("multipleObjectsCheckbox");
// Define desired classes with their carbon footprints
var desiredClasses = {
  "carrot": 0.24,
  "apple": 0.25,
  "broccoli": 0.57,
  "banana": 0.82,
  "orange": 0.30,
};

video.width = 600;
video.height = 450;

if (navigator.mediaDevices.getUserMedia) {
  navigator.mediaDevices
    .getUserMedia({
      video: true,
    })
    .then(function (stream) {
      video.srcObject = stream;
      video.play();
    })
    .catch(function (error) {});
}

// Store bounding boxes globally
var boundingBoxes = [];

// Draw bounding boxes on canvas
function drawBoundingBoxes() {
  boundingBoxes.forEach(function(bbox) {
    // Draw bounding box
    context.strokeRect(bbox.x, bbox.y, bbox.width, bbox.height);
    context.lineWidth = 1;
    context.fillStyle = "rgba(195, 255, 104, 0.1)";
    context.fillRect(bbox.x, bbox.y, bbox.width, bbox.height);

    // Draw text background for class
    const text = bbox.class;
    const padding = 2;
    const textBackgroundWidth = context.measureText(text).width + padding * 2 + 2;
    const textBackgroundHeight = 16 + padding * 2; // Assuming font size 16px
    context.fillStyle = 'rgba(255, 255, 255, 0.8)';
    context.fillRect(bbox.x, bbox.y, textBackgroundWidth + 2, textBackgroundHeight);

    // Draw text background for carbon footprint
    const text2 = 'CO2 ' + desiredClasses[bbox.class];
    const text2BackgroundWidth = context.measureText(text2).width + padding * 2;
    context.fillRect(bbox.x + bbox.width - text2BackgroundWidth - 4, bbox.y, text2BackgroundWidth + 2, textBackgroundHeight);

    // Draw label text for class
    context.fillStyle = 'green';
    context.font = '16px Montserrat';
    context.fillText(bbox.class, bbox.x + 2, bbox.y + 14);

    // Draw label text for carbon footprint
    context.font = '14px Montserrat';
    context.fillText(text2, bbox.x + bbox.width - text2BackgroundWidth + 2, bbox.y + 14);
  });
}

// Video rendering
const VIDEO_FPS = 30;
setInterval(() => {
  context.drawImage(video, 0, 0, video.width, video.height);
  drawBoundingBoxes();
}, 1000 / VIDEO_FPS);

// Function to close the modal
function closeModal() {
  modal.style.display = "none";
  // Add the event listener back
  socketActive = true;
  autoModalCheckbox.checked = false;
}

// Inference logic using COCO-SSD model
INFERENCE_AT_EDGE_FPS = 5
cocoSsd.load().then(model => {
  setInterval(() => {
    var data = canvas;
    model.detect(data).then(result => {
      if (result.length > 0) {
        boundingBoxes = [];
        result.forEach(function(obj) {
          var bbox = {
            x: obj['bbox'][0],
            y: obj['bbox'][1],
            width: obj['bbox'][2],
            height: obj['bbox'][3],
            class: obj['class']
          };

          if (Object.keys(desiredClasses).includes(bbox.class)) {
            var cropCanvas = document.createElement('canvas');
            cropCanvas.width = bbox.width;
            cropCanvas.height = bbox.height;
            var cropContext = cropCanvas.getContext('2d');
            cropContext.drawImage(video, bbox.x, bbox.y, bbox.width, bbox.height, 0, 0, bbox.width, bbox.height);
            var croppedImageDataURL = cropCanvas.toDataURL("image/jpeg", 0.5);
            bbox.croppedImage = croppedImageDataURL
            boundingBoxes.push(bbox);
          }
        });
        if (modal.style.display != "block" && boundingBoxes.length > multipleObjectsCheckbox.checked) {
          var html_popup_content = '';
          boundingBoxes.forEach(function(bbox) {
            internal_content = `<div class="object ${bbox.class}"><img src="${bbox.croppedImage}" alt="Cropped Image"><div class="obj-description"><p><span>Class:</span> ${(bbox.class).charAt(0).toUpperCase() + (bbox.class).slice(1)}</p><p><span>Carbon Footprint:</span> ${desiredClasses[bbox.class]}Kg/Kg of ${bbox.class}s</p></div></div>`;
            html_popup_content = html_popup_content.concat(internal_content);
          });
          popupContent.innerHTML = html_popup_content;
          if (autoModalCheckbox.checked) {
            modal.style.display = "block";
          }
        }
      }
    });
  }, 1000 / INFERENCE_AT_EDGE_FPS);
});

// Event listener to close modal when <span> (x) is clicked
span.onclick = function() {
  closeModal();
}

// Event listener to close modal when clicked outside of it
window.onclick = function(event) {
  if (event.target == modal) {
    closeModal();
  }
}
