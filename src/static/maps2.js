
   
 function placeMarker(location) {
  if ( marker ) {
    marker.setPosition(location);
  } else {
    marker = new google.maps.Marker({
      position: location,
      map: map
    });
  }
  document.getElementById("lat").value = location.lat();
  document.getElementById("lng").value =location.lng();
}


var nastavenie = function(){
   console.log("mapa RRRRRR");
   map = document.getElementById("map");
   google.maps.event.addListener(map, 'click', function(event) {
   //map.addListener('click', function(event) {
   placeMarker(event.latLng);
   console.log("kliknutie na mapu");
  
  });
    
    
}

$(document).ready(nastavenie);