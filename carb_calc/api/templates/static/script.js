var socket = io.connect(
  window.location.protocol + "//" + document.domain + ":" + location.port
  /*'http://localhost:6400'*/
);

socket.on("connect", function () {
  console.log("Connected...!", socket.connected);
});

var canvas = document.getElementById("canvas");
var context = canvas.getContext("2d");
var mycanvas = document.getElementById("mycanvas")
var mycontext = mycanvas.getContext("2d")
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
  context.clearRect(0, 0, width, height);
  socket.emit("image", data);
}, 1000 / FPS);

/*
socket.on("processed_image", function (image) {
  photo.setAttribute("src", image);
});
*/

socket.on("result", function(result){
  mycontext.clearRect(0,0,width,height)
  photo.setAttribute("src", result['image']);

  x = result['bboxes'][0]['bbox'][0]
  y = result['bboxes'][0]['bbox'][1]

  mycontext.beginPath();
  mycontext.rect(188, 50, 200, 100);
  mycontext.fillStyle = 'rgba(255, 255, 255, 0)';
  mycontext.fill();
})

socket.on("classification", function (text) {
  classification.textContent=text;
})

/*
socket.on("bboxes", function(bboxes){
  width = video.width;
  height = video.height;
  context.drawImage(video, 10, 10);
  context.beginPath();
  context.rect(188, 50, 200, 100);
  context.fillStyle = '';
  context.fill();
  context.lineWidth = 7;
  context.strokeStyle = '';
  context.stroke();

})
*/
