
console.log(alternativesList)


function addTrip(trip){
    hours=Math.floor(trip.duration/60)
    minutes=trip.duration%60
    var li = document.createElement('li');
    element=trip.path[0].name+" - "+trip.path[trip.path.length-1].name+"<BR/><b>"+hours+"h"+minutes+"<b/>"
    li.innerHTML=li.innerHTML + element;
    alternativesList.insertBefore(li, alternativesList.firstChild);
    li.onclick = function() {
        addTripDetails(trip);
    };
}


function addTripDetails(data){

    path=data.path
    console.log("Change data : "+path[0].name+Date.now())
    stepsList.innerHTML=""
    console.log(path[0])
    for(let i=0; i<path.length; i++){
        var step = document.createElement('li');
        step.innerHTML='<div class="step-marker">'+(i+1)+'</div>'+
            '<div>'+
            '<div>'+path[i].name+'</div>'+
            '</div>';
        stepsList.appendChild(step)
    }
    console.log("Change time : "+Date.now())
}
