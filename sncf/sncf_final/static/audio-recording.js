navigator.mediaDevices.getUserMedia({audio:true}).then(stream => {handlerFunction(stream)})

let isRecording=false

zoom=7
var mymap = L.map('mapid').setView([46.71, 1.71], zoom);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: 'Map data © <a href="https://openstreetmap.org">OpenStreetMap</a> contributors',
    maxZoom: 18,
}).addTo(mymap);

function clearMap() {
  for(i in mymap._layers) {
      if(mymap._layers[i]._path != undefined) {
          try {
            mymap.removeLayer(mymap._layers[i]);
          }
          catch(e) {
              console.log("problem with " + e + mymap._layers[i]);
          }
      }
  }
}

function displayMap(data){
  mlat=0
  mlon=0
  size=0

  clearMap()

  max=data[data.length-1].duration
  min=data[0].duration

  alternativesList.innerHTML = ""

  for(let i=data.length-1; i>=0; i--){
    path=data[i].path
    addTrip(data[i])
    var latlongs = path.map((e)=>{
      mlat+=e.lat;
      mlon+=e.lon;
      return [e.lat,e.lon]
    })
    //Get mean latitude and longitude to calculate the center of the map
    size+=latlongs.length
    duration=data[i].duration
    g=((duration-min)/(max-min))*255
    color= "rgb("+g+","+g+",255)";
    var polyline = L.polyline(latlongs, {color: color}).addTo(mymap);
  }

  console.log("OK")
  alternativesList.firstChild.onclick()
  mlat=mlat/size
  mlon=mlon/size

  mymap.setView([mlat, mlon], zoom);
}

function handlerFunction(stream) {
  rec = new MediaRecorder(stream);
  rec.ondataavailable = e => {
    audioChunks.push(e.data);
    if (rec.state == "inactive"){
      blob = new Blob(audioChunks,{type:'audio/mpeg-3'});
      upload(blob)
    }
  }
}


function setStartDest(start,dest){
  document.getElementById("start").value=start;
  document.getElementById("end").value=dest;
}

search.onclick = e => {// Prevent the default form submission
  const start = document.getElementById("start").value;
  const end = document.getElementById("end").value;
  console.log(`Starting point: ${start}, End point: ${end}`);

  var xhttp = new XMLHttpRequest();
  xhttp.open("POST", "http://localhost:8000/bestPath", true);

  xhttp.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
  xhttp.responseType='json'
  params={
    "start":start,
    "end":end
  }
  xhttp.send(JSON.stringify(params));
  xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
      console.log(this.response)
      displayMap(this.response.paths)
    }
  }
}


recordButton.onclick = e => {
  if (!isRecording) {
    recordButton.style.backgroundColor = "blue"
    audioChunks = [];
    rec.start();
    isRecording=true
  } else {
    isRecording=false
    recordButton.style.backgroundColor = "white"
    rec.stop();
  }
}

function upload(blob) {
  console.log('BLOB: ', blob)
  var xhttp = new XMLHttpRequest();
  xhttp.open("POST", "http://localhost:8000/bestPathAudio", true);
  xhttp.responseType='json'
  var data = new FormData();
  data.append('data', blob, 'audio_blob');
  console.log('DATA SENT: ', data)
  xhttp.send(data);
  xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
        console.log(this.response)
        displayMap(this.response.paths)
        setStartDest(this.response.start,this.response.dest)
    }
  };
}