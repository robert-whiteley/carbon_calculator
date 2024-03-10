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

video.width = 400;
video.height = 300;

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

const FPS = 5;
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

        console.log(result['bboxes'][0]['class'])
        x = result['bboxes'][0]['bbox'][0]
        y = result['bboxes'][0]['bbox'][1]
        if (x<0){
          x=0
        }
        if (y<0){
          y=0
        }

        box_width = result['bboxes'][0]['bbox'][2]*width - x
        box_height = result['bboxes'][0]['bbox'][3]*height - y
        x = x*width
        y = y*height
        console.log(x,y, box_width, box_height)

        context.strokeStyle = 'green';
        context.strokeRect(x, y, box_width, box_height);
        context.linewidth = 5;
        context.fillStyle = "rgba(195, 255, 104, 0.1)";
        context.fillRect(x, y, box_width, box_height);

        // Draw background for the label text
        context.fillStyle = 'green'; // Background color for the text
        const textWidth = context.measureText(result['bboxes'][0]['class']).width;
        context.fillRect(x, y, textWidth + 10, 20);

        // Draw label text
        context.fillStyle = 'white';
        context.font = '14px Verdana';
        context.fillText(result['bboxes'][0]['class'], x + 5, y + 15);

        // Extract the class and carbon footprint per unit
        var detectedClass = result['bboxes'][0]['class'];

        // Populate the popup modal with the extracted information
        var popupContent = document.getElementById('popupContent');
        popupContent.innerHTML = `
          <img src="" alt="Cropped Image">
          <p>Class: ${detectedClass}</p>
        `;

        // Show the popup modal
        modal.style.display = "block";
        socketActive = false;
    }
  }
})

function closeModal() {
  modal.style.display = "none";

  // Add the event listener back
  socketActive = true;
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

socket.on("classification", function (text) {
  classification.textContent=text;
})
