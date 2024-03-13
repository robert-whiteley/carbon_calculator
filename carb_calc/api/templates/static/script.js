/*var socket = io.connect(
  //window.location.protocol + "//" + document.domain + ":" + location.port
  'https://carbon-calculator-rw-klerphlnqq-ew.a.run.app'
);
*/
var socket = io.connect('localhost:8080');

socket.on("connect", function () {
  console.log("Connected...!", socket.connected);
});

// Get the modal
var modal = document.getElementById("popupModal");
// Get the <span> element that closes the modal
var span = document.getElementsByClassName("close")[0];
// Define a boolean flag to control sending and listening
var socketActive = true;
var canvas = document.getElementById("canvas");
var context = canvas.getContext("2d");
const video = document.querySelector("#videoElement");
var classification = document.getElementById("classification")
var bboxes = document.getElementById("bboxes")
var autoModalCheckbox = document.getElementById("autoModalCheckbox");

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
    .catch(function (err0r) {});
}
// Store bounding boxes globally
var boundingBoxes = [];

// Draw bounding boxes
function drawBoundingBoxes() {
  boundingBoxes.forEach(function(bbox) {
    context.strokeRect(bbox.x, bbox.y, bbox.width, bbox.height);
    context.lineWidth = 1;
    context.fillStyle = "rgba(195, 255, 104, 0.1)";
    context.fillRect(bbox.x, bbox.y, bbox.width, bbox.height);

    // Draw label text on top corner of the bounding box
    context.fillStyle = 'green';
    context.font = '16px Montserrat';
    context.fillText(bbox.class, bbox.x+2, bbox.y + 14);
  });
}

// Video rendering
const VIDEO_FPS = 30;
setInterval(() => {
  width = video.width;
  height = video.height;
  context.drawImage(video, 0, 0, width, height);

  // Draw bounding boxes
  drawBoundingBoxes();
}, 1000 / VIDEO_FPS);

// Inference
const INFERENCE_FPS = 1;
setInterval(() => {
  var data = canvas.toDataURL("image/jpeg", 0.5);
  socket.emit("image", data);
}, 1000 / INFERENCE_FPS);


socket.on("result", function(result){
  if (socketActive){
    if (result['bboxes'].length >0){
      // Clear previous bounding boxes
      boundingBoxes = [];

      result['bboxes'].forEach(function(obj){
        var bbox = {
          x: obj['bbox'][0] * width,
          y: obj['bbox'][1] * height,
          width: obj['bbox'][2] * width - obj['bbox'][0] * width,
          height: obj['bbox'][3] * height - obj['bbox'][1] * height,
          class: obj['class']
        };

        // Add to global bounding boxes
        boundingBoxes.push(bbox);

        // Create a new canvas to draw the cropped image
        var cropCanvas = document.createElement('canvas');
        cropCanvas.width = bbox.width;
        cropCanvas.height = bbox.height;
        var cropContext = cropCanvas.getContext('2d');

        // Draw the cropped image on the new canvas
        cropContext.drawImage(video, bbox.x, bbox.y, bbox.width, bbox.height, 0, 0, bbox.width, bbox.height);

        // Convert the cropped image canvas to a data URL
        var croppedImageDataURL = cropCanvas.toDataURL("image/jpeg", 0.5);

        // Populate the popup modal with the extracted information
        var popupContent = document.getElementById('popupContent');
        popupContent.innerHTML = `
        <img src="${croppedImageDataURL}" alt="Cropped Image">
        <p>Class: ${bbox.class}</p>
        `;
      });

      if (autoModalCheckbox.checked) {
        // Show the popup modal
        modal.style.display = "block";
        socketActive = false;
      }
    }
  }
})

function closeModal() {
  modal.style.display = "none";
  // Add the event listener back
  socketActive = true;
  autoModalCheckbox.checked = false;
}

// When the user clicks on <span> (x), close the modal
span.onclick = function() {
  closeModal();
}

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
  if (event.target == modal) {
    closeModal();
  }
}
