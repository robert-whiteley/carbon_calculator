var socket = io.connect(
  window.location.protocol + "//" + document.domain + ":" + location.port
  /*'http://localhost:6400'*/
);

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

const FPS = 10;
setInterval(() => {
  width = video.width;
  height = video.height;
  context.drawImage(video, 0, 0, width, height);
  var data = canvas.toDataURL("image/jpeg", 0.5);
  socket.emit("image", data);
}, 1000 / FPS);

socket.on("result", function(result){
  if (socketActive){
    console.log(result['bboxes'])
    if (result['bboxes'].length >0){
      result['bboxes'].forEach(function(obj){
        console.log(obj['class'])
        x = obj['bbox'][0]
        y = obj['bbox'][1]
        if (x < 0){
          x = 0
        }
        if (y < 0){
          y = 0
        }

        box_width = obj['bbox'][2] * width - x
        box_height = obj['bbox'][3] * height - y
        x = x * width
        y = y * height

        // Draw bounding box
        context.strokeRect(x, y, box_width, box_height);
        context.lineWidth = 1;
        context.fillStyle = "rgba(195, 255, 104, 0.1)";
        context.fillRect(x, y, box_width, box_height);

        // Draw label text on top corner of the bounding box
        context.fillStyle = 'green';
        context.font = '14px Arial';
        context.fillText(obj['class'], x+2, y + 14);
        // Extract the class and carbon footprint per unit
        var detectedClass = obj['class'];



        // Create a new canvas to draw the cropped image
        var cropCanvas = document.createElement('canvas');
        cropCanvas.width = box_width;
        cropCanvas.height = box_height;
        var cropContext = cropCanvas.getContext('2d');

        // Draw the cropped image on the new canvas
        cropContext.drawImage(video, x, y, box_width, box_height, 0, 0, box_width, box_height);

        // Convert the cropped image canvas to a data URL
        var croppedImageDataURL = cropCanvas.toDataURL("image/jpeg", 0.5);

        // Populate the popup modal with the extracted information
        var popupContent = document.getElementById('popupContent');
        popupContent.innerHTML = `
        <img src="${croppedImageDataURL}" alt="Cropped Image">
        <p>Class: ${detectedClass}</p>
        `;
      });
      console.log(autoModalCheckbox.checked);
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
